import os
from unittest import mock

from typer.testing import CliRunner

from snok import __version__
from snok.cli import app


def test_version(cli_runner: CliRunner) -> None:
    response = cli_runner.invoke(app, ["version"])
    assert response.exit_code == 0
    assert response.stdout == __version__


@mock.patch("snok.cli._add")
def test_new_package_setup(
    mock_add: mock.MagicMock, cli_runner: CliRunner, setup_test_project_dir: str
) -> None:
    response = cli_runner.invoke(
        app,
        ["new", "test_package", "-o", setup_test_project_dir],
    )
    assert response.exit_code == 0

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


@mock.patch("snok.cli._add")
def test_new_app_setup(
    mock_add: mock.MagicMock, cli_runner: CliRunner, setup_test_project_dir: str
) -> None:
    response = cli_runner.invoke(
        app,
        [
            "new",
            "test_app",
            "-o",
            setup_test_project_dir,
            "--type",
            "app",
        ],
    )
    assert response.exit_code == 0

    # assert the output directory exists
    for path in [
        f"{setup_test_project_dir}/test_app",
        f"{setup_test_project_dir}/tests",
        f"{setup_test_project_dir}/.git",
        f"{setup_test_project_dir}/README.md",
        f"{setup_test_project_dir}/pyproject.toml",
        f"{setup_test_project_dir}/.gitignore",
        f"{setup_test_project_dir}/test_app/__init__.py",
        f"{setup_test_project_dir}/test_app/router.py",
        f"{setup_test_project_dir}/test_app/logger.py",
        f"{setup_test_project_dir}/migrations/env.py",
        f"{setup_test_project_dir}/test_app/kit/db.py",
        f"{setup_test_project_dir}/tests/__init__.py",
        f"{setup_test_project_dir}/tests/conftest.py",
        f"{setup_test_project_dir}/tests/health/__init__.py",
    ]:
        assert os.path.exists(path)


@mock.patch("snok.cli._add")
def test_generate_model(
    mock_add: mock.MagicMock, cli_runner: CliRunner, setup_test_project_dir: str
) -> None:
    response = cli_runner.invoke(
        app,
        [
            "new",
            "test_generate_model_app",
            "-o",
            setup_test_project_dir,
            "--type",
            "app",
        ],
    )
    assert response.exit_code == 0

    cwd = os.getcwd()
    os.chdir(f"{setup_test_project_dir}")
    response = cli_runner.invoke(
        app,
        ["generate", "model", "person", "name:str", "age:int"],
    )
    os.chdir(cwd)
    assert response.exit_code == 0

    # assert the output directory exists
    for path in [
        f"{setup_test_project_dir}/test_generate_model_app",
        f"{setup_test_project_dir}/tests",
        f"{setup_test_project_dir}/.git",
        f"{setup_test_project_dir}/README.md",
        f"{setup_test_project_dir}/pyproject.toml",
        f"{setup_test_project_dir}/.gitignore",
        f"{setup_test_project_dir}/test_generate_model_app/__init__.py",
        f"{setup_test_project_dir}/test_generate_model_app/router.py",
        f"{setup_test_project_dir}/test_generate_model_app/logger.py",
        f"{setup_test_project_dir}/migrations/env.py",
        f"{setup_test_project_dir}/test_generate_model_app/kit/db.py",
        f"{setup_test_project_dir}/tests/__init__.py",
        f"{setup_test_project_dir}/tests/conftest.py",
        f"{setup_test_project_dir}/tests/health/__init__.py",
    ]:
        assert os.path.exists(path)


@mock.patch("snok.cli._add")
def test_generate_model_fails(
    mock_add: mock.MagicMock, cli_runner: CliRunner, setup_test_project_dir: str
) -> None:
    response = cli_runner.invoke(
        app,
        [
            "new",
            "test_generate_model_app",
            "-o",
            setup_test_project_dir,
            "--type",
            "app",
        ],
    )
    assert response.exit_code == 0

    cwd = os.getcwd()
    os.chdir(f"{setup_test_project_dir}")
    response = cli_runner.invoke(
        app,
        ["generate", "model"],
    )
    os.chdir(cwd)
    assert response.exit_code == 2

    cwd = os.getcwd()
    os.chdir(f"{setup_test_project_dir}")
    response = cli_runner.invoke(
        app,
        ["generate", "model", "person", "name:"],
    )
    os.chdir(cwd)
    assert response.exit_code == 1

    cwd = os.getcwd()
    os.chdir(f"{setup_test_project_dir}")
    response = cli_runner.invoke(
        app,
        ["generate", "model", "person", "name"],
    )
    os.chdir(cwd)
    assert response.exit_code == 1


