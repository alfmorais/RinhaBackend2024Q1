from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL")
ASYNC_DATABASE_URL = config("ASYNC_DATABASE_URL")
DB_USERNAME = config("DB_USERNAME")
DB_SECRET = config("DB_SECRET")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")
