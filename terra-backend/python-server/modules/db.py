from __future__ import annotations

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine


def make_session_factory(engine: Engine) -> type[Session]:
    """
    Create a SQLAlchemy session factory.

    Usage:
        SessionFactory = make_session_factory(engine)
        with SessionFactory() as session:
            ...
    """
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        future=True,   # safe with SQLAlchemy 1.4+, noop otherwise
    )
