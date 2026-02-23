"""API endpoints for document management."""
import logging
import os
from typing import List
from fastapi import APIRouter, HTTPException
from app.models.schemas import DocumentInfo, DocumentListResponse
from app.services.rag_service import RAGService
from app.services.vector_store import VectorStore
from app.config import settings
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize services
rag_service = RAGService()
vector_store = VectorStore()


@router.get("", response_model=DocumentListResponse)
async def list_documents():
    """
    List all uploaded documents.

    Returns:
        DocumentListResponse with list of all documents
    """
    try:
        # Get document IDs from vector store
        document_ids = vector_store.list_documents()

        documents = []
        for doc_id in document_ids:
            # Get chunk count
            stats = rag_service.get_document_stats(doc_id)

            # Try to get file info from disk
            pdf_path = os.path.join(settings.upload_dir, f"{doc_id}.pdf")
            file_size = 0
            filename = f"{doc_id}.pdf"
            uploaded_at = datetime.now()

            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                uploaded_at = datetime.fromtimestamp(os.path.getctime(pdf_path))

                # Try to extract original filename from metadata
                # (In a production app, you'd store this in a database)

            # Get page count (placeholder - would need to be stored)
            from app.services.pdf_processor import PDFProcessor
            processor = PDFProcessor()
            page_count = processor.get_page_count(pdf_path) if os.path.exists(pdf_path) else 0

            doc_info = DocumentInfo(
                document_id=doc_id,
                filename=filename,
                file_size=file_size,
                page_count=page_count,
                uploaded_at=uploaded_at,
                chunk_count=stats["chunk_count"]
            )

            documents.append(doc_info)

        return DocumentListResponse(
            documents=documents,
            total=len(documents)
        )

    except Exception as e:
        logger.error(f"Error listing documents: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document and its chunks from the system.

    Args:
        document_id: Document ID to delete

    Returns:
        Success message
    """
    try:
        # Delete from vector store
        success = rag_service.delete_document(document_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Document {document_id} not found"
            )

        # Delete PDF file
        pdf_path = os.path.join(settings.upload_dir, f"{document_id}.pdf")
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.info(f"Deleted file: {pdf_path}")

        return {
            "message": f"Document {document_id} deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )


@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Get information about a specific document.

    Args:
        document_id: Document ID

    Returns:
        Document information
    """
    try:
        stats = rag_service.get_document_stats(document_id)

        if stats["chunk_count"] == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Document {document_id} not found"
            )

        # Get file info
        pdf_path = os.path.join(settings.upload_dir, f"{document_id}.pdf")
        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=404,
                detail=f"Document file {document_id}.pdf not found"
            )

        file_size = os.path.getsize(pdf_path)
        uploaded_at = datetime.fromtimestamp(os.path.getctime(pdf_path))

        from app.services.pdf_processor import PDFProcessor
        processor = PDFProcessor()
        page_count = processor.get_page_count(pdf_path)

        return DocumentInfo(
            document_id=document_id,
            filename=f"{document_id}.pdf",
            file_size=file_size,
            page_count=page_count,
            uploaded_at=uploaded_at,
            chunk_count=stats["chunk_count"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document {document_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error getting document: {str(e)}"
        )