@mock.patch("snok.cli._add")
def test_generate_router(
    mock_add: mock.MagicMock, cli_runner: CliRunner, setup_test_project_dir: str
) -> None:
    response = cli_runner.invoke(
        app,
        [
            "new",
            "test_generate_router_app",
            "-o",
            setup_test_project_dir,
            "--type",
            "app",
        ],
    )
    assert response.exit_code == 0

    cwd = os.getcwd()
    os.chdir(f"{setup_test_project_dir}")
    response = cli_runner.invoke(
        app,
        ["generate", "router", "myrouter", "hello", "world"],
    )
    os.chdir(cwd)
    assert response.exit_code == 0

    # assert the output directory exists
    for path in [
        f"{setup_test_project_dir}/test_generate_router_app",
        f"{setup_test_project_dir}/tests",
        f"{setup_test_project_dir}/.git",
        f"{setup_test_project_dir}/README.md",
        f"{setup_test_project_dir}/pyproject.toml",
        f"{setup_test_project_dir}/.gitignore",
        f"{setup_test_project_dir}/test_generate_router_app/__init__.py",
        f"{setup_test_project_dir}/test_generate_router_app/router.py",
        f"{setup_test_project_dir}/test_generate_router_app/myrouter/router.py",
        f"{setup_test_project_dir}/test_generate_router_app/logger.py",
        f"{setup_test_project_dir}/migrations/env.py",
        f"{setup_test_project_dir}/test_generate_router_app/kit/db.py",
        f"{setup_test_project_dir}/tests/__init__.py",
        f"{setup_test_project_dir}/tests/conftest.py",
        f"{setup_test_project_dir}/tests/health/__init__.py",
    ]:
        assert os.path.exists(path)

    # assert the hello and world functions exist
    for path in [
        f"{setup_test_project_dir}/test_generate_router_app/myrouter/router.py",
    ]:
        assert "async def _hello" in open(path).read()
        assert "async def _world" in open(path).read()


@mock.patch("snok.cli._add")
def test_generate_scaffold(
    mock_add: mock.MagicMock, cli_runner: CliRunner, setup_test_project_dir: str
) -> None:
    response = cli_runner.invoke(
        app,
        [
            "new",
            "test_generate_scaffold_app",
            "-o",
            setup_test_project_dir,
            "--type",
            "app",
        ],
    )
    assert response.exit_code == 0

    cwd = os.getcwd()
    os.chdir(f"{setup_test_project_dir}")
    response = cli_runner.invoke(
        app,
        ["generate", "scaffold", "person", "name:str", "age:int"],
    )
    os.chdir(cwd)
    assert response.exit_code == 0

    # assert the output directory exists
    for path in [
        f"{setup_test_project_dir}/test_generate_scaffold_app",
        f"{setup_test_project_dir}/tests",
        f"{setup_test_project_dir}/.git",
        f"{setup_test_project_dir}/README.md",
        f"{setup_test_project_dir}/pyproject.toml",
        f"{setup_test_project_dir}/.gitignore",
        f"{setup_test_project_dir}/test_generate_scaffold_app/__init__.py",
        f"{setup_test_project_dir}/test_generate_scaffold_app/router.py",
        f"{setup_test_project_dir}/test_generate_scaffold_app/logger.py",
        f"{setup_test_project_dir}/migrations/env.py",
        f"{setup_test_project_dir}/test_generate_scaffold_app/kit/db.py",
        f"{setup_test_project_dir}/test_generate_scaffold_app/persons/router.py",
        f"{setup_test_project_dir}/test_generate_scaffold_app/persons/schemas.py",
        f"{setup_test_project_dir}/test_generate_scaffold_app/persons/service.py",
        f"{setup_test_project_dir}/tests/__init__.py",
        f"{setup_test_project_dir}/tests/conftest.py",
        f"{setup_test_project_dir}/tests/health/__init__.py",
    ]:
        assert os.path.exists(path)
