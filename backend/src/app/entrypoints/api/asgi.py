"""ASGI entry point for the API application."""

from granian.utils.proxies import wrap_asgi_with_proxy_headers

from .main import create_app

app = wrap_asgi_with_proxy_headers(create_app(), trusted_hosts=["*"])
