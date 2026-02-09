import importlib
from unittest.mock import Mock, patch

import app.entrypoints.api.asgi as asgi_module


def test_asgi_app_is_wrapped_with_proxy_headers() -> None:
    fake_fastapi_app = Mock(name="fastapi_app")
    wrapped_app = Mock(name="wrapped_app")

    with (
        patch(
            "app.entrypoints.api.main.create_app",
            return_value=fake_fastapi_app,
        ) as create_app_mock,
        patch(
            "granian.utils.proxies.wrap_asgi_with_proxy_headers",
            return_value=wrapped_app,
        ) as wrap_mock,
    ):

        importlib.reload(asgi_module)

        create_app_mock.assert_called_once()
        wrap_mock.assert_called_once_with(fake_fastapi_app)
        assert asgi_module.app is wrapped_app
