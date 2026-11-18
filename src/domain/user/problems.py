from dataclasses import dataclass


@dataclass
class UserInvalidStatusProblem:
  user_id: str
  current_status: str
  required_status: str


UserProblem = UserInvalidStatusProblem
