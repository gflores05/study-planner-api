from pydantic import BaseModel


class AnswerDTO(BaseModel):
  id: str
  text: str
  option: str


class AnswerAIDTO(BaseModel):
  t: str
  o: str
