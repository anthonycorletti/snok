from enum import Enum, unique

APP_NAME = "snok"
APP_DESC = "🚀 A simple, modern, full-stack toolkit for Python 🐍"
PYPROJECT_TOML_FILENAME = "pyproject.toml"
BASE_DEPS = [
    "alembic",
    "asyncpg",
    "fastapi<0.100.0",  # TODO: due to sqlmodel
    "httpx",
    "itsdangerous",
    "jinja2",
    "modal",
    "pydantic<2.0.0",  # TODO: due to sqlmodel
    "python-dateutil",
    "python-dotenv",
    "python-multipart",
    "rich",
    "sqlmodel",
    "structlog",
    "uvicorn",
]

BASE_DEV_DEPS = [
    "asgi-lifespan",
    "black",
    "coverage",
    "greenlet",
    "invoke",
    "mypy",
    "pre-commit",
    "pytest-asyncio",
    "pytest-cov",
    "pytest-xdist",
    "pytest",
    "ruff",
    "watchfiles",
]


@unique
class ProjectType(str, Enum):
    package = "package"
    app = "app"


@unique
class DepencencyAction(str, Enum):
    add = "add"
    remove = "remove"


@unique
class BumpType(Enum):
    MAJOR = "major"
    MINOR = "minor"


@unique
class ContentType(str, Enum):
    model = "model"
    router = "router"
    # TODO: Add support for htmx and tailwind
    # view = "view"
    scaffold = "scaffold"


@unique
class DatabaseCommand(str, Enum):
    migrate = "migrate"
    upgrade = "upgrade"
    downgrade = "downgrade"
    revision = "revision"


@unique
class DeploymentPlatform(str, Enum):
    modal = "modal"
