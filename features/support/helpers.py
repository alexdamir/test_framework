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