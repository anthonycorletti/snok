from enum import Enum, unique

APP_NAME = "snok"
APP_DESC = "🚀 A simple, modern, full-stack toolkit for Python 🐍"


@unique
class ProjectType(str, Enum):
    package = "package"
    # app = "app" TODO: Add support
