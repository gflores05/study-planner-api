# Study Planner API

A FastAPI service that generates study plans and assessments for students using an LLM.

A student asks for a **`StudyPlan`** for a `subject`, an education `level` and a `grade`. Generation runs asynchronously off a RabbitMQ queue: an LLM (OpenAI via [LangChain](https://python.langchain.com/)) returns a list of **topics**, each with **sub-topics** (and their study material) and a 15-question multiple-choice **assessment**. Everything is persisted in PostgreSQL, and the student is notified over a **WebSocket** when the plan is ready or has failed. The student can then take each topic's assessment through the API and get a score.

The web client lives next to this repo in `../study-planner-ui`.

## Technologies

- [FastAPI](https://fastapi.tiangolo.com/) — HTTP + WebSocket API
- [SQLAlchemy](https://www.sqlalchemy.org/) (async, `asyncpg`) + [Alembic](https://alembic.sqlalchemy.org/) — PostgreSQL persistence and migrations
- [RabbitMQ](https://www.rabbitmq.com/) via [aio-pika](https://aio-pika.readthedocs.io/) — event/command messaging
- [LangChain OpenAI](https://python.langchain.com/docs/integrations/chat/openai/) — structured-output study plan generation
- [Pydantic](https://docs.pydantic.dev/) / [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — DTOs and env-driven configuration
- [dependency-injector](https://python-dependency-injector.ets-labs.org/) — DI container
- [PyJWT](https://pyjwt.readthedocs.io/) — app-managed JWT authentication
- [Exa](https://exa.ai/) — web search tool (implemented, not wired in yet; see [Known gaps](#known-gaps))

## Architecture

The codebase follows a hexagonal (ports & adapters) layout, split into three top-level layers under `src/`, plus a shared kernel and generic utilities:

```
src/
├── domain/          # Aggregates, value objects, domain events, and domain errors ("problems")
├── application/     # Use cases, ports (inbound/outbound interfaces), DTOs, mappers, messages
├── infrastructure/  # Adapters (HTTP, WebSockets, persistence, messaging, AI, auth), DI container, config, logging
├── shared/          # Cross-cutting building blocks: Result, Option, AggregateRoot, DomainEvent
└── util/            # Stateless helper functions (string/date/result utilities)
```

**`src/domain/`** — the core model, framework-free. Every aggregate exposes `create(...)` (new instance, new id) and `reconstitute(...)` (rebuild from persistence), and state changes go through methods that validate the current status and raise domain events:

- `study_plan` — a `StudyPlan` (`subject`, `level`, `grade`, `topics`, `status`, `created_by_user_id`). `level` is one of `Elementary School` / `High School` / `Preparatory` / `University` / `Postgraduate`; `grade` is 1–12. Status flow: `PENDING` → `.request()` → `GENERATING` → `.report_plan_generated()` → `COMPLETED`, or `.report_failure()` → `FAILED`. Raises `StudyPlanRequested`, `StudyPlanGenerated`, `StudyPlanErrorReported`.
- `topic` — a `Topic` belongs to a study plan: `title`, `sub_topics`, and an optional `assessment`. `.add_sub_topic()` and `.generate_assessment()` (raises `TopicAssessmentGenerated`).
- `sub_topic` — a `SubTopic`: `title` plus a list of `study_material` strings (books, papers, tutorials suggested by the LLM).
- `assessment` — an `Assessment` for one topic: `questions`, `status`, `score`, `started_on`, `completed_on`. Status flow: `PENDING` → `.start()` → `IN_PROGRESS` → `.complete()` → `COMPLETED`. `.answer_question()` only works while `IN_PROGRESS`. On completion `score` is the percentage of correctly answered questions.
- `question` / `answer` — a `Question` has `text`, `options` (`Answer`s), the correct `answer` and the `selected_answer`. Options are `AnswerOption` values `a`/`b`/`c`/`d`.
- `user` — a `User` (`email`, `name`, hashed `password`, `status`, `last_login_on`). `.register()`, `.login()` (fails unless `ACTIVE`), `.change_password()`, `.activate()`/`.deactivate()`.
- `value_objects/` and each aggregate's `value_objects/` — typed, self-validating values (`StudyPlanId`, `Grade`, `Subject`, `Email`, `Password`, `NonEmptyString`, …) built with `parse(...) -> Result[...]`.

**`src/application/`** — orchestrates the domain to fulfill a request, without knowing about FastAPI, RabbitMQ, SQLAlchemy or OpenAI:

- `use_cases/` — one class per operation, grouped by `study_plan/` (`RequestStudyPlan`, `GenerateStudyPlan`, `GetStudyPlan`), `topic/` (`GetTopic`), `assessment/` (`GetAssessment`, `StartAssessment`, `AnswerQuestion`, `CompleteAssessment`) and `user/` (`RegisterUser`, `Login`, `RefreshToken`, `AuthenticateUser`, `ChangePassword`). Each folder also has an `error(s).py` with the exception family the HTTP layer maps to status codes.
- `ports/inbound/` — the use case interfaces the adapters call.
- `ports/outbound/` — interfaces the application depends on but doesn't implement: `repositories/`, `lookups/`, `messaging/` (`EventPublisherPort`, `MessageEvent`), `security/` (`PasswordHasherPort`, `TokenServicePort`) and `ai/` (`StudyPlanAIServicePort`).
- `messages/` — wire message types crossing the broker (`study_plan_messages.py`) and `DomainEventPublisher`, which repositories use to publish an aggregate's domain events after a save.
- `dtos/` and `mappers/` — data shapes crossing the HTTP/AI boundaries and conversions to and from the domain.

**`src/infrastructure/`** — everything concrete and swappable:

- `adapters/inbound/http/` — FastAPI app assembly (`api.py`), routers (`study_plan_router.py`, `topic_router.py`, `assessment_router.py`, `auth_router.py`, `user_router.py`, `websockets_router.py`), `security.py` (the `CurrentUser` bearer-token dependency) and `middlewares/error_handler.py` (maps each error family to HTTP status codes).
- `adapters/outbound/persistence/` — SQLAlchemy ORM `models/` (one per table, all inheriting `DbModel` from `config/database.py`, which provides `id`/`created_on`/`modified_on`/`version`), `mappers/` (ORM ↔ domain via `reconstitute()`), `repositories/` and `lookups/`. `util/jsonb_dataclass.py` stores dataclasses in JSONB columns.
- `adapters/outbound/messaging/` — `EventPublisher` (publishes to the RabbitMQ topic exchange), `EventConsumer` (one durable queue, dispatches by message type), `register_consumers.py` (handler registry) and `handlers/` — split into **event handlers** (react to something that happened) and **command handlers** (do something). See [How a study plan is generated](#how-a-study-plan-is-generated).
- `adapters/outbound/ai/` — `StudyPlanAIServiceOpenAIAdapter` (LangChain `ChatOpenAI` + `with_structured_output`), `prompts.py`, and `tools/internet_search.py` (Exa search tool).
- `adapters/outbound/auth/` — `JwtTokenService` (HS256) and `Pbkdf2PasswordHasher` (PBKDF2-HMAC-SHA256, 600k iterations, random 16-byte salt stored as `salt || digest`).
- `adapters/outbound/websockets/` — `RealtimeConnectionManager`, an in-memory `user_id → set[WebSocket]` registry (supports several tabs/devices per user).
- `config/` — `container.py` (DI container), `settings.py` (env-driven `Settings`), `lifespan.py` (startup/shutdown), `database.py` (`Database`: async engine + session factory), `messaging.py` (`MessageBroker`: shared robust connection + channel).
- `logging/` — `configure_logging` (a single `dictConfig` applied at process start) plus a correlation-id `ContextVar` and logging filter.

**`src/shared/`** — a small functional-style kernel: `Result`/`Option` (explicit success/failure and presence/absence instead of exceptions for expected cases), `AggregateRoot`/`DomainEvent`/`DomainEventId` and `ValidationError`.

**`src/util/`** — plain stateless helpers (`date_util.utc_now`, `result_util.traverse`, `string_util`).

### How a study plan is generated

Generation is asynchronous. The HTTP request only creates the plan; the work happens off the broker:

```
POST /v1/study-plan/request
  └─ RequestStudyPlanUseCase  ── StudyPlan.create() + .request()  (PENDING → GENERATING), save
       └─ StudyPlanRepository.save() publishes  StudyPlanRequestedEvent
            └─ study_plan_requested_event_handler     ──►  publishes  GenerateStudyPlanCommand
                 └─ generate_study_plan_command_handler
                      └─ GenerateStudyPlanUseCase
                           ├─ StudyPlanAIService.generate(subject, level, grade)   (OpenAI, structured output)
                           ├─ for each topic: save Topic, its SubTopics, its Assessment + 15 Questions
                           ├─ success ── .report_plan_generated()  (→ COMPLETED)  ──►  StudyPlanGeneratedEvent
                           │     └─ study_plan_generated_event_handler  ──►  ReportStudyPlanGeneratedCommand
                           │           └─ handler pushes it to the user's WebSockets
                           └─ LLM failure ── .report_failure()  (→ FAILED)  ──►  StudyPlanErrorReportedEvent
                                 └─ study_plan_error_reported_event_handler  ──►  ReportStudyPlanErrorCommand
                                       └─ handler pushes it to the user's WebSockets
```

1. `POST /v1/study-plan/request` returns the new `study_plan_id` immediately. Use cases never publish directly: the **repository** publishes the aggregate's domain events after the save (`DomainEventPublisher` maps `StudyPlan` domain events to wire messages; other aggregates' events are currently not published).
2. An **event handler** never calls a use case. It re-publishes a **command** message, which a separate command handler picks up and executes. This keeps "something happened" and "please do this" independently routable.
3. The LLM response is validated against `StudyPlanAIGeneratedDTO`, which uses short keys (`ts`, `t`, `st`, `sm`, `qs`, `os`, `a`, `o`) to keep the structured output small. Each value then goes through the domain value objects (`TopicTitle`, `AnswerOption`, …), so an invalid answer option fails the generation.
4. The client polls `GET /v1/study-plan/{id}` or, better, listens on its WebSocket.

**Messaging topology.** Everything goes through one durable **topic exchange** `domain_events`. Messages are published with `routing_key = study_plan.<event_name>` and `type = <event_name>`, persistent delivery and JSON bodies. A single durable queue `domain_events_service` is bound to `study_plan.*`, and `EventConsumer` dispatches each message to the handler registered for its `type` in `register_consumers.py`. Messages are acked once the handler returns. If a handler raises, the message is rejected **without requeue** (`message.process()` defaults to `requeue=False`), so it is dropped. `GenerateStudyPlanCommand`'s handler catches `StudyPlanError` and only logs it.

### Real-time notifications

Connect to `ws://<host>/ws/{user_id}` (the `id` from `GET /v1/user/me`). When a plan finishes, every open socket of the plan's owner receives:

```json
{"event": "ReportStudyPlanGeneratedCommand", "payload": {"event_id": "...", "occurred_on": "...", "study_plan_id": "...", "reported_by_user_id": "..."}}
```

or, on failure, `"event": "ReportStudyPlanErrorCommand"` with an extra `payload.error`. Messages for users with no open socket are dropped. Connections are kept in process memory, so with more than one API instance a notification only reaches sockets connected to the instance that consumed the command.

### Taking an assessment

Each topic has one assessment, created with status `PENDING`:

1. `POST /v1/assessment/{id}/start` → `IN_PROGRESS`
2. `POST /v1/assessment/{id}/answer` with `{"question_id": "...", "selected_answer": "a" | "b" | "c" | "d"}`, once per question (answering again overwrites the selection)
3. `POST /v1/assessment/{id}/complete` → `COMPLETED`, `score` = % of correct answers

Calling a step in the wrong status returns `412` (`AssessmentInvalidStatusError`).

## Dependency injection

The app uses [`dependency-injector`](https://python-dependency-injector.ets-labs.org/) instead of plain FastAPI `Depends` factories. `src/infrastructure/config/container.py` declares every provider (`Settings` → `Database`/`MessageBroker`/`RealtimeConnectionManager` singletons → repositories → AI service → use cases → message handlers). `src/main.py` wires the container into the modules that use `@inject` / `Provide[...]` (routers, `security.py`, `lifespan.py`). **A new module that uses `Provide[...]` must be added to that `wire(...)` list**, or its dependencies silently stay unresolved.

Tests swap implementations with `container.<provider>.override(providers.Object(fake))` — see `tests/http/test_auth_endpoints.py`.

## Requirements

- Python >= 3.14 (see `.python-version`)
- [uv](https://docs.astral.sh/uv/) for dependency and environment management
- Docker, to run PostgreSQL and RabbitMQ locally via `../docker-compose.yml`
- An OpenAI API key

## Setup

```bash
# Install dependencies (including the dev group)
uv sync

# Start PostgreSQL (5432) + RabbitMQ (5672, management UI on 15672) from the repo root
docker compose -f ../docker-compose.yml up -d

# Create a .env (see Configuration below), then apply migrations
uv run alembic upgrade head
```

A minimal `.env` for the local `docker-compose.yml`:

```dotenv
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=postgres

RABBITMQ_URL=amqp://admin:rabbitpass@localhost:5672/

OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=<at least 32 random bytes>
ALLOWED_ORIGINS=http://localhost:5173
```

Generate a `JWT_SECRET_KEY` rather than keeping the default:

```bash
uv run python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Users sign themselves up through `POST /v1/auth/register`, so no seeding is needed.

## Configuration

Environment variables, loaded from `.env` by `src/infrastructure/config/settings.py`:

| Variable                          | Default                                       | Description |
| --------------------------------- | --------------------------------------------- | ----------- |
| `DATABASE_HOST`                   | `localhost`                                   | PostgreSQL host |
| `DATABASE_PORT`                   | `5432`                                        | PostgreSQL port |
| `DATABASE_USER`                   | `user`                                        | PostgreSQL user |
| `DATABASE_PASSWORD`               | `password`                                    | PostgreSQL password |
| `DATABASE_NAME`                   | `mydb`                                        | PostgreSQL database. The app builds `postgresql+asyncpg://...` from these five; Alembic (`migrations/env.py`) builds its own sync URL from the same variables |
| `DATABASE_ECHO`                   | `False`                                       | Log every SQL statement |
| `OPENAI_API_KEY`                  | `xxxxx`                                       | OpenAI key used by `StudyPlanAIServiceOpenAIAdapter` |
| `AI_MODEL`                        | `gpt-4o-mini`                                 | Chat model used for generation |
| `AI_TEMPERATURE`                  | `0.0`                                         | Sampling temperature |
| `RABBITMQ_URL`                    | `amqp://admin:pass@localhost:5672/`           | RabbitMQ connection string. The local compose file uses `admin:rabbitpass`, so set this |
| `RABBITMQ_PREFETCH_COUNT`         | `10`                                          | Max unacked messages the consumer holds at once |
| `JWT_SECRET_KEY`                  | `change-me-jwt-secret-key-at-least-32-bytes`  | HS256 signing key. **Replace it** |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `15`                                          | Access token lifetime |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS`   | `7`                                           | Refresh token lifetime |
| `ALLOWED_ORIGINS`                 | `[]`                                          | Comma-separated CORS origins (plain string, **not** JSON), e.g. `http://localhost:5173,https://app.example.com`. The middleware also sets `allow_credentials=True` and all methods/headers |
| `LOG_LEVEL`                       | `INFO`                                        | Level of the `src.*` logger namespace |
| `DEBUG`                           | `False`                                       | Currently unused |
| `APP_NAME`                        | `Study Planner`                               | Currently unused |
| `AI_AGENT`                        | `openai`                                      | Currently unused (the OpenAI adapter is always used) |
| `GEMINI_API_KEY`                  | `xxxx`                                        | Currently unused |
| `EXA_API_KEY`                     | `xxxxx`                                       | Currently unused (the Exa search tool isn't wired in) |
| `LANGSMITH_API_KEY`               | `xxxxx`                                       | Currently unused by the code |

## Running locally

```bash
uv run fastapi dev
```

`fastapi` picks the app up from `[tool.fastapi] entrypoint = "src.main:app"` in `pyproject.toml`. The API is served at `http://localhost:8000` with interactive docs at `/docs` (use **Authorize** to paste an access token). The root `main.py` is an unused placeholder.

On startup the lifespan runs `Database.init()` (`metadata.create_all`, which creates missing tables but never alters existing ones) and starts the RabbitMQ consumer **in the same process**, so the API needs RabbitMQ to boot and also does the generation work. On shutdown it disposes the engine and closes the broker connection.

## API

There is no global prefix. Every route except `/v1/auth/*`, the WebSocket and the docs requires an `Authorization: Bearer <access_token>` header. A missing, expired, malformed or wrong-type token, or one whose user no longer exists or isn't active, returns `401` (`UserInvalidToken`).

| Method | Path                            | Description |
| ------ | ------------------------------- | ----------- |
| POST   | `/v1/auth/register`             | Create a user (`email`, `name`, `password`; password must be 8–32 characters). `201` with the new `id`. Duplicate email → `409` |
| POST   | `/v1/auth/login`                | `email` + `password` → `access_token` + `refresh_token`. Wrong credentials → `401` |
| POST   | `/v1/auth/refresh`              | `refresh_token` → a new `access_token` |
| GET    | `/v1/user/me`                   | The current user (`id`, `email`, `name`) |
| PUT    | `/v1/user/me/password`          | Change password (`current_password`, `new_password`). `204` |
| POST   | `/v1/study-plan/request`        | Request a plan (`subject`, `level`, `grade`). Returns `study_plan_id`; generation is asynchronous. An unknown `level` silently falls back to `University` |
| GET    | `/v1/study-plan/{id}`           | A study plan with its topics, sub-topics and assessments, and its `status` (`PENDING`/`GENERATING`/`COMPLETED`/`FAILED`) |
| GET    | `/v1/topic/{id}?include_children=true` | A topic. `include_children` is **required**; `false` omits sub-topics and the assessment |
| GET    | `/v1/assessment/{id}`           | An assessment with its questions |
| POST   | `/v1/assessment/{id}/start`     | `PENDING` → `IN_PROGRESS` |
| POST   | `/v1/assessment/{id}/answer`    | Answer one question (`question_id`, `selected_answer` in `a`–`d`) |
| POST   | `/v1/assessment/{id}/complete`  | `IN_PROGRESS` → `COMPLETED`, computes `score` |
| WS     | `/ws/{user_id}`                 | Real-time study plan notifications (see [Real-time notifications](#real-time-notifications)) |

Errors come back as `{"error": "<ExceptionName>", "message": "...", "data": {...}}`. Status codes are assigned per exception family in `src/infrastructure/adapters/inbound/http/middlewares/error_handler.py`: `400` invalid input, `401` invalid credentials/token, `404` not found, `409` user already exists, `412` invalid status transition, `500` internal/unknown errors.

## Logging

Configured once at process start (`src/main.py` → `configure_logging(settings)`) via `logging.config.dictConfig` in `src/infrastructure/logging/config.py`. All `src.*` loggers share one console handler at `LOG_LEVEL`; everything else logs at `WARNING`. The format includes a `correlation_id` field fed by a `ContextVar` (`src/infrastructure/logging/context.py`). Nothing calls `set_correlation_id` yet, so it currently prints `-`.

## Development

```bash
# Lint / format (2-space indent, configured in pyproject.toml)
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy src

# Tests
uv run pytest
```

Tests use in-memory fakes (`tests/fakes/`) and need neither PostgreSQL nor RabbitMQ. The HTTP tests build the app with `create_app` and a `TestClient` used **without** a `with` block, so the lifespan (DB init and broker consumer) never runs.

### Migrations

Migrations live in `migrations/versions/`. `migrations/env.py` sets `target_metadata = None`, so `--autogenerate` can't detect model changes: write the `upgrade()`/`downgrade()` by hand.

```bash
uv run alembic revision -m "describe the change"   # then fill in the generated file
uv run alembic upgrade head
```

Keep migrations and the ORM models in `src/infrastructure/adapters/outbound/persistence/models/` in sync, since `Database.init()` creates tables from the models on startup.

### Adding a feature end to end

1. **Domain** — add or extend the aggregate under `src/domain/<aggregate>/`, with value objects that `parse(...) -> Result` and methods that validate status and `add_domain_event(...)`.
2. **Application** — add the inbound port under `ports/inbound/`, the use case under `use_cases/`, DTOs/mappers, and new error classes in the folder's `error(s).py`.
3. **Infrastructure** — implement any new outbound port (repository, ORM model, persistence mapper), register providers in `container.py`, add the route, map the new errors in `error_handler.py`, and add the router module to `container.wire(...)` in `src/main.py` and to `create_app`.
4. **Async work** — add the message classes to `application/messages/`, map the domain event in `DomainEventPublisher._map_domain_event_to_message`, add the event/command handlers, register them in `register_consumers.py` by message type, and make sure the routing key matches the consumer's bindings (`study_plan.*` today).

### Conventions

- Indentation is **2 spaces** everywhere (`.editorconfig` and `[tool.ruff] indent-width = 2`), migrations included.
- Prefer `Result`/`Option` (`src/shared/`) over exceptions for expected failures in the domain and application layers. Use cases convert domain "problems" into the application's exception families with `unwrap_or_map_and_raise(...)`, and the HTTP layer maps those to status codes.
- Persistence models are separate from domain aggregates on purpose. Repositories convert between them via `reconstitute()`; the domain layer never imports SQLAlchemy.
- Domain events are published by repositories after a successful save, not by use cases.
- Event handlers publish commands; only command handlers run use cases.
- Use cases depend on ports (`Protocol`s), never on infrastructure classes.

## Known gaps

- `tests/unit/application/use_cases/test_generate_study_plan_use_case.py` fails at import (it uses a removed `ports.outbound.ai.prompt_provider` module), and `tests/unit/domain/test_user.py` expects a 128-character password to be valid while `Password` caps it at 32. Run `uv run pytest --ignore=tests/unit/application/use_cases/test_generate_study_plan_use_case.py` to skip the former.
- Resources aren't scoped to their owner: any authenticated user can read a study plan, topic or assessment by id.
- `/ws/{user_id}` doesn't authenticate, so anyone who knows a user id can listen to that user's notifications.
- `StudyPlanAIServiceOpenAIAdapter` calls the synchronous `chain.invoke(...)` inside an async method, blocking the event loop for the whole LLM call.
- The prompt tells the model it has an `internet_search` tool, but the Exa tool (`tools/internet_search.py`) isn't bound to the model.
- A failed message is dropped, not retried or dead-lettered.
