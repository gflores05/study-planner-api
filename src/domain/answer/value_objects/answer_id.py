from dataclasses import dataclass
from uuid import uuid4

from shared.result import Result
from src.util.string_util import is_valid_uuid


@dataclass(frozen=True)
class AnswerId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["AnswerId"]:
    if not is_valid_uuid(value):
      return Result.fail("The id should be a valid uuid v4")

    return Result.ok(AnswerId(value=value))

  @staticmethod
  def create() -> "AnswerId":
    return AnswerId(value=str(uuid4()))
