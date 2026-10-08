from typing import Protocol

from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_id import SubTopicId
from src.shared.option import Option


class SubTopicRepository(Protocol):
  async def get(self, id: SubTopicId) -> Option[SubTopic]: ...
  async def save(self, sub_topic: SubTopic) -> None: ...
