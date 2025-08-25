import React, { useState } from 'react';
import { AnalysisForm } from './components/AnalysisForm';
import { AnalysisResults } from './components/AnalysisResults';

interface AnalysisData {
  topic: string;
  research: {
    summary: string;
    key_insights: string[];
    sources: string[];
    citations: string[];
  };
  videos: Array<{
    title: string;
    channel: string;
    url: string;
    summary: string;
    key_points: string[];
    topics: string[];
    technical_complexity: number;
    sentiment: {
      positive: number;
      negative: number;
      neutral: number;
    };
    speakers: Record<string, string>;
    timestamps: Array<{
      time: string;
      content: string;
    }>;
    relevance: number;
  }>;
  combined_analysis: {
    main_themes: string[];
    key_findings: string[];
    recommendations: string[];
  };
  suggested_questions: string[];
}

function App() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);

  const handleAnalysisComplete = (data: AnalysisData) => {
    setAnalysisData(data);
  };

  return (
    <div className="App" style={{ padding: '20px' }}>
      <AnalysisForm onAnalysisComplete={handleAnalysisComplete} />
      {analysisData && <AnalysisResults data={analysisData} />}
    </div>
  );
}

export default App;
