# ChatAgent vs ChatMessage - Microsoft Agent Framework

This document explains the difference between **ChatAgent** and **ChatMessage** in the Microsoft Agent Framework, commonly used in Azure AI agentic workflows.

## 🧩 ChatMessage

`ChatMessage` represents **a single message** in a conversation. It contains **data only**, not logic.

A `ChatMessage` includes:
- **role** — `user`, `assistant`, `system`, `tool`, etc.
- **content** — text or structured information
- optional metadata

**Example:**

```python
ChatMessage(role="user", content="What's the weather?")
```

Think of it as:
> A message in a chat app — just "who said what."

## 🤖 ChatAgent

`ChatAgent` represents the **agent itself**, the component that:
- Reads input messages
- Calls tools or functions
- Applies reasoning
- Generates output messages
- Produces the next `ChatMessage`

This is your agent's **brain/logic**.

**Example:**

```python
agent = ChatAgent(model=my_model, tools=[calculator, search])
result = agent.step(messages)
```

Think of it as:
> The person writing the messages — the decision-maker.

## 🔥 Summary

| Component | Purpose | Analogy |
| :--- | :--- | :--- |
| **ChatMessage** | Holds text/content of a message | A message in a chat app |
| **ChatAgent** | Generates responses, executes tools, applies logic | The person behind the keyboard |

## Why This Separation Matters

Separating messages from the agent allows:
- Clean inspection of conversation history
- Easy debugging and replay
- Flexible multi-agent architectures
- Swapping models/tools without changing message format
