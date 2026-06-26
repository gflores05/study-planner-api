from dataclasses import dataclass

from src.application.dtos.sub_topic import SubTopicDTO


@dataclass
class TopicDTO:
  id: str
  title: str
  sub_topics: list[SubTopicDTO]
