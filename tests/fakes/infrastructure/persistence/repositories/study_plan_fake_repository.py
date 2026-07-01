from src.domain.study_plan.study_plan import StudyPlan
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.shared.option import Option


class FakeStudyPlanRepository:
  def __init__(self, data: list[StudyPlan]):
    self.data = data

  async def get(self, id: StudyPlanId) -> Option[StudyPlan]:
    return Option.of(next((sp for sp in self.data if sp.id == id), None))

  async def save(self, study_plan: StudyPlan) -> None:
    exists = (await self.get(study_plan.id)).is_some

    if exists:
      self.data = [st if st.id != study_plan.id else study_plan for st in self.data]
    else:
      self.data.append(study_plan)
