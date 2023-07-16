import json
from typing import Any


with open("config.json", "r") as fp:
    config: dict[Any, Any] = json.load(fp)
