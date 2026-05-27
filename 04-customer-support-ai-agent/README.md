# Customer Support Agent with Memory

This Streamlit app implements an AI-Powered customer support agent for synthetic data generated using DeepSeek. The agent uses DeepSeek v4 Pro model and maintains a memory of past interactions using Mem0 library with Qdrant as the vector store.


## Features
- Chat interface for interacting with the AI customer support agent.
- Persistent memory of customer interactions and profiles.
- Synthetic data generation for testing and demonstration.
- Utilizes DeepSeek v4 Pro model for intelligent response.


## How to Get Started
1. Clone the repository:
```bash
git clone https://github.com/wenyuliuinfo/llm-ai-agent-apps.git
cd 04-customer-support-ai-agent/python
```

2. Install the prerequisites:
```bash
pip install -U -r requirements.txt
```

3. Ensure Qdrant is running: the app expects Qdrant to be running on http://localhost:6333. Adjust the configuration in the code if your setup is different:
```bash
docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

4. Run the application:
```bash
streamlit run data-visualisation-ai-agent.py
```
