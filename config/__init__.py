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