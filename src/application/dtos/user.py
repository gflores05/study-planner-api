from typing import Literal

from pydantic import BaseModel, Field


class UserDTO(BaseModel):
  id: str
  email: str
  name: str


class RegisterUserRequestDTO(BaseModel):
  email: str = Field(examples=["jane.doe@example.com"])
  name: str = Field(examples=["Jane Doe"])
  password: str = Field(description="Between 8 and 128 characters.")


class RegisterUserResponseDTO(BaseModel):
  id: str


class LoginRequestDTO(BaseModel):
  email: str = Field(examples=["jane.doe@example.com"])
  password: str


class TokenResponseDTO(BaseModel):
  access_token: str
  refresh_token: str
  token_type: Literal["bearer"] = "bearer"


class RefreshTokenRequestDTO(BaseModel):
  refresh_token: str


class AccessTokenResponseDTO(BaseModel):
  access_token: str
  token_type: Literal["bearer"] = "bearer"


class ChangePasswordRequestDTO(BaseModel):
  current_password: str
  new_password: str = Field(description="Between 8 and 128 characters.")
