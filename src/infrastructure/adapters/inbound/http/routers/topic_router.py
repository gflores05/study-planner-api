from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.application.dtos.topic import (
  TopicDTO,
)
from src.application.ports.inbound.topic.get_topic_use_case import (
  GetTopicUseCasePort,
)
from src.domain.user.user import User
from src.infrastructure.adapters.outbound.auth.user_context import get_user_context
from src.infrastructure.config.container import Container

router = APIRouter(prefix="/v1/topic", tags=["topic"])


@router.get("/{id}", response_model=TopicDTO)
@inject
async def get_topic(
  id: str,
  include_children: bool,
  use_case: Annotated[
    GetTopicUseCasePort, Depends(Provide[Container.get_topic_use_case])
  ],
  user: User = Depends(get_user_context),
) -> TopicDTO:
  return await use_case.execute(id=id, include_children=include_children)
