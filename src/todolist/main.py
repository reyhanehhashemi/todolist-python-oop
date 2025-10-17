"""
Main entry point for the ToDo List application.

This module initializes all components and starts the CLI interface.
"""

from .repositories.project_repository import ProjectRepository
from .repositories.task_repository import TaskRepository
from .services.project_service import ProjectService
from .services.task_service import TaskService
from .cli.commands import CLI
from .config import settings


def main() -> None:
    """
    Main function to start the application.

    Initializes repositories, services, and CLI, then starts
    the interactive interface.
    """
    # Display configuration
    print("=" * 50)
    print("ToDo List Application - Phase 1")
    print("=" * 50)
    print("\nConfiguration:")
    print(f"  Max Projects: {settings.max_number_of_project}")
    print(f"  Max Tasks: {settings.max_number_of_task}")

    # Initialize repositories
    project_repo = ProjectRepository()
    task_repo = TaskRepository()

    # Initialize services
    project_service = ProjectService(project_repo, task_repo)
    task_service = TaskService(task_repo)

    # Initialize and run CLI
    cli = CLI(project_service, task_service)

    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
