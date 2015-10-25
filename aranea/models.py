from urllib.parse import urlparse, urlunparse, urljoin


class Link:
    __slots__ = 'tag_type', 'url', 'rel'  # NB: rel for <link> tags
    types = {
        'a': 'href',
        'link': 'href',
        'script': 'src',
        'img': 'src',
    }
    # A list of <link> tag 'rel' attributes that count as resources,
    # c.f. hyperlinks to other documents. Seeg
    # http://www.w3schools.com/tags/att_link_rel.asp:
    _resource_rel_values = frozenset(('icon', 'prefetch', 'stylesheet'))

    def __init__(self, type_, url, rel):
        self.tag_type = type_
        # FIXME: handle anchors properly
        self.url = urlparse(url)._replace(fragment='')
        self.rel = rel

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, str(self))

    def __str__(self):
        return urlunparse(self.url)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
                other.tag_type == self.tag_type and
                other.url == self.url and
                other.rel == self.rel)
        else:
            return NotImplemented

    def is_resource(self):
        if self.tag_type == 'link':
            return self.rel in self._resource_rel_values
        else:
            return self.tag_type != 'a'

    def is_internal(self, domain, base_url):
        'Whether this Link refers to a page in our target domain'
        resolved = urlparse(urljoin(base_url, urlunparse(self.url)))
        return resolved.netloc == domain


class Page:
    def __init__(self, url, base_url, links):
        self.base_url = base_url
        self.url = url
        self.domain = urlparse(url).netloc
        self.links = links

    def _resolve(self, link):
        return urljoin(self.base_url, str(link))

    @property
    def urls(self):
        return set(map(self._resolve, self.links))

    @property
    def internal_urls(self):
        return set(map(self._resolve, filter(
            lambda l: l.is_internal(self.domain, self.base_url), self.links)))

    @property
    def resource_urls(self):
        return set(map(self._resolve, filter(
            lambda l: l.is_resource(), self.links)))
