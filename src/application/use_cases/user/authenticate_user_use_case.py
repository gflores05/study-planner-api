from src.application.ports.outbound.repositories.user_repository import UserRepository
from src.application.ports.outbound.security.token_service import TokenServicePort
from src.application.use_cases.user.tokens import ACCESS, resolve_token_user
from src.domain.user.user import User


class AuthenticateUserUseCaseAdapter:
  def __init__(self, user_repository: UserRepository, token_service: TokenServicePort):
    self.user_repository = user_repository
    self.token_service = token_service

  async def execute(self, access_token: str) -> User:
    return await resolve_token_user(
      token=access_token,
      type=ACCESS,
      token_service=self.token_service,
      user_repository=self.user_repository,
    )
