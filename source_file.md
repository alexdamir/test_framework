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

## 12. Navigation Steps (features/steps/navigation_steps.py)
```python
from behave import given, when, then
from features.support.page_objects.base_page import BasePage

@given('I navigate to "{url}"')
def step_navigate_to_url(context, url):
    """Navigate to a specific URL"""
    base_page = BasePage(context.page)
    full_url = url if url.startswith('http') else f"{context.config.base_url}{url}"
    base_page.navigate_to(full_url)
    base_page.wait_for_load_state()

@when('I go back in browser history')
def step_go_back(context):
    """Navigate back in browser history"""
    context.page.go_back()

@when('I go forward in browser history')
def step_go_forward(context):
    """Navigate forward in browser history"""
    context.page.go_forward()

@when('I refresh the page')
def step_refresh_page(context):
    """Refresh the current page"""
    context.page.reload()

@when('I click the link "{link_text}"')
def step_click_link(context, link_text):
    """Click a link by its text"""
    context.page.click(f"a:has-text('{link_text}')")

@when('I click the button "{button_text}"')
def step_click_button(context, button_text):
    """Click a button by its text"""
    context.page.click(f"button:has-text('{button_text}')")

@when('I click the element with id "{element_id}"')
def step_click_by_id(context, element_id):
    """Click an element by its ID"""
    context.page.click(f"#{element_id}")

@when('I click the element with class "{class_name}"')
def step_click_by_class(context, class_name):
    """Click an element by its class"""
    context.page.click(f".{class_name}")

@when('I hover over "{element_text}"')
def step_hover_element(context, element_text):
    """Hover over an element"""
    context.page.hover(f"text={element_text}")

@when('I scroll to "{element_text}"')
def step_scroll_to_element(context, element_text):
    """Scroll to an element"""
    element = context.page.locator(f"text={element_text}")
    element.scroll_into_view_if_needed()

@when('I wait for "{seconds}" seconds')
def step_wait_seconds(context, seconds):
    """Wait for a specified number of seconds"""
    context.page.wait_for_timeout(int(seconds) * 1000)

@when('I wait for the element "{selector}" to appear')
def step_wait_for_element(context, selector):
    """Wait for an element to appear"""
    context.page.wait_for_selector(selector, timeout=30000)

@when('I wait for the element "{selector}" to disappear')
def step_wait_for_element_hidden(context, selector):
    """Wait for an element to disappear"""
    context.page.wait_for_selector(selector, state="hidden", timeout=30000)

@then('I should be on the "{expected_page}" page')
def step_verify_current_page(context, expected_page):
    """Verify current page by URL pattern"""
    url_patterns = {
        "home": "",
        "login": "/login",
        "dashboard": "/dashboard",
        "profile": "/profile",
        "settings": "/settings"
    }
    
    expected_pattern = url_patterns.get(expected_page.lower(), f"/{expected_page}")
    current_url = context.page.url
    assert expected_pattern in current_url, \
        f"Expected to be on '{expected_page}' page (URL containing '{expected_pattern}'), but current URL is '{current_url}'"

@then('the page title should be "{expected_title}"')
def step_verify_page_title(context, expected_title):
    """Verify page title"""
    actual_title = context.page.title()
    assert expected_title in actual_title, \
        f"Expected title to contain '{expected_title}', but actual title is '{actual_title}'"

@then('the element "{selector}" should be visible')
def step_verify_element_visible(context, selector):
    """Verify an element is visible"""
    assert context.page.is_visible(selector), f"Element '{selector}' is not visible"

@then('the element "{selector}" should not be visible')
def step_verify_element_not_visible(context, selector):
    """Verify an element is not visible"""
    assert not context.page.is_visible(selector), f"Element '{selector}' is visible but shouldn't be"

@then('the element "{selector}" should contain text "{expected_text}"')
def step_verify_element_text(context, selector, expected_text):
    """Verify element contains specific text"""
    actual_text = context.page.text_content(selector) or ""
    assert expected_text in actual_text, \
        f"Expected element '{selector}' to contain '{expected_text}', but actual text is '{actual_text}'"

@then('the current URL should contain "{url_fragment}"')
def step_verify_url_contains(context, url_fragment):
    """Verify current URL contains a specific fragment"""
    current_url = context.page.url
    assert url_fragment in current_url, \
        f"Expected URL to contain '{url_fragment}', but current URL is '{current_url}'"

@then('I should see a link to "{link_text}"')
def step_verify_link_exists(context, link_text):
    """Verify a link with specific text exists"""
    link_selector = f"a:has-text('{link_text}')"
    assert context.page.is_visible(link_selector), f"Link with text '{link_text}' not found"

@then('I should see a button labeled "{button_text}"')
def step_verify_button_exists(context, button_text):
    """Verify a button with specific text exists"""
    button_selector = f"button:has-text('{button_text}')"
    assert context.page.is_visible(button_selector), f"Button with text '{button_text}' not found"
```

