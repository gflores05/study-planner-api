from src.application.dtos.study_plan import (
  StudyPlanDTO,
)
from src.application.mappers.study_plan_mapper import map_study_plan_domain_to_dto
from src.application.ports.outbound.repositories.study_plan_repository import (
  StudyPlanRepository,
)
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId


class GetStudyPlanUseCase:
  def __init__(self, study_plan_repository: StudyPlanRepository) -> None:
    self.study_plan_repository = study_plan_repository

  async def execute(self, id: str) -> StudyPlanDTO:
    study_plan_id = StudyPlanId.parse(id).unwrap_or_raise()

    study_plan = (await self.study_plan_repository.get(study_plan_id)).get_or_raise(
      ValueError("StudyPlanNotFound")
    )

    return map_study_plan_domain_to_dto(study_plan)
