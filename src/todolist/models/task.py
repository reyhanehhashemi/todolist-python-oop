"""
Task domain model.

This module defines the Task entity representing a single task
within a project.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from ..utils.validators import validate_non_empty_string, validate_status


class TaskStatus(str, Enum):
    """Enumeration of valid task statuses."""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    @classmethod
    def values(cls) -> list[str]:
        """Return list of all valid status values."""
        return [status.value for status in cls]


@dataclass
class Task:
    """
    Task entity representing a single task within a project.

    Attributes:
        id: Unique identifier (UUID)
        title: Task title
        description: Detailed description of the task
        status: Current status (TODO, IN_PROGRESS, DONE)
        project_id: ID of the parent project
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """

    title: str
    project_id: str
    description: str = ""
    status: str = TaskStatus.TODO.value
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        self._validate()

    def _validate(self) -> None:
        """
        Validate task attributes.

        Raises:
            ValidationError: If validation fails
        """
        validate_non_empty_string(self.title, "Task title", max_length=100)
        validate_non_empty_string(self.project_id, "Project ID")
        validate_status(self.status, TaskStatus.values(), "Task status")

        # Description can be empty, but if provided, must be string
        if self.description and not isinstance(self.description, str):
            from ..utils.exceptions import ValidationError

            raise ValidationError("Task description must be a string")

    def update_status(self, new_status: str) -> None:
        """
        Update task status.

        Args:
            new_status: New status value

        Raises:
            ValidationError: If status is invalid
        """
        validate_status(new_status, TaskStatus.values(), "New status")
        self.status = new_status
        self.updated_at = datetime.now()

    def update_details(
        self, title: Optional[str] = None, description: Optional[str] = None
    ) -> None:
        """
        Update task details.

        Args:
            title: New title (optional)
            description: New description (optional)

        Raises:
            ValidationError: If validation fails
        """
        if title is not None:
            validate_non_empty_string(title, "Task title", max_length=100)
            self.title = title

        if description is not None:
            if not isinstance(description, str):
                from ..utils.exceptions import ValidationError

                raise ValidationError("Task description must be a string")
            self.description = description

        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """Return string representation of task."""
        return (
            f"Task(id={self.id[:8]}..., title='{self.title}', "
            f"status={self.status})"
        )

    def __repr__(self) -> str:
        """Return detailed string representation of task."""
        return (
            f"Task(id='{self.id}', title='{self.title}', "
            f"description='{self.description[:30]}...', "
            f"status='{self.status}', project_id='{self.project_id}', "
            f"created_at={self.created_at.isoformat()}, "
            f"updated_at={self.updated_at.isoformat()})"
        )
