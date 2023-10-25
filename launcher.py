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
import asyncio

import asqlite
import uvicorn

import core
import time2grow


async def main() -> None:
    async with asqlite.create_pool("database/database.db") as pool:
        database: time2grow.Database = time2grow.Database(pool)
        await database.setup()

        app: time2grow.Server = time2grow.Server()
        bot: time2grow.Bot = time2grow.Bot(server=app, database=database)

        app.bot = bot

        config: uvicorn.Config = uvicorn.Config(app, host='0.0.0.0', port=8000)
        server: uvicorn.Server = uvicorn.Server(config)

        asyncio.create_task(bot.start())
        await server.serve()


asyncio.run(main())
