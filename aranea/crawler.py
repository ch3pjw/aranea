import asyncio
import logging

from soup import make_page

log = logging.getLogger(__file__)

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


@asyncio.coroutine
def crawl(client, url, loop):
    pages = {}
    yield from _crawl(client, url, pages, loop)
    return pages
