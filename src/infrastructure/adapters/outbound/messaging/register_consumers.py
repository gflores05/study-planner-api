from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject

from src.infrastructure.adapters.outbound.messaging.event_consumer import EventConsumer
from src.infrastructure.config.container import Container


@inject
async def register_consumers(
  study_plan_requested_event_handler: Callable[[dict], Awaitable[None]] = Provide[
    Container.study_plan_requested_event_handler
  ],
  event_consumer: EventConsumer = Provide[Container.event_consumer],
) -> None:
  event_consumer.register("StudyPlanRequested", study_plan_requested_event_handler)

  await event_consumer.start()
