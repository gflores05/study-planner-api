from collections.abc import Iterator
from datetime import timedelta

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient

from src.application.use_cases.user.tokens import ACCESS, REFRESH, build_claims
from src.infrastructure.adapters.inbound.http.api import create_app
from src.infrastructure.config.container import Container
from tests.conftest import JANE_EMAIL, JANE_PASSWORD, UserScenario

NEW_PASSWORD = "an0ther-passw0rd"


@pytest.fixture
def client(user_scenario: UserScenario) -> Iterator[TestClient]:
  container = Container()
  container.user_repository.override(providers.Object(user_scenario.user_repository))
  container.user_lookup.override(providers.Object(user_scenario.user_lookup))
  container.password_hasher.override(providers.Object(user_scenario.password_hasher))
  container.token_service.override(providers.Object(user_scenario.token_service))
  container.token_settings.override(providers.Object(user_scenario.token_settings))
  container.wire(
    modules=[
      "src.infrastructure.adapters.inbound.http.security",
      "src.infrastructure.adapters.inbound.http.routers.auth_router",
      "src.infrastructure.adapters.inbound.http.routers.user_router",
      "src.infrastructure.adapters.inbound.http.routers.study_plan_router",
    ]
  )

  # Not used as a context manager, so the lifespan (DB, broker) never starts.
  yield TestClient(create_app(container=container))

  container.unwire()


def _login(client: TestClient, password: str = JANE_PASSWORD):
  return client.post("/v1/auth/login", json={"email": JANE_EMAIL, "password": password})


def _bearer(token: str) -> dict[str, str]:
  return {"Authorization": f"Bearer {token}"}


def test_register_then_login(client: TestClient):
  response = client.post(
    "/v1/auth/register",
    json={"email": "john@example.com", "name": "John", "password": "pa55word-long"},
  )
  assert response.status_code == 201
  assert response.json()["id"]

  login = client.post(
    "/v1/auth/login",
    json={"email": "JOHN@example.com", "password": "pa55word-long"},
  )
  assert login.status_code == 200
  me = client.get("/v1/user/me", headers=_bearer(login.json()["access_token"]))
  assert me.json() == {
    "id": response.json()["id"],
    "email": "john@example.com",
    "name": "John",
  }


def test_register_rejects_a_duplicate_email(client: TestClient):
  response = client.post(
    "/v1/auth/register",
    json={"email": JANE_EMAIL, "name": "Jane", "password": "pa55word-long"},
  )

  assert response.status_code == 409
  assert response.json()["error"] == "UserAlreadyExists"


def test_register_rejects_a_weak_password_without_echoing_it(client: TestClient):
  response = client.post(
    "/v1/auth/register",
    json={"email": "john@example.com", "name": "John", "password": "short"},
  )

  assert response.status_code == 400
  assert response.json()["data"]["field"] == "Password"
  assert "short" not in response.text


def test_login_returns_bearer_tokens(client: TestClient):
  response = _login(client)

  assert response.status_code == 200
  body = response.json()
  assert body["token_type"] == "bearer"
  assert body["access_token"] and body["refresh_token"]


def test_login_rejects_bad_credentials(client: TestClient):
  response = _login(client, password="wrong-password")

  assert response.status_code == 401
  assert response.json()["error"] == "UserInvalidCredentials"


def test_refresh_returns_a_new_access_token(client: TestClient):
  refresh_token = _login(client).json()["refresh_token"]

  response = client.post("/v1/auth/refresh", json={"refresh_token": refresh_token})

  assert response.status_code == 200
  me = client.get("/v1/user/me", headers=_bearer(response.json()["access_token"]))
  assert me.status_code == 200


def test_refresh_rejects_an_access_token(client: TestClient):
  access_token = _login(client).json()["access_token"]

  response = client.post("/v1/auth/refresh", json={"refresh_token": access_token})

  assert response.status_code == 401
  assert response.json()["error"] == "UserInvalidToken"


def test_me_returns_the_current_user(client: TestClient, user_scenario: UserScenario):
  response = client.get(
    "/v1/user/me", headers=_bearer(_login(client).json()["access_token"])
  )

  assert response.status_code == 200
  assert response.json() == {
    "id": str(user_scenario.jane.id),
    "email": JANE_EMAIL,
    "name": "Jane Doe",
  }


@pytest.mark.parametrize(
  "make_headers",
  [
    pytest.param(lambda s: {}, id="no token"),
    pytest.param(lambda s: _bearer("garbage"), id="garbage"),
    pytest.param(
      lambda s: _bearer(
        s.token_service.encode(build_claims(s.jane, REFRESH), timedelta(minutes=5))
      ),
      id="refresh token",
    ),
    pytest.param(
      lambda s: _bearer(
        s.token_service.encode(build_claims(s.jane, ACCESS), timedelta(seconds=-1))
      ),
      id="expired",
    ),
  ],
)
@pytest.mark.parametrize("path", ["/v1/user/me", "/v1/study-plan/some-id"])
def test_protected_routes_reject_invalid_tokens(
  client: TestClient, user_scenario: UserScenario, make_headers, path: str
):
  response = client.get(path, headers=make_headers(user_scenario))

  assert response.status_code == 401
  assert response.json()["error"] == "UserInvalidToken"


def test_change_password(client: TestClient):
  headers = _bearer(_login(client).json()["access_token"])

  response = client.put(
    "/v1/user/me/password",
    headers=headers,
    json={"current_password": JANE_PASSWORD, "new_password": NEW_PASSWORD},
  )

  assert response.status_code == 204
  assert _login(client, password=JANE_PASSWORD).status_code == 401
  assert _login(client, password=NEW_PASSWORD).status_code == 200


def test_change_password_rejects_a_wrong_current_password(client: TestClient):
  headers = _bearer(_login(client).json()["access_token"])

  response = client.put(
    "/v1/user/me/password",
    headers=headers,
    json={"current_password": "wrong-password", "new_password": NEW_PASSWORD},
  )

  assert response.status_code == 401
  assert response.json()["error"] == "UserInvalidCredentials"


def test_change_password_requires_a_token(client: TestClient):
  response = client.put(
    "/v1/user/me/password",
    json={"current_password": JANE_PASSWORD, "new_password": NEW_PASSWORD},
  )

  assert response.status_code == 401
  assert response.json()["error"] == "UserInvalidToken"
