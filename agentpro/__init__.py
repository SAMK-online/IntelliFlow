from .agent import AgentPro
from typing import Any
from agentpro.tools import CodeEngine, YouTubeSearchTool, SlideGenerationTool # add more tools when available

# Initialize optional tools
try:
    from agentpro.tools import AresInternetTool
    ares_tool = AresInternetTool()
    has_ares = True
except (ImportError, ValueError):
    ares_tool = None
    has_ares = False

# Initialize required tools
code_tool = CodeEngine()
youtube_tool = YouTubeSearchTool()
slide_tool = SlideGenerationTool()

__all__ = ['AgentPro', 'code_tool', 'youtube_tool', 'slide_tool']
if has_ares:
    __all__.append('ares_tool')
