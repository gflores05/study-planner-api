import os
from typing import Protocol

from deepagents import create_deep_agent

from src.infrastructure.adapters.outbound.ai.tools.internet_search import (
  internet_search,
)


class AIAgent(Protocol):
  async def send_content(self, prompt: str, system_prompt: str) -> str:
    agent = create_deep_agent(
      model=os.getenv("AGENT_MODEL", "agent_model"),
      tools=[internet_search],
      system_prompt=system_prompt,
    )

    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    return result["messages"][-1].content
