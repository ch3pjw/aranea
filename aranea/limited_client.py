import asyncio
from aiohttp import ClientSession


class LimitedClientSession(ClientSession):
    def __init__(self, concurrent_requests=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._semaphore = asyncio.BoundedSemaphore(concurrent_requests)

    @asyncio.coroutine
    def get(self, *args, **kwargs):
        yield from self._semaphore.acquire()
        try:
            return (yield from super().get(*args, **kwargs))
        finally:
            self._semaphore.release()
