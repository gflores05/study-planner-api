from dependency_injector import containers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.adapters.inbound.http.middlewares.error_handler import (
  register_error_handlers,
)
from src.infrastructure.adapters.inbound.http.routers import (
  assessment_router,
  study_plan_router,
  topic_router,
  user_router,
  websockets_router,
)
from src.infrastructure.config.lifespan import lifespan_factory


def create_app(container: containers.DeclarativeContainer) -> FastAPI:
  app = FastAPI(lifespan=lifespan_factory())
  setattr(app, "container", container)

  settings = container.settings()

  origins = settings.allowed_origins

  app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  # Routers
  app.include_router(study_plan_router.router)
  app.include_router(topic_router.router)
  app.include_router(assessment_router.router)
  app.include_router(websockets_router.router)
  app.include_router(user_router.router)

  # Error Handler
  register_error_handlers(app)

  return app
