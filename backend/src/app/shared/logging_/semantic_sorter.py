from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import logging

    from structlog.typing import EventDict


class SemanticSorter:
    """Sort event dictionary keys in a semantic order."""

    def __init__(self, order: list[str]) -> None:
        self._order = order

    def __call__(
        self, _logger: logging.Logger, _method_name: str, event_dict: EventDict
    ) -> EventDict:
        """Sort event dictionary keys in a semantic order."""
        ordered = {k: event_dict[k] for k in self._order if k in event_dict}
        ordered.update({k: v for k, v in event_dict.items() if k not in ordered})
        return ordered
