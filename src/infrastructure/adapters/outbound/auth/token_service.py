import jwt
from fastapi import HTTPException, status

from src.infrastructure.config.settings import Settings


class TokenService:
  def __init__(self, settings: Settings):
    self.settings = settings

  def verify(self, token: str) -> dict:
    try:
      # Fetch public signing keys from Auth0
      jwks_url = f"https://{self.settings.auth0_domain}/.well-known/jwks.json"
      jwks_client = jwt.PyJWKClient(jwks_url)
      signing_key = jwks_client.get_signing_key_from_jwt(token)

      # Validate signature, audience, and expiration date
      payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=self.settings.auth0_audience,
        issuer=f"https://{self.settings.auth0_domain}/",
      )
      return payload  # Contains user identifiers like 'sub'
    except jwt.ExpiredSignatureError:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
      )
    except jwt.InvalidTokenError as e:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
      )
    except Exception:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to parse token"
      )
