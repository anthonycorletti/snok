import os
from typing import Any, Dict, Iterable, List, Optional

import httpx
import toml
from invoke import Context
from packaging.requirements import Requirement, SpecifierSet
from typer import Exit

from snok.const import PYPROJECT_TOML_FILENAME, BumpType, DepencencyAction


def _get_default_output_dir() -> str:
    """Returns the default output directory of the project."""
    return os.path.dirname(os.getenv("VIRTUAL_ENV", os.getcwd()))


def _get_snok_path() -> str:
    """Returns the path to the snok package."""
    return os.path.dirname(os.path.abspath(__file__))


def _run_cmd(
    cmd: List[str],
    pty: bool = True,
    echo: bool = True,
) -> None:  # pragma: no cover
    ctx = Context()
    try:
        ctx.run(
            " ".join(cmd),
            pty=pty,
            echo=echo,
        )
    except Exception:
        raise Exit(1)


def _get_package_version_from_pypi(r: Requirement) -> SpecifierSet:  # pragma: no cover
    response = httpx.get(f"https://pypi.org/pypi/{r.name}/json")
    return SpecifierSet(f'>={response.json()["info"]["version"]}')


def _get_requirement(s: str) -> Requirement:  # pragma: no cover
    return Requirement(s)


def _requirement_has_version(r: Requirement) -> bool:  # pragma: no cover
    return r.specifier is not None and r.specifier != ""


def _get_full_requirement_spec(package: str) -> Requirement:  # pragma: no cover
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


def _get_requested_reqs(
    packages: List[str],
) -> Dict[str, Requirement]:  # pragma: no cover
    result = dict()
    for package in packages:
        r = _get_full_requirement_spec(package=package)
        result[r.name] = r
    return result


class TomlEncoder(toml.TomlEncoder):  # pragma: no cover
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


def _update_pyproject_toml(
    packages: List[str],
    dependency_action: DepencencyAction,
    dependency_group_name: Optional[str] = None,
) -> None:  # pragma: no cover
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

    with open(PYPROJECT_TOML_FILENAME, "w") as f:
        toml.dump(pyproject_toml, f, encoder=TomlEncoder())


def _snok_sources() -> List[str]:  # pragma: no cover
    """Returns the list of sources to lint with mypy, black,
    and ruff from pyproject.toml."""
    pyproject_toml = toml.load(PYPROJECT_TOML_FILENAME)
    return pyproject_toml["tool"]["snok"]["sources"]


def _get_project_name() -> str:  # pragma: no cover
    pyproject_toml = toml.load(PYPROJECT_TOML_FILENAME)
    return pyproject_toml["project"]["name"]


def _bump_version_string(
    version: str, bump: Optional[BumpType] = None
) -> str:  # pragma: no cover
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


def _install_node_module_requirements() -> None:  # pragma: no cover
    _run_cmd(
        [
            "npm",
            "install",
            "-D",
            "tailwindcss",
            "@tailwindcss/forms",
            "prettier",
        ]
    )
