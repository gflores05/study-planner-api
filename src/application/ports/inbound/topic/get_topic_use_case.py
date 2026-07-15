from typing import Protocol

from src.application.dtos.topic import TopicDTO


class GetTopicUseCasePort(Protocol):
  async def execute(self, id: str, include_children: bool) -> TopicDTO: ...
