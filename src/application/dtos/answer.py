from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class AnswerDTO:
  id: str
  text: str
  option: str


class AnswerAIDTO(BaseModel):
  t: str
  o: str
