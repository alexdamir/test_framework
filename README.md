# Test Framework

BDD Test Framework using Python, Playwright, Behave, and Poetry.

## Setup

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Install dependencies: `poetry install`
3. Install Playwright browsers: `poetry run playwright install`

## Running Tests

```bash
# Run all BDD tests
poetry run behave

# Run specific feature
poetry run behave features/login.feature

# Run with specific browser
BROWSER=firefox poetry run behave

# Run in headless mode
HEADLESS=true poetry run behave

# Run with tags
poetry run behave --tags=@smoke
