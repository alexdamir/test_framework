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
