# IntelliFlow

IntelliFlow is a flexible framework for building AI agents with multiple specialized tools. This repository allows you to create powerful agents that can search the internet, generate code, analyze YouTube videos, create presentations, and more.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-Apache%202.0-blue" alt="License: Apache 2.0">
</p>

## Features

- 🧠 **Flexible Agent Architecture**: Built on the ReAct framework to combine reasoning and action
- 🔧 **Modular Tool System**: Easily extend with custom tools
- 🌐 **Internet Search**: Real-time web search using the Ares API
- 💻 **Code Generation & Execution**: Generate and run Python code on-the-fly
- 🎬 **YouTube Analysis**: Search, extract transcripts, and summarize YouTube videos
- 📊 **Presentation Generation**: Create PowerPoint presentations automatically

## Quick Start

### Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/SAMK-online/IntelliFlow.git
cd IntelliFlow
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
TRAVERSAAL_ARES_API_KEY=your_traversaal_ares_api_key
```
Ares internet tool: Searches the internet for real-time information using the Traversaal Ares API. To get `TRAVERSAAL_ARES_API_KEY`. Follow these steps:

1. Go to the [Traversaal API platform](https://api.traversaal.ai/)
2. Log in or create an account
3. Click **"Create new secret key"**
4. Copy the generated key and paste in `.env` file :

### Running the Agent

From the command line:

```bash
python main.py
```

This starts an interactive session with the agent where you can enter queries.

### Basic Usage

```python
from agentpro import AgentPro, ares_tool, code_tool, youtube_tool
agent = AgentPro(tools=[ares_tool, code_tool, youtube_tool])

# Run a query
response = agent("Generate a summary on the latest AI advancements")
print(response)
```
You can also use the Quick Start Jupyter Notebook to run IntelliFlow directly in Colab.

## Tools Overview
The IntelliFlow toolkit comes with a variety of default tasks, such as:

- **Internet Research**: "What are the latest developments in quantum computing?"
- **Code Generation**: "Create a Python script to analyze stock prices and generate a chart"
- **YouTube Analysis**: "Find and summarize recent videos about machine learning"
- **Presentation Creation**: "Make a presentation about renewable energy sources"

### AresInternetTool

Searches the internet for real-time information using the Traversaal Ares API.

```python
ares_tool = AresInternetTool()
result = ares_tool.run("recent advances in AI")
```

### CodeEngine

Generates and executes Python code based on natural language descriptions.

```python
code_tool = CodeEngine()
result = code_tool.run("create a bar chart comparing FAANG stocks")
```

### YouTubeSearchTool

Searches for YouTube videos, extracts transcripts, and summarizes content.

```python
youtube_tool = YouTubeSearchTool()
result = youtube_tool.run("machine learning tutorials")
```

### SlideGenerationTool

Creates PowerPoint presentations from structured content.

```python
slide_tool = SlideGenerationTool()
slides = [
    {"slide_title": "Introduction", "content": "Overview of the topic"},
    {"slide_title": "Key Points", "content": "The main arguments and findings"}
]
result = slide_tool.run(slides)
```

### DataAnalysisTool

Analyzes data files and provides statistical insights, visualizations, and exploratory data analysis.

```python
data_tool = DataAnalysisTool()

# Basic usage with a file path
result = data_tool.run("path/to/data.csv")

# With specific analysis parameters
analysis_params = {
    "file_path": "path/to/data.csv",
    "analysis_type": "visualization",
    "viz_type": "correlation",
    "columns": ["age", "income", "education"]
}
result = data_tool.run(analysis_params)
```

## Creating Custom Tools

You can create your own tools by extending the `Tool` base class:

```python
from agentpro.tools.base import Tool

class MyCustomTool(Tool):
    name: str = "My Custom Tool"
    description: str = "Description of what your tool does"
    arg: str = "Information about the required input format"

    def run(self, prompt: str) -> str:
        # Your tool implementation here
        return "Result of the tool operation"
```

Then initialize your agent with the custom tool:

```python
custom_tool = MyCustomTool()
agent = AgentPro(tools=[custom_tool, ares_tool, code_tool])
```

## Project Structure

```
IntelliFlow/
├── agentpro/                 # Core framework
│   ├── __init__.py
│   ├── agent.py              # Main agent implementation
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py           # Base tool classes
│   │   ├── ares_tool.py      # Internet search
│   │   ├── code_tool.py      # Code generation
│   │   ├── youtube_tool.py   # YouTube analysis
│   │   ├── slide_tool.py     # Presentation generation
│   │   └── data_tool.py      # Data analysis
│   └── examples/
│       ├── __init__.py
│       └── example_usage.py  # Usage examples
├── ariel_view/               # Advanced analysis platform
│   ├── ariel_agent.py        # Enhanced agent for topic analysis
│   ├── backend/              # Flask API server
│   ├── frontend/             # React TypeScript UI
│   └── tools/                # Enhanced tools (Perplexity, YouTube)
├── main.py                   # CLI entry point
├── requirements.txt          # Dependencies
├── SECURITY.md              # Security guidelines
└── .env.example             # Environment template
```

## Requirements

- Python 3.8+
- OpenAI API key
- Traversaal Ares API key (for internet search)

## Security

IntelliFlow follows security best practices. See [SECURITY.md](SECURITY.md) for detailed security information and guidelines.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for more details.
