from src.domain.assessment.assessment import Assessment
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.shared.option import Option


class FakeAssessmentRepository:
  def __init__(self, data: list[Assessment]):
    self.data = data

  async def get(self, id: AssessmentId) -> Option[Assessment]:
    return Option.of(next((sp for sp in self.data if sp.id == id), None))

  async def save(self, assessment: Assessment) -> None:
    exists = (await self.get(assessment.id)).is_some

    if exists:
      self.data = [st if st.id != assessment.id else assessment for st in self.data]
    else:
      self.data.append(assessment)
