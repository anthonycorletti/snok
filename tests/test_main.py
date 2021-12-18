import os

from python_project_template.main import foo


def test_timezone() -> None:
    assert foo() == "foo"
    assert os.environ["TZ"] == "UTC"
