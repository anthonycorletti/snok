from enum import Enum, unique

APP_NAME = "snok"
APP_DESC = "🚀 A simple, modern, full-stack toolkit for Python 🐍"
PYPROJECT_TOML_FILENAME = "pyproject.toml"
BASE_APP_PACKAGES = [
    "alembic",
    "asyncpg",
    "fastapi",
    "greenlet",
    "httpx",
    "itsdangerous",
    "jinja2",
    "python-dateutil",
    "python-dotenv",
    "python-multipart",
    "rich",
    "sqlmodel",
    "structlog",
    "uvicorn",
]

BASE_APP_DEV_PACKAGES = [
    "asgi-lifespan",
    "coverage",
    "pytest-asyncio",
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
    view = "view"
    scaffold = "scaffold"
