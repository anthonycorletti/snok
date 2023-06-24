import importlib
from typing import List, Optional

from typer import Argument, Exit, Option, Typer, echo

from snok import __version__
from snok.const import APP_DESC, APP_NAME, BumpType, DepencencyAction, ProjectType
from snok.services.new import NewPackageService
from snok.utils import (
    _bump_version_string,
    _get_default_output_dir,
    _get_project_name,
    _run_cmd,
    _snok_sources,
    _update_pyproject_toml,
)

app = Typer(
    name=APP_NAME,
    help=APP_DESC,
    no_args_is_help=True,
)


@app.callback()
def main_callback() -> None:
    pass


main_callback.__doc__ = APP_NAME


@app.command("version")
def _version() -> None:
    """Prints the version."""
    echo(__version__, nl=False)


@app.command(
    "new",
    help="Create various types of Python projects.",
    no_args_is_help=True,
)
def _new(
    name: str = Argument(
        ...,
        help="The name of the project.",
    ),
    description: str = Option(
        "A new Python project.",
        "-d",
        "--description",
        help="The description of the project. Defaults to 'A new Python project.'",
    ),
    type: ProjectType = Option(
        "package",
        "-t",
        "--type",
        help="The type of project to create. Defaults to 'package'",
    ),
    output_dir: str = Option(
        _get_default_output_dir(),
        "-o",
        "--output-dir",
        help="The output directory of the project. "
        "Defaults to the same directory of the current virtual environment.",
    ),
) -> None:
    new_project_service_dispatcher = {
        ProjectType.package: NewPackageService,
    }
    new_project_service = new_project_service_dispatcher[type]()
    new_project_service.create(
        name=name, desc=description, type=type, output_dir=output_dir
    )


@app.command(
    "clean",
    help="Clean the project. Power-washers not included.",
)
def _clean() -> None:  # pragma: no cover
    _run_cmd(
        " ".join(
            [
                "rm",
                "-rf",
                "build",
                "dist",
                "site",
                "htmlcov",
                ".mypy_cache",
                ".pytest_cache",
                ".ruff_cache",
                "*.egg-info",
                "coverage.xml",
                ".coverage",
            ]
        ),
        shell=True,
    )


@app.command(
    "install",
    help="Install the project.",
)
def _install(
    editable: bool = Option(
        True,
        "-e",
        "--editable",
        help="Install the project in editable mode. Defaults to True.",
    ),
    dependency_groups: Optional[List[str]] = Option(
        ["dev"],
        "-g",
        "--dependency-groups",
        help="The dependency groups to install. Defaults to ['dev'].",
    ),
) -> None:  # pragma: no cover
    _run_cmd(
        "pip install --upgrade pip",
    )
    dep_install_str = "."
    if dependency_groups and dependency_groups != ["prod"]:
        dep_install_str += f"[{','.join(dependency_groups)}]"
    _run_cmd(
        " ".join(
            [
                "pip",
                "install",
                "-e" if editable else "",
                dep_install_str,
            ]
        ),
    )
    _run_cmd(
        "pre-commit install",
    )
    _run_cmd(
        "pre-commit autoupdate",
    )
    _run_cmd(
        "if command -v pyenv 1>/dev/null 2>&1; then pyenv rehash; fi",
        shell=True,
    )


@app.command(
    "add",
    help="Add packages to the project.",
    no_args_is_help=True,
)
def _add(
    packages: List[str] = Argument(
        ...,
        help="The packages to add.",
    ),
    dependency_group: str = Option(
        None,
        "-g",
        "--dependency-group",
        help="The dependency group to add the packages to. Defaults to None.",
    ),
) -> None:  # pragma: no cover
    _update_pyproject_toml(
        packages=packages,
        dependency_action=DepencencyAction.add,
        dependency_group_name=dependency_group,
    )
    _install(dependency_groups=[dependency_group] if dependency_group else ["all"])


