from typing import Protocol


class EventHandlerPort(Protocol):
  async def handle(self, payload: dict) -> None: ...
