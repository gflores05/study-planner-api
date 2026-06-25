from dataclasses import dataclass
from uuid import uuid4

from shared.result import Result
from src.util.string_util import is_valid_uuid


@dataclass(frozen=True)
class DomainEventId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["DomainEventId"]:
    if not is_valid_uuid(value):
      return Result.fail("The domain event id should be a valid uuid v4")

    return Result.ok(DomainEventId(value=value))

  @staticmethod
  def create() -> "DomainEventId":
    return DomainEventId(value=str(uuid4()))
