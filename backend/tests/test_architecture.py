from pytest_archon import archrule


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
        .should_not_import(
            "fastapi*", "pydantic*", "sqlalchemy*", "starlette*", "uvicorn*"
        )
        .check("app")
    )
