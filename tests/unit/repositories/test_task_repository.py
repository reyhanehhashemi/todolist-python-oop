"""
Unit tests for TaskRepository.
"""

import pytest
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.models.task import Task
from src.todolist.utils.exceptions import ResourceNotFoundError, LimitExceededError
from src.todolist.config import settings


class TestTaskRepository:
    """Test TaskRepository functionality."""

    def test_add_task(self, task_repo, sample_task):
        """Test adding a task to repository."""
        added_task = task_repo.add(sample_task)

        assert added_task.id == sample_task.id
        assert task_repo.count() == 1

    def test_get_by_id_exists(self, task_repo, sample_task):
        """Test retrieving existing task by ID."""
        task_repo.add(sample_task)
        retrieved = task_repo.get_by_id(sample_task.id)

        assert retrieved.id == sample_task.id
        assert retrieved.title == sample_task.title

    def test_get_by_id_not_exists(self, task_repo):
        """Test retrieving non-existent task raises error."""
        with pytest.raises(ResourceNotFoundError):
            task_repo.get_by_id("non-existent-id")

    def test_get_all_empty(self, task_repo):
        """Test getting all tasks from empty repository."""
        tasks = task_repo.get_all()

        assert tasks == []

    def test_get_all_multiple(self, task_repo, sample_project):
        """Test getting all tasks."""
        task1 = Task(title="Task 1", project_id=sample_project.id)
        task2 = Task(title="Task 2", project_id=sample_project.id)

        task_repo.add(task1)
        task_repo.add(task2)

        tasks = task_repo.get_all()

        assert len(tasks) == 2

    def test_get_by_project_id(self, task_repo, sample_project):
        """Test getting tasks by project ID."""
        project_id = sample_project.id
        task1 = Task(title="Task 1", project_id=project_id)
        task2 = Task(title="Task 2", project_id=project_id)
        task3 = Task(title="Task 3", project_id="other-project")

        task_repo.add(task1)
        task_repo.add(task2)
        task_repo.add(task3)

        tasks = task_repo.get_by_project_id(project_id)

        assert len(tasks) == 2
        assert all(t.project_id == project_id for t in tasks)

    def test_update_task(self, task_repo, sample_task):
        """Test updating a task."""
        task_repo.add(sample_task)
        sample_task.title = "Updated Title"

        updated = task_repo.update(sample_task)

        assert updated.title == "Updated Title"

    def test_update_non_existent(self, task_repo, sample_task):
        """Test updating non-existent task raises error."""
        with pytest.raises(ResourceNotFoundError):
            task_repo.update(sample_task)

    def test_delete_task(self, task_repo, sample_task):
        """Test deleting a task."""
        task_repo.add(sample_task)
        task_repo.delete(sample_task.id)

        assert task_repo.count() == 0

    def test_delete_non_existent(self, task_repo):
        """Test deleting non-existent task raises error."""
        with pytest.raises(ResourceNotFoundError):
            task_repo.delete("non-existent-id")

    def test_delete_by_project_id(self, task_repo, sample_project):
        """Test cascade delete by project ID."""
        project_id = sample_project.id
        task1 = Task(title="Task 1", project_id=project_id)
        task2 = Task(title="Task 2", project_id=project_id)
        task3 = Task(title="Task 3", project_id="other-project")

        task_repo.add(task1)
        task_repo.add(task2)
        task_repo.add(task3)

        deleted_count = task_repo.delete_by_project_id(project_id)

        assert deleted_count == 2
        assert task_repo.count() == 1

    def test_count(self, task_repo, sample_project):
        """Test counting tasks."""
        assert task_repo.count() == 0

        task_repo.add(Task(title="Task 1", project_id=sample_project.id))
        assert task_repo.count() == 1

        task_repo.add(Task(title="Task 2", project_id=sample_project.id))
        assert task_repo.count() == 2

    def test_exists(self, task_repo, sample_task):
        """Test checking task existence."""
        assert not task_repo.exists(sample_task.id)

        task_repo.add(sample_task)
        assert task_repo.exists(sample_task.id)

    def test_clear(self, task_repo, sample_task):
        """Test clearing all tasks."""
        task_repo.add(sample_task)
        task_repo.clear()

        assert task_repo.count() == 0
