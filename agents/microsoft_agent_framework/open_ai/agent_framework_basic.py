"""
Basic example of using the Microsoft Agent Framework OpenAI module.
"""

import asyncio

import rich
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIAgentClient
from openai import OpenAI


async def main() -> None:
    """Example of non-streaming response (get the complete result at once)."""
    pass


if __name__ == "__main__":
    asyncio.run(main())
