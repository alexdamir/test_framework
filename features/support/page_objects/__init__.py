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