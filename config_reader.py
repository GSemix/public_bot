from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    SQL_PATH: SecretStr
    PEOPLES_PATH: SecretStr
    SPHERES_PATH: SecretStr
    EVENTS_PATH: SecretStr
    USERS_PATH: SecretStr
    STATES_PATH: SecretStr

    # Вложенный класс с дополнительными указаниями для настроек
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()
