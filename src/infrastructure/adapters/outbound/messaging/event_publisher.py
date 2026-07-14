import logging
from datetime import datetime

from aio_pika import DeliveryMode, Message

from src.application.ports.outbound.messaging.message import MessageEvent

logger = logging.getLogger(__name__)


class EventPublisher:
  EXCHANGE_NAME = "domain_events"

  def __init__(self, message_broker) -> None:
    self._message_broker = message_broker

  async def publish(self, event: MessageEvent) -> None:
    try:
      channel = await self._message_broker.get_channel()

      # Declare exchange (idempotent — safe to call every time)
      exchange = await channel.declare_exchange(
        self.EXCHANGE_NAME,
        type="topic",  # topic lets consumers filter by routing key
        durable=True,  # survives broker restarts
      )

      payload = self._serialize(event)
      message = Message(
        body=payload.encode(),
        content_type="application/json",
        delivery_mode=DeliveryMode.PERSISTENT,  # survives broker restarts
        message_id=str(event.event_id),
        type=event.event_name,
        timestamp=event.occurred_on,
      )

      routing_key = f"study_plan.{event.event_name}"

      await exchange.publish(message, routing_key=routing_key)

      logger.info(
        "Event published",
        extra={
          "event_name": event.event_name,
          "event_id": event.event_id,
          "routing_key": routing_key,
        },
      )

    except Exception as e:
      logger.error(f"Failed to publish event {event.event_name}: {e}")
      raise

  def _serialize(self, event: MessageEvent) -> str:
    return event.model_dump_json()
    # return json.dumps(data, default=self._json_serializer)

  @staticmethod
  def _json_serializer(obj):
    if isinstance(obj, datetime):
      return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
