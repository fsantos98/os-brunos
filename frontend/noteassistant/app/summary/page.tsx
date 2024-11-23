"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../components/SideBar";
import SummaryDisplay from "../components/SummaryDisplay";
import { useRouter } from "next/navigation";

interface Summary {
  id: string;
  content: string;
  timestamp: string;
}

const SummariesPage = () => {
  const [summaries, setSummaries] = useState<Summary[]>([]);
  const [selectedSummary, setSelectedSummary] = useState<Summary | null>(null);

  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn) {
      router.push('/auth/login');
    } else {
      setIsLoading(false); // User is logged in, so stop loading
    }
  }, [router]);

  

  useEffect(() => {
    // Replace with your API call
    const fetchSummaries = async () => {
      const response = await fetch("localhost:3000/api/summaries");
      const data = await response.json();
      setSummaries(data);
      if (data.length > 0) {
        setSelectedSummary(data[data.length - 1]); // Set the latest summary by default
      }
    };

    fetchSummaries();
  }, []);

  const handleSelectSummary = (id: string) => {
    const summary = summaries.find((summary) => summary.id === id) || null;
    setSelectedSummary(summary);
  };

  if (isLoading) {
    return <div>Loading...</div>; // Render a loading screen or nothing
  }

  return (
    <div className="flex h-screen">
      <Sidebar summaries={summaries} onSelect={handleSelectSummary} />
      <SummaryDisplay summary={selectedSummary} />
    </div>
  );
};

export default SummariesPage;
