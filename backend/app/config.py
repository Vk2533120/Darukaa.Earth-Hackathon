import os

from pydantic_settings import BaseSettings

# Load .env file if it exists (development).
# In production, environment variables are set by the hosting platform.
env_file = os.path.join(os.path.dirname(__file__), "..", ".env")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://username:password@localhost:5432/darukaa_earth"

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    # Auth
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # App
    APP_ENV: str = "development"

    model_config = {
        "env_file": env_file,
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
