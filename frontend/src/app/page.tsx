'use client';

import { useState } from 'react';
import { uploadDocument, queryDocument } from '@/lib/api';
import { QueryResponse, DocumentUploadResponse } from '@/types';
import FileUpload from '@/components/FileUpload';
import QuestionInput from '@/components/QuestionInput';
import ResponseCard from '@/components/ResponseCard';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [document, setDocument] = useState<DocumentUploadResponse | null>(null);
  const [questions, setQuestions] = useState<string[]>(['']);
  const [querying, setQuerying] = useState(false);
  const [responses, setResponses] = useState<QueryResponse[]>([]);
  const [currentResponseIndex, setCurrentResponseIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      const result = await uploadDocument(file);
      setDocument(result);
      console.log('Document uploaded:', result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();

    // Filter out empty questions
    const validQuestions = questions.filter(q => q.trim().length > 0);
    if (validQuestions.length === 0) return;

    setQuerying(true);
    setError(null);
    setResponses([]);
    setCurrentResponseIndex(0);

    try {
      // Process each question
      const results: QueryResponse[] = [];
      for (const singleQuestion of validQuestions) {
        const result = await queryDocument(
          singleQuestion,
          document?.document_id,
          3  // Optimized for fast, concise answers
        );
        results.push(result);
      }

      setResponses(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Query failed');
    } finally {
      setQuerying(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-6 md:p-8 lg:p-12">
      <div className="max-w-7xl mx-auto">
        {/* Modern Header */}
        <header className="text-center mb-16 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full text-sm font-semibold mb-6 shadow-lg">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
            </svg>
            AI-Powered Document Analysis
          </div>

          <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-indigo-900 to-purple-900 mb-6">
            Smart Document Assistant
          </h1>

          <p className="text-xl md:text-2xl text-gray-700 mb-6 max-w-3xl mx-auto leading-relaxed">
            Extract insights from your PDFs with AI-powered answers and precise citations
          </p>

          <div className="flex items-center justify-center gap-3 flex-wrap">
            <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl shadow-md">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 text-white rounded-lg flex items-center justify-center font-bold text-sm">
                1
              </div>
              <span className="font-semibold text-gray-900">Upload PDF</span>
            </div>
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
            <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl shadow-md">
              <div className="w-8 h-8 bg-gradient-to-br from-green-600 to-emerald-600 text-white rounded-lg flex items-center justify-center font-bold text-sm">
                2
              </div>
              <span className="font-semibold text-gray-900">Ask Questions</span>
            </div>
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
            <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl shadow-md">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-pink-600 text-white rounded-lg flex items-center justify-center font-bold text-sm">
                3
              </div>
              <span className="font-semibold text-gray-900">Get Answers</span>
            </div>
          </div>
        </header>

        {/* Error Display */}
        {error && (
          <div className="mb-8 p-4 bg-red-50 border-2 border-red-200 rounded-xl flex items-start gap-3 animate-fade-in">
            <div className="flex-shrink-0 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-red-900">Error</p>
              <p className="text-sm text-red-800">{error}</p>
            </div>
            <button
              onClick={() => setError(null)}
              className="flex-shrink-0 text-red-400 hover:text-red-600"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-8 lg:gap-12">
          {/* Left Column: Input Section */}
          <div className="space-y-8">
            <FileUpload
              onFileSelect={handleFileSelect}
              onUpload={handleUpload}
              uploading={uploading}
              selectedFile={file}
              uploadedDocument={document}
            />

            <QuestionInput
              questions={questions}
              onQuestionsChange={setQuestions}
              onSubmit={handleQuery}
              querying={querying}
              documentReady={!!document}
              documentName={document?.filename}
            />
          </div>

          {/* Right Column: Results Section */}
          <div className="lg:sticky lg:top-8 lg:self-start">
            <ResponseCard
              responses={responses}
              currentIndex={currentResponseIndex}
              onNavigate={setCurrentResponseIndex}
            />
          </div>
        </div>

        {/* Modern Footer */}
        <footer className="mt-20 text-center">
          <div className="inline-flex items-center gap-3 px-6 py-3 bg-white rounded-full shadow-lg">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
              </svg>
            </div>
            <span className="text-sm font-semibold text-gray-700">Powered by</span>
            <span className="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">Ollama AI</span>
          </div>
        </footer>
      </div>
    </div>
  );
}
