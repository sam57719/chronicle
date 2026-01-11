"""Domain exceptions."""

from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from app.shared.domain import DomainID

T = TypeVar("T", bound="DomainID")


class DomainException(Exception):
    """Base for all business logic errors."""

    pass


class InvalidDomainId[T](DomainException):
    """Raised when an ID is malformed or has the wrong type."""

    def __init__(
        self, id_class: type[T], value: Any, message: str | None = None
    ) -> None:
        """Initialize the exception."""
        self.id_class = id_class
        self.value = value
        self.message = message or (
            f"Invalid {id_class.__name__}: " f"'{value}' is not a valid UUID."
        )
        super().__init__(self.message)
