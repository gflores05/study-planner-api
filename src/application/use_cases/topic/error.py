class TopicError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

  def to_dict(self) -> dict[str, object]:
    return self.__dict__


class TopicInvalidInputError(TopicError):
  def __init__(self, value: str, field: str):
    super().__init__("TopicInvalidInput")
    self.value = value
    self.field = field

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "value": self.value, "field": self.field}


class TopicNotFoundError(TopicError):
  def __init__(self, topic_id: str):
    super().__init__("TopicNotFoundError")
    self.topic_id = topic_id

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "topic_id": self.topic_id}


class TopicUnknownError(TopicError):
  def __init__(self):
    super().__init__("TopicUnknownError")

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self)}
