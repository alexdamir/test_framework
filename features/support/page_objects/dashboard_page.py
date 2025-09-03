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