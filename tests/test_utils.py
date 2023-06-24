from packaging.requirements import Requirement

from snok.utils import _get_reqs_from_pyproject_toml


def test_get_reqs_from_pyproject_toml() -> None:
    pyproject_toml = {"project": {"dependencies": ["pendulum"]}}
    result = _get_reqs_from_pyproject_toml(
        pyproject_toml=pyproject_toml,
    )
    assert result == {"pendulum": Requirement("pendulum")}

    pyproject_toml_optional = {
        "project": {
            "dependencies": ["fastapi"],
            "optional-dependencies": {
                "dev": ["pendulum"],
            },
        },
    }
    result = _get_reqs_from_pyproject_toml(
        pyproject_toml=pyproject_toml_optional,
        dependency_group_name="dev",
    )
    assert result == {"pendulum": Requirement("pendulum")}
