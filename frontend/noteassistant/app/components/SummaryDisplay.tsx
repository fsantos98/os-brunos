import React from "react";

interface Summary {
  id: string;
  content: string;
  timestamp: string;
}

interface SummaryDisplayProps {
  summary: Summary | null;
}

const SummaryDisplay: React.FC<SummaryDisplayProps> = ({ summary }) => {
  if (!summary) {
    return <div className="p-4">No summary selected.</div>;
  }

  return (
    <div className="flex-1 p-6">
      <h2 className="text-2xl font-bold mb-2">Latest Summary</h2>
      <p className="text-gray-600 text-sm mb-4">
        {new Date(summary.timestamp).toLocaleString()}
      </p>
      <p className="text-lg">{summary.content}</p>
    </div>
  );
};

export default SummaryDisplay;
