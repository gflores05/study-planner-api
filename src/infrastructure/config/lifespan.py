from contextlib import asynccontextmanager

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI

from src.infrastructure.adapters.outbound.messaging.register_consumers import (
  register_consumers,
)
from src.infrastructure.config.container import Container
from src.infrastructure.config.database import Database
from src.infrastructure.config.messaging import MessageBroker


@inject
def lifespan_factory(
  db: Database = Provide[Container.db],
  message_broker: MessageBroker = Provide[Container.message_broker],
):
  @asynccontextmanager
  async def lifespan(app: FastAPI):
    await db.init()  # startup
    await register_consumers()
    yield
    await db.close()
    await message_broker.close()

  return lifespan
