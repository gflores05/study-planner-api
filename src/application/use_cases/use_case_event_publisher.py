import asyncio

from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.shared.aggregate_root import AggregateRoot


class UseCaseEventPublisher:
  def __init__(self, event_publisher: EventPublisherPort):
    self.event_publisher = event_publisher

  async def _publish_events[T](self, domain: AggregateRoot[T]):
    async with asyncio.TaskGroup() as tg:
      for event in domain.domain_events:
        tg.create_task(self.event_publisher.publish(event))

    domain.clear_domain_events()
