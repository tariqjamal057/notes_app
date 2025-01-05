from pydantic_settings import BaseSettings, SettingsConfigDict


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

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")




settings = Settings()
