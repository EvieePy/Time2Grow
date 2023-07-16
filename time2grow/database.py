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
import logging

import asqlite


logger: logging.Logger = logging.getLogger(__name__)


class Database:
    def __init__(self, pool: asqlite.Pool) -> None:
        self.pool = pool

    async def setup(self) -> None:
        async with self.pool.acquire() as connection:
            with open("database/SCHEMA.sql", "r") as schema:
                await connection.executescript(schema.read())

        logger.info("Successfully setup database.")

    async def update_stats(
        self,
        username: str,
        /,
        *,
        minutes: int = 0,
        planted: int = 0,
        watered: int = 0,
        wilted: int = 0,
        killed: int = 0,
        epic: int = 0,
        sabotaged: int = 0,
        victim: int = 0,
        disasters: int = 0,
        survived: int = 0,
        thugged: int = 0,
    ) -> None:
        query: str = """
        INSERT INTO stats(username) VALUES ($1) ON CONFLICT DO UPDATE SET 
            minutes = minutes + $2,
            planted = planted + $3,
            watered = watered + $4,
            wilted = wilted + $5,
            killed = killed + $6,
            epic = epic + + $7,
            sabotaged = sabotaged + $8,
            victim = victim + $9,
            disasters = disasters + $10,
            survived = survived + $11,
            thugged = thugged + $12
        WHERE username = $1
        """

        async with self.pool.acquire() as connection:
            await connection.execute(
                query,
                username,
                minutes,
                planted,
                watered,
                wilted,
                killed,
                epic,
                sabotaged,
                victim,
                disasters,
                survived,
                thugged,
            )

        logger.info(f"Updated stats for {username}")
