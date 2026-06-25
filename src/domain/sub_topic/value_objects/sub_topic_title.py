from dataclasses import dataclass

from shared.result import Result


@dataclass(frozen=True)
class SubTopicTitle:
  value: str

  @staticmethod
  def create(value: str) -> Result["SubTopicTitle"]:
    if len(value) == 0:
      return Result.fail("The sub topic title cannot be empty")

    return Result.ok(SubTopicTitle(value=value))
