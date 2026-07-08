from src.application.dtos.study_plan import StudyPlanDTO, StudyPlanStatusDTO
from src.application.mappers.topic_mapper import map_topic_domain_to_dto
from src.domain.study_plan.study_plan import StudyPlan, StudyPlanStatus


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