@app.command(
    "remove",
    help="Remove packages from the project.",
    no_args_is_help=True,
)
def _remove(
    packages: List[str] = Argument(
        ...,
        help="The packages to remove.",
    ),
    dependency_group: str = Option(
        None,
        "-g",
        "--dependency-group",
        help="The dependency group to remove the packages from. Defaults to None.",
    ),
) -> None:  # pragma: no cover
    _update_pyproject_toml(
        packages=packages,
        dependency_action=DepencencyAction.remove,
        dependency_group_name=dependency_group,
    )
    _run_cmd(
        f"pip uninstall -y {' '.join(packages)}",
    )
    _install(dependency_groups=[dependency_group] if dependency_group else ["all"])


@app.command(
    "lint",
    help="Check typing and formatting.",
)
def _lint() -> None:  # pragma: no cover
    echo("Linting...")
    out = _run_cmd(
        f"mypy {' '.join(_snok_sources())}",
        shell=True,
        check=False,
        capture_output=True,
    )
    if out is not None and out.returncode != 0:
        echo(out.stdout.decode("utf-8").strip(), err=True)
        raise Exit(code=1)
    out = _run_cmd(
        f"black --check {' '.join(_snok_sources())}",
        shell=True,
        check=False,
        capture_output=True,
    )
    if out is not None and out.returncode != 0:
        echo(out.stdout.decode("utf-8").strip(), err=True)
        raise Exit(code=1)
    out = _run_cmd(
        f"ruff {' '.join(_snok_sources())}",
        shell=True,
        check=False,
        capture_output=True,
    )
    if out is not None and out.returncode != 0:
        echo(out.stdout.decode("utf-8").strip(), err=True)
        raise Exit(code=1)


@app.command(
    "format",
    help="Format the code.",
)
def _format() -> None:  # pragma: no cover
    echo("Formatting...")
    out = _run_cmd(
        f"black {' '.join(_snok_sources())}",
        shell=True,
        check=False,
        capture_output=True,
    )
    if out is not None and out.returncode != 0:
        echo(out.stdout.decode("utf-8"), err=True)
        raise Exit(code=1)
    out = _run_cmd(
        f"ruff {' '.join(_snok_sources())} --fix",
        shell=True,
        check=False,
        capture_output=True,
    )
    if out is not None and out.returncode != 0:
        echo(out.stdout.decode("utf-8"), err=True)
        raise Exit(code=1)


@app.command(
    "test",
    help="Run the tests.",
)
def _test() -> None:  # pragma: no cover
    echo("Running tests...")
    out = _run_cmd(
        "pytest",
        shell=True,
        check=False,
        capture_output=True,
    )
    if out is not None and out.returncode != 0:
        echo(out.stdout.decode("utf-8"), err=True)
        if out.stderr:
            echo(out.stderr.decode("utf-8"), err=True)
        raise Exit(code=1)
    elif out is not None:
        echo(out.stdout.decode("utf-8"))


@app.command(
    "build",
    help="Build the project.",
)
def _build() -> None:  # pragma: no cover
    _run_cmd(
        "pip install --upgrade build",
    )
    _run_cmd(
        "python -m build",
    )


@app.command(
    "publish",
    help="Publish the project.",
)
def _publish() -> None:  # pragma: no cover
    _run_cmd(
        "pip install --upgrade twine",
    )
    _run_cmd(
        "twine upload dist/*",
    )


@app.command(
    "ok",
    help="Run a suite of commands to make things ok for local dev.",
)
def _ok() -> None:  # pragma: no cover
    _clean()
    _install(dependency_groups=["all"])
    _format()
    _lint()
    _test()


@app.command("bump-version", help="Bump the version.")
def _bump_version(
    part: Optional[BumpType] = Option(
        None,
        "-p",
        "--part",
        help="The part of the version to bump. Defaults to None.",
    ),
) -> None:  # pragma: no cover
    project_name = _get_project_name()
    _version = importlib.import_module(f"{project_name}").__version__

    print(f"Current version: {_version}")
    new_version = _bump_version_string(_version, part)
    version_file = f"{project_name}/__init__.py"
    with open(version_file, "r") as f:
        lines = f.readlines()
    with open(version_file, "w") as f:
        for line in lines:
            if line.startswith("__version__"):
                f.write(f'__version__ = "{new_version}"\n')
            else:
                f.write(line)
    print(f"New version: {new_version}")
