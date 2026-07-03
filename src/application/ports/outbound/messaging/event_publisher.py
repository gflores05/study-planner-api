from typing import Protocol

from src.shared.domain_event import DomainEvent


class EventPublisherPort(Protocol):
  async def publish(self, event: DomainEvent) -> None: ...
