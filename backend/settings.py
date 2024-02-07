from pydantic import (BaseModel)
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str = 'prod.db'
    model_config = SettingsConfigDict(env_prefix='db_')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='app_')
    host: str = ""
    algorithm_salt: str = "SECURESALTFORENCODING"
    algorithm_min_length: int = 6
    database: DatabaseSettings = DatabaseSettings()


settings = Settings()
