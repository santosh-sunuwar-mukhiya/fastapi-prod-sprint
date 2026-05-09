from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory - goes up 3 levels from config.py (core -> app -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

_base_config = SettingsConfigDict(
    env_file=str(BASE_DIR / ".env"),
    env_ignore_empty=True,
    extra="ignore",
)

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config

class SecuritySettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_REFRESH_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = _base_config

class NotificationSettings(BaseSettings):
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SENDER_EMAIL: str
    SENDER_NAME: str

    model_config = _base_config

class AppSettings(BaseSettings):
    DATABASE_URL: str
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    RELOAD: bool = True
    APP_NAME: str = "Authentication and Login System."
    APP_DOMAIN: str = "localhost:8000"

    model_config = _base_config


app_settings = AppSettings()
db_settings = DatabaseSettings()
security_settings = SecuritySettings()
notification_settings = NotificationSettings()

