from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject

from src.infrastructure.adapters.outbound.messaging.event_consumer import EventConsumer
from src.infrastructure.config.container import Container


@inject
async def register_consumers(
  study_plan_requested_event_handler: Callable[[dict], Awaitable[None]] = Provide[
    Container.study_plan_requested_event_handler
  ],
  study_plan_generated_event_handler: Callable[[dict], Awaitable[None]] = Provide[
    Container.study_plan_generated_event_handler
  ],
  generate_study_plan_command_handler: Callable[[dict], Awaitable[None]] = Provide[
    Container.generate_study_plan_command_handler
  ],
  report_study_plan_generated_command_handler: Callable[
    [dict], Awaitable[None]
  ] = Provide[Container.report_study_plan_generated_command_handler],
  event_consumer: EventConsumer = Provide[Container.event_consumer],
) -> None:
  # Events
  event_consumer.register("StudyPlanRequestedEvent", study_plan_requested_event_handler)
  event_consumer.register("StudyPlanGeneratedEvent", study_plan_generated_event_handler)

  # Commands
  event_consumer.register(
    "GenerateStudyPlanCommand", generate_study_plan_command_handler
  )
  event_consumer.register(
    "ReportStudyPlanGeneratedCommand", report_study_plan_generated_command_handler
  )

  await event_consumer.start()
