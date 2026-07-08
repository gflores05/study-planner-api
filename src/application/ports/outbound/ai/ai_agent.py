from typing import Protocol


class AIAgentPort(Protocol):
  async def send_content(self, prompt: str, system_prompt: str) -> str: ...
