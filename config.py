import json
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent

CONFIG_FILE = HERE / "config.json"

if not CONFIG_FILE.exists():
    raise FileNotFoundError(f"Config file {CONFIG_FILE} not found.")


@dataclass
class Config:
    pushbullet_token: str


def load_config() -> Config:
    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)
        return Config(
            pushbullet_token=data["pushbullet_token"],
        )
