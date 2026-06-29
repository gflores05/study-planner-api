import asyncio

from src.application.dtos.topic import TopicDTO
from src.application.mappers.topic_mapper import map_topic_dto_to_domain
from src.application.ports.outbound.messaging.event_publisher import EventPublisher
from src.application.ports.outbound.repositories.topic_repository import TopicRepository
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.topic.topic import Topic
from src.util.date_util import utc_now
from src.util.result_util import traverse


class BulkCreateTopicUseCase(UseCaseEventPublisher):
  def __init__(
    self,
    topic_repository: TopicRepository,
    event_publisher: EventPublisher,
  ):
    self.topic_repository = topic_repository
    self.event_publisher = event_publisher

  async def execute(self, dtos: list[TopicDTO]) -> None:
    topics = traverse([map_topic_dto_to_domain(dto) for dto in dtos]).unwrap_or_raise()

    async with asyncio.TaskGroup() as tg:
      for topic in topics:
        topic.add_assessment(generated_on=utc_now())
        topic.add_sub_topics(generated_on=utc_now())
        tg.create_task(self._save_topic(topic))

  async def _save_topic(self, topic: Topic) -> None:
    await self.topic_repository.save(topic)

    await self._publish_events(topic)
