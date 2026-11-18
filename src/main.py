from src.infrastructure.adapters.inbound.http.api import create_app
from src.infrastructure.config.container import Container
from src.infrastructure.config.settings import get_settings
from src.infrastructure.logging.config import configure_logging

if __name__ == "src.main":
  configure_logging(get_settings())
  container = Container()
  container.wire(
    modules=[
      __name__,
      "src.infrastructure.config.lifespan",
      "src.infrastructure.adapters.inbound.http.routers.study_plan_router",
      "src.infrastructure.adapters.inbound.http.routers.assessment_router",
      "src.infrastructure.adapters.inbound.http.routers.topic_router",
      "src.infrastructure.adapters.inbound.http.security",
      "src.infrastructure.adapters.inbound.http.routers.auth_router",
      "src.infrastructure.adapters.inbound.http.routers.user_router",
      "src.infrastructure.adapters.inbound.http.routers.websockets_router",
    ]
  )

  app = create_app(container=container)
