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
from typing import Any

import asqlite
import logging
import twitchio
from twitchio.ext import commands, routines

import core

from .api import Server
from .plant import Plant


logger: logging.Logger = logging.getLogger(__name__)


class Bot(commands.Bot):

    def __init__(self, *, server: Server, pool: asqlite.Pool) -> None:
        self.server = server
        self.pool = pool

        self.plants: dict[str, Plant] = {}
        self._previous_dispatch: list[dict[str, Any]] = []

        self.game_loop.start()

        config: dict[str, Any] = core.config['BOT']
        super().__init__(token=config['token'], prefix=config['prefix'], initial_channels=config['channels'])

    async def event_command_error(self, context: commands.Context, error: commands.TwitchCommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.CommandOnCooldown):
            return

    @routines.routine(minutes=1, wait_first=True)
    async def game_loop(self) -> None:
        for username, plant in self.plants.copy().items():
            if plant.dead:
                del self.plants[username]

        for plant in self.plants.values():
            plant.update()

        self.dispatch()

    def plants_to_json(self) -> list[dict[str, Any]]:
        return [p.as_dict() for p in self.plants.values()]

    def dispatch(self, data: dict[str, Any] | None = None):
        if not data:
            data = {'extra': None}

        plant_data = self.plants_to_json()
        data['plants'] = plant_data

        self.server.dispatch(data)
        self._previous_dispatch = plant_data

    async def event_ready(self) -> None:
        print(f'Logged in: {self.nick}')

    @commands.command()
    @commands.cooldown(1, 60, commands.Bucket.user)
    async def seed(self, ctx: commands.Context) -> None:
        if len(self.plants) == core.config['GAME']['available']:
            await ctx.send('Plant house is full... Buy plant when plant house not full!')
            return

        username: str = ctx.author.name
        if username in self.plants:
            await ctx.send(f'@{username} you may not own more den 1 plant, limited space for plants in plant house PixelBob')
            return

        self.plants[username] = Plant(username)
        await ctx.send(f'@{username} planted a plant in the plant house! SeemsGood')

        self.dispatch({'extra': {'event': 'create', 'username': username}})

    @commands.command()
    @commands.cooldown(1, 60, commands.Bucket.user)
    async def water(self, ctx: commands.Context) -> None:
        username: str = ctx.author.name

        if username not in self.plants:
            await ctx.send("You can't water da ground and expect a plant to grow from magic... Buy a plant FamilyMan")
            return

        plant: Plant = self.plants[username]
        if plant.dead:
            await ctx.send("Your plant is dead... Buy a new one.")
            return

        await ctx.send(f'@{username} watered their plant MyAvatar')

        plant.update(water=True)
        self.dispatch({'extra': {'event': 'water', 'username': username}})
