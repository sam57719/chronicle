"""Shared architectural ports and base interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Self, TypeVar

T = TypeVar("T")


class ValueObject[T](ABC):
    """Guard for all Value Objects: requires .value and .create()."""

    @property
    @abstractmethod
    def value(self) -> T:
        """The underlying raw value."""
        ...

    @classmethod
    @abstractmethod
    def create(cls, value: Any) -> Self:
        """Business factory for the value object."""
        ...

    def __str__(self) -> str:
        """Return a string representation of the Value Object."""
        return str(self.value)
