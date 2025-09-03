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
