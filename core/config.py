from pathlib import Path

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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_prefix='APP_CONFIG__',
                                      env_nested_delimiter='__')

    db: DbConfig
    jwt_config: JWTConfig = JWTConfig()
    mail_config: MailConfig = MailConfig()

settings = Settings()