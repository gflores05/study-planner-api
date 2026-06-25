from dataclasses import dataclass
from uuid import uuid4

from shared.result import Result
from src.util.string_util import is_valid_uuid


@dataclass(frozen=True)
class SubTopicId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["SubTopicId"]:
    if not is_valid_uuid(value):
      return Result.fail("The id should be a valid uuid v4")

    return Result.ok(SubTopicId(value=value))

  @staticmethod
  def create() -> "SubTopicId":
    return SubTopicId(value=str(uuid4()))
