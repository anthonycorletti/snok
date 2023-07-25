from enum import Enum, unique
from pathlib import Path
from typing import List

PARENT = Path(__file__).parent
STATIC_PATH = PARENT / "static"
TEMPLATES_PATH = PARENT / "templates"
ORIGINS: List = []
LOCAL_DOMAINS: List = ["localhost","127.0.0.1"]
EXTRA_ORIGINS = ["http://localhost", "http://127.0.0.1", "http://localhost:8000", "http://127.0.0.1:8000"]
API_V0 = "/api/v0"

@unique
class ENV(str, Enum):
    dev = "dev"
    test = "test"
    prod = "prod"
