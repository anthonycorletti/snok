import subprocess
from enum import Enum, unique

from invoke import task
from invoke.context import Context
from packaging.version import Version

from python_project_template import __version__

PACKAGE_NAME = "python_project_template"
VERSION_FILE = f"{PACKAGE_NAME}/__init__.py"


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


@task
def update_version_number_from_commit_message(ctx: Context) -> None:
    """update version number from commit message

    Specify the commit message to use to determine the part of the version
    number to bump. The commit message should be of the form:

        bumpversion: <major|minor|micro>

    """
    commit_msg = subprocess.check_output(
        ["git", "log", "--format=%B", "-n", "1", "HEAD"]
    ).decode("utf-8")
    if commit_msg.startswith("bumpversion: "):
        bump_type = commit_msg.split(": ")[1].strip()
        if bump_type == "major":
            update_version_number(ctx, BumpType.MAJOR)
        elif bump_type == "minor":
            update_version_number(ctx, BumpType.MINOR)
        elif bump_type == "micro":
            update_version_number(ctx, BumpType.MICRO)
    else:
        print(f"Commit message does not start with 'bumpversion:' - {commit_msg}")
