import uuid

from src.domain.study_plan.study_plan import StudyPlan, StudyPlanStatus
from src.domain.study_plan.value_objects.grade import Grade
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.study_plan.value_objects.subject import Subject
from src.infrastructure.adapters.outbound.persistence.mappers.topic_mapper import (
  map_topic_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.study_plan_model import (
  StudyPlanModel,
)


def map_study_plan_model_to_domain(model: StudyPlanModel) -> StudyPlan:
  return StudyPlan.reconstitute(
    id=StudyPlanId.parse(str(model.id)).unwrap_or_raise(),
    created_on=model.created_on,
    modified_on=model.modified_on,
    version=model.version,
    subject=Subject.parse(model.subject).unwrap_or_raise(),
    level=model.level,
    status=map_db_study_plan_status_to_domain(model.status),
    topics=[map_topic_model_to_domain(t) for t in model.topics],
    grade=Grade.parse(model.grade).unwrap_or_raise(),
  )


def map_db_study_plan_status_to_domain(db_status: str) -> StudyPlanStatus:
  match db_status:
    case "PENDING":
      return StudyPlanStatus.PENDING
    case "GENERATING":
      return StudyPlanStatus.GENERATING
    case "COMPLETED":
      return StudyPlanStatus.COMPLETED
    case "FAILED":
      return StudyPlanStatus.FAILED

  return StudyPlanStatus.UNKNOWN


def map_study_plan_domain_to_model(domain: StudyPlan) -> StudyPlanModel:
  return StudyPlanModel(
    id=uuid.UUID(str(domain.id)),
    created_on=domain.created_on,
    modified_on=domain.modified_on,
    version=domain.version,
    subject=str(domain.subject),
    level=domain.level,
    status=map_domain_study_plan_status_to_db(domain.status),
    grade=int(domain.grade),
  )


def map_domain_study_plan_status_to_db(db_status: StudyPlanStatus) -> str:
  match db_status:
    case StudyPlanStatus.PENDING:
      return "PENDING"
    case StudyPlanStatus.GENERATING:
      return "GENERATING"
    case StudyPlanStatus.COMPLETED:
      return "COMPLETED"
    case StudyPlanStatus.FAILED:
      return "FAILED"

  return "UNKNOWN"
