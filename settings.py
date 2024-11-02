from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    db_username: str = 'user'
    db_password: str = 'password'
    db_ip: str = 'database'
    db_port: str = '5432'
    db_name: str = 'postgres'
    model_config = SettingsConfigDict(env_file='.env')


settings = _Settings()
