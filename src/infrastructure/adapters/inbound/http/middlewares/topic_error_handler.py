from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.application.use_cases.topic.error import (
  TopicInvalidInputError,
  TopicNotFoundError,
)


def topic_error_handler(request: Request, ex: Exception):
  match ex:
    case TopicInvalidInputError():
      return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(ex), "field": ex.field, "value": ex.value},
      )
    case TopicNotFoundError():
      return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(ex), "id": ex.topic_id},
      )
  return JSONResponse(
    status_code=500,
    content={"message": "Server Error"},
  )
