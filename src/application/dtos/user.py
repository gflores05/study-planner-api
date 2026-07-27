from pydantic import BaseModel


class CreateUserRequestDTO(BaseModel):
  auth0_id: str
  email: str
  name: str
  picture: str | None
  provider: str


class CreateUserResponseDTO(BaseModel):
  id: str
