"""
Database-backed project service for business logic.

This module provides high-level operations for project management
using database repositories.
"""

from typing import Optional
from sqlalchemy.orm import Session
from ..models.project import Project
from ..repositories.db_project_repository import DBProjectRepository
from ..repositories.db_task_repository import DBTaskRepository
from ..utils.exceptions import (
    ResourceNotFoundError,
    ValidationError,
    DuplicateResourceError,
)


class DBProjectService:
    """
    Service layer for project management with database persistence.

    This class provides business logic for creating, updating,
    and managing projects using PostgreSQL storage.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize project service with database session.

        Args:
            session: SQLAlchemy database session
        """
        self._project_repo = DBProjectRepository(session)
        self._task_repo = DBTaskRepository(session)
        self._session = session

    def create_project(
            self,
            title: str,
            description: str = "",
    ) -> Project:
        """
        Create a new project.

        Args:
            title: Project title (max 30 words)
            description: Project description (max 150 words, optional)

        Returns:
            Created project

        Raises:
            ValidationError: If validation fails
            DuplicateResourceError: If project with same title exists
            LimitExceededError: If project limit is reached
        """
        # Check for duplicate title
        if self._project_repo.exists_by_title(title):
            raise DuplicateResourceError("Project", title)

        # Create project entity (validation happens in __post_init__)
        project = Project(title=title, description=description)

        # Persist to database
        return self._project_repo.add(project)

    def get_project(self, project_id: int) -> Project:
        """
        Retrieve a project by ID.

        Args:
            project_id: Project identifier

        Returns:
            Project entity

        Raises:
            ResourceNotFoundError: If project not found
        """
        return self._project_repo.get_by_id(project_id)

    def get_project_by_title(self, title: str) -> Optional[Project]:
        """
        Retrieve a project by title.

        Args:
            title: Project title

        Returns:
            Project entity if found, None otherwise
        """
        return self._project_repo.get_by_title(title)

    def get_all_projects(self) -> list[Project]:
        """
        Retrieve all projects.

        Returns:
            List of all projects
        """
        return self._project_repo.get_all()

    def update_project(
            self,
            project_id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,
    ) -> Project:
        """
        Update project details.

        Args:
            project_id: Project identifier
            title: New title (optional, max 30 words)
            description: New description (optional, max 150 words)

        Returns:
            Updated project

        Raises:
            ResourceNotFoundError: If project not found
            ValidationError: If validation fails
            DuplicateResourceError: If new title conflicts with existing project
        """
        # Get existing project
        project = self._project_repo.get_by_id(project_id)

        # Check for title conflict if title is being changed
        if title is not None and title != project.title:
            if self._project_repo.exists_by_title(title):
                raise DuplicateResourceError("Project", title)

        # Update project (validation happens in update_details)
        project.update_details(title=title, description=description)

        # Persist changes
        return self._project_repo.update(project)

    def delete_project(self, project_id: int, cascade: bool = True) -> None:
        """
        Delete a project.

        Args:
            project_id: Project identifier
            cascade: If True, also delete all tasks in the project

        Raises:
            ResourceNotFoundError: If project not found
        """
        # Verify project exists
        self._project_repo.get_by_id(project_id)

        # Delete associated tasks if cascade is True
        if cascade:
            self._task_repo.delete_by_project_id(project_id)

        # Delete project
        self._project_repo.delete(project_id)

    def count_projects(self) -> int:
        """
        Get total project count.

        Returns:
            Number of projects
        """
        return self._project_repo.count()

    def project_exists(self, project_id: int) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: Project identifier

        Returns:
            True if project exists, False otherwise
        """
        return self._project_repo.exists(project_id)

    def commit(self) -> None:
        """Commit the current database transaction."""
        self._session.commit()

    def rollback(self) -> None:
        """Rollback the current database transaction."""
        self._session.rollback()
