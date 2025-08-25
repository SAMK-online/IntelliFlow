from setuptools import setup, find_packages

setup(
    name="agentpro",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'openai',
        'youtube_transcript_api',
        'duckduckgo-search',
        'requests',
        'python-pptx',
        'pydantic',
        'python-dotenv',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'openpyxl',
        'pyarrow',
        'scikit-learn',
    ],
)
