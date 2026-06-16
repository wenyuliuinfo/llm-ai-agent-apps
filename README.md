# LLM & AI Agent Applications

This repository is a practical, project-based exploration of building applications powered by Large Language Models (LLMs) and AI agents. It is inspired by the "Awesome LLM Apps" ecosystem and focuses on translating core concepts into functional, real-world Python code.

## 🎯 About This Repository

The primary goal of this repo is to provide a hands-on learning journey for developers who want to move beyond simple API calls and start building intelligent, autonomous AI systems. It covers the entire spectrum, from foundational agentic frameworks to complex, multi-agent workflows.

Through a series of structured projects, you will learn how to:
- Design and implement AI agents that can reason, plan, and execute tasks.
- Build multi-agent systems where agents collaborate to solve complex problems.
- Apply agents to specific domains like customer support, data processing, and journalism.

## 📂 Repository Structure

The content is organized into progressive modules, each focusing on a key aspect of LLM-powered application development.

```
llm-ai-agent-apps/
    ├── 00-ai-agent-framework/ # Foundational concepts and "context engineering"
    ├── 01-sequential-workflow/ # Building agents with structured, step-by-step processes
    ├── 02-starter-ai-agents/ # Templates and examples for creating your first agents
    ├── 03-data-process-ai-agent/ # An agent specialized in processing and analyzing data
    ├── 04-customer-support-ai-agent/ # Building a customer service agent using RAG and tools
    ├── 05-journalist-ai-agent/ # An agent that researches and writes news articles
    ├── .gitignore
    └── README.md
```


Each project folder typically contains:
*   **`README.md`**: A detailed guide for that specific project.
*   **`.py` Python scripts**: The core application code, structured for clarity and reusability.
*   **`requirements.txt`**: A list of project-specific Python dependencies.

## 🚀 Getting Started

### Prerequisites
To effectively use this repository, you should have:
*   Solid knowledge of Python programming.
*   A basic understanding of LLMs and prompt engineering.
*   An API key for an LLM provider (e.g., OpenAI, Anthropic, Azure OpenAI, or a local model via Ollama).

### Installation & Running the Code

1. **Clone the repository:**
    ```bash
    git clone https://github.com/wenyuliuinfo/llm-ai-agent-apps.git
    cd llm-ai-agent-apps
    ```

2. **Set up a Python environment:**
It's highly recommended to use a virtual environment.
    ```bash
    # Using venv (Python 3.9+)
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install base dependencies:**
Many projects will likely use langchain, openai, and other common libraries. You can install the core ones globally, or navigate to each project and install its specific requirements.txt.
    ```bash
    cd <lesson_folder_name>/python
    pip install -U -r requirements.txt
    ```

4. **Set up your API Keys:**
Most projects will require an API key. Create a .env file in the root directory or in the specific project folder and add your keys:
    ```text
    OPENAI_API_KEY="your-api-key-here"
    DEEPSEEK_API_KEY="your-api-key-here"
    DEEPSEEK_BASE_URL="your-url-here"
    ```

5. Run a Project:
Navigate into a project folder and execute the main Python script.
    ```bash
    streamlit run data-visualisation-ai-agent.py
    ```

## 🧠 Key Topics & Projects Covered
This repository is designed to take you from a beginner to a proficient builder of AI agents. The projects are structured as follows:

#### 1. Foundations & Frameworks (00-ai-agent-framework)
- Introduces the core concepts of AI agents, including their architecture, reasoning loops, and tool use.
- Covers context engineering – the art of providing LLMs with the right context, memory, and instructions to perform tasks reliably.

#### 2. Sequential Workflow (01-sequential-workflow)
- Explores building agents that follow a predefined, step-by-step process.
- Learn how to create chains of operations where the output of one step becomes the input for the next, ensuring reliable and predictable outcomes.

#### 3. Starter AI Agents (02-starter-ai-agents)
- A hands-on module with templates for creating your first agent.
- Provides examples of agents that can answer questions, use simple tools, and maintain conversational memory.

#### 4. Data Processing AI Agent (03-data-process-ai-agent)
- An agent specialized in data tasks.
- Demonstrates how to build an agent that can load, clean, transform, and analyze structured data (like CSV files) using natural language commands.

#### 5. Customer Support AI Agent (04-customer-support-ai-agent)
- A more advanced project incorporating Retrieval-Augmented Generation (RAG).
- Builds a customer service agent that can access a knowledge base (e.g., product documentation) to provide accurate and context-aware answers to user queries.

#### 6. Journalist AI Agent (05-journalist-ai-agent)
- The most complex project in the series.
- Develops an agentic system that can autonomously research a topic from multiple sources, synthesize information, and generate a structured news article or report.

