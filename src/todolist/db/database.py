"""
Database connection and session management.

This module handles SQLAlchemy engine creation and session management.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from ..config.settings import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10,
)


# Enable foreign key constraints for SQLite (if needed in future)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable foreign key constraints for SQLite."""
    if 'sqlite' in str(dbapi_conn):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """
    Create a new database session.

    Returns:
        SQLAlchemy Session instance

    Note:
        Caller is responsible for closing the session.
    """
    return SessionLocal()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Yields:
        SQLAlchemy Session instance

    Example:
        with get_db_context() as db:
            db.add(project)
            db.commit()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.

    Note:
        This creates all tables defined in models.
        In production, use Alembic migrations instead.
    """
    from ..models import Base
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Drop all database tables.

    Warning:
        This will delete all data! Use only in development/testing.
    """
    from ..models import Base
    Base.metadata.drop_all(bind=engine)
