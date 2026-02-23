# Smart Document Assistant

Chat with your PDFs and get answers with actual citations showing where the information came from. Uses Ollama AI locally to process documents and generate answers. The main feature here is precise citation tracking - you can click on any citation and it'll highlight exactly which part of the PDF was used.

## What it does

- Upload PDFs and extract text with position tracking
- Ask questions using Ollama AI (runs locally on your machine)
- Get answers with citations that show page numbers, character positions, and the exact text
- Click citations to jump to and highlight the source in the PDF
- Uses ChromaDB for vector search
- Built with Next.js 14 and FastAPI

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Frontend  │      │   FastAPI    │      │   Ollama   │
│  (Next.js)  │────▶ │   Backend    │────▶ │    Local   │
│             │      │              │      │            │
└─────────────┘      └──────┬───────┘      └────────────┘
                            │
                     ┌──────▼──────┐
                     │  ChromaDB   │
                     │ (Vectors)   │
                     └─────────────┘
```

### Stack

Frontend: Next.js 14, TypeScript, Tailwind, React-PDF, React-Dropzone

Backend: Python 3.11+, FastAPI, LangChain, ChromaDB, pdfplumber, Ollama AI (local models)

## Setup

You'll need Node.js 20+, Python 3.11+, and Ollama installed locally.

**Install Ollama:**
1. Download from https://ollama.ai
2. Pull a model: `ollama pull llama2` (or any model you prefer)

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```
Runs on `http://localhost:8000`

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```
Runs on `http://localhost:3000`

## Project Structure

```
The "Smart" Document Assistant/
├── backend/
│   ├── app/
│   │   ├── api/              # REST API endpoints
│   │   │   ├── upload.py     # PDF upload
│   │   │   ├── query.py      # Question answering
│   │   │   └── documents.py  # Document management
│   │   ├── services/
│   │   │   ├── pdf_processor.py    # PDF extraction with positions
│   │   │   ├── chunker.py          # Intelligent chunking
│   │   │   ├── vector_store.py     # Vector database
│   │   │   └── rag_service.py      # RAG pipeline with citations
│   │   ├── models/
│   │   │   └── schemas.py    # Pydantic models
│   │   ├── config.py         # Settings
│   │   └── main.py           # FastAPI app
│   ├── uploads/              # Uploaded PDFs
│   ├── chroma_db/            # Vector database
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/       # React components
│   │   ├── lib/              # API client
│   │   └── types/            # TypeScript types
│   └── package.json
│
└── README.md                 # This file
```

## How it works

The citation tracking is pretty straightforward:

1. Extract text from PDFs using pdfplumber and track page numbers + character positions
2. Split into chunks but keep the position metadata (`{page_number, char_start, char_end}`)
3. Store chunks in ChromaDB for vector search
4. When you ask a question, retrieve relevant chunks (they still have their position data)
5. Send the chunks to Ollama to generate an answer based on the context
6. Return the answer with citations containing page, position, relevance score, and original text
7. Frontend displays the PDF and highlights the exact paragraph when you click a citation

## API

Check out the docs at `http://localhost:8000/api/docs` once the backend is running.

Main endpoints:

`POST /api/upload` - Upload a PDF (multipart/form-data)

`POST /api/query` - Ask questions and get citations back
```json
{
  "question": "What is the main topic?",
  "max_citations": 3
}
```

## TODO

Working on:
- [ ] PDF viewer component
- [ ] Chat interface
- [ ] Citation highlighting overlay
- [ ] Document management UI

Later:
- [ ] Multi-document queries
- [ ] Authentication
- [ ] Rate limiting
- [ ] Streaming responses
- [ ] Docker setup
- [ ] Deployment config

## Notes

Uses Ollama to run AI models locally - no API keys needed. You can switch models by running:
```bash
ollama pull mistral  # or llama2, codellama, etc.
```

Then update your backend config to use the new model. ChromaDB works fine for now, but you could use Pinecone instead if needed.

## Troubleshooting

Ollama not working? Make sure it's running: `ollama serve` and you've pulled a model: `ollama pull llama2`

Node version: Built with Node 19, but 20+ is better. Use `nvm install 20 && nvm use 20` if you run into issues.

Python imports failing? Try `pip install --upgrade pip && pip install -r requirements.txt --force-reinstall`

CORS errors? Check that `backend/app/config.py` has `cors_origins: str = "http://localhost:3000"`

## License

MIT - do whatever you want with it.
