from dataclasses import dataclass
from uuid import uuid4

from shared.result import Result
from src.util.string_util import is_valid_uuid


@dataclass(frozen=True)
class TopicId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["TopicId"]:
    if not is_valid_uuid(value):
      return Result.fail("The id should be a valid uuid v4")

    return Result.ok(TopicId(value=value))

  @staticmethod
  def create() -> "TopicId":
    return TopicId(value=str(uuid4()))

  def __str__(self) -> str:
    return self.value
