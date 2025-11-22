# src/todolist/models/__init__.py
"""
Models package.

Contains both in-memory (Phase 1) and database (Phase 2) models.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all database models."""
    pass


# Phase 1 - In-memory models
from .task import Task, TaskStatus
from .project import Project

# Phase 2 - Database models
from .db_project import DBProject
from .db_task import DBTask, TaskStatus as DBTaskStatus

__all__ = [
    # Base
    'Base',
    # Phase 1
    'Task',
    'TaskStatus',
    'Project',
    # Phase 2
    'DBProject',
    'DBTask',
    'DBTaskStatus',
]
