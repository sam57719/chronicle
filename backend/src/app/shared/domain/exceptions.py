"""Domain exceptions."""

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from app.shared.domain import DomainID

T = TypeVar("T", bound="DomainID")


class DomainException(Exception):
    """Base for all business logic errors."""

    pass


class InvalidDomainId[T](DomainException):
    """
    Raised when an ID is malformed.

    [T] allows us to track which specific ID class failed.
    """

    def __init__(self, id_class: type[T], value: str) -> None:
        """Initialise the exception."""
        self.id_class = id_class
        self.value = value
        self.message = f"Invalid {id_class.__name__}: '{value}' is not a valid UUIDv7."
        super().__init__(self.message)
