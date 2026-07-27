from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.application.use_cases.user.error import (
  UserInvalidInputError,
  UserNotFoundError,
  UserUnauthorized,
)


def user_error_handler(request: Request, ex: Exception):
  match ex:
    case UserInvalidInputError():
      return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(ex), "field": ex.field, "value": ex.value},
      )
    case UserNotFoundError():
      return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(ex), "id": ex.user_id},
      )
    case UserUnauthorized():
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Unauthorized"},
      )

  return JSONResponse(
    status_code=500,
    content={"message": "Server Error"},
  )
