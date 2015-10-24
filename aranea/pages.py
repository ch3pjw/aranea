from urllib.parse import urlparse
from bs4 import BeautifulSoup

from links import extract_links


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


def make_page(url, html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    base = soup.find('base')
    base_url = base['href'] if base else ''
    return Page(url, base_url, extract_links(soup))
