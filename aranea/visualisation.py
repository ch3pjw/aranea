from urllib.parse import urlparse
from graphviz import Digraph


def _process_page(g, page, include_resources):
    s = lambda url: urlparse(url).path
    for link_url in page.internal_urls - page.resource_urls:
        g.edge(s(page.url), s(link_url))
    if include_resources:
        for link_url in page.resource_urls & page.internal_urls:
            g.node(s(link_url), color='gray')
            g.edge(s(page.url), s(link_url), color='gray')


def make_graph(url, pages, include_resources=False):
    g = Digraph(comment='Site map generated from {!r}'.format(url))
    for page_url, page in pages.items():
        if isinstance(page, Exception):
            g.node(page_url, label='{} {}'.format(page_url, page), color='red')
        else:
            _process_page(g, page, include_resources)
    return g
