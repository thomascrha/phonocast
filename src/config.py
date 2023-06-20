from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings


class Config(BaseSettings):
    PROJECT_PATH: Path = Path(__file__).resolve()
    STATIC_PATH: Path = Path.joinpath(PROJECT_PATH, "static")
    TEMPLATES_PATH: Path = Path.joinpath(PROJECT_PATH, "templates")


@lru_cache(maxsize=10)
def get_config():
    return Config()


config = Config()
