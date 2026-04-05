"""Tests for the Menagerist CalVer versioning scheme."""

from __future__ import annotations

import datetime
from unittest.mock import MagicMock, patch

import pytest
from menagerist_versioning import menagerist_calver

TODAY = datetime.date(2026, 4, 15)
JANUARY = datetime.date(2026, 1, 5)


def make_version(
    tag: str | None = None,
    distance: int = 0,
    dirty: bool = False,
) -> MagicMock:
    """Create a mock ScmVersion."""
    version = MagicMock()
    version.tag = tag
    version.distance = distance
    version.dirty = dirty
    return version


def _freeze(date: datetime.date):
    """Return a context manager that freezes datetime.date.today()."""
    mock = patch("menagerist_versioning.datetime.date")

    def start():
        m = mock.start()
        m.today.return_value = date
        m.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)
        return m

    return mock, start


@pytest.fixture
def freeze_date():
    """Freeze date to 2026-04-15."""
    with patch("menagerist_versioning.datetime.date") as mock_date:
        mock_date.today.return_value = TODAY
        mock_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)
        yield mock_date


@pytest.fixture
def freeze_date_january():
    """Freeze date to 2026-01-05."""
    with patch("menagerist_versioning.datetime.date") as mock_date:
        mock_date.today.return_value = JANUARY
        mock_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)
        yield mock_date


class TestNoTag:
    """Behaviour when no tag exists."""

    def test_no_tag_returns_dev_version(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(distance=5))
        assert result == "2026.04.0.dev5"

    def test_no_tag_zero_distance(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version())
        assert result == "2026.04.0.dev0"


class TestCleanTag:
    """Behaviour on a clean-tagged commit."""

    def test_clean_tag_returns_exact_version(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.04.0"))
        assert result == "2026.04.0"

    def test_clean_tag_patch_one(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.04.1"))
        assert result == "2026.04.1"

    def test_dirty_tag_is_not_clean(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.04.0", dirty=True))
        assert result != "2026.04.0"

    def test_nonzero_distance_is_not_clean(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.04.0", distance=1))
        assert result != "2026.04.0"


class TestSameMonthDev:
    """Behaviour when commits exist after a tag in the same month."""

    def test_same_month_increments_patch(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.04.0", distance=1))
        assert result == "2026.04.1.dev1"

    def test_same_month_higher_patch(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.04.2", distance=3))
        assert result == "2026.04.3.dev3"

    def test_same_month_dirty(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(
            make_version(tag="2026.04.0", distance=1, dirty=True)
        )
        assert result == "2026.04.1.dev1"


class TestNewMonth:
    """Behaviour when the current month differs from the tag month."""

    def test_new_month_resets_patch(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.03.2", distance=5))
        assert result == "2026.04.0.dev5"

    def test_new_year(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2025.12.0", distance=3))
        assert result == "2026.04.0.dev3"


class TestVPrefix:
    """Behaviour with v-prefixed tags."""

    def test_v_prefix_is_stripped(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="v2026.04.0"))
        assert result == "2026.04.0"

    def test_v_prefix_dev(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="v2026.04.0", distance=2))
        assert result == "2026.04.1.dev2"


class TestMalformedTag:
    """Behaviour with unparseable tags."""

    def test_malformed_tag_falls_back_to_dev(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="not-a-version", distance=3))
        assert result == "2026.04.0.dev3"

    def test_incomplete_tag_falls_back_to_dev(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="2026.04", distance=2))
        assert result == "2026.04.0.dev2"

    def test_empty_tag_falls_back_to_dev(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(tag="", distance=1))
        assert result == "2026.04.0.dev1"


class TestMonthPadding:
    """Ensure the month is always zero-padded."""

    def test_single_digit_month_is_padded(self, freeze_date_january: MagicMock) -> None:
        result = menagerist_calver(make_version(distance=1))
        assert result == "2026.01.0.dev1"

    def test_double_digit_month_unchanged(self, freeze_date: MagicMock) -> None:
        result = menagerist_calver(make_version(distance=1))
        assert result == "2026.04.0.dev1"
