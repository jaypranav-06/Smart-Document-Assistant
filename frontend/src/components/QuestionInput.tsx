'use client';

interface QuestionInputProps {
  questions: string[];
  onQuestionsChange: (questions: string[]) => void;
  onSubmit: (e: React.FormEvent) => void;
  querying: boolean;
  documentReady: boolean;
  documentName?: string;
}

export default function QuestionInput({
  questions,
  onQuestionsChange,
  onSubmit,
  querying,
  documentReady,
  documentName,
}: QuestionInputProps) {
  const addQuestion = () => {
    onQuestionsChange([...questions, '']);
  };

  const removeQuestion = (index: number) => {
    if (questions.length > 1) {
      onQuestionsChange(questions.filter((_, i) => i !== index));
    }
  };

  const updateQuestion = (index: number, value: string) => {
    const newQuestions = [...questions];
    newQuestions[index] = value;
    onQuestionsChange(newQuestions);
  };

  const validQuestionCount = questions.filter(q => q.trim()).length;

  return (
    <div
      className={`bg-white rounded-2xl shadow-xl p-8 border transition-all duration-300 ${
        documentReady
          ? 'border-green-200 hover:shadow-2xl'
          : 'border-gray-100 opacity-75'
      }`}
    >
      <div className="flex items-center gap-3 mb-6">
        <div
          className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold shadow-lg transition-all duration-300 ${
            documentReady
              ? 'bg-gradient-to-br from-green-600 to-emerald-600 text-white'
              : 'bg-gray-300 text-gray-600'
          }`}
        >
          2
        </div>
        <h2 className="text-2xl font-bold text-gray-900">Ask Questions</h2>
      </div>

      {!documentReady && (
        <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-3">
          <div className="flex-shrink-0 w-6 h-6 bg-amber-500 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div>
            <p className="text-sm font-semibold text-amber-900">Upload Document First</p>
            <p className="text-xs text-amber-700 mt-1">
              Please upload a PDF document in Step 1 before asking questions
            </p>
          </div>
        </div>
      )}

      {documentReady && (
        <div className="mb-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-green-900">
                Ready to Answer: <span className="font-bold">{documentName}</span>
              </p>
              <p className="text-xs text-green-700 mt-1 flex items-center gap-1">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Tip: Add multiple questions to get comprehensive answers
              </p>
            </div>
          </div>
        </div>
      )}

      <form onSubmit={onSubmit} className="space-y-4">
        {/* Question Inputs */}
        <div className="space-y-3">
          {questions.map((question, index) => (
            <div key={index} className="group">
              <div className="flex gap-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold">
                      {index + 1}
                    </span>
                    <span className="text-sm font-semibold text-gray-700">
                      Question {index + 1}
                    </span>
                  </div>
                  <div className="relative">
                    <textarea
                      value={question}
                      onChange={(e) => updateQuestion(index, e.target.value)}
                      placeholder={
                        documentReady
                          ? 'What would you like to know about this document?'
                          : 'Upload a document first...'
                      }
                      rows={2}
                      className="w-full p-4 pr-12 border-2 border-gray-200 rounded-xl focus:ring-2
                        focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 placeholder-gray-400
                        disabled:bg-gray-50 disabled:cursor-not-allowed transition-all duration-200
                        resize-none hover:border-gray-300"
                      disabled={!documentReady}
                    />
                    {question.trim() && (
                      <div className="absolute right-4 top-1/2 -translate-y-1/2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center shadow-sm">
                        <svg className="w-3.5 h-3.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                </div>
                {questions.length > 1 && (
                  <div className="flex items-center mt-3">
                    <button
                      type="button"
                      onClick={() => removeQuestion(index)}
                      className="p-3 bg-red-50 text-red-600 rounded-xl hover:bg-red-100
                        transition-all duration-200 opacity-0 group-hover:opacity-100 flex items-center justify-center shadow-sm"
                      title="Remove question"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Add Question Button */}
        <button
          type="button"
          onClick={addQuestion}
          disabled={!documentReady}
          className="w-full py-3 px-4 border-2 border-dashed border-indigo-300 text-indigo-600 rounded-xl
            hover:border-indigo-500 hover:bg-indigo-50 disabled:border-gray-300 disabled:text-gray-400
            disabled:cursor-not-allowed transition-all duration-200 font-medium flex items-center
            justify-center gap-2 group"
        >
          <svg className="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Another Question
        </button>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!documentReady || querying || validQuestionCount === 0}
          className="w-full py-4 px-6 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl
            hover:from-green-700 hover:to-emerald-700 disabled:from-gray-300 disabled:to-gray-400
            disabled:cursor-not-allowed transition-all duration-300 font-bold text-lg
            flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transform hover:scale-[1.02]
            disabled:hover:scale-100"
        >
          {querying ? (
            <>
              <svg className="animate-spin h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Processing Your Questions...</span>
            </>
          ) : (
            <>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span>Get Answers {validQuestionCount > 0 ? `(${validQuestionCount})` : ''}</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
