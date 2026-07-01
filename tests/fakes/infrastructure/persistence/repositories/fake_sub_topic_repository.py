from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_id import SubTopicId
from src.shared.option import Option


class FakeSubTopicRepository:
  def __init__(self, data: list[SubTopic]):
    self.data = data

  async def get(self, id: SubTopicId) -> Option[SubTopic]:
    return Option.of(next((sp for sp in self.data if sp.id == id), None))

  async def save(self, sub_topic: SubTopic) -> None:
    exists = (await self.get(sub_topic.id)).is_some

    if exists:
      self.data = [st if st.id != sub_topic.id else sub_topic for st in self.data]
    else:
      self.data.append(sub_topic)
