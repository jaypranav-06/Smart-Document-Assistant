# Smart Document Assistant - Backend

FastAPI backend for the RAG-powered document Q&A system with citation highlighting.

## Features

- PDF upload and processing with position tracking
- Intelligent text chunking with metadata preservation
- Vector embeddings using OpenAI
- ChromaDB for local vector storage
- RAG pipeline with LangChain
- Citation tracking (page numbers + character positions)
- REST API endpoints

## Prerequisites

- Python 3.11+
- OpenAI API key

## Setup

1. Create virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. Run the server:
```bash
python -m app.main
# Or with uvicorn:
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/api/docs`

## API Endpoints

### Upload Document
```bash
POST /api/upload
Content-Type: multipart/form-data

# Upload a PDF file
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@document.pdf"
```

### Query Documents
```bash
POST /api/query
Content-Type: application/json

{
  "question": "What is the main topic of this document?",
  "document_id": "optional-document-id",
  "max_citations": 3
}
```

### List Documents
```bash
GET /api/documents
```

### Delete Document
```bash
DELETE /api/documents/{document_id}
```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   │   ├── upload.py
│   │   ├── query.py
│   │   └── documents.py
│   ├── models/       # Data models
│   │   └── schemas.py
│   ├── services/     # Business logic
│   │   ├── pdf_processor.py  # PDF text extraction
│   │   ├── chunker.py         # Intelligent chunking
│   │   ├── vector_store.py    # Vector database
│   │   └── rag_service.py     # RAG pipeline
│   ├── config.py     # Configuration
│   └── main.py       # FastAPI app
├── uploads/          # Uploaded PDFs
├── chroma_db/        # Vector database
└── requirements.txt
```

## Citation Feature

The system tracks exact positions of text in PDFs:
- Page numbers
- Character start/end positions
- Bounding boxes (for future enhancement)

This enables the frontend to highlight the exact paragraph used to generate each answer.

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black app/
```

Lint:
```bash
pylint app/
```
