from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from keyfa.logmodule.logfactory import get_logger
from keyfa.exception.responseexception import ResponseException
from keyfa.exception.throw import throw
from keyfa.rdb.lifecycle import AsyncLifecycle

logger = get_logger()
class AdviceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:        
        print ("advicemiddleware dispatch")
        async_lifecycle = None
        try:            
            async_lifecycle = AsyncLifecycle()
            await async_lifecycle.start()

            response = await call_next(request)            
            dict_param = dict(
                query=request.query_params,
                path=request.path_params
            )
            try:
                form = await request.form()
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
        
        except ResponseException as re: # 사용자 정의 예외. > 400일때 던진다.
            return throw(re.error_code, re.message)

        except Exception as ex:
            return throw("GE-001", f"advice middleware exception :: {ex}")
        
        finally:
            if async_lifecycle is not None:
                await async_lifecycle.end()



