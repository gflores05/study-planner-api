from src.application.messages.study_plan_messages import (
  GenerateStudyPlanCommandMessage,
  ReportStudyPlanErrorCommandMessage,
  ReportStudyPlanGeneratedCommandMessage,
  StudyPlanErrorReportedEventMessage,
  StudyPlanGeneratedEventMessage,
  StudyPlanRequestedEventMessage,
)
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort


async def study_plan_requested_event_handler_factory(
  event_publisher: EventPublisherPort,
):
  async def handle(payload: dict):
    event = StudyPlanRequestedEventMessage.model_validate(payload)

    await event_publisher.publish(
      GenerateStudyPlanCommandMessage(
        event_id=event.event_id,
        occurred_on=event.occurred_on,
        study_plan_id=event.study_plan_id,
        generated_by_user_id=event.requested_by_user_id,
      )
    )

  return handle


async def study_plan_generated_event_handler_factory(
  event_publisher: EventPublisherPort,
):
  async def handle(payload: dict):
    event = StudyPlanGeneratedEventMessage.model_validate(payload)

    await event_publisher.publish(
      ReportStudyPlanGeneratedCommandMessage(
        event_id=event.event_id,
        occurred_on=event.occurred_on,
        study_plan_id=event.study_plan_id,
        reported_by_user_id=event.generated_by_user_id,
      )
    )

  return handle


async def study_plan_error_reported_event_handler_factory(
  event_publisher: EventPublisherPort,
):
  async def handle(payload: dict):
    event = StudyPlanErrorReportedEventMessage.model_validate(payload)

    await event_publisher.publish(
      ReportStudyPlanErrorCommandMessage(
        event_id=event.event_id,
        occurred_on=event.occurred_on,
        study_plan_id=event.study_plan_id,
        reported_by_user_id=event.reported_by_user_id,
        error=event.error,
      )
    )

  return handle
