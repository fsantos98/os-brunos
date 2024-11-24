import React, { useEffect } from "react";
import Mermaid from "react-mermaid2";

interface Summary {
  id: number;
  title: string;
  summary_text: string;
  user_id: number;
  createdAt: string;
}

interface SummaryDisplayProps {
  summary: Summary | null;
}

const extractAndReplaceMermaidHTML = (htmlString: string): React.ReactNode => {
  const mermaidRegex = /```(?:\s*mermaid)?\s*([\s\S]*?)```/i;

  const result: React.ReactNode[] = [];
  let remainingText = htmlString;
  let match;

  while ((match = mermaidRegex.exec(remainingText)) !== null) {
    const [fullMatch, mermaidCode] = match;

    // Add HTML before the Mermaid block
    const beforeHTML = remainingText.slice(0, match.index);
    if (beforeHTML) {
      result.push(
        <div
          key={`text-${result.length}`}
          dangerouslySetInnerHTML={{ __html: beforeHTML }}
        />
      );
    }

    // Add the rendered Mermaid diagram
    result.push(
      <Mermaid
        key={`mermaid-${result.length}`}
        chart={mermaidCode.trim()}
        config={{
          startOnLoad: true,
          theme: "default",
        }}
      />
    );

    // Update remaining text to after the current match
    remainingText = remainingText.slice(match.index + fullMatch.length);
  }

  // Add any remaining HTML after the last Mermaid block
  if (remainingText) {
    result.push(
      <div
        key={`text-${result.length}`}
        dangerouslySetInnerHTML={{ __html: remainingText }}
      />
    );
  }

  return result;
};

const SummaryDisplay: React.FC<SummaryDisplayProps> = ({ summary }) => {
  useEffect(() => {
    // Mermaid needs to be explicitly initialized when the component mounts
    const script = document.createElement("script");
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.4.0/mermaid.min.js";
    script.onload = () => {
      if (window.mermaid) {
        window.mermaid.initialize({ startOnLoad: true });
      }
    };
    document.body.appendChild(script);
    return () => {
      document.body.removeChild(script); // Clean up script on component unmount
    };
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg border border-gray-200 p-8">
        {summary ? (
          <>
            <div className="text-center mb-6">
              <h2 className="text-4xl font-semibold text-indigo-700">
                Transcript Summary
              </h2>
              <b className="text-sm text-gray-500">{summary.createdAt}</b>
              <p className="text-gray-500 mt-1">{summary.title}</p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-300 overflow-hidden text-lg text-gray-800 leading-relaxed break-words overflow-y-auto max-h-96">
              {extractAndReplaceMermaidHTML(summary.summary_text)}
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
