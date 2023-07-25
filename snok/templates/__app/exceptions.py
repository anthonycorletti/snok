from typing import Dict, Optional


class BaseException(Exception):
    """Base class for exceptions."""


exception_handlers: Optional[Dict] = {}
