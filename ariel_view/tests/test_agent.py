import asyncio
from dotenv import load_dotenv
from ..ariel_agent import ArielViewAgent

async def test_analysis():
    # Load environment variables
    load_dotenv()
    
    # Initialize agent
    agent = ArielViewAgent()
    
    # Test topic
    topic = "Impact of AI on healthcare in 2025"
    
    try:
        # Run analysis
        result = await agent.analyze_topic(topic)
        
        # Print results
        print(f"\n=== Analysis Results for: {topic} ===\n")
        
        print("Research Summary:")
        print(result.research_findings.summary)
        print("\nKey Research Insights:")
        for insight in result.research_findings.key_insights:
            print(f"- {insight}")
            
        print("\nVideo Insights:")
        for video in result.video_insights:
            print(f"\nVideo: {video.title}")
            print(f"Channel: {video.channel}")
            print(f"Relevance Score: {video.relevance_score}")
            print("Key Points:")
            for point in video.key_points:
                print(f"- {point}")
                
        print("\nCombined Analysis:")
        for key, value in result.combined_analysis.items():
            print(f"\n{key}:")
            print(value)
            
        print("\nSuggested Follow-up Questions:")
        for question in result.suggested_questions:
            print(f"- {question}")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_analysis())
