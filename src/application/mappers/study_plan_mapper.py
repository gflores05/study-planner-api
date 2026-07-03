from src.application.dtos.study_plan import StudyPlanDTO
from src.application.mappers.topic_mapper import map_topic_domain_to_dto
from src.domain.study_plan.study_plan import StudyPlan


def map_study_plan_domain_to_dto(domain: StudyPlan) -> StudyPlanDTO:
  return StudyPlanDTO(
    id=str(domain.id),
    subject=str(domain.subject),
    level=domain.level,
    topics=[map_topic_domain_to_dto(t) for t in domain.topics],
    grade=int(domain.grade),
  )
