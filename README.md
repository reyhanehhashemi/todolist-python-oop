# ToDoList - Python OOP (In-Memory) - Phase 1

A CLI-based ToDo List application built with Python using OOP principles.

## Phase 1 Features
- In-memory storage
- Project management (CRUD)
- Task management (CRUD)
- Status tracking
- Configuration via .env

## Technology Stack
- Python 3.9+
- Poetry (dependency management)
- Git (version control)

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Poetry

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/todolist-python-oop.git
cd todolist-python-oop

2. Install dependencies with Poetry:
bash
poetry install

3. Create environment configuration:
bash
cp .env.example .env

4. Run the application:
bash
poetry run python -m src.todolist.main

## Project Structure

todolist-python-oop/
├── src/todolist/        # Application source code
├── tests/               # Test files
├── .env.example         # Environment template
└── pyproject.toml       # Poetry configuration

## Development Workflow

- `main` branch: Stable, production-ready code
- `develop` branch: Integration branch for features
- Feature branches: Created from `develop` for new work

## License
This project is for educational purposes.


**File: `.env.example`**

```bash
# ToDoList Configuration
# Copy this file to .env and adjust values as needed

# Maximum number of projects allowed
MAX_NUMBER_OF_PROJECT=10

# Maximum number of tasks allowed per project
MAX_NUMBER_OF_TASK=50
