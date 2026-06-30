import os

from flask.cli import load_dotenv

load_dotenv(".env.development")


class AppConfig:
    """
    Utility class to get environment variables.

    Values are retrieved from the .env file.
    """

    MYSQL_DB_USER: str = os.getenv("MYSQL_DB_USER")
    MYSQL_DB_PASSWORD: str = os.getenv("MYSQL_DB_PASSWORD")
    MYSQL_DB_PORT: str = os.getenv("MYSQL_DB_PORT")
    MYSQL_DB_NAME: str = os.getenv("MYSQL_DB_NAME")
    MYSQL_DB_HOST: str = os.getenv("MYSQL_DB_HOST")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "development_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
