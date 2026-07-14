from typing import Protocol

from src.application.ports.outbound.messaging.message import MessageEvent


class EventPublisherPort(Protocol):
  async def publish(self, event: MessageEvent) -> None: ...
