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
import logging
import random
from typing import Any

import asqlite
import twitchio
from twitchio.ext import commands, routines

import core

from .api import Server
from .database import Database
from .plant import Plant


logger: logging.Logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *, server: Server, database: Database) -> None:
        self.server = server
        self.database = database

        self.plants: dict[str, Plant] = {}
        self._previous_dispatch: list[dict[str, Any]] = []

        self.game_loop.start()

        config: dict[str, Any] = core.config["BOT"]
        super().__init__(
            token=config["token"],
            prefix=config["prefix"],
            initial_channels=[config["channel"]],
        )

    async def event_command_error(self, context: commands.Context, error: commands.TwitchCommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.CommandOnCooldown):
            return

        logger.error(error)

    @routines.routine(minutes=1, wait_first=True)
    async def game_loop(self) -> None:
        for username, plant in self.plants.copy().items():
            if plant.dead:
                del self.plants[username]

        for plant in self.plants.values():
            await plant.update()

        top: list[Plant] = list(sorted(self.plants.values(), key=lambda p: p.created))
        for index, plant in enumerate(top, 1):
            plant.top = index

        self.dispatch()

    def plants_to_json(self) -> list[dict[str, Any]]:
        return list(reversed([p.as_dict() for p in self.plants.values()]))

    def dispatch(self, data: dict[str, Any] | None = None):
        if not data:
            data = {"extra": None}

        plant_data: list[dict[str, Any]] = self.plants_to_json()
        data["plants"] = plant_data

        self.server.dispatch(data)
        self._previous_dispatch = plant_data

    async def event_ready(self) -> None:
        print(f"Logged in: {self.nick}")

    @commands.command()
    @commands.cooldown(1, core.config["COOLDOWNS"]["plant"], commands.Bucket.user)
    async def plant(self, ctx: commands.Context) -> None:
        if len(self.plants) == core.config["GAME"]["available"]:
            await ctx.send("Plant house is full... Buy plant when plant house not full!")
            return

        username: str = ctx.author.name
        if username in self.plants:
            await ctx.send(f"{username} you may not own more then 1 plant PixelBob")
            return

        self.plants[username] = Plant(username, database=self.database, top=len(self.plants) + 1)
        await ctx.send(f"{username} planted a plant in the plant house SeemsGood")

        self.dispatch({"extra": {"event": "create", "username": username}})
        await self.database.update_stats(username, planted=1)

    @commands.command()
    @commands.cooldown(1, core.config["COOLDOWNS"]["water"], commands.Bucket.user)
    async def water(self, ctx: commands.Context) -> None:
        username: str = ctx.author.name

        if username not in self.plants:
            await ctx.send("You can't water da ground and expect a plant to grow from magic... Buy a plant FamilyMan")
            return

        plant: Plant = self.plants[username]
        if plant.dead:
            await ctx.send("Your plant is dead RIP. Buy a new one.")
            return

        await ctx.send(f"{username} watered their plant MyAvatar")
        await plant.update(water=True)

        self.dispatch({"extra": {"event": "water", "username": username}})
        await self.database.update_stats(username, watered=1)

    @commands.command()
    @commands.cooldown(1, core.config["COOLDOWNS"]["thug"], commands.Bucket.user)
    async def thug(self, ctx: commands.Context) -> None:
        username: str = ctx.author.name

        if username not in self.plants:
            await ctx.send("You can't thug da air... Buy a plant FamilyMan")
            return

        plant: Plant = self.plants[username]
        if plant.dead:
            await ctx.send("Your plant is dead RIP. Buy a new one.")
            return

        await ctx.send(f"{username} thug lifed their plant GlitchCat")
        await plant.update(glasses=True)

        self.dispatch({"extra": {"event": "glasses", "username": username}})
        await self.database.update_stats(username, thugged=1)

    @commands.command()
    @commands.cooldown(1, core.config["COOLDOWNS"]["attack"], commands.Bucket.user)
    async def attack(self, ctx: commands.Context, *, recipient: str = "") -> None:
        username: str = ctx.author.name
        recipient = recipient.lower()

        if recipient not in self.plants:
            await ctx.send(f"{username} used their most special attack on the wind... It did nothing!")
            return

        if username == recipient:
            await ctx.send(f"{username} tripped over themself. Kinda weird cause they don't have legs")
            return

        plant: Plant = self.plants[recipient]
        if plant.dead:
            await ctx.send(f"{username} tried to attack a ghost. But they got scared and ran away FailFish")
            return

        if plant.wilted:
            await ctx.send(f"{username} attacked a thirsty plant. They felt bad and went to bed crying BibleThump")
            return

        reversed_: bool = False

        attack: str = random.choice(core.config["GAME"]["attacks"])
        if username not in self.plants:
            await ctx.send(f"{username} used {attack} on {recipient}, it did something.")
            await plant.update(attacked=True)

        else:
            outcome: int = random.randint(0, core.config["GAME"]["reverse_attack_chance"])
            if outcome == 0:
                reversed_ = True
                attacker_plant: Plant = self.plants[username]

                woops: str = random.choice(core.config["GAME"]["woops"])
                await ctx.send(
                    f"{username} used {attack} on {recipient}, but {woops}, and {recipient} stole all their water."
                )

                await plant.update(water=True)
                await attacker_plant.update(attacked=True)
            else:
                await ctx.send(f"{username} used {attack} on {recipient}, it was super effective.")
                await plant.update(attacked=True)

        self.dispatch(
            data={
                "extra": {
                    "event": "attacked",
                    "attacker": username,
                    "recipient": recipient,
                    "reversed": reversed_
                }
            }
        )
        await self.database.update_stats(recipient, victim=1)
        await self.database.update_stats(username, sabotaged=1)
