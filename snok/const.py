from enum import Enum, unique

APP_NAME = "snok"
APP_DESC = "🚀 A simple, modern, full-stack toolkit for Python 🐍"
PYPROJECT_TOML_FILENAME = "pyproject.toml"


@unique
class ProjectType(str, Enum):
    package = "package"
    # app = "app" TODO: Add support


@unique
class DepencencyAction(str, Enum):
    add = "add"
    remove = "remove"


@unique
class BumpType(Enum):
    MAJOR = "major"
    MINOR = "minor"
