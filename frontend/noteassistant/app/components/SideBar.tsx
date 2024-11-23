import React from "react";

interface Summary {
  id: string;
  content: string;
  timestamp: string;
}

interface SidebarProps {
  summaries: Summary[];
  onSelect: (id: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ summaries, onSelect }) => {
  return (
    <aside className="w-1/4 bg-gray-100 p-4 border-r">
      <h2 className="text-xl font-bold mb-4 text-black">Previous Summaries</h2>
      <ul className="space-y-2">
        {summaries.map((summary) => (
          <li
            key={summary.id}
            className="cursor-pointer p-2 rounded-md hover:bg-gray-200"
            onClick={() => onSelect(summary.id)}
          >
            {new Date(summary.timestamp).toLocaleString()}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
