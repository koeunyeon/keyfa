import traceback
import json

from fastapi import Request, Response
from starlette.responses import JSONResponse
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from keyfa.logmodule.logfactory import get_logger
from keyfa.schema.baseresponseschema import ResponseSchema, ErrorResponseSchema
from keyfa.exception.responseexception import ResponseException

logger = get_logger()
class ResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
    
    def throw(self, code, message):
        trace = traceback.format_exc()
        log_message = f"{message} | {trace}"
        logger.exception(log_message)

        
        return JSONResponse(
            content=ResponseSchema(
                http_status_code=500,
                error=ErrorResponseSchema(
                    code=code,
                    message=message
                )
            ).model_dump_json(),
            status_code=500
        )


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:        
        try:
            print ("dispatch")
            response = await call_next(request)

            if response.headers.get("content-type") != "application/json":
                return response

            # only json patch
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            content = response_body.decode()
            content = json.loads(content)

            print (content)
            
            ret = ResponseSchema(
                http_status_code=response.status_code,
                result = content
            ).model_dump_json()

            print ("ret", ret)
            
            ret = json.loads(ret)
            print ("ret 2", ret)
            
            #response.headers["content-length"] = str(len(ret))
            return JSONResponse(
                content = ret,
                status_code=response.status_code
            )
            
            return Response(
                content = ret, 
                status_code = response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

            return ret
            #return response
        except ResponseException as re:
            return self.throw(re.error_code, re.message)

        except Exception as ex:
            return self.throw("GE-001", f"global exception :: {ex}")



