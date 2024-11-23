"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../components/SideBar";
import SummaryDisplay from "../components/SummaryDisplay";
import { useRouter } from "next/navigation";

interface Summary {
  id: number;
  summary_text: string;
  user_id: number;
}

const SummariesPage = () => {
  const [summaries, setSummaries] = useState<Summary[]>([]);
  const [selectedSummary, setSelectedSummary] = useState<Summary | null>(null);

  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const isLoggedIn = localStorage.getItem("isLoggedIn");
    if (!isLoggedIn) {
      router.push("/auth/login");
    } else {
      setIsLoading(false); // User is logged in, so stop loading
    }
  }, [router]);

  useEffect(() => {
    // Replace with your API call
    const fetchSummaries = async () => {
      try {
        const response = await fetch(
          "http://ec2-18-246-27-158.us-west-2.compute.amazonaws.com:5111/summaries/1"
        );
        const data = await response.json();
        console.log(data);

        // Ensure data structure is valid before using
        if (data && data.summaries) {
          setSummaries(data.summaries);
          if (data.summaries.length > 0) {
            setSelectedSummary(data.summaries[data.summaries.length - 1]); // Set the latest summary by default
          }
        }
      } catch (error) {
        console.error("Error fetching summaries:", error);
      }
    };

    fetchSummaries();
  }, []);

  const handleSelectSummary = (id: number) => {
    const summary = summaries.find((summary) => summary.id === id) || null;
    setSelectedSummary(summary);
  };

  if (isLoading) {
    return <div>Loading...</div>; // Render a loading screen or nothing
  }

  console.log('selectedSummary: ', selectedSummary);

  return (
    <div className="flex h-screen">
      <Sidebar summaries={summaries} onSelect={handleSelectSummary} />
      <SummaryDisplay summary={selectedSummary} />
    </div>
  );
};

export default SummariesPage;
