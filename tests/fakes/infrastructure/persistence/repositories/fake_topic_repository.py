from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_id import TopicId
from src.shared.option import Option


class FakeTopicRepository:
  def __init__(self, data: list[Topic]):
    self.data = data

  async def get(self, id: TopicId) -> Option[Topic]:
    return Option.of(next((sp for sp in self.data if sp.id == id), None))

  async def save(self, topic: Topic) -> None:
    exists = (await self.get(topic.id)).is_some

    if exists:
      self.data = [st if st.id != topic.id else topic for st in self.data]
    else:
      self.data.append(topic)
