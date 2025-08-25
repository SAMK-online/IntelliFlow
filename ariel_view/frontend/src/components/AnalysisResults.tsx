import React from 'react';


interface AnalysisResultsProps {
  data: {
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
  };
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data }) => {
  return (
    <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
      {JSON.stringify(data, null, 2)}
    </pre>
  );
};
