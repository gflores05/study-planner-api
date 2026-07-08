import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection


class MessageBroker:
  _connection: AbstractConnection | None = None
  _channel: AbstractChannel | None = None

  def __init__(self, rabbitmq_url: str, prefetch_count: int) -> None:
    self._rabbitmq_url = rabbitmq_url
    self._prefetch_count = prefetch_count

  async def get_connection(self) -> AbstractConnection:
    if self._connection is None or self._connection.is_closed:
      self._connection = await aio_pika.connect_robust(self._rabbitmq_url)
    return self._connection

  async def get_channel(self) -> AbstractChannel:
    if self._channel is None or self._channel.is_closed:
      connection = await self.get_connection()
      self._channel = await connection.channel()
      await self._channel.set_qos(prefetch_count=self._prefetch_count)
    return self._channel

  async def close(self) -> None:
    if self._channel and not self._channel.is_closed:
      await self._channel.close()
    if self._connection and not self._connection.is_closed:
      await self._connection.close()
    self._connection = None
    self._channel = None
