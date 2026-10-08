from dataclasses import dataclass

from pydantic import BaseModel, Field


class SubTopicDTO(BaseModel):
  id: str
  title: str
  study_material: list[str]
  topic_id: str
  created_by_user_id: str


class SubTopicAIDTO(BaseModel):
  t: str = Field(description="The sub-topic title")
  sm: list[str] = Field(description="List of study materials for the sub-topic")


@dataclass
class SubTopicResponseDTO:
  id: str
