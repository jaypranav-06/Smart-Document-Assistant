"""Vector database service for document embeddings."""
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from app.services.chunker import DocumentChunk
from app.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Manage vector embeddings and similarity search."""

    def __init__(self):
        """Initialize vector store with ChromaDB."""
        # Initialize embedding model based on provider
        if settings.ai_provider == "ollama":
            self.embedding_model = OllamaEmbeddings(
                model=settings.ollama_embedding_model,
                base_url=settings.ollama_base_url
            )
            logger.info(f"Using Ollama embeddings: {settings.ollama_embedding_model}")
        else:
            self.embedding_model = OpenAIEmbeddings(
                openai_api_key=settings.openai_api_key,
                model=settings.embedding_model
            )
            logger.info(f"Using OpenAI embeddings: {settings.embedding_model}")

        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path=settings.chroma_db_path,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Collection name
        self.collection_name = "document_chunks"

        # Initialize LangChain's Chroma wrapper
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_model
        )

        logger.info(f"Vector store initialized with collection: {self.collection_name}")

    def add_chunks(self, chunks: List[DocumentChunk]) -> List[str]:
        """
        Add document chunks to the vector store.

        Args:
            chunks: List of DocumentChunks to add

        Returns:
            List of chunk IDs that were added
        """
        if not chunks:
            logger.warning("No chunks to add to vector store")
            return []

        try:
            # Prepare data for insertion
            texts = [chunk.text for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            ids = [chunk.chunk_id for chunk in chunks]

            # Add to vector store
            self.vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids
            )

            logger.info(f"Added {len(chunks)} chunks to vector store")
            return ids

        except Exception as e:
            logger.error(f"Error adding chunks to vector store: {e}")
            raise

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[tuple[DocumentChunk, float]]:
        """
        Search for similar chunks.

        Args:
            query: Query string
            k: Number of results to return
            filter_dict: Optional metadata filter (e.g., {"document_id": "doc123"})

        Returns:
            List of tuples (DocumentChunk, relevance_score)
        """
        try:
            # Perform similarity search with scores
            results = self.vectorstore.similarity_search_with_relevance_scores(
                query=query,
                k=k,
                filter=filter_dict
            )

            # Convert results to DocumentChunk objects
            chunk_results = []
            for doc, score in results:
                metadata = doc.metadata

                # Reconstruct DocumentChunk from metadata
                chunk = DocumentChunk(
                    chunk_id=metadata["chunk_id"],
                    text=doc.page_content,
                    page_number=metadata["page"],
                    char_start=metadata["char_start"],
                    char_end=metadata["char_end"],
                    document_id=metadata["document_id"],
                    chunk_index=0,  # Not stored in metadata
                    metadata=metadata
                )

                chunk_results.append((chunk, score))

            logger.info(f"Found {len(chunk_results)} similar chunks for query")
            return chunk_results

        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            raise

    def delete_document(self, document_id: str) -> bool:
        """
        Delete all chunks for a specific document.

        Args:
            document_id: Document ID to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the collection
            collection = self.chroma_client.get_collection(self.collection_name)

            # Delete all chunks with this document_id
            collection.delete(
                where={"document_id": document_id}
            )

            logger.info(f"Deleted all chunks for document {document_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False

    def get_document_chunk_count(self, document_id: str) -> int:
        """
        Get the number of chunks for a document.

        Args:
            document_id: Document ID

        Returns:
            Number of chunks
        """
        try:
            collection = self.chroma_client.get_collection(self.collection_name)

            # Query with filter
            results = collection.get(
                where={"document_id": document_id}
            )

            return len(results["ids"]) if results and "ids" in results else 0

        except Exception as e:
            logger.error(f"Error getting chunk count for {document_id}: {e}")
            return 0

    def list_documents(self) -> List[str]:
        """
        List all unique document IDs in the vector store.

        Returns:
            List of document IDs
        """
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            results = collection.get()

            # Extract unique document IDs from metadata
            document_ids = set()
            if results and "metadatas" in results:
                for metadata in results["metadatas"]:
                    if "document_id" in metadata:
                        document_ids.add(metadata["document_id"])

            return list(document_ids)

        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
