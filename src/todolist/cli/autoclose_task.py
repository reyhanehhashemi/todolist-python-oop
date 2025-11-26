"""
Auto-close overdue tasks command.
Designed to be run as a standalone script or cron job.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_dir))


def auto_close_overdue_tasks():
    """
    Close all tasks that have passed their deadline.

    This function connects to the database and closes all tasks
    where deadline < now and status != CLOSED.

    Returns:
        int: Number of tasks closed
    """
    try:
        # Import inside function to avoid circular import issues
        from ..config.settings import settings
        from ..services.db_task_service import DBTaskService
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        # Create database engine
        engine = create_engine(
            settings.DATABASE_URL,
            echo=False  # Disable SQL logging for cron jobs
        )

        # Create session
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        try:
            # Create service and run auto-close
            task_service = DBTaskService(session)
            closed_count = task_service.auto_close_overdue_tasks()

            # Log result with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Auto-close completed: {closed_count} task(s) closed")

            return closed_count

        finally:
            session.close()
            engine.dispose()

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"[{timestamp}] ERROR: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise


def main():
    """Entry point for command-line execution."""
    try:
        closed_count = auto_close_overdue_tasks()
        sys.exit(0)  # Success
    except Exception:
        sys.exit(1)  # Failure


if __name__ == "__main__":
    main()
