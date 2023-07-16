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
import json
import logging
import secrets
from typing import TYPE_CHECKING, Any, AsyncGenerator

import aiohttp
from sse_starlette import EventSourceResponse
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


if TYPE_CHECKING:
    from .bot import Bot


logger: logging.Logger = logging.getLogger(__name__)


class Server(Starlette):
    def __init__(self) -> None:
        self.bot: Bot | None = None

        routes: list[Route] = [
            Route("/event", self.event_endpoint, methods=["GET"]),
            Mount("/", app=StaticFiles(directory="static", html=True), name="static"),
        ]
        middleware: list[Middleware] = [
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ]

        super().__init__(routes=routes, middleware=middleware)
        self.listeners: dict[str, asyncio.Queue] = {}

    def dispatch(self, data: dict[str, Any]) -> None:
        asyncio.create_task(self._dispatch(data=data))

    async def _dispatch(self, data: dict[str, Any]) -> None:
        for queue in self.listeners.values():
            await queue.put(data)

    async def event_endpoint(self, request: Request) -> EventSourceResponse:
        identifier: str = secrets.token_urlsafe(12)
        self.listeners[identifier] = asyncio.Queue()

        return EventSourceResponse(self.process_event(identifier=identifier, request=request))

    async def process_event(self, *, identifier: str, request: Request) -> AsyncGenerator[Any, Any] | None:
        logger.info(f'Event Listener "{identifier}" has connected.')
        queue: asyncio.Queue = self.listeners[identifier]

        if self.bot:
            initial = json.dumps({"event": None, "plants": self.bot.plants_to_json()})
            yield initial

        while True:
            try:
                data: dict[str, Any] = await queue.get()
                yield json.dumps(data)
            except asyncio.CancelledError:
                break

            if await request.is_disconnected():
                break

        logger.info(f'Event Listener "{identifier}" has disconnected.')
        del self.listeners[identifier]
