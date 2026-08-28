# Contributing to DocBot

Thank you for your interest in contributing! Here is how to get started.

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install flake8 pytest
   ```
4. Copy `.env.example` to `.env` and fill in your credentials

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

- Follow PEP 8
- Max line length: 100 characters
- Add docstrings to all public functions and classes
- Use type hints wherever possible

## Submitting a Pull Request

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make your changes with clear, descriptive commits
3. Add or update tests for your changes
4. Run the test suite and ensure it passes
5. Push and open a Pull Request against `main`

## Commit Message Format

Use conventional commits:

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` adding or updating tests
- `chore:` maintenance tasks
- `ci:` CI/CD changes

## Reporting Issues

Open a GitHub Issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your Python version and OS
