from dependency_injector import containers
from fastapi import FastAPI

from src.application.use_cases.assessment.error import AssessmentError
from src.application.use_cases.study_plan.errors import StudyPlanError
from src.infrastructure.adapters.inbound.http.middlewares.assessment_error_handler import (
  assessment_error_handler,
)
from src.infrastructure.adapters.inbound.http.middlewares.study_plan_error_handler import (
  study_plan_error_handler,
)
from src.infrastructure.adapters.inbound.http.routers import (
  assessment_router,
  study_plan_router,
)
from src.infrastructure.config.lifespan import lifespan_factory


def create_app(container: containers.DeclarativeContainer) -> FastAPI:
  app = FastAPI(lifespan=lifespan_factory())
  setattr(app, "container", container)

  # Routers
  app.include_router(study_plan_router.router)
  app.include_router(assessment_router.router)

  # Error Handler
  app.add_exception_handler(StudyPlanError, study_plan_error_handler)
  app.add_exception_handler(AssessmentError, assessment_error_handler)

  return app
