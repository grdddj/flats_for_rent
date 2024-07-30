import json
import sys
from pathlib import Path
from typing import Any

import requests

from config import load_config
from logger import get_json_logger

logger = get_json_logger(Path(__file__).with_suffix(".log"))
config = load_config()


def send_pushbullet_message(title: str, body: Any) -> None:
    logger.info({"event": "PushbulletMessage", "title": title, "body": body})
    msg = {"type": "note", "title": title, "body": str(body)}
    resp = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        data=json.dumps(msg),
        headers={
            "Authorization": "Bearer " + config.pushbullet_token,
            "Content-Type": "application/json",
        },
    )
    if resp.status_code != 200:
        logger.error(
            {
                "event": "PushbulletError",
                "status_code": resp.status_code,
                "response": resp.text,
            }
        )
        raise Exception("Error", resp.status_code)
    else:
        logger.info({"event": "PushbulletSuccess"})


if __name__ == "__main__":
    message = " ".join(sys.argv[1:])
    send_pushbullet_message("My message", message)
