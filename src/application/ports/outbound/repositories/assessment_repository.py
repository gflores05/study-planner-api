from typing import Protocol

from src.domain.assessment.assessment import Assessment
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.shared.option import Option


class AssessmentRepository(Protocol):
  async def get(self, id: AssessmentId) -> Option[Assessment]: ...
  async def save(self, assessment: Assessment) -> None: ...
