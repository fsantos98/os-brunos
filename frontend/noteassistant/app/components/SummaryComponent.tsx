'use client';

import { useState } from 'react';

const SummaryComponent: React.FC = () => {
  const [date, setDate] = useState<string>(new Date().toISOString().split('T')[0]); // Default to today
  const [startTime, setStartTime] = useState<string>('');
  const [endTime, setEndTime] = useState<string>('');
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://ec2-18-246-27-158.us-west-2.compute.amazonaws.com:5111/summaries/1`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch summary');
      }
      const data = await response.json();
      setSummary(data.summary);
    } catch (err) {
      console.error('Error fetching summary:', err);
      setError('Failed to load summary. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-semibold mb-6 text-center text-black">Get Transcript Summary</h1>
      <div className="space-y-4">
        <div className="flex flex-col space-y-2">
          <label htmlFor="date" className="font-medium text-black">Date:</label>
          <input
            type="date"
            id="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div className="flex space-x-4">
          <div className="flex flex-col space-y-2 w-1/2">
            <label htmlFor="start-time" className="font-medium text-black">Start Time:</label>
            <input
              type="time"
              id="start-time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div className="flex flex-col space-y-2 w-1/2">
            <label htmlFor="end-time" className="font-medium text-black">End Time:</label>
            <input
              type="time"
              id="end-time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>
        <button
          onClick={fetchSummary}
          disabled={loading}
          className={`w-full py-2 px-4 rounded-md text-white ${
            loading ? 'bg-gray-400' : 'bg-indigo-600 hover:bg-indigo-700'
          } focus:outline-none`}
        >
          {loading ? 'Loading...' : 'Get Summary'}
        </button>
      </div>
      {error && <p className="mt-4 text-red-600 text-center">{error}</p>}
      {summary && (
        <div className="mt-6 p-4 bg-gray-100 rounded-md">
          <h2 className="text-xl font-medium mb-2">Summary:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
};

export default SummaryComponent;
