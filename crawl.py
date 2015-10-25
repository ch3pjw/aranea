#! /usr/bin/env python
import asyncio
import logging

from aranea.limited_client import LimitedClientSession
from aranea.crawler import crawl
from aranea.visualisation import make_graph

log = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    client = LimitedClientSession(3, loop=loop)
    try:
        crawled_pages = loop.run_until_complete(crawl(
            client, 'http://aiohttp.readthedocs.org/en/stable/index.html',
            loop=loop))
    finally:
        client.close()
        loop.close()
    g = make_graph('url_here', crawled_pages)
    print(g.source)
