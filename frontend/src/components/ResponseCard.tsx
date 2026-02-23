'use client';

import { QueryResponse } from '@/types';

interface ResponseCardProps {
  responses: QueryResponse[];
  currentIndex: number;
  onNavigate: (index: number) => void;
}

export default function ResponseCard({
  responses,
  currentIndex,
  onNavigate,
}: ResponseCardProps) {
  if (responses.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-xl p-12 text-center border border-gray-100">
        <div className="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">No Answers Yet</h3>
        <p className="text-gray-600 mb-2">
          Upload a document and ask questions to see AI-powered answers with citations
        </p>
        <p className="text-sm text-gray-500 flex items-center justify-center gap-1">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Tip: You can ask multiple questions at once
        </p>
      </div>
    );
  }

  const currentResponse = responses[currentIndex];

  const goToPrevious = () => {
    onNavigate(Math.max(0, currentIndex - 1));
  };

  const goToNext = () => {
    onNavigate(Math.min(responses.length - 1, currentIndex + 1));
  };

  return (
    <div className="space-y-6">
      {/* Main Answer Card */}
      <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
        {/* Navigation Header */}
        <div className="flex items-center justify-between mb-6 pb-6 border-b-2 border-gray-100">
          <div className="flex items-center gap-3">
            <div className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full font-bold shadow-lg">
              Q&A
            </div>
            {responses.length > 1 && (
              <div className="flex items-center gap-2">
                <span className="text-lg font-bold text-gray-900">
                  {currentIndex + 1}
                </span>
                <span className="text-gray-400">/</span>
                <span className="text-sm text-gray-600">
                  {responses.length}
                </span>
              </div>
            )}
          </div>

          {/* Navigation Controls */}
          {responses.length > 1 && (
            <div className="flex items-center gap-2">
              <button
                onClick={goToPrevious}
                disabled={currentIndex === 0}
                className="p-2.5 rounded-lg bg-gray-100 text-gray-700 hover:bg-indigo-100 hover:text-indigo-600
                  disabled:bg-gray-50 disabled:text-gray-300 disabled:cursor-not-allowed
                  transition-all duration-200"
                title="Previous"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                onClick={goToNext}
                disabled={currentIndex === responses.length - 1}
                className="p-2.5 rounded-lg bg-gray-100 text-gray-700 hover:bg-indigo-100 hover:text-indigo-600
                  disabled:bg-gray-50 disabled:text-gray-300 disabled:cursor-not-allowed
                  transition-all duration-200"
                title="Next"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          )}
        </div>

        {/* Dots Navigation */}
        {responses.length > 1 && (
          <div className="flex items-center justify-center gap-2 mb-8">
            {responses.map((_, idx) => (
              <button
                key={idx}
                onClick={() => onNavigate(idx)}
                className={`h-2.5 rounded-full transition-all duration-300 ${
                  idx === currentIndex
                    ? 'w-10 bg-gradient-to-r from-indigo-600 to-purple-600'
                    : 'w-2.5 bg-gray-300 hover:bg-gray-400'
                }`}
                title={`Question ${idx + 1}`}
              />
            ))}
          </div>
        )}

        {/* Question Section */}
        <div className="mb-8">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl flex items-center justify-center font-bold text-lg shadow-lg">
              Q
            </div>
            <div className="flex-1">
              <p className="text-xs text-blue-600 font-bold uppercase tracking-wider mb-3">
                Question
              </p>
              <p className="text-xl font-bold text-gray-900 leading-relaxed">
                {currentResponse.question}
              </p>
            </div>
          </div>
        </div>

        {/* Answer Section */}
        <div className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border border-green-200">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 text-white rounded-xl flex items-center justify-center font-bold text-lg shadow-lg">
              A
            </div>
            <div className="flex-1">
              <p className="text-xs text-green-700 font-bold uppercase tracking-wider mb-3">
                Answer
              </p>
              <p className="text-gray-800 leading-relaxed text-lg">
                {currentResponse.answer}
              </p>
            </div>
          </div>
        </div>

        {/* Metadata */}
        <div className="mt-6 pt-6 border-t border-gray-200 flex items-center justify-between text-sm">
          <div className="flex items-center gap-2 text-gray-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>
              Processed in <span className="font-bold">{currentResponse.processing_time_ms.toFixed(0)}ms</span>
            </span>
          </div>
          <div className="flex items-center gap-2 text-indigo-600 font-medium">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>{currentResponse.citations.length} Citation{currentResponse.citations.length !== 1 ? 's' : ''}</span>
          </div>
        </div>
      </div>

      {/* Citations Card */}
      <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-600 text-white rounded-xl flex items-center justify-center shadow-lg">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">
            Source Citations ({currentResponse.citations.length})
          </h3>
        </div>

        <p className="text-sm text-gray-600 mb-6">
          Relevant excerpts from the document that support the answer above
        </p>

        <div className="space-y-4">
          {currentResponse.citations.map((citation, idx) => (
            <div
              key={citation.chunk_id}
              className="group relative p-5 border-l-4 border-purple-500 bg-gradient-to-r from-purple-50 to-pink-50 rounded-r-xl hover:shadow-md transition-all duration-200"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="inline-flex items-center justify-center w-8 h-8 bg-purple-500 text-white rounded-full font-bold text-sm shadow">
                    {idx + 1}
                  </span>
                  <span className="text-sm font-bold text-purple-900">
                    Citation {idx + 1}
                  </span>
                </div>
                <span className="px-3 py-1 bg-purple-600 text-white rounded-full text-xs font-bold shadow">
                  Page {citation.page_number}
                </span>
              </div>

              <p className="text-gray-800 leading-relaxed mb-4 pl-11">
                "{citation.text}"
              </p>

              <div className="flex items-center gap-6 text-xs pl-11">
                <div className="flex items-center gap-1.5 text-gray-600">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span className="font-mono">Pos: {citation.char_start}–{citation.char_end}</span>
                </div>
                <div className="flex items-center gap-1.5 text-purple-700 font-semibold">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <span>Relevance: {(citation.relevance_score * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
