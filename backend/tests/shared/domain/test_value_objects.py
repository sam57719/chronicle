from typing import Any, cast
from uuid import UUID, uuid7

import pytest

from app.shared.domain.exceptions import InvalidDomainId
from app.shared.domain.value_objects import DomainID


def test_domain_id_from_invalid_string_raises_error() -> None:
    with pytest.raises(InvalidDomainId) as exc:
        DomainID.create("not-a-valid-uuid")

    assert "not-a-valid-uuid" in str(exc.value)
    assert "DomainID" in str(exc.value)


def test_domain_id_from_domain_id_returns_same_domain_id() -> None:
    domain_id = DomainID.create()
    assert DomainID.create(domain_id) == domain_id


def test_domain_id_from_valid_string_returns_domain_id() -> None:
    uuid_str = str(uuid7())
    domain_id = DomainID.create(uuid_str)
    assert str(domain_id.value) == uuid_str


def test_domain_id_from_uuid_returns_domain_id() -> None:
    uuid_ = uuid7()
    domain_id = DomainID.create(uuid_)
    assert str(domain_id.value) == str(uuid_)


def test_domain_id_from_none_generate_new_uuid() -> None:
    domain_id = DomainID.create()
    assert isinstance(domain_id.value, UUID)


def test_domain_id_create_with_incompatible_type_raises_error() -> None:
    with pytest.raises(InvalidDomainId):
        DomainID.create(cast(Any, object()))


def test_direct_instantiation_of_domain_id_with_uuid() -> None:
    uuid_ = uuid7()
    domain_id = DomainID(uuid_)
    assert str(domain_id.value) == str(uuid_)


def test_direct_instantiation_of_domain_id_with_not_uuid() -> None:
    uuid_str = str(uuid7())
    with pytest.raises(InvalidDomainId):
        # noinspection PyTypeChecker
        DomainID(uuid_str)  # type: ignore[arg-type]


def test_domain_id_with_non_uuid_value_raises_error() -> None:
    with pytest.raises(InvalidDomainId):
        DomainID.create("not-a-uuid")
