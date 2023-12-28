from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from keyfa.rdb.lifecycle import AsyncLifecycle

class RdbMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint,
    ):
        async_lifecycle = AsyncLifecycle()
        await async_lifecycle.start()

        try:
            response = await call_next(request)
        except Exception as e:
            raise e
        finally:
            await async_lifecycle.end()

        return response