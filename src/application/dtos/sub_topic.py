from dataclasses import dataclass


@dataclass
class SubTopicDTO:
  id: str
  title: str
  study_material: list[str]
  topic_id: str


@dataclass
class SubTopicAIDTO:
  t: str
  sm: list[str]
