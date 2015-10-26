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
    '''Handles the recursive logic of crawling. The aim is to build up a shared
    mapping of URLs to Page objects. Every time we request a new Page, we put a
    Task as a placeholder for that page in the mapping until the Page is
    created, to prevent retrieving a page more than once.

    If retireving a page results in an error, we store that instead so the error
    information can eventually be represented to the user.
    '''
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
    # Run the child crawlers concurrently, and only return once they have all
    # retrieved all their pages:
    yield from asyncio.gather(*tasks, loop=loop)
    return page


@asyncio.coroutine
def crawl(client, url, loop):
    pages = {}
    root_page = yield from _crawl(client, url, pages, loop)
    pages[url] = root_page
    return pages
