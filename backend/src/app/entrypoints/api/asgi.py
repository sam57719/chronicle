"""ASGI entry point for the API application.

This module pulls trusted proxy hosts from application settings so the
behaviour can be configured via environment variables (e.g.:
`MG_API__TRUSTED_HOSTS`).
"""

from typing import TYPE_CHECKING, cast

from granian.utils.proxies import wrap_asgi_with_proxy_headers

from app.shared.config import get_settings

from .main import create_app

if TYPE_CHECKING:
    from starlette.types import ASGIApp


def create_asgi_app() -> ASGIApp:
    """Create the ASGI app wrapped with proxy header support."""
    settings = get_settings()
    wrapped_app = wrap_asgi_with_proxy_headers(
        create_app(),
        trusted_hosts=settings.api.trusted_hosts,
    )
    return cast("ASGIApp", wrapped_app)


app = create_asgi_app()
