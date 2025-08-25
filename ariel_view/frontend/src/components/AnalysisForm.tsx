import React, { useState } from 'react';
import axios from 'axios';

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

interface AnalysisFormProps {
  onAnalysisComplete: (data: AnalysisData) => void;
}

export const AnalysisForm: React.FC<AnalysisFormProps> = ({ onAnalysisComplete }) => {
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = 'http://127.0.0.1:5003';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      console.log('Making API request to:', `${API_URL}/api/analyze`);
      const response = await axios.post(`${API_URL}/api/analyze`, {
        topic,
        options: { depth: 'quick' }
      });
      console.log('API response:', response.data);
      onAnalysisComplete(response.data);
    } catch (err) {
      console.error('API error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ margin: '20px' }}>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter topic to analyze"
          disabled={isLoading}
          style={{ marginRight: '10px', padding: '5px' }}
        />
        <button type="submit" disabled={isLoading || !topic}>
          {isLoading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
      {error && <div style={{ color: 'red', marginTop: '10px' }}>{error}</div>}
    </div>
  );
};
