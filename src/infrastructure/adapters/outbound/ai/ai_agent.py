import time

from deepagents import create_deep_agent
from google.genai.errors import APIError
from langchain_google_genai import ChatGoogleGenerativeAI

from src.infrastructure.adapters.outbound.ai.tools.internet_search import (
  internet_search_factory,
)
from src.infrastructure.config.settings import Settings


class AIAgent:
  def __init__(self, settings: Settings) -> None:
    self.settings = settings

  async def send_content(
    self, prompt: str, system_prompt: str, max_retries=5, initial_delay=2
  ) -> str:

    model = ChatGoogleGenerativeAI(
      model=self.settings.google_agent_model, api_key=self.settings.gemini_api_key
    )

    agent = create_deep_agent(
      model=model,
      tools=[internet_search_factory(self.settings.exa_api_key)],
      system_prompt=system_prompt,
    )

    delay = initial_delay
    for attempt in range(max_retries):
      try:
        result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

        return result["messages"][-1].content
      except APIError as e:
        if e.code == 503:
          print(
            f"Attempt {attempt + 1} failed due to 503 (High Demand). Retrying in {delay}s."
          )
          time.sleep(delay)
          delay *= 2
        else:
          raise e
      except Exception as e:
        print(f"Non-retryable error: {e}")
        raise e

    raise Exception("Max retries exceeded. Gemini API is still unavailable.")
