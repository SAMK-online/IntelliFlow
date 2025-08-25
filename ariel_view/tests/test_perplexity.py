import os
import requests
from typing import Dict, Any, List
from pydantic import BaseModel

class ResearchResponse(BaseModel):
    sources: List[Dict[str, str]]
    summary: str
    key_insights: List[str]
    citations: List[str]

def test_perplexity():
    """Test the Perplexity API directly"""
    api_key = os.environ.get("PERPLEXITY_API_KEY", "test_key_placeholder")
    url = "https://api.perplexity.ai/chat/completions"
    
    # Test query
    query = "What are the latest developments in quantum computing?"
    
    research_prompt = f"""
    Perform a comprehensive analysis of: {query}
    
    Please structure your response in the following format:
    1. Summary: A comprehensive overview of the topic
    2. Key Insights: Bullet points of the most important findings
    3. Sources: List of primary sources and their key contributions
    4. Citations: Specific quotes or data points with attributions
    
    Focus on providing factual, well-sourced information with a balance of technical 
    and non-technical explanations.
    """
    
    payload = {
        "model": "sonar-deep-research",
        "messages": [
            {"role": "user", "content": research_prompt}
        ],
        "max_tokens": 2000
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("\n=== Testing Perplexity API ===")
        print(f"Query: {query}")
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print("\nAPI Response:")
        print(content)
        
        # Parse the response into sections
        sections = parse_response(content)
        
        # Create structured response
        research = ResearchResponse(
            sources=[{"name": source} for source in sections.get("Sources", [])],
            summary=sections.get("Summary", "").strip(),
            key_insights=sections.get("Key Insights", []),
            citations=sections.get("Citations", [])
        )
        
        print("\nStructured Response:")
        print("\nSummary:")
        print(research.summary)
        
        print("\nKey Insights:")
        for insight in research.key_insights:
            print(f"- {insight}")
            
        print("\nSources:")
        for source in research.sources:
            print(f"- {source['name']}")
            
        print("\nCitations:")
        for citation in research.citations:
            print(f"- {citation}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def parse_response(content: str) -> Dict[str, Any]:
    """Parse the structured response"""
    sections = {
        "Summary": "",
        "Key Insights": [],
        "Sources": [],
        "Citations": []
    }
    
    current_section = None
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers
        lower_line = line.lower()
        for section in sections.keys():
            if lower_line.startswith(section.lower() + ":"):
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

if __name__ == "__main__":
    test_perplexity()
