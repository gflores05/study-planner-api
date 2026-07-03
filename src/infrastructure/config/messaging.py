from src.infrastructure.adapters.outbound.messaging.event_publisher import (
  EventPublisher,
)


def get_event_publisher():
  return EventPublisher()