## 13. Navigation Feature Example (features/navigation.feature)
```gherkin
Feature: Website Navigation
  As a user
  I want to navigate through the website
  So that I can access different pages and features

  Background:
    Given I am on the "home" page

  Scenario: Navigate to different pages using navigation menu
    When I click the link "Login"
    Then I should be on the "login" page
    And the page title should be "Login"
    
  Scenario: Navigate using browser controls
    Given I navigate to "/dashboard"
    When I go back in browser history
    Then I should be on the "home" page
    When I go forward in browser history
    Then I should be on the "dashboard" page

  Scenario: Page refresh functionality
    Given I am on the "dashboard" page
    When I refresh the page
    Then I should be on the "dashboard" page
    And the element "#main-content" should be visible

  Scenario: Wait for dynamic content
    Given I am on the "dashboard" page
    When I click the button "Load Data"
    And I wait for the element ".loading-spinner" to disappear
    Then the element ".data-table" should be visible
    And the element ".data-table" should contain text "Data loaded successfully"

  Scenario: Navigation with hover effects
    When I hover over "User Menu"
    Then the element ".dropdown-menu" should be visible
    When I click the link "Profile"
    Then I should be on the "profile" page

  Scenario Outline: Navigate to various pages
    When I click the link "<link_text>"
    Then I should be on the "<expected_page>" page
    And the current URL should contain "<url_fragment>"

    Examples:
      | link_text | expected_page | url_fragment |
      | About     | about        | /about       |
      | Contact   | contact      | /contact     |
      | Services  | services     | /services    |
      | Blog      | blog         | /blog        |
```

## 14. Dashboard Page Object (features/support/page_objects/dashboard_page.py)
```python
from .base_page import BasePage

class DashboardPage(BasePage):
    # Locators
    MAIN_CONTENT = "#main-content"
    USER_MENU = ".user-menu"
    NAVIGATION_BAR = ".navbar"
    LOAD_DATA_BUTTON = "button:has-text('Load Data')"
    LOADING_SPINNER = ".loading-spinner"
    DATA_TABLE = ".data-table"
    PROFILE_LINK = "a:has-text('Profile')"
    LOGOUT_BUTTON = "button:has-text('Logout')"
    
    def is_dashboard_loaded(self) -> bool:
        """Check if dashboard is fully loaded"""
        return self.is_visible(self.MAIN_CONTENT) and self.is_visible(self.NAVIGATION_BAR)
    
    def click_user_menu(self):
        """Click on user menu"""
        self.click(self.USER_MENU)
    
    def click_profile_link(self):
        """Navigate to profile page"""
        self.click(self.PROFILE_LINK)
    
    def load_data(self):
        """Click load data button and wait for completion"""
        self.click(self.LOAD_DATA_BUTTON)
        self.wait_for_selector(self.LOADING_SPINNER, timeout=5000)
        self.page.wait_for_selector(self.LOADING_SPINNER, state="hidden", timeout=30000)
    
    def logout(self):
        """Perform logout"""
        self.click(self.USER_MENU)
        self.click(self.LOGOUT_BUTTON)
    
    def get_data_table_text(self) -> str:
        """Get text content from data table"""
        return self.get_text(self.DATA_TABLE)
```

