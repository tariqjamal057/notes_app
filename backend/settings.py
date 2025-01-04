from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class for application configuration.

    Attributes:
        MONGO_URI (str): MongoDB connection string
        SECRET_KEY (str): Secret key for JWT token encryption
        DEFAULT_TIMEZONE (str): Default timezone for the application
    """

    MONGO_URI: str
    SECRET_KEY: str
    DEFAULT_TIMEZONE: str

    class Config:
        env_file = "../.env"


settings = Settings()
