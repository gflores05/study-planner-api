from typing import Protocol

from src.shared.aggregate_root import AggregateRoot


class DomainEventPublisherPort(Protocol):
  async def publish_events[T](self, domain: AggregateRoot[T]) -> None: ...
