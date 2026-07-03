from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.domain.study_plan.study_plan import StudyPlanError
from src.infrastructure.adapters.inbound.http.middlewares.study_plan_error_handler import (
  study_plan_error_handler,
)
from src.infrastructure.adapters.inbound.http.routers import study_plan_router
from src.infrastructure.config.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
  await init_db()  # startup
  yield
  await close_db()


def create_app() -> FastAPI:
  app = FastAPI(lifespan=lifespan)
  app.include_router(study_plan_router.study_plan_router)
  app.add_exception_handler(StudyPlanError, study_plan_error_handler)
  return app
