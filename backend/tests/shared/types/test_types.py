import pytest
from pydantic import BaseModel, ValidationError

from app.shared.types import CSV, ValidatedNetworkHostStr  # noqa: TC001


class _CSVModel(BaseModel):
    values: CSV[str]


class _NetworkHostModel(BaseModel):
    host: ValidatedNetworkHostStr


def test_csv_type_splits_comma_separated_values() -> None:
    # noinspection PyTypeChecker
    model = _CSVModel(values="a, b, c")

    assert model.values == ["a", "b", "c"]


def test_csv_type_strips_empty_values() -> None:
    # noinspection PyTypeChecker
    model = _CSVModel(values="a, , b,   ,c")

    assert model.values == ["a", "b", "c"]


def test_csv_accepts_list_input() -> None:
    model = _CSVModel(values=["a", "b", "c"])

    assert model.values == ["a", "b", "c"]


def test_validated_network_host_str_accepts_localhost() -> None:
    model = _NetworkHostModel(host="localhost")

    assert model.host == "localhost"


def test_validated_network_host_str_accepts_ip_address() -> None:
    model = _NetworkHostModel(host="127.0.0.1")

    assert model.host == "127.0.0.1"


def test_validated_network_host_str_rejects_invalid_value() -> None:
    with pytest.raises(ValidationError):
        _NetworkHostModel(host="not-a-host")


def test_validated_network_host_str_returns_str() -> None:
    model = _NetworkHostModel(host="127.0.0.1")
    assert model.host == "127.0.0.1"
    assert isinstance(model.host, str)
