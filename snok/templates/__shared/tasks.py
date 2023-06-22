import json
from enum import Enum, unique
from typing import Any, Dict, Iterable, List, Optional
from urllib.request import urlopen

from invoke import task
from invoke.context import Context

PACKAGE_NAME = "{{ __template_name }}"
PYPROJECT_TOML_FILENAME = "pyproject.toml"
VERSION_FILE = f"{PACKAGE_NAME}/__init__.py"
SOURCES = " ".join(["{{ __template_name }}", "tests", "tasks.py"])


@unique
class DepencencyAction(str, Enum):
    add = "add"
    remove = "remove"


def _update_pyproject_toml(
    packages: List[str],
    dependency_action: DepencencyAction,
    dependency_group_name: Optional[str] = None,
) -> None:
    import toml
    from packaging.requirements import Requirement, SpecifierSet

    def _get_package_version_from_pypi(r: Requirement) -> SpecifierSet:
        with urlopen(f"https://pypi.org/pypi/{r.name}/json") as response:
            package_data = json.load(response)
            return SpecifierSet(f'>={package_data["info"]["version"]}')

    def _get_requirement(s: str) -> Requirement:
        return Requirement(s)

    def _requirement_has_version(r: Requirement) -> bool:
        return r.specifier is not None and r.specifier != ""

    def _get_full_requirement_spec(package: str) -> Requirement:
        r = _get_requirement(package)
        if not _requirement_has_version(r):
            r.specifier = _get_package_version_from_pypi(r)
        return r

    def _get_reqs_from_pyproject_toml(
        pyproject_toml: Dict,
        dependency_group_name: Optional[str] = None,
    ) -> Dict[str, Requirement]:
        project = pyproject_toml["project"]
        dep_list = project["dependencies"]
        if dependency_group_name:
            dep_list = project["optional-dependencies"][dependency_group_name]
        return {Requirement(d).name: Requirement(d) for d in dep_list}

    def _get_requested_reqs(packages: List[str]) -> Dict[str, Requirement]:
        result = dict()
        for package in packages:
            r = _get_full_requirement_spec(package=package)
            result[r.name] = r
        return result

    pyproject_toml = toml.load(PYPROJECT_TOML_FILENAME)

    current_deps = _get_reqs_from_pyproject_toml(
        pyproject_toml=pyproject_toml,
        dependency_group_name=dependency_group_name,
    )
    requested_deps = _get_requested_reqs(
        packages=packages,
    )

    result = dict()
    if dependency_action == DepencencyAction.add:
        # for all the add requests, check if the dependency is already installed
        # if the dependency is already installed, remove it from the current deps
        # add the requested dependency to the result
        # add the remaining current deps to the result
        # if there are no requested deps, then just re-install the current deps
        for name, requested_dep in requested_deps.items():
            if name in current_deps:
                current_deps.pop(name)
            result[name] = requested_dep
        result.update(current_deps)
    elif dependency_action == DepencencyAction.remove:
        # for all the remove requests, check if the dependency is already installed
        # if the dependency is installed, remove it from the current deps
        for name, current_dep in current_deps.items():
            if name not in requested_deps:
                result[name] = current_dep
    else:
        raise ValueError(
            f"Invalid dependency action: {dependency_action}. "
            f"Valid options are: {DepencencyAction.add}, "
            f"{DepencencyAction.remove}"
        )

    result_list = sorted([str(v) for v in result.values()])

    if dependency_group_name is not None:
        pyproject_toml["project"]["optional-dependencies"][
            dependency_group_name
        ] = result_list
    else:
        pyproject_toml["project"]["dependencies"] = result_list

    class TomlEncoder(toml.TomlEncoder):
        def __init__(self, _dict: type = dict, preserve: bool = False) -> None:
            super().__init__(_dict=_dict, preserve=preserve)
            self.dump_funcs[str] = self._dump_str

        def dump_list(self, v: Iterable[Any]) -> str:
            end = "\n"
            leading_space = " " * 4
            retval = f"[{end}"
            for u in v:
                retval += leading_space + str(self.dump_value(u)) + f",{end}"
            retval += "]"
            return retval

        def _dump_str(self, v: str) -> str:
            if v.startswith("/("):
                result = "'''\n" + v + "'''"
            else:
                result = toml.encoder._dump_str(v)  # type: ignore
            if result.startswith('"^') or result.endswith('$"'):
                result = "'" + result + "'"
                result = result.replace('"', "")
            return result.replace("\\\\", "\\")

    with open(PYPROJECT_TOML_FILENAME, "w") as f:
        toml.dump(pyproject_toml, f, encoder=TomlEncoder())


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
                "htmlcov",
                ".mypy_cache",
                ".pytest_cache",
                ".ruff_cache",
                "*.egg-info",
                "coverage.xml",
                ".coverage",
            ]
        ),
        pty=True,
        echo=True,
    )


@task(iterable=["dependency_groups"], aliases=["i"], optional=["dependency_groups"])
def install(ctx: Context, dependency_groups: Optional[List[str]] = None) -> None:
    """install

    Install dependencies.
    """
    if not dependency_groups:
        dependency_groups = ["dev"]
    ctx.run(
        "pip install --upgrade pip",
        pty=True,
        echo=True,
    )
    dep_install_str = "."
    if dependency_groups and dependency_groups != ["prod"]:
        dep_install_str += f"[{','.join(dependency_groups)}]"
    ctx.run(
        f"pip install -e '{dep_install_str}'",
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


@task(iterable=["packages"], post=[install], optional=["dependency_group_name"])
def add(
    ctx: Context, packages: List[str], dependency_group_name: Optional[str] = None
) -> None:
    """add

    Add dependencies.
    """
    _update_pyproject_toml(
        packages=packages,
        dependency_action=DepencencyAction.add,
        dependency_group_name=dependency_group_name,
    )


@task(iterable=["packages"], aliases=["rm"], optional=["dependency_group_name"])
def remove(
    ctx: Context, packages: List[str], dependency_group_name: Optional[str] = None
) -> None:
    """remove

    Remove dependencies.
    """
    _update_pyproject_toml(
        packages=packages,
        dependency_action=DepencencyAction.remove,
        dependency_group_name=dependency_group_name,
    )
    removals = " ".join(packages)
    print(f"Uninstalling {removals}...")
    ctx.run(
        f"pip uninstall -y {removals}",
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
        "pytest",
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


def _bump_version(version: str, bump: Optional[BumpType] = None) -> str:
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
    else:
        v = Version(f"{v.major}.{v.minor}.{v.micro + 1}")
    return str(v)


@task(aliases=["uv"])
def update_version_number(ctx: Context, part: Optional[BumpType] = None) -> None:
    """update version number

    Specify the part of the version number to bump. The default is to bump the
    micro version number. Other options are major and minor.
    """
    from {{ __template_name }} import __version__

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
