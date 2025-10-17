"""
Unit tests for Project model.
"""

import pytest
from src.todolist.models.project import Project
from src.todolist.utils.exceptions import ValidationError


class TestProject:
    """Test Project model functionality."""

    def test_project_creation_valid(self):
        """Test creating a valid project."""
        project = Project(title="Test Project", description="Test Description")

        assert project.title == "Test Project"
        assert project.description == "Test Description"
        assert project.id is not None
        assert project.created_at is not None
        assert project.updated_at is not None

    def test_project_creation_empty_title(self):
        """Test that empty title raises validation error."""
        with pytest.raises(ValidationError, match="Project title cannot be empty"):
            Project(title="")

    def test_project_creation_title_too_long(self):
        """Test that title exceeding max length raises error."""
        long_title = "x" * 101
        with pytest.raises(ValidationError, match="cannot exceed 100 characters"):
            Project(title=long_title)

    def test_project_creation_no_description(self):
        """Test creating project without description."""
        project = Project(title="Test Project")

        assert project.title == "Test Project"
        assert project.description == ""

    def test_update_details(self):
        """Test updating project details."""
        project = Project(title="Original", description="Original desc")

        project.update_details(title="Updated", description="Updated desc")

        assert project.title == "Updated"
        assert project.description == "Updated desc"

    def test_update_details_partial(self):
        """Test updating only title."""
        project = Project(title="Original", description="Original desc")

        project.update_details(title="New Title")

        assert project.title == "New Title"
        assert project.description == "Original desc"

    def test_str_representation(self):
        """Test string representation of project."""
        project = Project(title="Test Project")
        str_repr = str(project)

        assert "Test Project" in str_repr
