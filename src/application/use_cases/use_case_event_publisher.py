import asyncio

from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.messaging.message import MessageEvent
from src.shared.aggregate_root import AggregateRoot
from src.shared.domain_event import DomainEvent


class UseCaseEventPublisher:
  def __init__(self, event_publisher: EventPublisherPort):
    self.event_publisher = event_publisher

  async def _publish_events[T](self, domain: AggregateRoot[T]) -> None:
    async with asyncio.TaskGroup() as tg:
      for event in domain.domain_events:
        message = self._map_domain_event_to_message(event)
        if message is not None:
          tg.create_task(self.event_publisher.publish(message))

    domain.clear_domain_events()

  def _map_domain_event_to_message(
    self, domain_event: DomainEvent
  ) -> MessageEvent | None:
    return None
