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
