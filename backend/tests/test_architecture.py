import importlib.metadata

from pytest_archon import archrule


def _get_installed_packages() -> list[str]:
    """Returns a dictionary of package names and their versions."""
    return [dist.metadata["Name"] for dist in importlib.metadata.distributions()]


def _get_installed_packages_patterns() -> list[str]:
    return [f"{pkg}*" for pkg in _get_installed_packages()]


def test_domain_is_pure() -> None:
    """
    Ensures Domain modules (Entities, Value Objects, Ports) only import from:
    1. Other domain modules.
    2. The Python Standard Library.
    """
    (
        archrule("Domain layer purity")
        # Match domain folders in shared or features
        .match("app.*.domain*", "app.*.*.domain*")
        # Forbid all outer layers
        .should_not_import("app.entrypoints*")
        .should_not_import("app.*.infrastructure*", "app.*.*.infrastructure*")
        .should_not_import("app.*.application*", "app.*.*.application*")
        # Ensure no web framework leakage
        .should_not_import(*_get_installed_packages_patterns())
        .check("app")
    )
