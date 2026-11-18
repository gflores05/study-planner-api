from src.application.dtos.user import RegisterUserRequestDTO, RegisterUserResponseDTO
from src.application.ports.outbound.lookups.user_lookup import UserLookupPort
from src.application.ports.outbound.repositories.user_repository import UserRepository
from src.application.ports.outbound.security.password_hasher import PasswordHasherPort
from src.application.use_cases.user.error import (
  UserAlreadyExists,
  UserInvalidInputError,
)
from src.domain.user.user import User
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.name import Name
from src.domain.user.value_objects.password import Password
from src.util.date_util import utc_now


class RegisterUserUseCaseAdapter:
  def __init__(
    self,
    user_repository: UserRepository,
    user_lookup: UserLookupPort,
    password_hasher: PasswordHasherPort,
  ):
    self.user_repository = user_repository
    self.user_lookup = user_lookup
    self.password_hasher = password_hasher

  async def execute(self, dto: RegisterUserRequestDTO) -> RegisterUserResponseDTO:
    email = Email.parse(dto.email).unwrap_or_map_and_raise(
      lambda e: UserInvalidInputError(value=dto.email, field="Email")
    )
    name = Name.parse(dto.name).unwrap_or_map_and_raise(
      lambda e: UserInvalidInputError(value=dto.name, field="Name")
    )
    # The password is never echoed back in the error.
    password = Password.parse(dto.password).unwrap_or_map_and_raise(
      lambda e: UserInvalidInputError(value=None, field="Password")
    )

    existing = await self.user_lookup.get_by_email(email)

    if existing.is_some:
      raise UserAlreadyExists(email=str(email))

    user = User.register(
      email=email,
      name=name,
      password=self.password_hasher.hash(password),
      registered_on=utc_now(),
    )

    await self.user_repository.save(user=user)

    return RegisterUserResponseDTO(id=str(user.id))
