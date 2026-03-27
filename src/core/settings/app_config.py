import yaml
from pydantic import BaseModel

from core.paths import APP_CONFIG_PATH


class LoggingCfg(BaseModel):
    level: str = "INFO"


class AppConfig(BaseModel):
    logging: LoggingCfg = LoggingCfg()

    @classmethod
    def from_sources(cls) -> "AppConfig":
        with APP_CONFIG_PATH.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
