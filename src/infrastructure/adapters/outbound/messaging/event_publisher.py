from src.shared.domain_event import DomainEvent


class EventPublisher:
  async def publish(self, event: DomainEvent) -> None:
    return None
