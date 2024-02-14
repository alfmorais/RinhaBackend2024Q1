import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url = os.environ["DATABASE_URL"]


settings = Settings()
