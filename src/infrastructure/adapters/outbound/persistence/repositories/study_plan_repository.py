from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.study_plan.study_plan import StudyPlan
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.infrastructure.adapters.outbound.persistence.mappers.study_plan_mapper import (
  map_study_plan_domain_to_model,
  map_study_plan_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.study_plan_model import (
  StudyPlanModel,
)
from src.shared.option import Option


class StudyPlanRepository:
  def __init__(self, session: AsyncSession):
    self._session = session

  async def get(self, id: StudyPlanId) -> Option[StudyPlan]:
    result = await self._session.execute(
      select(StudyPlanModel).where(StudyPlanModel.id == id)
    )

    row = result.scalar_one_or_none()

    if not row:
      return Option.nothing()
    return Option.some(map_study_plan_model_to_domain(row))

  async def save(self, study_plan: StudyPlan):
    study_plan.increment_version()
    model = map_study_plan_domain_to_model(study_plan)
    await self._session.merge(model)
    await self._session.flush()
