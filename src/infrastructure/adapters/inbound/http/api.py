from dependency_injector import containers
from fastapi import FastAPI

from src.domain.study_plan.study_plan import StudyPlanError
from src.infrastructure.adapters.inbound.http.middlewares.study_plan_error_handler import (
  study_plan_error_handler,
)
from src.infrastructure.adapters.inbound.http.routers import study_plan_router
from src.infrastructure.config.lifespan import lifespan_factory


def create_app(container: containers.DeclarativeContainer) -> FastAPI:
  app = FastAPI(lifespan=lifespan_factory())
  setattr(app, "container", container)
  app.include_router(study_plan_router.study_plan_router)
  app.add_exception_handler(StudyPlanError, study_plan_error_handler)
  return app
