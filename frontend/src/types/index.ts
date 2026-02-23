// TypeScript types for the application

export interface Citation {
  chunk_id: string;
  text: string;
  page_number: number;
  char_start: number;
  char_end: number;
  relevance_score: number;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  question: string;
  processing_time_ms: number;
}

export interface DocumentInfo {
  document_id: string;
  filename: string;
  file_size: number;
  page_count: number;
  uploaded_at: string;
  chunk_count: number;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  file_size: number;
  page_count: number;
  uploaded_at: string;
  status: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  timestamp: Date;
}
