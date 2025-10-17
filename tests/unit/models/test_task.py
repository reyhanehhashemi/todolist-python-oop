"""
Unit tests for Task model.
"""

import pytest
from src.todolist.models.task import Task, TaskStatus
from src.todolist.utils.exceptions import ValidationError


class TestTask:
    """Test suite for Task model."""

    def test_task_creation_valid(self):
        """Test valid task creation."""
        task = Task(
            title="Test Task",
            description="Test description",
            project_id=1
        )
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.project_id == 1
        assert task.status == TaskStatus.TODO.value
        assert task.id > 0

    def test_task_creation_empty_title(self):
        """Test task creation with empty title raises error."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            Task(title="", description="Test", project_id=1)

    def test_task_creation_title_too_long(self):
        """Test task creation with too long title raises error."""
        long_title = "a" * 31
        with pytest.raises(ValidationError, match="cannot exceed 30"):
            Task(title=long_title, description="Test", project_id=1)

    def test_task_creation_invalid_status(self):
        """Test task creation with invalid status raises error."""
        with pytest.raises(ValidationError, match="must be one of"):
            Task(title="Test", description="Test", project_id=1, status="INVALID")

    def test_update_status_valid(self):
        """Test updating task status to valid value."""
        task = Task(title="Test", description="Test", project_id=1)
        task.update_status(TaskStatus.IN_PROGRESS.value)
        assert task.status == TaskStatus.IN_PROGRESS.value

    def test_update_status_invalid(self):
        """Test updating task status to invalid value raises error."""
        task = Task(title="Test", description="Test", project_id=1)
        with pytest.raises(ValidationError, match="must be one of"):
            task.update_status("INVALID_STATUS")

    def test_update_details(self):
        """Test updating task details."""
        task = Task(title="Original", description="Original desc", project_id=1)
        task.update_details(title="Updated", description="Updated desc")
        assert task.title == "Updated"
        assert task.description == "Updated desc"

    def test_update_details_partial(self):
        """Test updating only some task details."""
        task = Task(title="Original", description="Original desc", project_id=1)
        task.update_details(title="Updated")
        assert task.title == "Updated"
        assert task.description == "Original desc"

    def test_str_representation(self):
        """Test string representation of task."""
        task = Task(title="Test Task", description="Test desc", project_id=1)
        task_str = str(task)
        assert "Test Task" in task_str
        assert "TODO" in task_str
