class UserError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


class UserInvalidInputError(UserError):
  def __init__(self, value: str | None, field: str):
    super().__init__("UserInvalidInput")
    self.value = value
    self.field = field


class UserNotFoundError(UserError):
  def __init__(self, user_id: str):
    super().__init__("UserNotFoundError")
    self.user_id = user_id


class UserUnknownError(UserError):
  def __init__(self):
    super().__init__("UserUnknownError")


class UserUnauthorized(UserError):
  def __init__(self):
    super().__init__("UserUnknownError")
