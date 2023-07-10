from typing import Dict, Optional

from {{ __template_name }}.log import log
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse


class BaseException(Exception):
    """Base class for exceptions."""


async def not_found_error(request: Request, exc: HTTPException) -> RedirectResponse:
    """Handle 404 errors."""
    log.error(f"[404] request made to {request.url}")
    return RedirectResponse(url="/404")


exception_handlers: Optional[Dict] = {
    404: not_found_error,
}
