from dataclasses import dataclass


@dataclass
class AnswerDTO:
  id: str
  text: str
  option: str


@dataclass
class AnswerAIDTO:
  t: str
  o: str
