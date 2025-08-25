import asyncio
from dotenv import load_dotenv
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import our tools
from ariel_view.tools.perplexity_tool import PerplexityResearchTool
from ariel_view.tools.enhanced_youtube_tool import EnhancedYouTubeAnalysisTool

async def test_perplexity_research():
    print("\n=== Testing Perplexity Research Tool ===")
    tool = PerplexityResearchTool()
    
    # Test topic that should have both technical and non-technical aspects
    topic = "Latest developments in quantum computing and its potential impact on cryptography"
    
    try:
        result = await tool.run(topic)
        
        print(f"\nResearch Results for: {topic}")
        print("\nSummary:")
        print(result.summary)
        
        print("\nKey Insights:")
        for insight in result.key_insights:
            print(f"- {insight}")
            
        print("\nSources:")
        for source in result.sources:
            print(f"- {source['name']}")
            
        print("\nCitations:")
        for citation in result.citations:
            print(f"- {citation}")
            
    except Exception as e:
        print(f"Error in Perplexity research: {str(e)}")

async def test_youtube_analysis():
    print("\n=== Testing Enhanced YouTube Analysis Tool ===")
    tool = EnhancedYouTubeAnalysisTool()
    
    # Test with a technical video topic
    query = "quantum computing explained"
    
    try:
        results = await tool.run(query)
        
        print(f"\nAnalysis Results for: {query}")
        for video in results:
            print(f"\nVideo: {video.title}")
            print(f"Channel: {video.channel}")
            print(f"URL: {video.url}")
            print(f"Duration: {video.duration}")
            print(f"Views: {video.view_count}")
            print(f"Published: {video.publish_date}")
            
            print("\nTranscript Summary:")
            print(video.transcript_summary)
            
            print("\nKey Points:")
            for point in video.key_points:
                print(f"- {point}")
                
            print("\nKey Topics:")
            for topic in video.key_topics:
                print(f"- {topic}")
                
            print("\nTechnical Complexity:", video.technical_complexity)
            
            print("\nSentiment Analysis:")
            for sentiment, score in video.sentiment_analysis.items():
                print(f"- {sentiment}: {score:.2f}")
                
            print("\nSpeakers:")
            for speaker, info in video.speaker_info.items():
                print(f"- {speaker}: {info}")
                
            print("\nRelevance Score:", video.relevance_score)
            
            print("\nKey Timestamps:")
            for time, desc in video.timestamps.items():
                print(f"- {time}: {desc}")
                
    except Exception as e:
        print(f"Error in YouTube analysis: {str(e)}")

async def main():
    # Load environment variables
    load_dotenv()
    
    # Set API keys for testing
    # Load from .env file instead of hardcoding
    from dotenv import load_dotenv
    load_dotenv()
    
    # Verify environment variables are set for testing
    required_keys = ["PERPLEXITY_API_KEY", "OPENAI_API_KEY", "TRAVERSAAL_ARES_API_KEY"]
    for key in required_keys:
        if not os.environ.get(key):
            print(f"Warning: {key} not set for testing")
    
    print("\nPlease provide the following API keys:")
    print("1. OpenAI API key for GPT-4 analysis")
    print("2. Traversaal Ares API key for YouTube search")
    
    # Run tests
    # await test_perplexity_research()
    # await test_youtube_analysis()
    print("\nTests are ready to run once you provide the required API keys.")
    print("Please update the script with your API keys and uncomment the test functions.")

if __name__ == "__main__":
    asyncio.run(main())
