from src.shared.domain_event import DomainEvent


class FakeEventPublisher:
  def __init__(self):
    self.events: list[DomainEvent] = []

  async def publish(self, event: DomainEvent) -> None:
    self.events.append(event)
