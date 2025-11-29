"""
Auto-close overdue tasks command.
Designed to be run as a standalone script or cron job.
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_dir))


def setup_logging():
    """Configure logging to both console and file."""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure logging
    log_file = log_dir / "auto_close.log"

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('| [%(asctime)s] %(message)s |',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def auto_close_overdue_tasks():
    """
    Close all tasks that have passed their deadline.

    This function connects to the database and closes all tasks
    where deadline < now and status != CLOSED.

    Returns:
        int: Number of tasks closed
    """
    logger = setup_logging()

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

            # Log result
            logger.info(f"Auto-close completed: {closed_count} task(s) closed")

            return closed_count

        finally:
            session.close()
            engine.dispose()

    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        logger.error(error_msg)
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
