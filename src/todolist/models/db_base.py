"""
Database base configuration and session management.

This module provides the SQLAlchemy base class, engine,
and session factory for database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from ..config import settings


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,  # Verify connections before using
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_db() -> None:
    """
    Initialize database by creating all tables.

    This function creates all tables defined in models
    that inherit from Base.
    """
    # Import models to register them with Base
    from . import db_project, db_task  # noqa: F401

    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """
    Create and return a new database session.

    Returns:
        SQLAlchemy Session instance

    Note:
        Caller is responsible for closing the session.
    """
    return SessionLocal()


def drop_db() -> None:
    """
    Drop all database tables.

    Warning:
        This will delete all data! Use only for testing.
    """
    Base.metadata.drop_all(bind=engine)
