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
