"""
Copyright (c) 2023 EvieePy(MystyPy)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import datetime
import random
from typing import Any

import core

from .database import Database


TICKS: int = core.config["GAME"]["ticks"]
if TICKS <= 0:
    raise RuntimeError("GAME ticks must be 1 or greater.")

DEATH: int = core.config["GAME"]["death_cycle"]
if DEATH <= 1:
    raise RuntimeError("GAME death_cycle must be 2 or greater.")

GROWTH: int = core.config["GAME"]["growth_cycles"] - 1
if GROWTH < 1:
    raise RuntimeError("GAME growth_cycles must be 1 or greater.")

WATER: int = core.config["GAME"]["water_cycle"]
if WATER < 1:
    raise RuntimeError("GAME water_cycle must be 1 or greater.")

GLASSES: int = core.config["GAME"]["glasses_minutes"]
if GLASSES < 0:
    raise RuntimeError("GAME glasses_cycle must not be negative.")

SPEECH_CHANCE: int = core.config["GAME"]["speech_chance"]


class Plant:
    def __init__(self, username: str, /, *, database: Database, top: int) -> None:
        self.database = database

        self.username = username

        self.total: int = 0
        self._loops: int = 0

        self.state: int = 0  # 0 == fully watered, DEATH == dead
        self.growth: int = 0  # 0 == baby, GROWTH - 1 == Epic

        self.wilted: bool = False
        self.dead: bool = False
        self.maxed: bool = False

        self.watering: bool = False
        self.watered_on: int = 0

        self.glasses: bool = False
        self.glasses_on: int = 0

        self.speech: bool = False
        self.speech_on: int = 0

        self.top = top
        self.created: datetime.datetime = datetime.datetime.now()

    async def update(self, water: bool = False, glasses: bool = False, attacked: bool = False) -> None:
        if water:
            self._loops = max(self._loops - (TICKS * WATER), 0)
            self.state = max(self.state - WATER, 0)
            self.watered_on = self.total
            self.watering = True
            self.wilted = False
        elif glasses:
            self.glasses_on = self.total
            self.glasses = True
            return
        elif attacked:
            self._loops = (DEATH * TICKS) - TICKS
            self.state = DEATH - 1
        else:
            self.total += 1
            self._loops += 1
            await self.database.update_stats(self.username, minutes=1)

        if self.glasses_on + GLASSES < self.total:
            self.glasses = False

        if self.watered_on < self.total:
            self.watering = False

        self.state = int(self._loops / TICKS if self._loops % TICKS == 0 else self.state)
        if self.state == DEATH:
            await self.died()
            return

        self.growth = min(int(self.total / TICKS if self.total % TICKS == 0 else self.growth), GROWTH)

        if self.growth == GROWTH and not self.maxed:
            await self.database.update_stats(self.username, epic=1)
            self.maxed = True

        self.wilted = self.state == (DEATH - 1)
        if self.wilted:
            await self.database.update_stats(self.username, wilted=1)

        if random.randint(0, SPEECH_CHANCE) == SPEECH_CHANCE and not self.speech and not attacked:
            self.speech = random.randint(1, 3)
            self.speech_on = self.total

        elif self.speech_on < self.total:
            self.speech = False

    async def died(self) -> None:
        self.dead = True

        self.wilted = False
        self.speech = False
        self.glasses = False
        self.maxed = False

        await self.database.update_stats(self.username, killed=1)

    def as_dict(self) -> dict[str, Any]:
        data = {
            "username": self.username,
            "state": self.state,
            "growth": self.growth,
            "total": self.total,
            "wilted": self.wilted,
            "dead": self.dead,
            "maxed": self.maxed,
            "watering": self.watering,
            "glasses": self.glasses,
            "speech": self.speech,
            "top": self.top,
        }

        return data
