from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager

from keyfa.config import Config
from keyfa.util.importutil import import_keyfa

from keyfa.util.logutil import get_logger, logging

def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        # on startup
        get_logger()
        get_logger("uvicorn.access", log_level=logging.INFO)
        get_logger("uvicorn.error", log_level=logging.INFO)    
        get_logger("uvicorn.error", log_level=logging.INFO)
        get_logger("uvicorn.default", log_level=logging.INFO)
        
        yield

        # on shutdown

    app = FastAPI(title="keyfa", lifespan=lifespan)
    import_keyfa(app)
    return app

def run_app():
    uvicorn.run(
        app="__main__:app",
        #app=app,
        host = Config.server.host,
        port = Config.server.port,
        reload=Config.server.reload,
        ssl_certfile=Config.server.ssl_certfile,
        ssl_keyfile=Config.server.ssl_keyfile,
        ssl_keyfile_password=Config.server.ssl_keypass
    )