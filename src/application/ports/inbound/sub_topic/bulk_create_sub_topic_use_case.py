from typing import Protocol

from src.application.dtos.sub_topic import SubTopicDTO


class BulkCreateSubTopicUseCase(Protocol):
  async def execute(self, dtos: list[SubTopicDTO]) -> list[SubTopicDTO]: ...
