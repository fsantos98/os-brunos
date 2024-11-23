import React from "react";

interface Summary {
  id: number;
  summary_text: string;
}

interface SidebarProps {
  summaries: Summary[]; // Fixed type to be an array of Summary objects
  onSelect: (id: number) => void; // Updated to use `number` for consistency
}

const Sidebar: React.FC<SidebarProps> = ({ summaries, onSelect }) => {
  console.log(summaries);

  return (
    <aside className="w-1/4 bg-gray-100 p-4 border-r">
      <h2 className="text-xl font-bold mb-4 text-black">Previous Summaries</h2>
      <ul className="space-y-2">
        {summaries.map((summary) => (
          <li
            key={summary.id}
            className="cursor-pointer p-2 rounded-md hover:bg-gray-200"
            onClick={() => onSelect(summary.id)} // Pass `number` directly
          >
            {summary.summary_text}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
