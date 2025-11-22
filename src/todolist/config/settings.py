"""
Configuration management module.

This module handles loading and validating environment variables
from .env file for application configuration.
"""

import os
from typing import Optional
from dotenv import load_dotenv

class Settings:
    """Application configuration settings loaded from environment variables."""

    def __init__(self) -> None:
        """Initialize settings by loading environment variables."""
        # Load .env file from project root
        load_dotenv()

        # Phase 1 - In-Memory Configuration
        self.max_number_of_project: int = self._get_int_env(
            "MAX_NUMBER_OF_PROJECT", default=10
        )
        self.max_number_of_task: int = self._get_int_env(
            "MAX_NUMBER_OF_TASK", default=50
        )

        # Phase 2 - Database Configuration
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "postgresql://todolist_user:todolist_pass@localhost:5432/todolist_db"
        )
        self.DB_ECHO: bool = os.getenv("DB_ECHO", "False").lower() == "true"

        # Validate configuration
        self._validate()

    def _get_int_env(self, key: str, default: int) -> int:
        """
        Get integer value from environment variable.

        Args:
            key: Environment variable name
            default: Default value if not found or invalid

        Returns:
            Integer value from environment or default
        """
        value: Optional[str] = os.getenv(key)
        if value is None:
            return default

        try:
            return int(value)
        except ValueError:
            print(
                f"Warning: Invalid value for {key}='{value}'. "
                f"Using default: {default}"
            )
            return default

    def _validate(self) -> None:
        """
        Validate configuration values.

        Raises:
            ValueError: If configuration values are invalid
        """
        # Validate Phase 1 settings
        if self.max_number_of_project < 1:
            raise ValueError(
                f"MAX_NUMBER_OF_PROJECT must be >= 1, "
                f"got {self.max_number_of_project}"
            )

        if self.max_number_of_task < 1:
            raise ValueError(
                f"MAX_NUMBER_OF_TASK must be >= 1, "
                f"got {self.max_number_of_task}"
            )

        # Validate Phase 2 settings
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set")

        if not self.DATABASE_URL.startswith(("postgresql://", "sqlite://")):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://' or 'sqlite://'"
            )

    def __repr__(self) -> str:
        """Return string representation of settings."""
        # Hide password in DATABASE_URL for security
        safe_url = self.DATABASE_URL
        if "@" in safe_url:
            parts = safe_url.split("@")
            user_pass = parts[0].split("://")[1]
            if ":" in user_pass:
                user = user_pass.split(":")[0]
                safe_url = safe_url.replace(user_pass, f"{user}:****")

        return (
            f"Settings("
            f"max_number_of_project={self.max_number_of_project}, "
            f"max_number_of_task={self.max_number_of_task}, "
            f"DATABASE_URL='{safe_url}', "
            f"DB_ECHO={self.DB_ECHO})"
        )

# Global settings instance
settings = Settings()
