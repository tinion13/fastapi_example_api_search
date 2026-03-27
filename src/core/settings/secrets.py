from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Secrets(BaseSettings):
    TRAVELPAYOUTS_AVIASALES_TOKEN: SecretStr
    OPENWEATHER_TOKEN: SecretStr

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
    )



@lru_cache
def get_secrets() -> Secrets:
    return Secrets() # pyright: ignore[reportCallIssue]
