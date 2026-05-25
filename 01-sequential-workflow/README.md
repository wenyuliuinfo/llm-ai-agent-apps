# Sequential Workflow - Stock Research Pipeline

This example shows how to create a workflow with sequential steps. Each step is handled by a specialized agent, and outputs flow to the next step.

Different from Teams (agents collaborate dynamically), Workflows give you explicit control over execution order and data flow.

## Key Concepts
- **Workflow**: Orchestrates a sequence of steps
- **Step**: Wraps an agent with a specific task
- Steps execute in order, each building on the previous one

Example prompts to try:
```
- "Analyze NVDA"
- "Research Tesla for investment"
```

## Workflow vs. Team

- Workflow: Explicit step order, predictable execution, clear data flow
- Team: Dynamic collaboration, leader decides who does what

### Use Workflow when
- Steps must happen in a specific order
- Each step has a clear, specialized role
- You want predictable, repeatable execution
- Output from step N feeds into step N+1

### Use Team when
- Agents need to collaborate dynamically
- The leader should decide who to involve
- Tasks benefit from back-and-forth discussion
  
### Advanced Workflow features
- Parallel: Run steps concurrently
- Condition: Run steps only if criteria met
- Loop: Repeat steps until condition met
- Router: Dynamically select which step to run
  

## How to Get Started
1. Clone the repository:
```bash
git clone https://github.com/wenyuliuinfo/llm-ai-agent-apps.git
cd 01-sequential-workflow/python
```

2. Install the prerequisites:
```bash
pip install -U -r requirements.txt
```

3. Run the application:
```bash
python stock-research-pipeline.py
```