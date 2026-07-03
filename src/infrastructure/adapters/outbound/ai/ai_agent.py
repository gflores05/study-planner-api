from deepagents import create_deep_agent

from src.infrastructure.adapters.outbound.ai.tools.internet_search import (
  internet_search_factory,
)
from src.infrastructure.config.settings import Settings


class AIAgent:
  def __init__(self, settings: Settings) -> None:
    self.settings = settings

  async def send_content(self, prompt: str, system_prompt: str) -> str:
    agent = create_deep_agent(
      model=self.settings.google_agent_model,
      tools=[internet_search_factory(self.settings)],
      system_prompt=system_prompt,
    )

    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    return result["messages"][-1].content
