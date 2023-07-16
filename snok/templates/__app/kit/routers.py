import json
from typing import Callable
from uuid import uuid4

from {{ __template_name }}._types import RequestLoggerMessage, ResponseLoggerMessage, Scope
from {{ __template_name }}.logger import log
from fastapi import Request, Response
from fastapi.routing import APIRoute


class _APIRoute(APIRoute):
    """_APIRoute.

    _APIRoute is a custom APIRoute class that adds a background task to the
    response to log request and response data.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def _log(
            req: RequestLoggerMessage,
            res: ResponseLoggerMessage,
        ) -> None:
            rid = {"rid": str(uuid4()).replace("-", "")}
            _res = {"res": json.loads(res.json())}
            _req = {"req": json.loads(req.json())}
            log.debug({**_res, **_req, **rid})

        async def custom_route_handler(request: Request) -> Response:
            body = await request.body() or None
            form = await request.form()
            params = request.query_params._dict
            req = RequestLoggerMessage(
                body=body,
                form=dict(form),
                params=params,
                scope=Scope(**dict(request.scope)),
            )
            response = await original_route_handler(request)
            res = ResponseLoggerMessage(
                status_code=response.status_code,
                raw_headers=response.raw_headers,
                body=response.body,
            )
            await _log(req=req, res=res)
            return response

        return custom_route_handler
