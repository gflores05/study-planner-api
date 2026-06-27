from typing import Protocol

from src.application.dtos.topic import TopicDTO


class BulkCreateTopicUseCase(Protocol):
  async def execute(self, dtos: list[TopicDTO]) -> list[TopicDTO]: ...
