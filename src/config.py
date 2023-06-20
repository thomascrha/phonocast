from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings


class Config(BaseSettings):
    PROJECT_PATH: Path = Path(__file__).resolve().parent
    STATIC_PATH: Path = Path.joinpath(PROJECT_PATH, "static")
    TEMPLATES_PATH: Path = Path.joinpath(PROJECT_PATH, "templates")

    PULSE_AUDIO_SINK_NAME: str = "Jackcast"


@lru_cache(maxsize=10)
def get_config():
    return Config()


config = Config()
