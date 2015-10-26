#! /usr/bin/env python
'''Aranea is a toy web-crawler that outputs a graph (in 'dot' format) of
the pages reachable by following links from the given url. It stays within
the given domain.

Direct the output to a file (e.g. example.dot) and convert using
  dot -Tpdf example.dot > example.pdf
or you can pipe the steps together to avoid generating the temporary file
  aranea http://example.com/ | dot -Tpdf > example.pdf
'''

import asyncio
import logging

import argh

from aranea.limited_client import LimitedClientSession
from aranea.crawler import crawl
from aranea.visualisation import make_graph

log = logging.getLogger(__name__)


def main(url, max_concurrent_requests, resources):
    loop = asyncio.get_event_loop()
    client = LimitedClientSession(max_concurrent_requests, loop=loop)
    try:
        crawled_pages = loop.run_until_complete(
            crawl(client, url, loop=loop))
    finally:
        client.close()
        loop.close()
    return make_graph('url_here', crawled_pages, resources)


def cli(
        url: 'The url from which to start crawling',
        max_concurrent_requests:
            'The maximum number of concurrent HTTP requests to handle during '
            'crawling' = 3,
        resources:
            'Whether to output page resources (e.g. script files) in the '
            'output' = False):
    g = main(url, max_concurrent_requests, resources)
    print(g.source)
cli.__doc__ = __doc__


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    argh.dispatch_command(cli)
