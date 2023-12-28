from contextvars import ContextVar, Token
from typing import Union
from urllib.parse import quote

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import Update, Delete, Insert

from keyfa.config import Config

session_context: ContextVar[str] = ContextVar("session_context")



def get_async_session_context() -> str:
    return session_context.get()


def set_async_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_async_session_context(context: Token) -> None:
    session_context.reset(context)

database_url = Config.rdb.get_url()
engines = {
    "writer": create_async_engine(database_url, pool_recycle=36000, echo=Config.rdb.echo),
    "reader": create_async_engine(database_url, pool_recycle=36000, echo=Config.rdb.echo),
}

class RoutingSession(Session):
    def get_bind(self, clause=None):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        else:
            return engines["reader"].sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession, sync_session_class=RoutingSession,
)

async_session: Union[Session, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_async_session_context,
)

Base = declarative_base()