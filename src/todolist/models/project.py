"""
Project domain model.

This module defines the Project entity representing a collection
of related tasks.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

from ..utils.validators import validate_non_empty_string


@dataclass
class Project:
    """
    Project entity representing a collection of related tasks.

    Attributes:
        id: Unique identifier (UUID)
        title: Project title
        description: Detailed description of the project
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """

    title: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate project data after initialization."""
        self._validate()

    def _validate(self) -> None:
        """
        Validate project attributes.

        Raises:
            ValidationError: If validation fails
        """
        validate_non_empty_string(self.title, "Project title", max_length=100)

        # Description can be empty, but if provided, must be string
        if self.description and not isinstance(self.description, str):
            from ..utils.exceptions import ValidationError

            raise ValidationError("Project description must be a string")

    def update_details(
        self, title: Optional[str] = None, description: Optional[str] = None
    ) -> None:
        """
        Update project details.

        Args:
            title: New title (optional)
            description: New description (optional)

        Raises:
            ValidationError: If validation fails
        """
        if title is not None:
            validate_non_empty_string(title, "Project title", max_length=100)
            self.title = title

        if description is not None:
            if not isinstance(description, str):
                from ..utils.exceptions import ValidationError

                raise ValidationError("Project description must be a string")
            self.description = description

        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """Return string representation of project."""
        return f"Project(id={self.id[:8]}..., title='{self.title}')"

    def __repr__(self) -> str:
        """Return detailed string representation of project."""
        return (
            f"Project(id='{self.id}', title='{self.title}', "
            f"description='{self.description[:30]}...', "
            f"created_at={self.created_at.isoformat()}, "
            f"updated_at={self.updated_at.isoformat()})"
        )
