"""
Unit tests for Task model.
"""
import pytest
from src.todolist.models.task import Task, TaskStatus
from src.todolist.utils.exceptions import ValidationError


class TestTask:
    """Test Task model."""

    def test_task_creation_valid(self):
        """Test valid task creation."""
        task = Task(
            title="Test Task",
            description="Test description",
            project_id="project-123"
        )
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.project_id == "project-123"
        assert task.status == TaskStatus.TODO
        assert task.id is not None

    def test_task_creation_empty_title(self):
        """Test that empty title raises error."""
        with pytest.raises(ValidationError):
            Task(title="", description="Test", project_id="project-123")

    def test_task_creation_title_too_long(self):
        """Test that title longer than 30 chars raises error."""
        long_title = "a" * 31
        with pytest.raises(ValidationError):
            Task(title=long_title, description="Test", project_id="project-123")

    def test_task_creation_invalid_status(self):
        """Test that invalid status raises error."""
        with pytest.raises(ValidationError):
            Task(title="Test", project_id="project-123", status="INVALID")

    def test_update_status_valid(self):
        """Test updating task status to valid value."""
        task = Task(title="Test", description="Test", project_id="project-123")
        task.update_status(TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS

    def test_update_status_invalid(self):
        """Test updating task status to invalid value raises error."""
        task = Task(title="Test", description="Test", project_id="project-123")
        with pytest.raises(ValidationError):
            task.update_status("INVALID")

    def test_update_details(self):
        """Test updating task details."""
        task = Task(title="Original", description="Original desc", project_id="proj-1")
        task.update_details(title="Updated", description="Updated desc")
        assert task.title == "Updated"
        assert task.description == "Updated desc"

    def test_update_details_partial(self):
        """Test updating only some task details."""
        task = Task(title="Original", description="Original desc", project_id="proj-1")
        task.update_details(title="Updated")
        assert task.title == "Updated"
        assert task.description == "Original desc"

    def test_str_representation(self):
        """Test string representation of task."""
        task = Task(title="Test Task", description="Test desc", project_id="proj-1")
        str_repr = str(task)
        assert "Test Task" in str_repr
        assert "TODO" in str_repr
