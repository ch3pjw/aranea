#! /usr/bin/env python
import asyncio
import logging

import aiohttp

from aranea.crawler import crawl

log = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    try:
        crawled_pages = loop.run_until_complete(crawl(
            client, 'http://aiohttp.readthedocs.org/en/stable/index.html',
            loop=loop))
    except:
        raise
    else:
        print(crawled_pages)
    finally:
        client.close()
        loop.close()
