import importlib.metadata

from pytest_archon import archrule

# Domain-safe third-party libraries.
# Any addition here is an explicit architectural decision.
ALLOWED_DOMAIN_PACKAGES = [
    "pydantic",  # FOR VALIDATION ONLY
]


def _get_forbidden_packages_patterns() -> list[str]:
    """
    Returns import patterns for all installed packages
    except those explicitly allowed in the domain layer.
    """
    allowed = tuple(ALLOWED_DOMAIN_PACKAGES)

    forbidden: list[str] = []
    for dist in importlib.metadata.distributions():
        name = dist.metadata["Name"]

        # Skip allowed packages (e.g. pydantic, pydantic-core)
        if name.startswith(allowed):
            continue

        forbidden.append(f"{name}*")

    return forbidden


def test_domain_is_pure() -> None:
    """
    Ensures Domain modules (Entities, Value Objects, Ports) only depend on:
    1. Other domain modules.
    2. The Python Standard Library.
    3. Explicitly allowed domain-safe libraries (e.g. pydantic).
    """
    (
        archrule("Domain layer purity")
        # Match domain folders (shared + feature domains)
        .match("app.*.domain*", "app.*.*.domain*")
        # Forbid all outer layers
        .should_not_import("app.entrypoints*")
        .should_not_import("app.*.infrastructure*", "app.*.*.infrastructure*")
        .should_not_import("app.*.application*", "app.*.*.application*")
        # Forbid all third-party packages except the allow-list
        .should_not_import(*_get_forbidden_packages_patterns())
        .check("app")
    )
