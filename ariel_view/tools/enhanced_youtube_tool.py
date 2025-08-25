from typing import List, Dict, Any
from pydantic import BaseModel
from openai import OpenAI
import os

class VideoAnalysis(BaseModel):
    video_id: str
    title: str
    channel: str
    url: str = ''
    publish_date: str = ''
    duration: str = ''
    view_count: int = 0
    transcript_summary: str = ''
    key_points: List[str] = []
    timestamps: Dict[str, str] = {}  # timestamp -> description
    relevance_score: float = 0.0
    sentiment_analysis: Dict[str, float] = {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
    technical_complexity: float = 5.0  # 0-10 score
    key_topics: List[str] = []
    speaker_info: Dict[str, str] = {}  # speaker -> role/description

class EnhancedYouTubeAnalysisTool:
    name: str = "enhanced_youtube_analysis"
    description: str = "performs in-depth analysis of relevant youtube videos"
    arg: str = "topic to analyze from youtube"

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        if not os.environ.get('OPENAI_API_KEY'):
            raise ValueError('OPENAI_API_KEY environment variable not set')

    def run(self, prompt: str) -> List[VideoAnalysis]:
        """
        Search for relevant videos and perform in-depth analysis
        Args:
            prompt: The topic to analyze
        Returns:
            List of VideoAnalysis objects containing detailed analysis of each relevant video
        """
        try:
            # Mock video search for now
            search_results = [
                {
                    'video_id': '123',
                    'title': 'Sample Video 1',
                    'channel': 'Sample Channel',
                    'duration': '10:00',
                    'view_count': 1000,
                    'publish_date': '2024-04-13'
                },
                {
                    'video_id': '456',
                    'title': 'Sample Video 2',
                    'channel': 'Sample Channel',
                    'duration': '15:00',
                    'view_count': 2000,
                    'publish_date': '2024-04-13'
                }
            ]
            
            analyzed_videos = []
            
            # Process each video in depth
            for video in search_results[:5]:  # Analyze top 5 most relevant videos
                analysis = self._analyze_video(video)
                if analysis:
                    analyzed_videos.append(analysis)
            
            return analyzed_videos

        except Exception as e:
            raise Exception(f"Error analyzing YouTube videos: {str(e)}")

    def _get_transcript(self, video_id: str) -> str:
        # Mock transcript for now
        return f"This is a mock transcript for video {video_id}. It contains some technical terms and discussions about various topics."

    def _get_video_metadata(self, video_id: str) -> Dict[str, Any]:
        # Mock metadata for now
        return {
            'title': f'Sample Video {video_id}',
            'channel': 'Sample Channel',
            'duration': '10:00',
            'view_count': 1000,
            'publish_date': '2024-04-13'
        }

    def _segment_transcript(self, transcript: str) -> List[str]:
        # Simple segmentation by sentences
        return [s.strip() for s in transcript.split('.') if s.strip()]

    def _combine_segment_analyses(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Combine all segment analyses
        all_topics = set()
        all_key_points = []
        summary_parts = []

        for analysis in analyses:
            all_topics.update(analysis.get('topics', []))
            all_key_points.extend(analysis.get('key_points', []))
            if 'summary' in analysis:
                summary_parts.append(analysis['summary'])

        return {
            'summary': ' '.join(summary_parts),
            'key_points': list(set(all_key_points)),
            'topics': list(all_topics)
        }

    def _calculate_overall_sentiment(self, analyses: List[Dict[str, Any]]) -> Dict[str, float]:
        # Average sentiment scores
        total_positive = sum(a.get('sentiment', {}).get('positive', 0) for a in analyses)
        total_negative = sum(a.get('sentiment', {}).get('negative', 0) for a in analyses)
        total_neutral = sum(a.get('sentiment', {}).get('neutral', 0) for a in analyses)
        count = len(analyses) or 1

        return {
            'positive': total_positive / count,
            'negative': total_negative / count,
            'neutral': total_neutral / count
        }

    def _calculate_technical_complexity(self, analyses: List[Dict[str, Any]]) -> float:
        # Average complexity scores
        total = sum(a.get('technical_complexity', 0) for a in analyses)
        return total / (len(analyses) or 1)

    def _extract_speakers(self, analyses: List[Dict[str, Any]]) -> Dict[str, str]:
        # Combine speaker information
        speakers = {}
        for analysis in analyses:
            if 'speakers' in analysis:
                speakers.update(analysis['speakers'])
        return speakers

    def _generate_smart_timestamps(self, transcript: str, analyses: List[Dict[str, Any]]) -> Dict[str, str]:
        # Mock timestamps for now
        return {
            '0:00': 'Introduction',
            '1:00': 'Main discussion',
            '5:00': 'Conclusion'
        }

    def _calculate_relevance_score(self, analysis: Dict[str, Any], query: str, complexity: float) -> float:
        # Mock relevance calculation
        return 0.8

    def _analyze_video(self, video_data: Dict[str, Any]) -> VideoAnalysis:
        """
        Perform detailed analysis of a single video
        Args:
            video_data: Data about the video from initial search
        Returns:
            VideoAnalysis object containing detailed analysis
        """
        try:
            # Get video transcript and metadata
            transcript = self._get_transcript(video_data["video_id"])
            metadata = self._get_video_metadata(video_data["video_id"])
            
            # Split transcript into segments for better analysis
            segments = self._segment_transcript(transcript)
            
            # Analyze each segment with LLM
            segment_analyses = []
            for segment in segments:
                analysis_prompt = f"""
                Analyze this video segment and provide:
                1. Summary of the segment
                2. Key points discussed
                3. Technical terms used and their explanations
                4. Speaker identification (if multiple speakers)
                5. Sentiment analysis
                6. Technical complexity (0-1 score)
                7. Key topics covered
                
                Segment: {segment}
                """
                
                segment_analysis = self._analyze_with_llm(analysis_prompt)
                segment_analyses.append(segment_analysis)
            
            # Combine segment analyses
            combined_analysis = self._combine_segment_analyses(segment_analyses)
            
            # Calculate overall metrics
            sentiment = self._calculate_overall_sentiment(segment_analyses)
            technical_complexity = self._calculate_technical_complexity(segment_analyses)
            
            # Extract speaker information
            speakers = self._extract_speakers(segment_analyses)
            
            # Generate timestamps with context
            timestamps = self._generate_smart_timestamps(transcript, segment_analyses)
            
            # Calculate relevance score based on multiple factors
            relevance_score = self._calculate_relevance_score(
                combined_analysis,
                video_data.get("search_query", ""),
                technical_complexity
            )
            
            return VideoAnalysis(
                video_id=video_data["video_id"],
                title=metadata["title"],
                channel=metadata["channel"],
                url=f"https://youtube.com/watch?v={video_data['video_id']}",
                publish_date=metadata["publish_date"],
                duration=metadata["duration"],
                view_count=metadata["view_count"],
                transcript_summary=combined_analysis["summary"],
                key_points=combined_analysis["key_points"],
                timestamps=timestamps,
                relevance_score=relevance_score,
                sentiment_analysis=sentiment,
                technical_complexity=technical_complexity,
                key_topics=combined_analysis["topics"],
                speaker_info=speakers
            )

        except Exception as e:
            print(f"Error analyzing video {video_data['video_id']}: {str(e)}")
            return None

    def _analyze_with_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Use LLM to analyze video content
        Args:
            prompt: Analysis prompt including transcript
        Returns:
            Dict containing analysis results
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert video content analyzer. "
                                                "Provide a structured analysis in JSON format with the following fields:"
                                                "summary, key_points (list), topics (list), sentiment (dict with positive/negative/neutral), "
                                                "technical_complexity (0-10), speaker_info (dict)."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            # Parse the JSON response
            # Safely parse JSON response instead of using eval
            try:
                import json
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                # Fallback: return as string if not valid JSON
                return response.choices[0].message.content
            
        except Exception as e:
            # Return default values on error
            print(f"Error in LLM analysis: {str(e)}")
            return {
                "summary": "Error analyzing video content",
                "key_points": ["Could not analyze video"],
                "topics": ["error"],
                "sentiment": {"positive": 0.33, "negative": 0.33, "neutral": 0.34},
                "technical_complexity": 5.0,
                "speaker_info": {}
            }
