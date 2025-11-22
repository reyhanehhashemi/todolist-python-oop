"""
Database repository for Task entities.

This module provides database-backed storage and retrieval operations
for Task entities using SQLAlchemy.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.db_task import DBTask
from ..models.task import Task, TaskStatus
from ..utils.exceptions import (
    ResourceNotFoundError,
    LimitExceededError,
)
from ..config import settings


class DBTaskRepository:
    """
    Database repository for managing Task entities.

    This class provides CRUD operations for tasks using PostgreSQL.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy database session
        """
        self._session = session

    def add(self, task: Task) -> Task:
        """
        Add a new task to the database.

        Args:
            task: Task entity to add

        Returns:
            The added task with database ID

        Raises:
            LimitExceededError: If maximum task limit is reached
        """
        # Check limit
        if self.count() >= settings.max_number_of_task:
            raise LimitExceededError("Task", settings.max_number_of_task)

        # Convert to DB model
        db_task = DBTask(
            title=task.title,
            description=task.description,
            status=task.status,
            project_id=task.project_id,
            deadline=task.deadline,
        )

        self._session.add(db_task)
        self._session.flush()

        # Update domain model with DB ID
        task.id = db_task.id
        return task

    def get_by_id(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Task identifier

        Returns:
            Task entity

        Raises:
            ResourceNotFoundError: If task is not found
        """
        db_task = self._session.get(DBTask, task_id)
        if db_task is None:
            raise ResourceNotFoundError("Task", str(task_id))

        return self._to_domain(db_task)

    def get_by_project_id(self, project_id: int) -> list[Task]:
        """
        Retrieve all tasks for a specific project.

        Args:
            project_id: Project identifier

        Returns:
            List of tasks in the project
        """
        db_tasks = (
            self._session.query(DBTask)
            .filter(DBTask.project_id == project_id)
            .all()
        )
        return [self._to_domain(t) for t in db_tasks]

    def get_all(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        db_tasks = self._session.query(DBTask).all()
        return [self._to_domain(t) for t in db_tasks]

    def update(self, task: Task) -> Task:
        """
        Update an existing task.

        Args:
            task: Task entity with updated data

        Returns:
            Updated task

        Raises:
            ResourceNotFoundError: If task is not found
        """
        db_task = self._session.get(DBTask, task.id)
        if db_task is None:
            raise ResourceNotFoundError("Task", str(task.id))

        # Update fields
        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status
        db_task.deadline = task.deadline

        self._session.flush()
        return task

    def delete(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: Task identifier

        Raises:
            ResourceNotFoundError: If task is not found
        """
        db_task = self._session.get(DBTask, task_id)
        if db_task is None:
            raise ResourceNotFoundError("Task", str(task_id))

        self._session.delete(db_task)
        self._session.flush()

    def delete_by_project_id(self, project_id: int) -> int:
        """
        Delete all tasks in a project.

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks deleted
        """
        deleted_count = (
            self._session.query(DBTask)
            .filter(DBTask.project_id == project_id)
            .delete()
        )
        self._session.flush()
        return deleted_count

    def count(self) -> int:
        """
        Get total count of tasks.

        Returns:
            Number of tasks in database
        """
        return self._session.query(DBTask).count()

    def count_by_project_id(self, project_id: int) -> int:
        """
        Get count of tasks in a specific project.

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks in the project
        """
        return (
            self._session.query(DBTask)
            .filter(DBTask.project_id == project_id)
            .count()
        )

    def exists(self, task_id: int) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: Task identifier

        Returns:
            True if task exists, False otherwise
        """
        return (
            self._session.query(DBTask.id)
            .filter(DBTask.id == task_id)
            .first()
            is not None
        )

    def _to_domain(self, db_task: DBTask) -> Task:
        """
        Convert database model to domain model.

        Args:
            db_task: Database task entity

        Returns:
            Domain task entity
        """
        task = Task(
            title=db_task.title,
            description=db_task.description,
            status=db_task.status,
            project_id=db_task.project_id,
            deadline=db_task.deadline,
        )
        task.id = db_task.id
        task.created_at = db_task.created_at
        task.updated_at = db_task.updated_at
        return task
