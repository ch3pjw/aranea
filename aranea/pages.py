from urllib.parse import urlparse


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
