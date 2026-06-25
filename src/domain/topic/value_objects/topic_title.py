from dataclasses import dataclass

from shared.result import Result


@dataclass(frozen=True)
class TopicTitle:
  value: str

  @staticmethod
  def create(value: str) -> Result["TopicTitle"]:
    if len(value) == 0:
      return Result.fail("The topic title cannot be empty")

    return Result.ok(TopicTitle(value=value))
