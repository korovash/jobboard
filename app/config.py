# app/config.py
from pydantic import BaseSettings, Field, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    ENV: str = Field("development", env="ENV")
    DB_URL: PostgresDsn = Field(..., env="DATABASE_URL")
    SECRET_KEY: str = Field("change-this-now", env="SECRET_KEY")
    COOKIE_NAME: str = Field("jobboard_session", env="COOKIE_NAME")
    LOG_FILE: str = Field("/opt/jobboard/jobboard.log", env="LOG_FILE")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_MAX_BYTES: int = Field(10 * 1024 * 1024, env="LOG_MAX_BYTES")  # 10 MB
    LOG_BACKUP_COUNT: int = Field(5, env="LOG_BACKUP_COUNT")
    # web
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    # pydantic config
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# singleton settings
settings = Settings()
