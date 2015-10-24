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

    def __str__(self):
        return urlunparse(self.url)

    def is_resource(self):
        if self.tag_type == 'link':
            return self.rel in self._resource_rel_values
        else:
            return self.tag_type != 'a'

    def is_internal(self, domain, base_url):
        'Whether this Link refers to a page in our target domain'
        resolved = urlparse(urljoin(base_url, urlunparse(self.url)))
        return resolved.netloc == domain
