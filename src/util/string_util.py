import uuid


def is_valid_uuid(s: str) -> bool:
  try:
    val = uuid.UUID(s, version=4)
    return str(val) == s.lower()
  except ValueError:
    return False
