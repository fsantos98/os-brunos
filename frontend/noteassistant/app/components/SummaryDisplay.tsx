import React from "react";

interface Summary {
  id: number;
  summary_text: string;
  user_id: number;
}

interface SummaryDisplayProps {
  summary: Summary | null; // Prop is an object containing a `summary` or `null`
}

const SummaryDisplay: React.FC<SummaryDisplayProps> = ({ summary }) => {
  if (!summary) {
    return <div className="p-4">No summary selected.</div>;
  }

  return (
    <div className="flex-1 p-6">
      <h2 className="text-2xl font-bold mb-2">Latest Summary</h2>
      <p className="text-lg">{summary.summary_text}</p>
    </div>
  );
};

export default SummaryDisplay;
