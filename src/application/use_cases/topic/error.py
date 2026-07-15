class TopicError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


class TopicInvalidInputError(TopicError):
  def __init__(self, value: str, field: str):
    super().__init__("TopicInvalidInput")
    self.value = value
    self.field = field


class TopicNotFoundError(TopicError):
  def __init__(self, topic_id: str):
    super().__init__("TopicNotFoundError")
    self.topic_id = topic_id


class TopicUnknownError(TopicError):
  def __init__(self):
    super().__init__("TopicUnknownError")
