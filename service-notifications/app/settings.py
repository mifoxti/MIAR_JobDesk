from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    amqp_url: str  # Для RabbitMQ
    postgres_url: str  # Для будущего БД

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
