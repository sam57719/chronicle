"""Custom versioning helpers for Menagerist."""

from __future__ import annotations

import datetime

from setuptools_scm.version import ScmVersion


def menagerist_calver(version: ScmVersion) -> str:
    """Return a CalVer-style version derived from SCM state."""
    today = datetime.date.today()
    year = today.year
    month = today.month

    if version.tag is None:
        return f"{year}.{month:02d}.0.dev{version.distance}"

    tag = str(version.tag)

    try:
        parts = tag.lstrip("v").split(".")
        tag_year = int(parts[0])
        tag_month = int(parts[1])
        tag_patch = int(parts[2])
    except (IndexError, ValueError):
        return f"{year}.{month:02d}.0.dev{version.distance}"

    if version.distance == 0 and not version.dirty:
        return f"{tag_year}.{tag_month:02d}.{tag_patch}"

    if year == tag_year and month == tag_month:
        return f"{year}.{month:02d}.{tag_patch + 1}.dev{version.distance}"

    return f"{year}.{month:02d}.0.dev{version.distance}"
