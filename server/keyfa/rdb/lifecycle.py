from uuid import uuid4
from keyfa.rdb.asyncsession import set_async_session_context, async_session, reset_async_session_context

from functools import wraps

class AsyncLifecycle:
    _context = None
    async def start(self):
        session_id = str(uuid4())
        self._context = set_async_session_context(session_id=session_id)
    
    async def end(self):
        await async_session.remove()
        reset_async_session_context(context=self._context)

def rdb_async_lifecycle(func):
    """
    rdb lifecycle 제어
    일반적으로 미들웨어에서 하지만, 혹시 다른 스코프가 필요할 때 데코레이터로 사용하면 됨.
    @rdb_async_lifecycle
    """
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            async_lifecycle = AsyncLifecycle()
            await async_lifecycle.start()

            result = await func(*args, **kwargs)
            await async_lifecycle.end()
        except Exception as e:                
            raise e
        return result
    return decorator