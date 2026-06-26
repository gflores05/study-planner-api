from typing import Protocol

from src.domain.study_plan.study_plan import StudyPlan
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.shared.option import Option


class StudyPlanRepository(Protocol):
  async def get(self, id: StudyPlanId) -> Option[StudyPlan]: ...
  async def save(self, study_plan: StudyPlan) -> None: ...
