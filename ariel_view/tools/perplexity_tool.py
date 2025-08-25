from typing import List, Dict, Any
import requests
import os
import re
import json
from pydantic import BaseModel

class ResearchResponse(BaseModel):
    sources: List[Dict[str, str]]
    summary: str
    key_insights: List[str]
    citations: List[str]

class PerplexityResearchTool:
    name: str = "perplexity_research"
    description: str = "performs deep research using perplexity sonar api"
    arg: str = "topic or query to research"
    api_key: str = None

    def __init__(self):
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable not set")

    def run(self, prompt: str) -> Dict[str, Any]:
        """
        Perform research on the given topic using Perplexity Sonar API
        Args:
            prompt: The topic or query to research
        Returns:
            Dictionary containing the API response
        """
        try:
            return self._call_perplexity_api(prompt)
        except Exception as e:
            return {"error": str(e)}

    def _call_perplexity_api(self, query: str) -> Dict[str, Any]:
        """
        Make the actual API call to Perplexity Sonar
        Args:
            query: The research query
        Returns:
            Dict containing the API response
        """
        url = "https://api.perplexity.ai/chat/completions"
        
        # Simple research prompt
        research_prompt = f"Analyze and provide information about {query}"

        payload = {
            "model": "sonar-deep-research",
            "messages": [
                {"role": "user", "content": research_prompt}
            ],
            "max_tokens": 1000
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            print(f"Making API call to Perplexity for query: {query}")
            print(f"Making request to {url}")
            print(f"Headers: {headers}")
            print(f"Payload: {payload}")
            
            response = requests.post(url, json=payload, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response text: {response.text}")
            
            response.raise_for_status()
            
            # Process the response
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"Perplexity API response: {content}")
            
            # Just return the content directly
            return {"content": content}
            
            return {"content": content}
            
        except Exception as e:
            print(f"Perplexity API error: {str(e)}")
            return {"error": str(e)}
        
    def _parse_research_response(self, content: str) -> Dict[str, Any]:
        """
        Parse the structured response from Perplexity
        Args:
            content: Raw response content
        Returns:
            Dict containing parsed sections
        """
        sections = {
            "Summary": "",
            "Key Insights": [],
            "Sources": [],
            "Citations": []
        }
        
        current_section = None
        current_list = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a section header
            for section in sections.keys():
                if line.lower().startswith(section.lower() + ":"):
                    current_section = section
                    break
            
            if current_section:
                if current_section == "Summary":
                    if not line.lower().startswith("summary:"):
                        sections["Summary"] += line + " "
                else:
                    # For list items
                    if line.startswith("-") or line.startswith("*"):
                        item = line.lstrip("- *").strip()
                        sections[current_section].append(item)
        
        return sections
