import traceback

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from keyfa.logmodule.logfactory import get_logger

logger = get_logger()
class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:            
            response = await call_next(request)
            dict_param = dict(
                query=request.query_params,
                path=request.path_params
            )
            try:
                form = request.form()
                dict_param["form"] = form(...)
            except Exception as ex:
                pass

            try:
                json = await request.json()
                dict_param["json"] = json
            except Exception as ex:
                pass

            logger.info(
                f"request :: {request.method} {request.url} | {dict_param} || response :: {response.status_code}"
            )
            
            return response

        except Exception as ex:
            raise ex
        