## 15. Helpers Utility (features/support/helpers.py)
```python
import json
import os
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from playwright.sync_api import Page, Locator

class TestHelpers:
    """Utility class with common helper functions for tests"""
    
    @staticmethod
    def load_test_data(filename: str) -> Dict[str, Any]:
        """Load test data from JSON file"""
        try:
            with open(f"config/{filename}", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Test data file {filename} not found")
            return {}
    
    @staticmethod
    def generate_timestamp() -> str:
        """Generate timestamp string for unique identifiers"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def generate_unique_email() -> str:
        """Generate unique email for testing"""
        timestamp = TestHelpers.generate_timestamp()
        return f"test_user_{timestamp}@example.com"
    
    @staticmethod
    def wait_for_page_load(page: Page, timeout: int = 30000):
        """Wait for page to fully load"""
        page.wait_for_load_state("networkidle", timeout=timeout)
    
    @staticmethod
    def take_screenshot_with_timestamp(page: Page, name: str) -> str:
        """Take screenshot with timestamp in filename"""
        timestamp = TestHelpers.generate_timestamp()
        filename = f"screenshots/{name}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        page.screenshot(path=filename, full_page=True)
        return filename
    
    @staticmethod
    def scroll_to_element(page: Page, selector: str):
        """Scroll element into view"""
        element = page.locator(selector)
        element.scroll_into_view_if_needed()
    
    @staticmethod
    def wait_for_text_change(page: Page, selector: str, initial_text: str, timeout: int = 10000):
        """Wait for text content to change from initial value"""
        start_time = time.time()
        while time.time() - start_time < timeout / 1000:
            current_text = page.text_content(selector) or ""
            if current_text != initial_text:
                return True
            time.sleep(0.5)
        return False
    
    @staticmethod
    def get_element_attributes(page: Page, selector: str) -> Dict[str, str]:
        """Get all attributes of an element"""
        element = page.locator(selector)
        return element.evaluate("el => Object.fromEntries([...el.attributes].map(attr => [attr.name, attr.value]))")
    
    @staticmethod
    def clear_and_type(page: Page, selector: str, text: str):
        """Clear input field and type new text"""
        page.fill(selector, "")  # Clear first
        page.type(selector, text, delay=50)  # Type with delay for more realistic input
    
    @staticmethod
    def select_dropdown_option(page: Page, dropdown_selector: str, option_text: str):
        """Select option from dropdown by text"""
        page.select_option(dropdown_selector, label=option_text)
    
    @staticmethod
    def upload_file(page: Page, file_input_selector: str, file_path: str):
        """Upload file using file input"""
        page.set_input_files(file_input_selector, file_path)
    
    @staticmethod
    def switch_to_new_tab(page: Page):
        """Switch to newly opened tab"""
        context = page.context
        pages = context.pages
        if len(pages) > 1:
            return pages[-1]  # Return the newest page
        return page
    
    @staticmethod
    def close_extra_tabs(page: Page):
        """Close all tabs except the main one"""
        context = page.context
        pages = context.pages
        for p in pages[1:]:  # Keep first page, close others
            p.close()

class DataHelpers:
    """Helper class for test data management"""
    
    @staticmethod
    def get_user_credentials(user_type: str = "valid_user") -> Dict[str, str]:
        """Get user credentials from test data"""
        test_data = TestHelpers.load_test_data("test_data.json")
        return test_data.get("users", {}).get(user_type, {})
    
    @staticmethod
    def get_test_urls() -> Dict[str, str]:
        """Get test URLs from test data"""
        test_data = TestHelpers.load_test_data("test_data.json")
        return test_data.get("urls", {})
    
    @staticmethod
    def get_timeout(timeout_type: str = "medium") -> int:
        """Get timeout value from test data"""
        test_data = TestHelpers.load_test_data("test_data.json")
        return test_data.get("timeouts", {}).get(timeout_type, 10000)

class AssertionHelpers:
    """Helper class for custom assertions"""
    
    @staticmethod
    def assert_element_has_class(page: Page, selector: str, expected_class: str):
        """Assert element has specific CSS class"""
        element = page.locator(selector)
        class_list = element.get_attribute("class") or ""
        assert expected_class in class_list.split(), \
            f"Element {selector} does not have class '{expected_class}'. Current classes: {class_list}"
    
    @staticmethod
    def assert_element_count(page: Page, selector: str, expected_count: int):
        """Assert specific number of elements match selector"""
        elements = page.locator(selector)
        actual_count = elements.count()
        assert actual_count == expected_count, \
            f"Expected {expected_count} elements with selector '{selector}', but found {actual_count}"
    
    @staticmethod
    def assert_url_matches_pattern(page: Page, pattern: str):
        """Assert current URL matches pattern"""
        import re
        current_url = page.url
        assert re.search(pattern, current_url), \
            f"URL '{current_url}' does not match pattern '{pattern}'"
    
    @staticmethod
    def assert_element_not_exists(page: Page, selector: str):
        """Assert element does not exist in DOM"""
        elements = page.locator(selector)
        assert elements.count() == 0, f"Element '{selector}' exists but should not"
```

