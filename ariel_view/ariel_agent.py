from typing import Dict, List, Any
from agentpro import AgentPro
from .tools.perplexity_tool import PerplexityResearchTool, ResearchResponse
from .tools.enhanced_youtube_tool import EnhancedYouTubeAnalysisTool, VideoAnalysis
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    topic: str
    research_findings: ResearchResponse
    video_insights: List[VideoAnalysis]
    combined_analysis: Dict[str, Any]
    suggested_questions: List[str]

class ArielViewAgent:
    def __init__(self):
        # Initialize tools
        self.research_tool = PerplexityResearchTool()
        self.youtube_tool = EnhancedYouTubeAnalysisTool()
        
        # Initialize base agent with our tools
        self.agent = AgentPro(tools=[
            self.research_tool,
            self.youtube_tool
        ])

    async def analyze_topic(self, topic: str) -> AnalysisResult:
        """
        Perform comprehensive analysis of a topic
        Args:
            topic: The topic or situation to analyze
        Returns:
            AnalysisResult containing all findings and insights
        """
        try:
            # Step 1: Perform deep research
            research_results = await self._conduct_research(topic)
            
            # Step 2: Analyze relevant videos
            video_results = await self._analyze_videos(topic, research_results)
            
            # Step 3: Synthesize findings
            combined_analysis = await self._synthesize_findings(
                topic,
                research_results,
                video_results
            )
            
            # Step 4: Generate follow-up questions
            suggested_questions = await self._generate_questions(
                topic,
                research_results,
                video_results
            )
            
            return AnalysisResult(
                topic=topic,
                research_findings=research_results,
                video_insights=video_results,
                combined_analysis=combined_analysis,
                suggested_questions=suggested_questions
            )

        except Exception as e:
            raise Exception(f"Error in Ariel View analysis: {str(e)}")

    async def _conduct_research(self, topic: str) -> ResearchResponse:
        """Perform deep research using Perplexity"""
        return await self.research_tool.run(topic)

    async def _analyze_videos(
        self,
        topic: str,
        research: ResearchResponse
    ) -> List[VideoAnalysis]:
        """Analyze relevant YouTube videos"""
        # Use research findings to enhance video search
        enhanced_query = self._enhance_video_query(topic, research)
        return await self.youtube_tool.run(enhanced_query)

    async def _synthesize_findings(
        self,
        topic: str,
        research: ResearchResponse,
        videos: List[VideoAnalysis]
    ) -> Dict[str, Any]:
        """Synthesize all findings into cohesive insights"""
        synthesis_prompt = f"""
        Synthesize the following research and video analysis about {topic}:
        
        Research Summary:
        {research.summary}
        
        Key Research Insights:
        {research.key_insights}
        
        Video Insights:
        {[video.transcript_summary for video in videos]}
        
        Provide:
        1. Overall narrative
        2. Key themes
        3. Potential implications
        4. Areas of consensus
        5. Areas of debate
        6. Data points and statistics
        """
        
        # Use the agent's LLM to synthesize
        synthesis = await self.agent.run(synthesis_prompt)
        
        return synthesis

    async def _generate_questions(
        self,
        topic: str,
        research: ResearchResponse,
        videos: List[VideoAnalysis]
    ) -> List[str]:
        """Generate insightful follow-up questions"""
        question_prompt = f"""
        Based on the research and analysis of {topic}, generate 5 insightful
        follow-up questions that would help deepen understanding or explore
        important aspects not fully covered in the current analysis.
        
        Consider:
        - Gaps in current research
        - Emerging trends
        - Potential implications
        - Alternative perspectives
        - Technical and non-technical aspects
        """
        
        questions = await self.agent.run(question_prompt)
        return questions

    def _enhance_video_query(
        self,
        topic: str,
        research: ResearchResponse
    ) -> str:
        """Enhance video search query using research insights"""
        # Use key insights to make video search more specific
        key_terms = " OR ".join(research.key_insights[:3])
        return f"{topic} ({key_terms})"
