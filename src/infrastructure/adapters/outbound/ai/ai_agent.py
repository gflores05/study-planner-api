import time

from deepagents import create_deep_agent
from google.genai.errors import APIError

from src.infrastructure.adapters.outbound.ai.tools.internet_search import (
  internet_search_factory,
)


class AIAgent:
  def __init__(self, google_agent_model: str, exa_api_key: str) -> None:
    self._google_agent_model = google_agent_model
    self._exa_api_key = exa_api_key

  async def send_content(
    self, prompt: str, system_prompt: str, max_retries=5, initial_delay=2
  ) -> str:

    agent = create_deep_agent(
      model=self._google_agent_model,
      tools=[internet_search_factory(self._exa_api_key)],
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
