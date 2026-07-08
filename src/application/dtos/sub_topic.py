from dataclasses import dataclass

from pydantic import BaseModel


class SubTopicDTO(BaseModel):
  id: str
  title: str
  study_material: list[str]
  topic_id: str


class SubTopicAIDTO(BaseModel):
  t: str
  sm: list[str]


@dataclass
class SubTopicResponseDTO:
  id: str
