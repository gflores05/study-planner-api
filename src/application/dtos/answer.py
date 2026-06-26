from dataclasses import dataclass


@dataclass
class AnswerDTO:
  id: str
  text: str
  option: str
