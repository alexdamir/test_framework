# Python Test Framework Structure (Playwright + Behave + Poetry)

## Project Structure
```
test_framework/
├── pyproject.toml
├── README.md
├── .gitignore
├── features/
│   ├── environment.py
│   ├── steps/
│   │   ├── __init__.py
│   │   ├── common_steps.py
│   │   ├── login_steps.py
│   │   └── navigation_steps.py
│   ├── support/
│   │   ├── __init__.py
│   │   ├── browser_manager.py
│   │   ├── config.py
│   │   ├── helpers.py
│   │   └── page_objects/
│   │       ├── __init__.py
│   │       ├── base_page.py
│   │       ├── login_page.py
│   │       └── dashboard_page.py
│   ├── login.feature
│   └── navigation.feature
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
├── reports/
│   └── .gitkeep
├── screenshots/
│   └── .gitkeep
└── config/
    ├── __init__.py
    ├── settings.py
    └── test_data.json
```

## 1. pyproject.toml
```toml
[tool.poetry]
name = "test-framework"
version = "0.1.0"
description = "BDD Test Framework using Playwright, Behave, and Poetry"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "features"}, {include = "tests"}, {include = "config"}]

[tool.poetry.dependencies]
python = "^3.9"
playwright = "^1.40.0"
behave = "^1.2.6"
pytest = "^7.4.0"
pytest-playwright = "^0.4.3"
allure-behave = "^2.13.2"
pydantic = "^2.5.0"
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.8.0"
pre-commit = "^3.6.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.behave]
paths = ["features"]
format = ["pretty", "json:reports/behave-report.json"]
junit = true
junit_directory = "reports"
show_timings = true

[tool.black]
line-length = 88
target-version = ['py39']

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
```

## 2. Environment Configuration (features/environment.py)
```python
import os
from playwright.sync_api import sync_playwright
from features.support.browser_manager import BrowserManager
from features.support.config import Config

def before_all(context):
    """Set up test environment before all scenarios"""
    context.config = Config()
    context.browser_manager = BrowserManager()
    
def before_scenario(context, scenario):
    """Set up before each scenario"""
    context.browser = context.browser_manager.get_browser()
    context.page = context.browser.new_page()
    
    # Set default timeout
    context.page.set_default_timeout(30000)
    
    # Add screenshot on failure
    context.scenario_name = scenario.name

def after_scenario(context, scenario):
    """Clean up after each scenario"""
    if scenario.status == "failed":
        # Take screenshot on failure
        screenshot_path = f"screenshots/{scenario.name.replace(' ', '_')}.png"
        context.page.screenshot(path=screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
    
    # Close page
    if hasattr(context, 'page'):
        context.page.close()

def after_all(context):
    """Clean up after all tests"""
    if hasattr(context, 'browser_manager'):
        context.browser_manager.close_all()
```

## 3. Browser Manager (features/support/browser_manager.py)
```python
from playwright.sync_api import sync_playwright, Browser
from typing import Optional
from .config import Config

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.config = Config()
        
    def get_browser(self) -> Browser:
        """Get or create browser instance"""
        if not self.browser:
            self.playwright = sync_playwright().start()
            
            browser_type = getattr(self.playwright, self.config.browser_name)
            self.browser = browser_type.launch(
                headless=self.config.headless,
                slow_mo=self.config.slow_mo
            )
        
        return self.browser
    
    def close_all(self):
        """Close browser and playwright"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
```

## 4. Configuration (features/support/config.py)
```python
import os
from typing import Optional
from pydantic import BaseModel

class Config(BaseModel):
    # Browser settings
    browser_name: str = os.getenv("BROWSER", "chromium")
    headless: bool = os.getenv("HEADLESS", "false").lower() == "true"
    slow_mo: int = int(os.getenv("SLOW_MO", "0"))
    
    # Application settings
    base_url: str = os.getenv("BASE_URL", "https://example.com")
    timeout: int = int(os.getenv("TIMEOUT", "30000"))
    
    # Test data
    test_username: str = os.getenv("TEST_USERNAME", "testuser")
    test_password: str = os.getenv("TEST_PASSWORD", "testpass")
    
    class Config:
        env_file = ".env"
```

## 5. Base Page Object (features/support/page_objects/base_page.py)
```python
from playwright.sync_api import Page, Locator
from abc import ABC
from typing import Optional

class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        
    def navigate_to(self, url: str):
        """Navigate to a URL"""
        self.page.goto(url)
        
    def wait_for_load_state(self, state: str = "networkidle"):
        """Wait for page load state"""
        self.page.wait_for_load_state(state)
        
    def click(self, selector: str):
        """Click an element"""
        self.page.click(selector)
        
    def fill(self, selector: str, value: str):
        """Fill an input field"""
        self.page.fill(selector, value)
        
    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        return self.page.text_content(selector) or ""
        
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return self.page.is_visible(selector)
        
    def wait_for_selector(self, selector: str, timeout: Optional[int] = None):
        """Wait for selector to appear"""
        self.page.wait_for_selector(selector, timeout=timeout)
        
    def take_screenshot(self, path: str):
        """Take a screenshot"""
        self.page.screenshot(path=path)
```

