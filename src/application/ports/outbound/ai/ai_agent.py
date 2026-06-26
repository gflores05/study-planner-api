from typing import Protocol


class AIAgent(Protocol):
  async def send_content(self, prompt: str, system_prompt: str) -> str: ...
