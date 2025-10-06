from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    DEBUG: bool
    DATABASE_URL: str
    REDIS_URL: str
    ENVIRONMENT: str

    class Config:
        env_file = ".env"

settings = Settings()
