import pytest

from app.shared.config.app_info import ApplicationInfo, LicenseInfo

pytestmark = pytest.mark.unit


def test_application_info_defaults() -> None:
    info = ApplicationInfo()

    assert info.name == "menagerist"
    assert info.display_name == "Menagerist"
    assert info.version == "0.0.0"
    assert info.description == ""
    assert info.license == LicenseInfo()


def test_application_info_can_override_fields() -> None:
    info = ApplicationInfo(
        name="menagerist",
        display_name="TestApp",
        version="1.2.3",
        description="Test description",
        license=LicenseInfo(
            name="MIT",
            url="https://opensource.org/licenses/MIT",
        ),
    )

    assert info.display_name == "TestApp"
    assert info.version == "1.2.3"
    assert info.description == "Test description"
    assert info.license.name == "MIT"
    assert info.license.url == "https://opensource.org/licenses/MIT"


def test_application_info_package_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.shared.config.app_info._PACKAGE_NAME", "nonexistent_package"
    )
    app_info = ApplicationInfo.from_package()
    assert app_info.name == "menagerist"