## 16. Settings Configuration (config/settings.py)
```python
import os
from typing import Dict, Any
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Environment settings
ENVIRONMENT = os.getenv("TEST_ENV", "dev")

# Base URLs for different environments
BASE_URLS = {
    "dev": "https://dev.example.com",
    "staging": "https://staging.example.com",
    "prod": "https://example.com"
}

# Browser configuration
BROWSER_CONFIG = {
    "default_browser": os.getenv("BROWSER", "chromium"),
    "headless": os.getenv("HEADLESS", "false").lower() == "true",
    "slow_mo": int(os.getenv("SLOW_MO", "0")),
    "video": os.getenv("VIDEO", "off"),  # 'on', 'off', 'retain-on-failure'
    "screenshot": os.getenv("SCREENSHOT", "only-on-failure"),  # 'on', 'off', 'only-on-failure'
}

# Timeout settings (in milliseconds)
TIMEOUTS = {
    "default": 30000,
    "short": 5000,
    "medium": 15000,
    "long": 60000,
    "page_load": 30000,
    "element_wait": 10000
}

# Test data settings
TEST_DATA = {
    "default_username": os.getenv("TEST_USERNAME", "testuser"),
    "default_password": os.getenv("TEST_PASSWORD", "testpass"),
    "admin_username": os.getenv("ADMIN_USERNAME", "admin"),
    "admin_password": os.getenv("ADMIN_PASSWORD", "adminpass")
}

# Directory paths
PATHS = {
    "screenshots": PROJECT_ROOT / "screenshots",
    "reports": PROJECT_ROOT / "reports",
    "test_data": PROJECT_ROOT / "config",
    "features": PROJECT_ROOT / "features",
    "downloads": PROJECT_ROOT / "downloads"
}

# Ensure directories exist
for path in PATHS.values():
    path.mkdir(exist_ok=True)

# Logging configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(PATHS["reports"] / "test.log")
}

# Report configuration
REPORT_CONFIG = {
    "generate_html": True,
    "generate_json": True,
    "generate_junit": True,
    "allure_results_dir": str(PATHS["reports"] / "allure-results"),
    "html_report_dir": str(PATHS["reports"] / "html")
}

# Database configuration (if needed for tests)
DATABASE_CONFIG = {
    "test_db_url": os.getenv("TEST_DB_URL", "sqlite:///test.db"),
    "reset_db_before_tests": True
}

# API configuration (if testing APIs)
API_CONFIG = {
    "base_url": os.getenv("API_BASE_URL", "https://api.example.com"),
    "timeout": 30,
    "retry_attempts": 3,
    "headers": {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
}

# Performance testing thresholds
PERFORMANCE_CONFIG = {
    "page_load_threshold": 3000,  # milliseconds
    "api_response_threshold": 1000,  # milliseconds
    "memory_usage_threshold": 100  # MB
}

def get_base_url(environment: str = None) -> str:
    """Get base URL for specified environment"""
    env = environment or ENVIRONMENT
    return BASE_URLS.get(env, BASE_URLS["dev"])

def get_timeout(timeout_type: str = "default") -> int:
    """Get timeout value for specified type"""
    return TIMEOUTS.get(timeout_type, TIMEOUTS["default"])

def get_browser_config() -> Dict[str, Any]:
    """Get browser configuration"""
    return BROWSER_CONFIG.copy()

def is_ci_environment() -> bool:
    """Check if running in CI environment"""
    ci_indicators = ["CI", "CONTINUOUS_INTEGRATION", "GITHUB_ACTIONS", "JENKINS_URL"]
    return any(os.getenv(indicator) for indicator in ci_indicators)
```

