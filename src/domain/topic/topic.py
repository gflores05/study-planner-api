from dataclasses import dataclass

from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.shared.aggregate_root import AggregateRoot


@dataclass(kw_only=True)
class Topic(AggregateRoot[TopicId]):
  title: TopicTitle
  sub_topics: list[SubTopic]

  @staticmethod
  def create(id: TopicId, title: TopicTitle, sub_topics: list[SubTopic]) -> "Topic":
    return Topic(id=id, title=title, sub_topics=sub_topics)

  @staticmethod
  def reconstitute(title: TopicTitle, sub_topics: list[SubTopic]) -> "Topic":
    return Topic(id=TopicId.create(), title=title, sub_topics=sub_topics)
