from pydantic import BaseModel, Field


class AnswerDTO(BaseModel):
  id: str
  text: str
  option: str


class AnswerAIDTO(BaseModel):
  t: str = Field(description="The answer text")
  o: str = Field(description="The answer option")
