from src.application.dtos.auth import TokenSettings
from src.application.dtos.user import LoginRequestDTO, TokenResponseDTO
from src.application.ports.outbound.lookups.user_lookup import UserLookupPort
from src.application.ports.outbound.repositories.user_repository import UserRepository
from src.application.ports.outbound.security.password_hasher import PasswordHasherPort
from src.application.ports.outbound.security.token_service import TokenServicePort
from src.application.use_cases.user.error import UserInvalidCredentials
from src.application.use_cases.user.tokens import ACCESS, REFRESH, build_claims
from src.domain.user.value_objects.email import Email
from src.util.date_util import utc_now


class LoginUseCaseAdapter:
  def __init__(
    self,
    user_repository: UserRepository,
    user_lookup: UserLookupPort,
    password_hasher: PasswordHasherPort,
    token_service: TokenServicePort,
    token_settings: TokenSettings,
  ):
    self.user_repository = user_repository
    self.user_lookup = user_lookup
    self.password_hasher = password_hasher
    self.token_service = token_service
    self.token_settings = token_settings

  async def execute(self, dto: LoginRequestDTO) -> TokenResponseDTO:
    # Every failure is reported the same way so the endpoint doesn't reveal
    # which emails are registered.
    email = Email.parse(dto.email).unwrap_or_map_and_raise(
      lambda e: UserInvalidCredentials()
    )
    user = (await self.user_lookup.get_by_email(email)).get_or_raise(
      UserInvalidCredentials()
    )

    if not self.password_hasher.verify(dto.password, user.password):
      raise UserInvalidCredentials()

    user.login(logged_in_on=utc_now()).unwrap_or_map_and_raise(
      lambda e: UserInvalidCredentials()
    )

    await self.user_repository.save(user=user)

    return TokenResponseDTO(
      access_token=self.token_service.encode(
        build_claims(user, ACCESS), self.token_settings.access_token_expires_in
      ),
      refresh_token=self.token_service.encode(
        build_claims(user, REFRESH), self.token_settings.refresh_token_expires_in
      ),
    )
