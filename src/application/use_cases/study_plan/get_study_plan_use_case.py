from src.application.dtos.study_plan import (
  StudyPlanDTO,
)
from src.application.mappers.study_plan_mapper import map_study_plan_domain_to_dto
from src.application.ports.outbound.repositories.study_plan_repository import (
  StudyPlanRepository,
)
from src.application.use_cases.study_plan.errors import (
  StudyPlanInvalidInputError,
  StudyPlanNotFoundError,
)
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId


class GetStudyPlanUseCaseAdapter:
  def __init__(self, study_plan_repository: StudyPlanRepository) -> None:
    self.study_plan_repository = study_plan_repository

  async def execute(self, id: str) -> StudyPlanDTO:
    study_plan_id = StudyPlanId.parse(id).unwrap_or_map_and_raise(
      lambda problem: StudyPlanInvalidInputError(
        value=str(problem.value), field="study_plan_id"
      )
    )

    study_plan = await self.study_plan_repository.get(study_plan_id)

    return map_study_plan_domain_to_dto(
      study_plan.get_or_raise(StudyPlanNotFoundError(study_plan_id=id))
    )
