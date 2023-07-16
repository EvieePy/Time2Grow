import logging
from typing import TextIO

from core import ColourFormatter, config

from .api import Server
from .bot import Bot
from .database import Database


__all__ = ("Server", "Bot", "Database")


# Setup logging formatter...
handler: logging.StreamHandler[TextIO] = logging.StreamHandler()
handler.setFormatter(ColourFormatter())

logger: logging.Logger = logging.getLogger("time2grow")
logger.addHandler(handler)
logger.setLevel(config["LOGGING"]["level"])
