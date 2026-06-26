from dataclasses import dataclass

from src.application.dtos.assessment import AssessmentDTO


@dataclass
class SubTopicDTO:
  id: str
  title: str
  study_material: list[str]
  assessment: AssessmentDTO
