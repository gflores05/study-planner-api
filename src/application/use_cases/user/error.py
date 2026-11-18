class UserError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

  def to_dict(self) -> dict[str, object]:
    return self.__dict__


class UserInvalidInputError(UserError):
  def __init__(self, value: str | None, field: str):
    super().__init__("UserInvalidInput")
    self.value = value
    self.field = field

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "value": self.value, "field": self.field}


class UserNotFoundError(UserError):
  def __init__(self, user_id: str):
    super().__init__("UserNotFoundError")
    self.user_id = user_id

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "user_id": self.user_id}


class UserAlreadyExists(UserError):
  def __init__(self, email: str):
    super().__init__("UserAlreadyExists")
    self.email = email

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "email": self.email}


class UserInvalidCredentials(UserError):
  """The email/password pair (or the current password) is wrong."""

  def __init__(self):
    super().__init__("UserInvalidCredentials")

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self)}


class UserInvalidToken(UserError):
  """The bearer/refresh token is missing, malformed, expired or of the wrong type."""

  def __init__(self):
    super().__init__("UserInvalidToken")

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self)}


class UserUnknownError(UserError):
  def __init__(self):
    super().__init__("UserUnknownError")

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self)}
