from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_BASE_URL: str = "http://127.0.0.1:8000/api"

    class Config:
        env_file = ".env"


settings = Settings()
