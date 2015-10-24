import logging

from bs4 import BeautifulSoup

from .models import Link, Page

log = logging.getLogger(__file__)


def _extract_links(soup):
    for tag_type, link_attribute_name in Link.types.items():
        for tag in soup.find_all(tag_type):
            try:
                yield Link(
                    tag_type, tag[link_attribute_name], tag.get('rel', [''])[0])
            except KeyError:
                log.debug('{!r} tag found with no {!r} attribute'.format(
                    tag_type, link_attribute_name))


def make_page(url, html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    base = soup.find('base')
    base_url = base['href'] if base else ''
    return Page(url, base_url, tuple(_extract_links(soup)))
