from src.application.dtos.study_plan import StudyPlanDTO, StudyPlanStatusDTO
from src.application.mappers.topic_mapper import map_topic_domain_to_dto
from src.application.messages.study_plan_messages import (
  StudyPlanGeneratedEventMessage,
  StudyPlanRequestedEventMessage,
)
from src.application.ports.outbound.messaging.message import MessageEvent
from src.domain.study_plan.domain_events import StudyPlanGenerated, StudyPlanRequested
from src.domain.study_plan.study_plan import StudyPlan, StudyPlanStatus
from src.shared.domain_event import DomainEvent


def map_study_plan_domain_to_dto(domain: StudyPlan) -> StudyPlanDTO:
  return StudyPlanDTO(
    id=str(domain.id),
    subject=str(domain.subject),
    level=domain.level,
    topics=[map_topic_domain_to_dto(t) for t in domain.topics],
    grade=int(domain.grade),
    status=study_plan_status_domain_to_dto(domain.status),
  )


def study_plan_status_domain_to_dto(status: StudyPlanStatus):
  match status:
    case StudyPlanStatus.PENDING:
      return StudyPlanStatusDTO.PENDING
    case StudyPlanStatus.GENERATING:
      return StudyPlanStatusDTO.GENERATING
    case StudyPlanStatus.COMPLETED:
      return StudyPlanStatusDTO.COMPLETED
    case StudyPlanStatus.FAILED:
      return StudyPlanStatusDTO.FAILED

  return StudyPlanStatusDTO.UNKNOWN


def map_study_plan_domain_event_to_message(
  domain_event: DomainEvent,
) -> MessageEvent | None:
  match domain_event:
    case StudyPlanRequested():
      return StudyPlanRequestedEventMessage(
        event_id=str(domain_event.event_id),
        occurred_on=domain_event.occurred_on,
        study_plan_id=domain_event.study_plan_id,
      )
    case StudyPlanGenerated():
      return StudyPlanGeneratedEventMessage(
        event_id=str(domain_event.event_id),
        occurred_on=domain_event.occurred_on,
        study_plan_id=domain_event.study_plan_id,
      )
    case _:
      return None
