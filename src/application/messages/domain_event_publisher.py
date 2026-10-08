import asyncio

from src.application.mappers.study_plan_mapper import (
  map_study_plan_domain_event_to_message,
)
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.messaging.message import MessageEvent
from src.domain.study_plan.study_plan import StudyPlan
from src.shared.aggregate_root import AggregateRoot
from src.shared.domain_event import DomainEvent


class DomainEventPublisher:
  def __init__(self, event_publisher: EventPublisherPort):
    self.event_publisher = event_publisher

  async def publish_events[T](self, domain: AggregateRoot[T]) -> None:
    async with asyncio.TaskGroup() as tg:
      for event in domain.domain_events:
        message = self._map_domain_event_to_message(domain, event)
        if message is not None:
          tg.create_task(self.event_publisher.publish(message))

    domain.clear_domain_events()

  def _map_domain_event_to_message[T](
    self, domain: AggregateRoot[T], domain_event: DomainEvent
  ) -> MessageEvent | None:
    match domain:
      case StudyPlan():
        return map_study_plan_domain_event_to_message(domain_event=domain_event)

    return None
