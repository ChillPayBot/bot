from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError, computed_field, field_validator
from typing import Optional, List, Dict, Any


class Settings(BaseSettings):
    BOT_TOKEN: str

    SUPPORT_LINK: Optional[str] = Field(default=None)
    SERVER_STATUS_URL: Optional[str] = Field(default=None)
    TERMS_OF_SERVICE_URL: Optional[str] = Field(default=None)
    CAPTCHA_ENABLE: bool = Field(default=False)

    WEBHOOK_BASE_URL: Optional[str] = None
    BASE_URL_API: Optional[str] = None
    WEB_SERVER_HOST: str = Field(default="0.0.0.0")
    WEB_SERVER_PORT: int = Field(default=8080)

    DEBUG: bool = Field(default=False)
    TRIAL_ENABLED: bool = Field(default=False)


_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
