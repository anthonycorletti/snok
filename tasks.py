from enum import Enum, unique

from invoke import task
from invoke.context import Context

from python_project_template import __version__

PACKAGE_NAME = "python_project_template"
VERSION_FILE = f"{PACKAGE_NAME}/__init__.py"
SOURCES = " ".join(["python_project_template", "tests", "tasks.py"])


@task
def clean(ctx: Context) -> None:
    """clean

    Remove all build, test, coverage and Python artifacts.
    """
    ctx.run(
        " ".join(
            [
                "rm -rf",
                "build",
                "dist",
                "*.egg-info",
                ".pytest_cache",
                ".mypy_cache",
                ".coverage",
                "htmlcov",
                ".ruff_cache",
                "coverage.xml",
            ]
        ),
        pty=True,
        echo=True,
    )


@task
def install(ctx: Context) -> None:
    """install

    Install dependencies.
    """
    ctx.run(
        "pip install --upgrade pip",
        pty=True,
        echo=True,
    )
    ctx.run(
        "pip install -e '.[dev]'",
        pty=True,
        echo=True,
    )
    ctx.run(
        "pre-commit install",
        pty=True,
        echo=True,
    )
    ctx.run(
        "pre-commit autoupdate",
        pty=True,
        echo=True,
    )
    ctx.run(
        "if command -v pyenv 1>/dev/null 2>&1; then pyenv rehash; fi",
        pty=True,
        echo=True,
    )


@task
def lint(ctx: Context) -> None:
    """lint

    Check typing and formatting.
    """
    ctx.run(
        f"mypy {SOURCES}",
        pty=True,
        echo=True,
    )
    ctx.run(
        f"black {SOURCES} --check",
        pty=True,
        echo=True,
    )
    ctx.run(
        f"ruff {SOURCES}",
        pty=True,
        echo=True,
    )


@task
def format(ctx: Context) -> None:
    """format

    Format the code.
    """
    ctx.run(
        f"black {SOURCES}",
        pty=True,
        echo=True,
    )
    ctx.run(
        f"ruff {SOURCES} --fix",
        pty=True,
        echo=True,
    )


@task
def test(ctx: Context) -> None:
    """test

    Run the tests.
    """
    ctx.run(
        " ".join(
            [
                "pytest",
                "-o",
                "console_output_style=progress",
                "--disable-warnings",
                "--cov=python_project_template",
                "--cov=tests",
                "--cov-report=term-missing",
                "--cov-report=xml",
                "--cov-report=html",
                "--cov-fail-under=100",
            ]
        ),
        pty=True,
        echo=True,
    )


@task
def build(ctx: Context) -> None:
    """build

    Build the package.
    """
    ctx.run(
        "pip install --upgrade build",
        pty=True,
        echo=True,
    )
    ctx.run(
        "python -m build",
        pty=True,
        echo=True,
    )


@task
def publish(ctx: Context) -> None:
    """publish

    Publish the package.
    """
    ctx.run(
        "pip install --upgrade twine",
        pty=True,
        echo=True,
    )
    ctx.run(
        "twine upload dist/*",
        pty=True,
        echo=True,
    )


@task
def all(ctx: Context) -> None:
    """all

    Run all the tasks that matter for local dev.
    """
    clean(ctx)
    install(ctx)
    format(ctx)
    lint(ctx)
    test(ctx)


@unique
class BumpType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    MICRO = "micro"


def _bump_version(version: str, bump: BumpType) -> str:
    """Bump a version string.

    Args:
        version (str): The version string to bump.
        bump (str): The type of bump to perform.

    Returns:
        str: The bumped version string.
    """
    from packaging.version import Version

    v = Version(version)
    if bump == BumpType.MAJOR:
        v = Version(f"{v.major + 1}.0.0")
    elif bump == BumpType.MINOR:
        v = Version(f"{v.major}.{v.minor + 1}.0")
    elif bump == BumpType.MICRO:
        v = Version(f"{v.major}.{v.minor}.{v.micro + 1}")
    else:
        raise ValueError(f"Invalid bump type: {bump}")
    return str(v)


@task
def update_version_number(ctx: Context, part: BumpType = BumpType.MICRO) -> None:
    """update version number

    Specify the part of the version number to bump. The default is to bump the
    micro version number. Other options are major and minor.
    """
    print(f"Current version: {__version__}")
    new_version = _bump_version(__version__, part)
    with open(VERSION_FILE, "r") as f:
        lines = f.readlines()
    with open(VERSION_FILE, "w") as f:
        for line in lines:
            if line.startswith("__version__"):
                f.write(f'__version__ = "{new_version}"\n')
            else:
                f.write(line)
    print(f"New version: {new_version}")
