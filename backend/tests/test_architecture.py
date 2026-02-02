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
        # Forbid all outer layers (current + target naming)
        .should_not_import("app.entrypoints*")
        .should_not_import("app.*.application*", "app.*.*.application*")
        .should_not_import("app.*.infrastructure*", "app.*.*.infrastructure*")
        .should_not_import("app.*.persistence*", "app.*.*.persistence*")
        .should_not_import("app.*.integrations*", "app.*.*.integrations*")
        # Forbid all third-party packages except the allowlist
        .should_not_import(*_get_forbidden_packages_patterns())
        .check("app")
    )


def test_application_does_not_import_outer_layers() -> None:
    """
    Ensures Application code (use cases, orchestration) does not depend on outer layers.

    Rules:
    - application cannot import: persistence, integrations, entrypoints
    - (also forbids current 'infrastructure' naming, which is an outer layer)
    """
    (
        archrule("Application layer imports")
        .match("app.*.application*", "app.*.*.application*")
        .should_not_import("app.entrypoints*")
        .should_not_import("app.*.infrastructure*", "app.*.*.infrastructure*")
        .should_not_import("app.*.persistence*", "app.*.*.persistence*")
        .should_not_import("app.*.integrations*", "app.*.*.integrations*")
        .check("app")
    )


def test_infrastructure_is_not_used_by_entrypoints() -> None:
    """
    Ensures outer layer implementations (infrastructure/persistence/integrations)
    do not depend on entrypoints.

    Rule:
    - persistence/integrations can import inwards (domain/application),
      but must not import entrypoints.
    """
    (
        archrule("Infrastructure does not depend on entrypoints")
        .match(
            "app.*.infrastructure*",
            "app.*.*.infrastructure*",
            "app.*.persistence*",
            "app.*.*.persistence*",
            "app.*.integrations*",
            "app.*.*.integrations*",
        )
        .should_not_import("app.entrypoints*")
        .check("app")
    )
