"""RAG (Retrieval Augmented Generation) service with citation tracking."""
import logging
import time
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.services.vector_store import VectorStore
from app.models.schemas import Citation, QueryResponse
from app.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """RAG service for question answering with citations."""

    # Citation-aware prompt template focused on concise, accurate answers
    PROMPT_TEMPLATE = """You are a helpful AI assistant that provides clear, concise answers from documents.

INSTRUCTIONS:
1. Read the context and find information that directly answers the question
2. Give a SHORT, SIMPLE answer using ONLY the information from the context
3. Answer in 2-3 sentences maximum - be direct and to the point
4. Use simple, clear English that anyone can understand
5. Do NOT include citation markers like [1], [2], [Source 1] - citations are shown separately
6. If the answer is not in the context, say "I cannot find this information in the document"

Context from documents:
{context}

Question: {question}

Provide a short, direct answer in simple English (2-3 sentences maximum). NO citation markers."""

    def __init__(self):
        """Initialize RAG service."""
        self.vector_store = VectorStore()

        # Initialize LLM based on provider
        if settings.ai_provider == "ollama":
            self.llm = ChatOllama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0.1,  # Very low for direct, factual answers
                num_ctx=2048,  # Reduced for faster processing
                num_predict=128  # Short responses (2-3 sentences)
            )
            logger.info(f"RAG service initialized with Ollama model: {settings.ollama_model}")
        else:
            self.llm = ChatOpenAI(
                openai_api_key=settings.openai_api_key,
                model=settings.openai_model,
                temperature=0.2  # Lower temperature for more factual responses
            )
            logger.info(f"RAG service initialized with OpenAI model: {settings.openai_model}")

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)

    def query(
        self,
        question: str,
        document_id: Optional[str] = None,
        max_citations: int = 3  # Optimized for fast, relevant answers
    ) -> QueryResponse:
        """
        Answer a question using RAG with citation tracking.

        Args:
            question: Question to answer
            document_id: Optional specific document to query
            max_citations: Maximum number of citations to return

        Returns:
            QueryResponse with answer and citations
        """
        start_time = time.time()

        try:
            # Step 1: Retrieve relevant chunks with scores
            filter_dict = {"document_id": document_id} if document_id else None

            relevant_chunks = self.vector_store.similarity_search(
                query=question,
                k=max_citations,
                filter_dict=filter_dict
            )

            if not relevant_chunks:
                logger.warning(f"No relevant chunks found for question: {question}")
                return QueryResponse(
                    answer="I couldn't find any relevant information in the documents to answer this question.",
                    citations=[],
                    question=question,
                    processing_time_ms=(time.time() - start_time) * 1000
                )

            # Log retrieved chunks for debugging
            logger.info(f"Retrieved chunks for query '{question}':")
            for i, (chunk, score) in enumerate(relevant_chunks):
                logger.info(f"  Chunk {i+1}: doc_id={chunk.document_id}, page={chunk.page_number}, score={score:.4f}, text_preview={chunk.text[:100]}...")

            # Step 2: Prepare context from retrieved chunks
            context_parts = []
            for chunk, score in relevant_chunks:
                # Just provide the text without source markers - citations are handled separately
                context_parts.append(f"{chunk.text}\n")

            context = "\n---\n".join(context_parts)

            # Step 3: Generate answer using LLM
            logger.info(f"Generating answer for: {question}")

            messages = self.prompt.format_messages(
                context=context,
                question=question
            )

            response = self.llm.invoke(messages)
            answer = response.content

            # Step 4: Create citations from retrieved chunks
            citations = []
            for chunk, score in relevant_chunks:
                citation = Citation(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                    page_number=chunk.page_number,
                    char_start=chunk.char_start,
                    char_end=chunk.char_end,
                    relevance_score=float(score)
                )
                citations.append(citation)

            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000

            logger.info(f"Query completed in {processing_time:.2f}ms with {len(citations)} citations")

            return QueryResponse(
                answer=answer,
                citations=citations,
                question=question,
                processing_time_ms=processing_time
            )

        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            raise

    def index_document(
        self,
        document_id: str,
        filename: str,
        file_path: str
    ) -> dict:
        """
        Process and index a document for RAG.

        Args:
            document_id: Unique document identifier
            filename: Original filename
            file_path: Path to the document file (any supported format)

        Returns:
            Dictionary with indexing statistics
        """
        from app.services.document_processor import DocumentProcessor
        from app.services.chunker import IntelligentChunker

        try:
            # Step 1: Extract text with positions (supports multiple formats)
            doc_processor = DocumentProcessor()
            segments, metadata = doc_processor.extract_text_with_positions(file_path)

            logger.info(f"Extracted {len(segments)} segments from {filename}")

            # Step 2: Chunk segments with metadata preservation
            chunker = IntelligentChunker()
            chunks = chunker.chunk_segments(segments, document_id, filename)

            logger.info(f"Created {len(chunks)} chunks from {filename}")

            # Step 3: Add chunks to vector store
            chunk_ids = self.vector_store.add_chunks(chunks)

            return {
                "document_id": document_id,
                "filename": filename,
                "page_count": metadata["page_count"],
                "chunk_count": len(chunks),
                "segments_count": len(segments),
                "total_chars": metadata["total_chars"]
            }

        except Exception as e:
            logger.error(f"Error indexing document {filename}: {e}", exc_info=True)
            raise

    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the index.

        Args:
            document_id: Document ID to delete

        Returns:
            True if successful, False otherwise
        """
        return self.vector_store.delete_document(document_id)

    def get_document_stats(self, document_id: str) -> dict:
        """
        Get statistics for a document.

        Args:
            document_id: Document ID

        Returns:
            Dictionary with document statistics
        """
        chunk_count = self.vector_store.get_document_chunk_count(document_id)

        return {
            "document_id": document_id,
            "chunk_count": chunk_count
        }
