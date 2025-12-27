import pytest

from app.shared.domain.exceptions import InvalidDomainId
from app.shared.domain.value_objects import DomainID


def test_domain_id_from_invalid_string_raises_error() -> None:
    with pytest.raises(InvalidDomainId) as exc:
        DomainID.from_str("not-a-valid-uuid")

    assert "not-a-valid-uuid" in str(exc.value)
    assert "DomainID" in str(exc.value)


def test_domain_id_with_non_uuid_value_raises_error() -> None:
    with pytest.raises(InvalidDomainId):
        DomainID(value="not-a-uuid")  # type: ignore
