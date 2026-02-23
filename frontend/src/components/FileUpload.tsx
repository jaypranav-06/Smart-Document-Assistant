'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  onUpload: () => void;
  uploading: boolean;
  selectedFile: File | null;
  uploadedDocument: {
    filename: string;
    page_count: number;
    document_id: string;
  } | null;
}

export default function FileUpload({
  onFileSelect,
  onUpload,
  uploading,
  selectedFile,
  uploadedDocument,
}: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles && acceptedFiles[0]) {
      onFileSelect(acceptedFiles[0]);
      setDragActive(false);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'text/html': ['.html', '.htm'],
      'application/rtf': ['.rtf'],
      'application/vnd.oasis.opendocument.text': ['.odt']
    },
    multiple: false,
    onDragEnter: () => setDragActive(true),
    onDragLeave: () => setDragActive(false),
  });

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 text-white rounded-xl flex items-center justify-center font-bold shadow-lg">
          1
        </div>
        <h2 className="text-2xl font-bold text-gray-900">Upload Document</h2>
      </div>

      <p className="text-gray-600 mb-6 leading-relaxed">
        Drop your document here or click to browse. Supports PDF, DOCX, TXT, MD, PPTX, XLSX, CSV, HTML, and more.
      </p>

      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
          isDragActive || dragActive
            ? 'border-indigo-500 bg-indigo-50 scale-[1.02]'
            : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />

        <div className="flex flex-col items-center gap-4">
          {/* Upload Icon */}
          <div className={`w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300 ${
            isDragActive || dragActive
              ? 'bg-indigo-100'
              : 'bg-gray-100'
          }`}>
            <svg
              className={`w-8 h-8 transition-colors duration-300 ${
                isDragActive || dragActive ? 'text-indigo-600' : 'text-gray-400'
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>

          {selectedFile ? (
            <div className="text-sm">
              <p className="font-semibold text-gray-900">{selectedFile.name}</p>
              <p className="text-gray-500 mt-1">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          ) : (
            <div className="text-sm">
              <p className="font-semibold text-gray-900">
                {isDragActive || dragActive ? 'Drop your document here' : 'Drag & drop your document'}
              </p>
              <p className="text-gray-500 mt-1">or click to browse</p>
            </div>
          )}
        </div>
      </div>

      <button
        onClick={onUpload}
        disabled={!selectedFile || uploading}
        className="w-full mt-6 py-3.5 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl
          hover:from-indigo-700 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400
          disabled:cursor-not-allowed transition-all duration-300 font-semibold text-base
          flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transform hover:scale-[1.02]
          disabled:hover:scale-100"
      >
        {uploading ? (
          <>
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processing Document...
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Upload Document
          </>
        )}
      </button>

      {uploadedDocument && (
        <div className="mt-6 p-5 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-green-900 mb-1">Document Ready!</p>
              <p className="text-sm text-green-800">
                <span className="font-medium">{uploadedDocument.filename}</span>
              </p>
              <div className="flex items-center gap-4 mt-2 text-xs text-green-700">
                <span className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                  {uploadedDocument.page_count} pages
                </span>
                <span className="font-mono">ID: {uploadedDocument.document_id.slice(0, 8)}...</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
