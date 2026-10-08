import logging.config

from src.infrastructure.config.settings import Settings
from src.infrastructure.logging.context import CorrelationIdFilter


def configure_logging(settings: Settings) -> None:
  logging.config.dictConfig(
    {
      "version": 1,
      "disable_existing_loggers": False,
      "filters": {
        "correlation_id": {"()": CorrelationIdFilter},
      },
      "formatters": {
        "default": {
          "format": (
            "%(asctime)s %(levelname)s [%(name)s] "
            "[correlation_id=%(correlation_id)s] %(message)s"
          ),
        },
      },
      "handlers": {
        "console": {
          "class": "logging.StreamHandler",
          "formatter": "default",
          "filters": ["correlation_id"],
        },
      },
      "loggers": {
        "src": {
          "level": settings.log_level,
          "handlers": ["console"],
          "propagate": False,
        },
      },
      "root": {"level": "WARNING", "handlers": ["console"]},
    }
  )
