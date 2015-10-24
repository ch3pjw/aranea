import asyncio
import logging
from collections import namedtuple
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

from link_extraction import extract_links

log = logging.getLogger()

Page = namedtuple('Page', ('url', 'page_links', 'resources'))


class Page:
    def __init__(self, url, base_url, links):
        self.base_url = base_url
        self.url = url
        self.domain = urlparse(url).netloc
        self._links = links

    @property
    def internal_links(self):
        return filter(
            lambda l: l.is_internal(self.domain, self.base_url), self._links)

    @property
    def external_links(self):
        return filter(
            lambda l: not l.is_internal(self.domain, self.base_url),
            self._links)

    @property
    def resource_links(self):
        return filter(lambda l: l.is_resource(), self._links)


def partition(predicate, iterable):
    a = []
    b = []
    for item in iterable:
        if predicate(item):
            a.append(item)
        else:
            b.append(item)
    return tuple(a), tuple(b)


@asyncio.coroutine
def get_page(client, url):
    log.debug('Fethching {!r}'.format(url))
    response = yield from client.get(url)
    if response.status == 200:
        return (yield from response.read())
    else:
        raise ValueError('need to handle bad responses, redirects...')


@asyncio.coroutine
def _crawl(client, url, pages, loop):
    html_string = yield from get_page(client, url)
    page = make_page(url, html_string)
    new_internal_urls = filter(
        lambda u: u not in pages, map(str, page.internal_links))
    tasks = []
    for new_url in new_internal_urls:
        task = loop.create_task(_crawl(client, new_url, pages, loop=loop))
        pages[new_url] = task
        tasks.append(task)
    for linked_page in (yield from asyncio.gather(*tasks, loop=loop)):
        pages[linked_page.url] = linked_page
    return page


def make_page(url, html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    base = soup.find('base')
    base_url = base['href'] if base else ''
    return Page(url, base_url, extract_links(soup))


@asyncio.coroutine
def crawl(client, url, loop):
    pages = {}
    yield from _crawl(client, url, pages, loop)
    return pages



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
