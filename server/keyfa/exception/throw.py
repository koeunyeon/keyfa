import traceback
from starlette.responses import JSONResponse

from keyfa.schema.baseresponseschema import ResponseSchema, ErrorResponseSchema
from keyfa.logmodule.logfactory import get_logger

logger = get_logger()

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