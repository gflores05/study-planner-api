from dataclasses import dataclass
from uuid import uuid4

from shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.string_util import is_valid_uuid


@dataclass(frozen=True)
class StudyPlanId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["StudyPlanId", ValidationError]:
    if not is_valid_uuid(value):
      return Result.fail(ValidationError("InvalidUUID", value=value))

    return Result.ok(StudyPlanId(value=value))

  @staticmethod
  def create() -> "StudyPlanId":
    return StudyPlanId(value=str(uuid4()))

  def __str__(self) -> str:
    return self.value
