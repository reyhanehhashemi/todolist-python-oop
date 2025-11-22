"""
Database repository for Project entities.

This module provides database-backed storage and retrieval operations
for Project entities using SQLAlchemy.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.db_project import DBProject
from ..models.project import Project
from ..utils.exceptions import (
    ResourceNotFoundError,
    LimitExceededError,
    DuplicateResourceError,
)
from ..config import settings


class DBProjectRepository:
    """
    Database repository for managing Project entities.

    This class provides CRUD operations for projects using PostgreSQL.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy database session
        """
        self._session = session

    def add(self, project: Project) -> Project:
        """
        Add a new project to the database.

        Args:
            project: Project entity to add

        Returns:
            The added project with database ID

        Raises:
            LimitExceededError: If maximum project limit is reached
            DuplicateResourceError: If project with same title exists
        """
        # Check limit
        if self.count() >= settings.max_number_of_project:
            raise LimitExceededError("Project", settings.max_number_of_project)

        # Convert to DB model
        db_project = DBProject(
            title=project.title,
            description=project.description,
        )

        try:
            self._session.add(db_project)
            self._session.flush()  # Get ID without committing

            # Update domain model with DB ID
            project.id = db_project.id
            return project

        except IntegrityError:
            self._session.rollback()
            raise DuplicateResourceError("Project", project.title)

    def get_by_id(self, project_id: int) -> Project:
        """
        Retrieve a project by its ID.

        Args:
            project_id: Project identifier

        Returns:
            Project entity

        Raises:
            ResourceNotFoundError: If project is not found
        """
        db_project = self._session.get(DBProject, project_id)
        if db_project is None:
            raise ResourceNotFoundError("Project", str(project_id))

        return self._to_domain(db_project)

    def get_by_title(self, title: str) -> Optional[Project]:
        """
        Retrieve a project by its title.

        Args:
            title: Project title

        Returns:
            Project entity if found, None otherwise
        """
        db_project = (
            self._session.query(DBProject)
            .filter(DBProject.title == title)
            .first()
        )

        return self._to_domain(db_project) if db_project else None

    def get_all(self) -> list[Project]:
        """
        Retrieve all projects.

        Returns:
            List of all projects
        """
        db_projects = self._session.query(DBProject).all()
        return [self._to_domain(p) for p in db_projects]

    def update(self, project: Project) -> Project:
        """
        Update an existing project.

        Args:
            project: Project entity with updated data

        Returns:
            Updated project

        Raises:
            ResourceNotFoundError: If project is not found
            DuplicateResourceError: If new title conflicts
        """
        db_project = self._session.get(DBProject, project.id)
        if db_project is None:
            raise ResourceNotFoundError("Project", str(project.id))

        # Update fields
        db_project.title = project.title
        db_project.description = project.description

        try:
            self._session.flush()
            return project

        except IntegrityError:
            self._session.rollback()
            raise DuplicateResourceError("Project", project.title)

    def delete(self, project_id: int) -> None:
        """
        Delete a project by its ID.

        Args:
            project_id: Project identifier

        Raises:
            ResourceNotFoundError: If project is not found
        """
        db_project = self._session.get(DBProject, project_id)
        if db_project is None:
            raise ResourceNotFoundError("Project", str(project_id))

        self._session.delete(db_project)
        self._session.flush()

    def count(self) -> int:
        """
        Get total count of projects.

        Returns:
            Number of projects in database
        """
        return self._session.query(DBProject).count()

    def exists(self, project_id: int) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: Project identifier

        Returns:
            True if project exists, False otherwise
        """
        return self._session.query(DBProject.id).filter(
            DBProject.id == project_id
        ).first() is not None

    def exists_by_title(self, title: str) -> bool:
        """
        Check if a project with given title exists.

        Args:
            title: Project title

        Returns:
            True if project exists, False otherwise
        """
        return self._session.query(DBProject.id).filter(
            DBProject.title == title
        ).first() is not None

    def _to_domain(self, db_project: DBProject) -> Project:
        """
        Convert database model to domain model.

        Args:
            db_project: Database project entity

        Returns:
            Domain project entity
        """
        project = Project(
            title=db_project.title,
            description=db_project.description,
        )
        project.id = db_project.id
        project.created_at = db_project.created_at
        project.updated_at = db_project.updated_at
        return project
