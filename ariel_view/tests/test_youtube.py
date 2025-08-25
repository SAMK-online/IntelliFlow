import os
from typing import Dict, Any, List
from pydantic import BaseModel
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import requests

class VideoAnalysis(BaseModel):
    video_id: str
    title: str
    channel: str
    url: str
    publish_date: str
    duration: str
    view_count: int
    transcript_summary: str
    key_points: List[str]
    timestamps: Dict[str, str]
    relevance_score: float
    sentiment_analysis: Dict[str, float]
    technical_complexity: float
    key_topics: List[str]
    speaker_info: Dict[str, str]

def test_youtube_analysis():
    """Test the enhanced YouTube analysis capabilities"""
    # Check for required API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Error: OPENAI_API_KEY not found in environment")
        return
        
    # Set up OpenAI for analysis
    os.environ["OPENAI_API_KEY"] = openai_key
    
    # Test video ID (using a quantum computing video as example)
    video_id = "JhHMJCUmq28"  # Example: 3Blue1Brown's quantum computing video
    
    try:
        print("\n=== Testing YouTube Analysis ===")
        print(f"Video ID: {video_id}")
        
        # Get video metadata
        metadata = get_video_metadata(video_id)
        print("\nVideo Metadata:")
        print(f"Title: {metadata['title']}")
        print(f"Channel: {metadata['channel']}")
        print(f"Duration: {metadata['duration']}")
        print(f"Views: {metadata['view_count']}")
        
        # Get transcript
        transcript = get_transcript(video_id)
        print("\nGot transcript, length:", len(transcript))
        
        # Split transcript into segments
        segments = segment_transcript(transcript)
        print(f"\nSplit into {len(segments)} segments")
        
        # Analyze each segment
        segment_analyses = []
        for i, segment in enumerate(segments):
            print(f"\nAnalyzing segment {i+1}/{len(segments)}...")
            analysis = analyze_segment(segment)
            segment_analyses.append(analysis)
        
        # Combine analyses
        combined = combine_analyses(segment_analyses)
        
        # Calculate overall metrics
        sentiment = calculate_sentiment(segment_analyses)
        complexity = calculate_complexity(segment_analyses)
        speakers = extract_speakers(segment_analyses)
        timestamps = generate_timestamps(transcript, segment_analyses)
        relevance = calculate_relevance(combined)
        
        # Create final analysis
        analysis = VideoAnalysis(
            video_id=video_id,
            title=metadata["title"],
            channel=metadata["channel"],
            url=f"https://youtube.com/watch?v={video_id}",
            publish_date=metadata["publish_date"],
            duration=metadata["duration"],
            view_count=metadata["view_count"],
            transcript_summary=combined["summary"],
            key_points=combined["key_points"],
            timestamps=timestamps,
            relevance_score=relevance,
            sentiment_analysis=sentiment,
            technical_complexity=complexity,
            key_topics=combined["topics"],
            speaker_info=speakers
        )
        
        # Print results
        print("\n=== Analysis Results ===")
        print(f"\nTitle: {analysis.title}")
        print(f"Channel: {analysis.channel}")
        print(f"URL: {analysis.url}")
        
        print("\nTranscript Summary:")
        print(analysis.transcript_summary)
        
        print("\nKey Points:")
        for point in analysis.key_points:
            print(f"- {point}")
            
        print("\nKey Topics:")
        for topic in analysis.key_topics:
            print(f"- {topic}")
            
        print("\nTechnical Complexity Score:", analysis.technical_complexity)
        
        print("\nSentiment Analysis:")
        for sentiment, score in analysis.sentiment_analysis.items():
            print(f"- {sentiment}: {score:.2f}")
            
        print("\nSpeakers:")
        for speaker, info in analysis.speaker_info.items():
            print(f"- {speaker}: {info}")
            
        print("\nKey Timestamps:")
        for time, desc in analysis.timestamps.items():
            print(f"- {time}: {desc}")
            
        print("\nRelevance Score:", analysis.relevance_score)
        
    except Exception as e:
        print(f"Error: {str(e)}")

def get_video_metadata(video_id: str) -> Dict[str, Any]:
    """Get video metadata using YouTube Data API"""
    # For testing, return mock data
    return {
        "title": "Quantum Computing Explained",
        "channel": "3Blue1Brown",
        "publish_date": "2025-04-13",
        "duration": "15:30",
        "view_count": 1000000
    }

def get_transcript(video_id: str) -> str:
    """Get video transcript"""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript_list])
    except Exception as e:
        print(f"Error getting transcript: {str(e)}")
        return ""

def segment_transcript(transcript: str, segment_size: int = 500) -> List[str]:
    """Split transcript into segments"""
    words = transcript.split()
    return [" ".join(words[i:i + segment_size]) 
            for i in range(0, len(words), segment_size)]

