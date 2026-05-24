# Building Effective Agents

**Content**
- [What are agents](#what-are-agents)
- [When to use agents](#when-to-use-agents)
- [When and how to use frameworks](#when-and-how-to-use-frameworks)
- [Building blocks, workflows, and agents](#building-blocks-workflows-and-agents)


## What are agents?
**Agent** can be defined in several ways. Some customers define agents as fully autonomous systems that operate independently over extended periods, using various tools to accomplish complex tasks. Others use the term to describe more prescriptive implementations that follow predefined workflows. We can categorize all these variations as **agentic systems**, but draw an important architectural distinction between workflows and agents.
- **Workflows** are systems where LLMs and tools are orchestrated through predefined code paths.
- **Agents** are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.


## When to use agents?
When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense.

When more complexity is warranted, workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale. For many applications, optimizing single LLM calls with retrieval and in-context examples is usually enough.


## When and how to use frameworks
There are many frameworks that make agentic systems easier to implement including:
- The Claude Agent SDK
- Strands Agent SDK
- Rivet, a drag and drop GUI LLM workflow builder
- Vellum, another GUI tool for building and testing complex workflows

These frameworks make it easy to get started by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls together. However, they often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice.

We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code.


## Building blocks, workflows, and agents
In this section, we will explore the common patterns for agentic systems we've seen in production. We'll start with our foundational building block - the augmented LLM - and progressively increase complexity, from simple compositional workflows to autonomous agents.


### Building block: The augmented LLM
The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use these capabilities - generating their own search queries, selecting appropriate tools, and determining what information to retain.

![augmented_llm](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%202.51.31 PM.png)

We recommend focusing on two key aspects of the implementation: tailoring these capabilities to your specific use case and ensuring they provide an easy, well-documented interface for your LLM. While there are many ways to implement these augmentations, one approach is through our recently released Model Context Protocol, which allows developers to integrate with a growing ecosystem of third-party tools with a simple client implementation.


### Workflow: Prompt chaining
Prompt chaining decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one. You can add programmatic checks on any intermediate steps to ensure that the process is still on track.

![prompt_chaining_workflow](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%202.56.48 PM.png)

**When to use this workflow**: This workflow is ideal for situations where the task can be easily and cleanly decomposed into fixed subtasks. The main goal is to trade off latency for higher accuracy, by making each LLM call an easier task.

Examples where prompt chaining is useful:
- Generating marketing copy, then translating it into a different language.
- Writing an outline of a document, checking that the outline meets certain criteria, then writing the document based on the outline.


### Workflow: Routing
Routing classifies an input and directs it to a specialized followup task. This workflow allows for separation of concerns, and building more specialized prompts. Without this workflow, optimizing for one kind of input can hurt performance on other inputs.

![routing_workflow](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%203.01.09 PM.png)

**When to use this workflow**: Routing works well for complex tasks where there are distinct categories that are better handled separately, and where classification can be handled accurately, either by an LLM or a more traditional classification model.

Examples where routing is useful:
- Directing different types of customer service queries (general questions, refund requests, technical support) into different downstream processes, prompts, and tools.
- Routing easy questions to smaller, cost-efficient models like Claude Haiku 4.5 and hard questions to more capable models like Claude Sonnet 4.5 to optimize for best performance.


### Workflow: Parallelization
LLMs can sometimes work simultaneously on a task and have their outputs aggregated programmatically. This workflow, parallelization, manifests in two key variations:
- **Sectioning**: Breaking a task into independent subtasks run in parallel.
- **Voting**: Running the same task multiple times to get diverse outputs.

![parallelization_workflow](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%203.06.52 PM.png)

**When to use this workflow**: Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results.

Examples where parallelization is useful:
- Sectioning: Implementing guardrails where one model instance processes user queries while another screens them for inappropriate content or requests. This tends to perform better than having the same LLM call handle both guardrails and the core response.
- Voting: Reviewing a piece of code for vulnerabilities, where several different prompt review and flag the code if they find a problem.


### Workflow: Orchestrator-Workers
In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLM, and synthesizes their results.

![orchestrator-workers-workflow](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%203.12.06 PM.png)

**When to use this workflow**: This workflow is well-suited for complex tasks where you can't predict the subtasks needed. Whereas it's topographically similar, the key difference from parallelization is its flexibility - subtasks aren't pre-defined, but determined by the orchestrator based on the specific input.

Example where orchestrator-workers is useful:
- Coding products that make complex changes to multiple files each time.
- Search tasks that involve gathering and analyzing information from multiple sources for possible relevant information.


### Workflow: Evaluator-Optimizer
In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop.

![evaluator-optimizer-workflow](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%203.17.22 PM.png)

**When to use this workflow**: This workflow is particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value. The two signs of good fit are, first, that LLM responses can be demonstrably improved when a human articulates their feedback; and second, that the LLM can provide such feedback.

Examples where evaluator-optimizer is useful:
- Literary translation there are nuances that the translator LLM might not capture initially, but where an evaluator LLM can provide useful critiques.
- Complex search tasks that require multiple rounds of searching and analysis to gather comprehensive information, where the evaluator decides whether further searches are warranted.


### Agents
Agents are emerging in production as LLMs mature in key capabilities - understanding complex inputs, engaging in reasoning and planning, using tools reliably, and recovering from errors. Agents begin their work with either a command from the human user. Once the task is clear, agents plan and operate independently, potentially returning to the human for further information or judgement. During execution, it's crucial for the agents to gain "ground truth" from the environment at each step to assess its progress. Agents can then pause for human feedback at checkpoints or when encountering blockers. The task often terminates upon completion, but it's also common to include stopping conditions to maintain control.

Agents can handle sophisticated tasks, but their implementation is often straightforward. They are typically just LLMs using tools based on environmental feedback in a loop. It is therefore crucial to design tool-sets and their documentation clearly and thoughtfully.

![autonomous-agent](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%203.25.46 PM.png)

**When to use agents**: Agents can be used for open-ended problems where it's difficult or impossible to predict the required number of steps, and where you can't hardcode a fixed path. The LLM will potentially operate for many turns, and you must have some level of trust in its decision-making. Agents' autonomy makes them ideal for scaling tasks in trusted environment.

Examples where agents are useful:
- A coding agent to resolve SWE-bench tasks, which involve edits to many files based on a task description.
- The "computer use" reference implementation, where Claude uses a computer to accomplish tasks.

![high-level-flow-of-coding-agent](/00-ai-agent-framework/images/Screenshot%202026-05-23%20at%203.30.06 PM.png)
