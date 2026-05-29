# AI Journalist Agent

This Streamlit app is an AI-Powered journalist agent that generates high-quality articles using DeepSeek. It automates the process of researching, writing, and editing articles, allowing you to create compelling content on any topic with ease.

## Features
- Search the web for relevant information on a given topic
- Writes well-structured, informative, and engaging articles
- Edits and refines the generated content to meet the high standards of New York Times

## How it Works
The AI Journalist Agent utilizes three main components:
- **Searcher**: Responsible for generating search terms based on the given topic and searching the web for relevant URLs using SerpAPI.
- **Writer**: Retrieves the text from the provided URLs using the NewspaperToolKit and writes a high-quality article based on the extracted information.
- **Editor**: Coordinates the workflow between the Searcher and Writer, and performs final editing and refinement of the generated article.

## How to Get Started
1. Clone the repository:
```bash
git clone https://github.com/wenyuliuinfo/llm-ai-agent-apps.git
cd 05-journalist-ai-agent/python
```

2. Install the prerequisites:
```bash
pip install -U -r requirements.txt
```


3. Run the application:
```bash
streamlit run journalist-ai-agent.py
```