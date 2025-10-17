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

        # Load configuration with default values
        self.max_number_of_project: int = self._get_int_env(
            "MAX_NUMBER_OF_PROJECT", default=10
        )
        self.max_number_of_task: int = self._get_int_env(
            "MAX_NUMBER_OF_TASK", default=50
        )

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

    def __repr__(self) -> str:
        """Return string representation of settings."""
        return (
            f"Settings("
            f"max_number_of_project={self.max_number_of_project}, "
            f"max_number_of_task={self.max_number_of_task})"
        )


# Global settings instance
settings = Settings()
