"""
End-to-end integration tests.
"""

import pytest
from src.todolist.repositories.project_repository import ProjectRepository
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.services.project_service import ProjectService
from src.todolist.services.task_service import TaskService
from src.todolist.models.task import TaskStatus


class TestEndToEnd:
    """Test complete user workflows."""

    @pytest.fixture
    def setup_services(self):
        """Setup complete service stack."""
        project_repo = ProjectRepository()
        task_repo = TaskRepository()
        project_service = ProjectService(project_repo, task_repo)
        task_service = TaskService(task_repo)

        return project_service, task_service

    def test_complete_workflow(self, setup_services):
        """Test complete user workflow from project creation to deletion."""
        project_service, task_service = setup_services

        # 1. Create project
        project = project_service.create_project(
            "My Project", "Test project description"
        )
        assert project.title == "My Project"

        # 2. Create tasks
        task1 = task_service.create_task("Task 1", project.id, "First task")
        task2 = task_service.create_task("Task 2", project.id, "Second task")

        # 3. Verify tasks in project
        tasks = task_service.get_tasks_by_project(project.id)
        assert len(tasks) == 2

        # 4. Update task status
        task_service.update_task_status(task1.id, TaskStatus.IN_PROGRESS.value)

        # 5. Get project summary
        summary = project_service.get_project_summary(project.id)
        assert summary["total_tasks"] == 2
        assert summary["status_breakdown"][TaskStatus.IN_PROGRESS.value] == 1
        assert summary["status_breakdown"][TaskStatus.TODO.value] == 1

        # 6. Update task details
        updated_task = task_service.update_task(
            task1.id, title="Updated Task 1", description="Updated description"
        )
        assert updated_task.title == "Updated Task 1"

        # 7. Complete a task
        task_service.update_task_status(task1.id, TaskStatus.DONE.value)
        completed_tasks = task_service.get_tasks_by_status(TaskStatus.DONE.value)
        assert len(completed_tasks) == 1

        # 8. Delete project with cascade
        result = project_service.delete_project(project.id, cascade=True)
        assert result["deleted_tasks"] == 2

        # 9. Verify everything is deleted
        assert project_service.count_projects() == 0
        assert task_service.count_tasks() == 0

    def test_multiple_projects_workflow(self, setup_services):
        """Test managing multiple projects."""
        project_service, task_service = setup_services

        # Create multiple projects
        project1 = project_service.create_project("Work", "Work tasks")
        project2 = project_service.create_project("Personal", "Personal tasks")

        # Create tasks in different projects
        task_service.create_task("Work Task 1", project1.id)
        task_service.create_task("Work Task 2", project1.id)
        task_service.create_task("Personal Task 1", project2.id)

        # Verify task distribution
        work_tasks = task_service.get_tasks_by_project(project1.id)
        personal_tasks = task_service.get_tasks_by_project(project2.id)

        assert len(work_tasks) == 2
        assert len(personal_tasks) == 1

        # Delete one project
        project_service.delete_project(project1.id, cascade=True)

        # Verify only project2 tasks remain
        assert task_service.count_tasks() == 1
        assert project_service.count_projects() == 1
