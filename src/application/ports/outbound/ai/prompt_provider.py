from dataclasses import dataclass

from typing_extensions import Protocol


@dataclass
class Prompts:
  system: str
  human: str


class PromptProvider[T](Protocol):
  async def get_prompts(self, params: T) -> Prompts: ...
