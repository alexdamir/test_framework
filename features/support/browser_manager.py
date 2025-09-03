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
