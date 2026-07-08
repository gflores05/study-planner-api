import json
import logging
from typing import Awaitable, Callable

from aio_pika.abc import AbstractIncomingMessage

from src.infrastructure.config.messaging import MessageBroker

logger = logging.getLogger(__name__)


class EventConsumer:
  EXCHANGE_NAME = "domain_events"

  def __init__(
    self, queue_name: str, routing_keys: list[str], message_broker: MessageBroker
  ):
    self._queue_name = queue_name
    self._routing_keys = routing_keys
    self._message_broker = message_broker
    self._handlers: dict[str, Callable[[dict], Awaitable[None]]] = {}

  def register(self, event_name: str, handler: Callable[[dict], Awaitable[None]]):
    """Register a handler for a specific event type."""
    self._handlers[event_name] = handler
    return self

  async def start(self) -> None:
    channel = await self._message_broker.get_channel()

    exchange = await channel.declare_exchange(
      self.EXCHANGE_NAME,
      type="topic",
      durable=True,
    )

    queue = await channel.declare_queue(
      self._queue_name,
      durable=True,  # survives broker restarts
    )

    # Bind queue to routing keys
    for key in self._routing_keys:
      await queue.bind(exchange, routing_key=key)

    await queue.consume(self._handle_message)
    logger.info(f"Consumer started on queue: {self._queue_name}")

  async def _handle_message(self, message: AbstractIncomingMessage) -> None:
    async with message.process():  # auto ack/nack
      try:
        payload = json.loads(message.body)
        event_name = message.type

        if event_name is None:
          raise Exception("Invalid event name")

        handler = self._handlers.get(event_name)
        if handler:
          await handler(payload)
        else:
          logger.warning(f"No handler registered for event: {event_name}")

      except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise  # triggers nack — message goes back to queue
