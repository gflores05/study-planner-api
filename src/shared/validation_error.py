class ValidationError(Exception):
  def __init__(self, message: str, value: object):
    super().__init__(message)

    self.value = value
