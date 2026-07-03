from typing import Literal

from exa_py import Exa
from exa_py.api import ContentsOptions

from src.infrastructure.config.settings import Settings


def get_category(topic: Literal["general", "news", "finance"]):
  match topic:
    case "general":
      return None
    case "news":
      return "news"
    case "finance":
      return "financial report"


def get_contents(include_raw_content: bool) -> ContentsOptions | Literal[False] | None:
  return {"text": True} if include_raw_content else None


def internet_search_factory(settings: Settings):
  exa = Exa(api_key=settings.exa_api_key)

  def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
  ):
    """Run a web search"""

    category = get_category(topic)
    contents = get_contents(include_raw_content)

    return exa.search(
      query=query,
      type="auto",
      num_results=max_results,
      contents=contents,
      category=category,
    )

  return internet_search
