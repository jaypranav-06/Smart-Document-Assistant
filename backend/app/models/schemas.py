"""Pydantic models for API request/response schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    document_id: str = Field(..., description="Unique identifier for the uploaded document")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    page_count: int = Field(..., description="Number of pages in the document")
    uploaded_at: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="processing", description="Processing status")


class Citation(BaseModel):
    """Citation information linking answer to source."""
    chunk_id: str = Field(..., description="ID of the source chunk")
    text: str = Field(..., description="The actual text from the source")
    page_number: int = Field(..., description="Page number in the PDF")
    char_start: int = Field(..., description="Character start position on the page")
    char_end: int = Field(..., description="Character end position on the page")
    relevance_score: float = Field(..., description="Relevance score from vector search")


class QueryRequest(BaseModel):
    """Request model for asking questions about documents."""
    question: str = Field(..., min_length=1, max_length=1000, description="Question to ask")
    document_id: Optional[str] = Field(None, description="Specific document ID to query, or None for all documents")
    max_citations: int = Field(default=3, ge=1, le=10, description="Maximum number of citations to return")


class QueryResponse(BaseModel):
    """Response model for question answering."""
    answer: str = Field(..., description="Generated answer to the question")
    citations: List[Citation] = Field(..., description="Source citations with position info")
    question: str = Field(..., description="Original question")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class DocumentInfo(BaseModel):
    """Information about a stored document."""
    document_id: str
    filename: str
    file_size: int
    page_count: int
    uploaded_at: datetime
    chunk_count: int = Field(..., description="Number of chunks stored")


class DocumentListResponse(BaseModel):
    """Response model for listing documents."""
    documents: List[DocumentInfo]
    total: int = Field(..., description="Total number of documents")


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy")
    version: str = Field(default="1.0.0")
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now)
