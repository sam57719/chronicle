from app.shared.config.app_info import ApplicationInfo, LicenseInfo


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
