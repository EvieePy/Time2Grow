import tomllib
from typing import Any


with open('config.toml', 'rb') as fp:
    config: dict[str, Any] = tomllib.load(fp)