## 6. Login Page Object (features/support/page_objects/login_page.py)
```python
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message"
    
    def login(self, username: str, password: str):
        """Perform login"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
        
    def is_login_form_visible(self) -> bool:
        """Check if login form is visible"""
        return self.is_visible(self.USERNAME_INPUT)
```

## 7. Common Steps (features/steps/common_steps.py)
```python
from behave import given, when, then
from features.support.page_objects.base_page import BasePage

@given('I am on the "{page_name}" page')
def step_navigate_to_page(context, page_name):
    url_map = {
        "login": f"{context.config.base_url}/login",
        "dashboard": f"{context.config.base_url}/dashboard",
        "home": context.config.base_url
    }
    
    base_page = BasePage(context.page)
    base_page.navigate_to(url_map.get(page_name.lower(), context.config.base_url))
    base_page.wait_for_load_state()

@when('I click on "{element_text}"')
def step_click_element(context, element_text):
    context.page.click(f"text={element_text}")

@then('I should see "{text}" on the page')
def step_verify_text_present(context, text):
    assert context.page.is_visible(f"text={text}"), f"Text '{text}' not found on page"

@then('I should be redirected to "{expected_url}"')
def step_verify_url(context, expected_url):
    current_url = context.page.url
    assert expected_url in current_url, f"Expected URL '{expected_url}' not in current URL '{current_url}'"
```

## 8. Login Steps (features/steps/login_steps.py)
```python
from behave import given, when, then
from features.support.page_objects.login_page import LoginPage

@given('I am on the login page')
def step_navigate_to_login(context):
    login_page = LoginPage(context.page)
    login_page.navigate_to(f"{context.config.base_url}/login")
    context.login_page = login_page

@when('I enter username "{username}" and password "{password}"')
def step_enter_credentials(context, username, password):
    context.login_page.login(username, password)

@when('I click the login button')
def step_click_login(context):
    context.login_page.click(context.login_page.LOGIN_BUTTON)

@then('I should see an error message "{error_message}"')
def step_verify_error_message(context, error_message):
    actual_error = context.login_page.get_error_message()
    assert error_message in actual_error, f"Expected error '{error_message}' not found in '{actual_error}'"

@then('I should be successfully logged in')
def step_verify_successful_login(context):
    # Wait for redirect after login
    context.page.wait_for_url("**/dashboard", timeout=10000)
    assert "/dashboard" in context.page.url
```

## 9. Feature File Example (features/login.feature)
```gherkin
Feature: User Login
  As a user
  I want to be able to log in to the application
  So that I can access my account

  Background:
    Given I am on the login page

  Scenario: Successful login with valid credentials
    When I enter username "testuser" and password "testpass"
    And I click the login button
    Then I should be successfully logged in

  Scenario: Login with invalid credentials
    When I enter username "invalid" and password "invalid"
    And I click the login button
    Then I should see an error message "Invalid username or password"

  Scenario Outline: Login with various invalid credentials
    When I enter username "<username>" and password "<password>"
    And I click the login button
    Then I should see an error message "<error_message>"

    Examples:
      | username | password | error_message              |
      | ""       | "pass"   | Username is required       |
      | "user"   | ""       | Password is required       |
      | ""       | ""       | Username and password required |
```

## 10. Test Data Configuration (config/test_data.json)
```json
{
  "users": {
    "valid_user": {
      "username": "testuser",
      "password": "testpass"
    },
    "admin_user": {
      "username": "admin",
      "password": "adminpass"
    }
  },
  "urls": {
    "login": "/login",
    "dashboard": "/dashboard",
    "profile": "/profile"
  },
  "timeouts": {
    "short": 5000,
    "medium": 10000,
    "long": 30000
  }
}
```

## 11. .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Test reports
reports/
screenshots/*.png
*.log

# Environment variables
.env

# Playwright
/test-results/
/playwright-report/
/playwright/.cache/
```

## 12. README.md
```markdown
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
```

## Project Structure

- `features/`: BDD feature files and step definitions
- `features/support/`: Page objects and utilities
- `tests/`: Unit and integration tests
- `config/`: Configuration files
- `reports/`: Test reports and screenshots
```

## Usage Commands

After setting up the project structure:

```bash
# Initialize project
poetry init
poetry install
poetry run playwright install

# Run tests
poetry run behave                    # All features
poetry run behave features/login.feature  # Specific feature
BROWSER=firefox poetry run behave    # Different browser
HEADLESS=true poetry run behave      # Headless mode

# Generate reports
poetry run behave -f allure_behave.formatter:AllureFormatter -o reports/
```

This framework provides:
- **BDD approach** with Gherkin scenarios
- **Page Object Model** for maintainable code
- **Cross-browser testing** with Playwright
- **Configurable environments** via environment variables
- **Automatic screenshots** on test failures
- **Comprehensive reporting** with Allure integration
- **Poetry** for dependency management