def analyze_segment(segment: str) -> Dict[str, Any]:
    """Analyze a transcript segment using GPT-4"""
    try:
        # Initialize OpenAI client
        client = openai.OpenAI()
        
        prompt = f"""
        Analyze this video segment and provide a detailed analysis in JSON format with the following structure:
        {{
            "summary": "A concise summary of the segment",
            "key_points": ["List of main points discussed"],
            "technical_terms": {{
                "term1": "explanation1",
                "term2": "explanation2"
            }},
            "speakers": {{
                "speaker1": "role/description1",
                "speaker2": "role/description2"
            }},
            "sentiment": {{
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 0.0
            }},
            "technical_complexity": 0.0,
            "topics": ["List of key topics covered"]
        }}
        
        Analyze this segment:
        {segment}
        
        Ensure:
        1. Sentiment scores sum to 1.0
        2. Technical complexity is between 0.0 and 1.0
        3. All lists are non-empty
        4. All text fields are properly escaped
        """
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert video content analyzer. Always return valid JSON matching the specified structure exactly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        content = response.choices[0].message.content
        try:
            # Try to parse as JSON
            import json
            result = json.loads(content)
            
            # Validate and fix the response structure
            default_structure = {
                "summary": "",
                "key_points": [],
                "technical_terms": {},
                "speakers": {},
                "sentiment": {"positive": 0.33, "negative": 0.33, "neutral": 0.34},
                "technical_complexity": 0.5,
                "topics": []
            }
            
            # Ensure all required fields exist
            for key, default_value in default_structure.items():
                if key not in result:
                    result[key] = default_value
                    
            # Validate sentiment scores
            sentiment = result["sentiment"]
            total = sum(sentiment.values())
            if total != 0:
                sentiment = {k: v/total for k, v in sentiment.items()}
                result["sentiment"] = sentiment
                
            # Validate technical complexity
            result["technical_complexity"] = max(0.0, min(1.0, float(result["technical_complexity"])))
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")
            # Return default structure
            return default_structure
            
    except Exception as e:
        print(f"Error in segment analysis: {str(e)}")
        return {}

def combine_analyses(analyses: List[Dict]) -> Dict[str, Any]:
    """Combine analyses from multiple segments"""
    combined = {
        "summary": "",
        "key_points": [],
        "topics": set(),
        "technical_terms": {},
        "speakers": {},
        "sentiment": {"positive": 0.0, "negative": 0.0, "neutral": 0.0},
        "technical_complexity": 0.0
    }
    
    valid_analyses = [a for a in analyses if isinstance(a, dict)]
    if not valid_analyses:
        return combined
        
    num_analyses = len(valid_analyses)
    
    for analysis in valid_analyses:
        # Text content
        combined["summary"] += analysis.get("summary", "") + " "
        combined["key_points"].extend(analysis.get("key_points", []))
        combined["topics"].update(set(analysis.get("topics", [])))
        combined["technical_terms"].update(analysis.get("technical_terms", {}))
        
        # Speaker information
        combined["speakers"].update(analysis.get("speakers", {}))
        
        # Numerical metrics
        sentiment = analysis.get("sentiment", {})
        for key in ["positive", "negative", "neutral"]:
            combined["sentiment"][key] += float(sentiment.get(key, 0.0))
            
        complexity = float(analysis.get("technical_complexity", 0.0))
        combined["technical_complexity"] += complexity
    
    # Average the numerical values
    for key in combined["sentiment"]:
        combined["sentiment"][key] /= num_analyses
    combined["technical_complexity"] /= num_analyses
    
    # Deduplicate lists
    combined["key_points"] = list(set(combined["key_points"]))
    combined["topics"] = list(combined["topics"])
    
    # Clean up the summary
    combined["summary"] = combined["summary"].strip()
    
    return combined

def calculate_sentiment(analyses: List[Dict]) -> Dict[str, float]:
    """Calculate overall sentiment"""
    sentiments = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
    
    for analysis in analyses:
        segment_sentiment = analysis.get("sentiment", {})
        for key in sentiments:
            sentiments[key] += segment_sentiment.get(key, 0.0)
    
    # Normalize
    total = sum(sentiments.values()) or 1
    return {k: v/total for k, v in sentiments.items()}

def calculate_complexity(analyses: List[Dict]) -> float:
    """Calculate overall technical complexity"""
    scores = [a.get("technical_complexity", 0.0) for a in analyses]
    return sum(scores) / len(scores) if scores else 0.0

def extract_speakers(analyses: List[Dict]) -> Dict[str, str]:
    """Extract speaker information"""
    speakers = {}
    for analysis in analyses:
        speakers.update(analysis.get("speakers", {}))
    return speakers

def generate_timestamps(transcript: str, analyses: List[Dict]) -> Dict[str, str]:
    """Generate timestamps with context"""
    # For testing, return mock timestamps
    return {
        "0:00": "Introduction to quantum computing",
        "5:30": "Explaining superposition",
        "10:15": "Quantum algorithms overview"
    }

def calculate_relevance(analysis: Dict) -> float:
    """Calculate relevance score"""
    # For testing, return mock score
    return 0.85

if __name__ == "__main__":
    test_youtube_analysis()
