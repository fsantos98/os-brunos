import React from 'react';

interface Summary {
  id: number;
  summary_text: string;
  user_id: number;
}

interface SidebarProps {
  summaries: Summary[];
  onSelect: (id: number) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ summaries, onSelect }) => {
  return (
    <div className="h-full p-6 bg-gradient-to-br from-indigo-600 to-indigo-800 shadow-lg">
      <h2 className="text-3xl font-bold mb-6 border-b border-indigo-400 pb-2">Summaries</h2>
      <ul className="space-y-4">
        {summaries.map((summary) => (
          <li
            key={summary.id}
            onClick={() => onSelect(summary.id)}
            className="cursor-pointer p-4 bg-indigo-500 hover:bg-indigo-400 rounded-md transition transform hover:scale-105 text-center"
          >
            Summary #{summary.id}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
