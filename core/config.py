import logging
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent.parent

class DbConfig(BaseModel):
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


class JWTConfig(BaseModel):
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_minutes: int = 42600
    public_key_path: Path = BASE_DIR / "certs" / "public_key.pem"
    private_key_path: Path = BASE_DIR / "certs" / "private_key.pem"


class MailConfig(BaseModel):
    admin_email: str = "social_network@example.com"
    port: int = 1025
    hostname: str = "localhost"


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = logging.INFO
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class RedisConfig(BaseModel):
    prefix: str = "cache"
    hostname: str = "localhost"
    port: int = 6379


class CeleryConfig(BaseModel):
    backend: str = "redis"
    hostname: str = "localhost"
    username: str = "guest"
    password: str = "guest"
    port: int = 6379
    include_path: str = "tasks.tasks"
    result_backend: str = "redis://localhost:6379/0"
    visibility_timeout: int = 3600
    task_serializer: str = "json"
    timezone: str = "Europe/Moscow"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_prefix='APP_CONFIG__',
                                      env_nested_delimiter='__')

    db: DbConfig
    jwt_config: JWTConfig = JWTConfig()
    mail_config: MailConfig = MailConfig()
    log_config: LoggingConfig = LoggingConfig()
    redis_config: RedisConfig = RedisConfig()
    celery_config: CeleryConfig = CeleryConfig()


settings = Settings()