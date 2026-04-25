import logging

from app.shared.logging_.semantic_sorter import SemanticSorter


def test_semantic_sorter_orders_keys() -> None:
    """Ensure keys specified in the sorter order appear first and in the
    requested order, with remaining keys preserved in their original
    insertion order.
    """
    event = {
        "level": "info",
        "event": "user_logged_in",
        "user_id": 123,
        "request_id": "req-1",
    }

    sorter = SemanticSorter(order=["request_id", "user_id", "event"])

    logger = logging.getLogger(__name__)
    result = sorter(logger, "info", event)

    # Keys from the provided order should be first, in that order
    assert list(result.keys()) == ["request_id", "user_id", "event", "level"]


def test_semantic_sorter_ignores_missing_order_keys_and_keeps_original() -> None:
    """If the requested order contains keys that are not present in the
    event dict they should be ignored and other keys must keep their original
    insertion order.
    """
    event = {"a": 1, "b": 2, "c": 3}

    # 'x' and 'y' are not present in the event dict and should be ignored
    sorter = SemanticSorter(order=["x", "b", "y"])

    logger = logging.getLogger(__name__)
    result = sorter(logger, "debug", event)

    # Only 'b' from the order should be moved to the front; remaining keys
    # should follow in the original insertion order (a, c)
    assert list(result.keys()) == ["b", "a", "c"]
