"""ASGI entry point for the API application.

This module pulls trusted proxy hosts from application settings so the
behaviour can be configured via environment variables (e.g.:
`MG_API__TRUSTED_HOSTS`).
"""

from granian.utils.proxies import wrap_asgi_with_proxy_headers

from app.shared.config import get_settings

from .main import create_app

_settings = get_settings()
_trusted = _settings.api.trusted_hosts

app = wrap_asgi_with_proxy_headers(create_app(), trusted_hosts=_trusted)
