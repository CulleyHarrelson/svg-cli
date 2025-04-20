# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- Install: `pip install -e .` or `pip install -r requirements.txt`
- Lint: `ruff check .`
- Type check: `mypy .`
- Test: `pytest`
- Single test: `pytest tests/test_file.py::test_function`

## Code Style Guidelines
- **Formatting**: Use Black with default settings
- **Imports**: Group by standard library, third-party, then local modules
- **Types**: Use type annotations for all functions and classes
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Use try/except with specific exception types
- **CLI Structure**: Use Click for command structure and argument parsing
- **Environment**: Store credentials in .env file, load with python-dotenv
- **API Calls**: Handle rate limits and timeouts in Claude API calls
- **SVG Handling**: Document all SVG manipulations with clear comments
- **Documentation**: Use docstrings for all functions, classes, and modules