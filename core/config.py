from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbConfig:
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50
    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_prefix='APP_CONFIG__',
                                      env_nested_delimiter='__')

    db_config: DbConfig

settings = Settings()