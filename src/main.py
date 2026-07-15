from src.infrastructure.adapters.inbound.http.api import create_app
from src.infrastructure.config.container import Container

if __name__ == "src.main":
  container = Container()
  container.wire(
    modules=[
      __name__,
      "src.infrastructure.config.lifespan",
      "src.infrastructure.adapters.inbound.http.routers.study_plan_router",
      "src.infrastructure.adapters.inbound.http.routers.assessment_router",
      "src.infrastructure.adapters.inbound.http.routers.topic_router",
      "src.infrastructure.adapters.inbound.http.routers.websockets_router",
    ]
  )

  app = create_app(container=container)
