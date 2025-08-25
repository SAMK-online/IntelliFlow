from typing import Dict, Any
from tools.perplexity_tool import PerplexityResearchTool

class TopicAnalyzer:
    def __init__(self):
        self.research_tool = PerplexityResearchTool()

    def analyze_topic(self, topic: str, depth: str = "quick") -> Dict[str, Any]:
        """
        Analyze a topic using the Perplexity API
        Args:
            topic: Topic to analyze
            depth: Analysis depth ('quick' or 'deep')
        Returns:
            Dict containing the API response
        """
        print(f"Analyzing topic: {topic}")

        try:
            # Get research results directly from the API
            print("Calling Perplexity API...")
            research = self.research_tool.run(topic)
            print(f"Research results: {research}")
            return research

        except Exception as e:
            print(f"Error in research analysis: {str(e)}")
            return {"error": str(e)}

