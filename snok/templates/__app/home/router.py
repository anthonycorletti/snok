from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from {{ __template_name }}.kit.routers import _APIRoute

views = Jinja2Templates(
    directory="views"
)

router = APIRouter(
    route_class=_APIRoute,
    tags=["home"]
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def _index(request: Request) -> Response:
    return views.TemplateResponse(
        name="index.html",
        context={"request": request},
    )


@router.get(
    "/404",
    response_class=HTMLResponse,
)
async def _not_found(request: Request) -> Response:
    return views.TemplateResponse(
        name="404.html",
        context={"request": request},
    )