from typing import Any
from pydantic import BaseModel, Field

class ErrorResponseSchema(BaseModel):
    code: str | None = Field(default=None, description="오류 코드")
    message: str | None = Field(default=None, description="오류 메시지")

class ResponseSchema(BaseModel):
    http_status_code: int = Field(default=200, description="HTTP STATUS CODE")
    result: Any = Field(default=None, description="success result")
    error: ErrorResponseSchema | None = Field(default=None, description="error infomation")


    

