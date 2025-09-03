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