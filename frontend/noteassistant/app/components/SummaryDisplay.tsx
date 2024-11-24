import React from "react";

interface Summary {
  id: number;
  summary_text: string;
  user_id: number;
}

interface SummaryDisplayProps {
  summary: Summary | null;
}

const SummaryDisplay: React.FC<SummaryDisplayProps> = ({ summary }) => {
  return (
    <div className="min-h-screen flex items-center justify-center ">
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg border border-gray-200 p-8">
        {summary ? (
          <>
            <div className="text-center mb-6">
              <h2 className="text-4xl font-semibold text-indigo-700">
                Transcript Summary
              </h2>
              <p className="text-gray-500 mt-1">Summary ID: #{summary.id}</p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-300 overflow-hidden">
  <div 
    dangerouslySetInnerHTML={{ __html: summary.summary_text }} 
    className="text-lg text-gray-800 leading-relaxed break-words overflow-y-auto max-h-96"
  />
</div>

          </>
        ) : (
          <div className="text-center">
            <h2 className="text-3xl font-semibold text-gray-600">
              No Summary Selected
            </h2>
            <p className="text-gray-500 mt-2">
              Please choose a summary from the sidebar.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SummaryDisplay;
