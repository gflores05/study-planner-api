from typing import Protocol

from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_id import TopicId
from src.shared.option import Option


class TopicRepository(Protocol):
  async def get(self, id: TopicId) -> Option[Topic]: ...
  async def save(self, topic: Topic) -> None: ...
