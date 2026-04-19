from typing import Annotated

from pydantic import BeforeValidator
from pydantic_settings import NoDecode


def _split_csv(v: object) -> list[str] | object:
    if isinstance(v, str):
        return [item.strip() for item in v.split(",")]
    return v


type CSV[T] = Annotated[list[T], NoDecode, BeforeValidator(_split_csv)]
