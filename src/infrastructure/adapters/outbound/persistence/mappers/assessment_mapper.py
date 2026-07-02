import uuid

from src.domain.assessment.assessment import Assessment, AssessmentStatus
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.topic.value_objects.topic_id import TopicId
from src.infrastructure.adapters.outbound.persistence.mappers.question_mapper import (
  map_question_domain_to_model,
  map_question_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.assessment_model import (
  AssessmentModel,
)
from src.shared.option import Option


def map_assessment_model_to_domain(model: AssessmentModel) -> Assessment:
  return Assessment.reconstitute(
    id=AssessmentId.parse(str(model.id)).unwrap_or_raise(),
    created_on=model.created_on,
    modified_on=model.modified_on,
    version=model.version,
    status=map_assessment_status_model_to_domain(model.status),
    score=Option.of(model.score),
    questions=[map_question_model_to_domain(q) for q in model.questions],
    started_on=Option.of(model.started_on),
    completed_on=Option.of(model.completed_on),
    topic_id=TopicId.parse(str(model.topic_id)).unwrap_or_raise(),
  )


def map_assessment_status_model_to_domain(db_status: str) -> AssessmentStatus:
  match db_status:
    case "PENDING":
      return AssessmentStatus.PENDING
    case "IN_PROGRESS":
      return AssessmentStatus.IN_PROGRESS
    case "COMPLETED":
      return AssessmentStatus.COMPLETED

  return AssessmentStatus.UNKNOWN


def map_assessment_domain_to_model(domain: Assessment) -> AssessmentModel:
  return AssessmentModel(
    id=uuid.UUID(str(domain.id)),
    created_on=domain.created_on,
    modified_on=domain.modified_on,
    version=domain.version,
    status=str(domain.status),
    score=domain.score.to_nullable(),
    questions=[map_question_domain_to_model(q) for q in domain.questions],
    started_on=domain.started_on.to_nullable(),
    completed_on=domain.completed_on.to_nullable(),
    topic_id=uuid.UUID(str(domain.topic_id)),
  )
