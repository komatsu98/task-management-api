from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management API"
    API_VERSION: str = "1.0"
    DATABASE_URI: str
    JWT_SECRET_KEY: str

    class ConfigDict:
        env_file = ".env"


settings = Settings()
