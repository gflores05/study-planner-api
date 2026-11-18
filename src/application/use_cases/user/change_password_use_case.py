from src.application.dtos.user import ChangePasswordRequestDTO
from src.application.ports.outbound.repositories.user_repository import UserRepository
from src.application.ports.outbound.security.password_hasher import PasswordHasherPort
from src.application.use_cases.user.error import (
  UserInvalidCredentials,
  UserInvalidInputError,
  UserNotFoundError,
)
from src.domain.user.value_objects.password import Password
from src.domain.user.value_objects.user_id import UserId
from src.util.date_util import utc_now


class ChangePasswordUseCaseAdapter:
  def __init__(
    self, user_repository: UserRepository, password_hasher: PasswordHasherPort
  ):
    self.user_repository = user_repository
    self.password_hasher = password_hasher

  async def execute(self, user_id: str, dto: ChangePasswordRequestDTO) -> None:
    id = UserId.parse(user_id).unwrap_or_map_and_raise(
      lambda e: UserInvalidInputError(value=user_id, field="UserId")
    )
    user = (await self.user_repository.get(id)).get_or_raise(
      UserNotFoundError(user_id=user_id)
    )

    if not self.password_hasher.verify(dto.current_password, user.password):
      raise UserInvalidCredentials()

    new_password = Password.parse(dto.new_password).unwrap_or_map_and_raise(
      lambda e: UserInvalidInputError(value=None, field="NewPassword")
    )

    user.change_password(
      password=self.password_hasher.hash(new_password), changed_on=utc_now()
    )

    await self.user_repository.save(user=user)
