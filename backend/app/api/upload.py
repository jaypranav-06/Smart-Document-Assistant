"""API endpoint for document upload."""
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models.schemas import DocumentUploadResponse, ErrorResponse
from app.services.rag_service import RAGService
from app.services.document_processor import DocumentProcessor
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["upload"])

# Initialize RAG service and document processor
rag_service = RAGService()
doc_processor = DocumentProcessor()


@router.post("", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document (supports multiple formats).

    This endpoint:
    1. Validates the uploaded file type and size
    2. Extracts text with position tracking from any supported format
    3. Chunks the text with metadata preservation
    4. Indexes the chunks in the vector database

    Supported formats: PDF, DOCX, TXT, MD, PPTX, XLSX, CSV, HTML, and more

    Args:
        file: Document file to upload

    Returns:
        DocumentUploadResponse with document metadata
    """
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        supported_extensions = doc_processor.get_supported_extensions()

        if file_ext not in supported_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported formats: {', '.join(supported_extensions)}"
            )

        # Validate file size
        contents = await file.read()
        file_size = len(contents)

        if file_size > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({file_size} bytes) exceeds maximum allowed size ({settings.max_file_size_bytes} bytes)"
            )

        # Auto-cleanup: Delete all existing documents before uploading new one
        # This ensures a clean state for each upload
        try:
            existing_docs = rag_service.vector_store.list_documents()
            if existing_docs:
                logger.info(f"Auto-cleanup: Removing {len(existing_docs)} existing document(s)")
                for old_doc_id in existing_docs:
                    rag_service.delete_document(old_doc_id)
                    # Also remove the file (check all possible extensions)
                    for ext in supported_extensions:
                        old_file_path = os.path.join(settings.upload_dir, f"{old_doc_id}{ext}")
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                            logger.info(f"Deleted old file: {old_file_path}")
                logger.info("Auto-cleanup completed")
        except Exception as e:
            logger.warning(f"Auto-cleanup failed (non-critical): {e}")
            # Continue with upload even if cleanup fails

        # Generate unique document ID
        document_id = str(uuid.uuid4())

        # Save file with original extension
        upload_path = os.path.join(settings.upload_dir, f"{document_id}{file_ext}")
        with open(upload_path, "wb") as f:
            f.write(contents)

        logger.info(f"Saved uploaded file: {file.filename} -> {upload_path}")

        # Process and index the document
        try:
            indexing_stats = rag_service.index_document(
                document_id=document_id,
                filename=file.filename,
                file_path=upload_path
            )

            logger.info(f"Successfully indexed document {document_id}: {indexing_stats}")

            # Return response
            return DocumentUploadResponse(
                document_id=document_id,
                filename=file.filename,
                file_size=file_size,
                page_count=indexing_stats["page_count"],
                uploaded_at=datetime.now(),
                status="completed"
            )

        except Exception as e:
            # Clean up file on error
            if os.path.exists(upload_path):
                os.remove(upload_path)
            raise

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )
