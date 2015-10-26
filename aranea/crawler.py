import asyncio
import logging

from .soup import make_page

log = logging.getLogger(__name__)

@asyncio.coroutine
def get_page(client, url):
    log.info('Fethching {!r}'.format(url))
    response = yield from client.get(url)
    try:
        if response.status == 200:
            return (yield from response.read())
        else:
            # FIXME: in production code this would handle redirects and raise
            # suitable exceptions:
            raise ValueError('Got {} whilst fetching {!r}'.format(
                response.status, url))
    finally:
        response.close()


@asyncio.coroutine
def _crawl(client, url, pages, loop):
    try:
        html_string = yield from get_page(client, url)
    except Exception as e:
        log.exception('Failed to get page {}'.format(url))
        return e
    page = make_page(url, html_string)
    internal_urls = page.internal_urls - page.resource_urls
    new_internal_urls = filter(lambda u: u not in pages, internal_urls)
    tasks = []
    for new_url in new_internal_urls:
        task = loop.create_task(_crawl(client, new_url, pages, loop=loop))
        pages[new_url] = task
        tasks.append(task)

        @task.add_done_callback
        def store_result(task, new_url=new_url):
            pages[new_url] = task.result()
    yield from asyncio.gather(*tasks, loop=loop)
    return page


@asyncio.coroutine
def crawl(client, url, loop):
    pages = {}
    root_page = yield from _crawl(client, url, pages, loop)
    pages[url] = root_page
    return pages