## 17. __init__.py Files

### features/__init__.py
```python
"""
BDD Test Features Package

This package contains all BDD feature files, step definitions,
and supporting utilities for the test framework.
"""

__version__ = "1.0.0"
__author__ = "Test Team"
```

### features/steps/__init__.py
```python
"""
Step Definitions Package

Contains all step definition modules for BDD scenarios.
"""

# Import all step modules to make them available to Behave
from . import common_steps
from . import login_steps
from . import navigation_steps

__all__ = [
    "common_steps",
    "login_steps", 
    "navigation_steps"
]
```

### features/support/__init__.py
```python
"""
Support Utilities Package

Contains page objects, configuration, and helper utilities
for the test framework.
"""

from .config import Config
from .helpers import TestHelpers, DataHelpers, AssertionHelpers
from .browser_manager import BrowserManager

__all__ = [
    "Config",
    "TestHelpers",
    "DataHelpers", 
    "AssertionHelpers",
    "BrowserManager"
]
```

### features/support/page_objects/__init__.py
```python
"""
Page Objects Package

Contains all page object classes following the Page Object Model pattern.
"""

from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage

__all__ = [
    "BasePage",
    "LoginPage",
    "DashboardPage"
]
```

### tests/__init__.py
```python
"""
Tests Package

Contains unit tests and integration tests separate from BDD features.
"""

__version__ = "1.0.0"
```

### tests/unit/__init__.py
```python
"""
Unit Tests Package

Contains unit tests for individual components and utilities.
"""
```

### tests/integration/__init__.py
```python
"""
Integration Tests Package

Contains integration tests for component interactions.
"""
```

### config/__init__.py
```python
"""
Configuration Package

Contains configuration files and settings for different environments.
"""

from .settings import (
    get_base_url,
    get_timeout,
    get_browser_config,
    is_ci_environment,
    BROWSER_CONFIG,
    TIMEOUTS,
    TEST_DATA,
    PATHS
)

__all__ = [
    "get_base_url",
    "get_timeout", 
    "get_browser_config",
    "is_ci_environment",
    "BROWSER_CONFIG",
    "TIMEOUTS",
    "TEST_DATA",
    "PATHS"
]
```

## 18. Environment File Template (.env.example)
```bash
# Browser Configuration
BROWSER=chromium  # chromium, firefox, webkit
HEADLESS=false
SLOW_MO=0
VIDEO=off  # on, off, retain-on-failure
SCREENSHOT=only-on-failure  # on, off, only-on-failure

# Environment
TEST_ENV=dev  # dev, staging, prod
BASE_URL=https://dev.example.com

# Test Credentials
TEST_USERNAME=testuser
TEST_PASSWORD=testpass
ADMIN_USERNAME=admin
ADMIN_PASSWORD=adminpass

# API Configuration (if needed)
API_BASE_URL=https://api.dev.example.com

# Database Configuration (if needed)
TEST_DB_URL=sqlite:///test.db

# Logging
LOG_LEVEL=INFO

# CI/CD
CI=false
```

## 19. README.md
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