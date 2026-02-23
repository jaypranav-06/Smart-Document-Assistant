"""API endpoint for querying documents."""
import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/query", tags=["query"])

# Initialize RAG service
rag_service = RAGService()


@router.post("", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Ask a question about uploaded documents.

    This endpoint:
    1. Retrieves relevant document chunks using vector similarity search
    2. Generates an answer using the LLM with the retrieved context
    3. Returns the answer with citations (page numbers and character positions)

    The citations can be used by the frontend to highlight the exact
    text in the PDF that was used to generate the answer.

    Args:
        request: QueryRequest with question and optional document_id

    Returns:
        QueryResponse with answer and citations
    """
    try:
        logger.info(f"Processing query: {request.question[:100]}...")

        # Validate question
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        # Query the RAG service
        response = rag_service.query(
            question=request.question,
            document_id=request.document_id,
            max_citations=request.max_citations
        )

        logger.info(
            f"Query successful: {len(response.citations)} citations, "
            f"{response.processing_time_ms:.2f}ms"
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )
