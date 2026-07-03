from dataclasses import dataclass
from uuid import uuid4

from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.string_util import is_valid_uuid


@dataclass(frozen=True)
class DomainEventId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["DomainEventId", ValidationError]:
    if not is_valid_uuid(value):
      return Result.fail(
        ValidationError(
          message="The domain event id should be a valid uuid v4", value=value
        )
      )

    return Result.ok(DomainEventId(value=value))

  @staticmethod
  def create() -> "DomainEventId":
    return DomainEventId(value=str(uuid4()))
