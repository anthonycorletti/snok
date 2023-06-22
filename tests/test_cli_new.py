import os

from typer.testing import CliRunner

from snok import __version__
from snok.cli import app


def test_new_package(cli_runner: CliRunner, setup_test_project_dir: str) -> None:
    response = cli_runner.invoke(
        app,
        ["new", "test_package", "-o", setup_test_project_dir],
    )
    assert response.exit_code == 0
    print(os.listdir(setup_test_project_dir))
    # assert the output directory exists
    for path in [
        f"{setup_test_project_dir}/test_package",
        f"{setup_test_project_dir}/tests",
        f"{setup_test_project_dir}/.git",
        f"{setup_test_project_dir}/README.md",
        f"{setup_test_project_dir}/pyproject.toml",
        f"{setup_test_project_dir}/.gitignore",
        f"{setup_test_project_dir}/test_package/__init__.py",
        f"{setup_test_project_dir}/test_package/main.py",
        f"{setup_test_project_dir}/tests/__init__.py",
        f"{setup_test_project_dir}/tests/conftest.py",
        f"{setup_test_project_dir}/tests/test_main.py",
        f"{setup_test_project_dir}/tests/test_version.py",
    ]:
        assert os.path.exists(path)


def test_version(cli_runner: CliRunner) -> None:
    response = cli_runner.invoke(app, ["version"])
    assert response.exit_code == 0
    assert response.stdout == __version__
