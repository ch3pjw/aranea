import logging

from urllib.parse import urlparse, urlunparse, urljoin

log = logging.getLogger()


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
    _resource_rel_values = frozenset((
        'author', 'icon', 'prefetch', 'stylesheet'))

    def __init__(self, type_, url, rel):
        self.tag_type = type_
        # FIXME: handle anchors properly
        self.url = urlparse(url)._replace(fragment='')
        self.rel = rel

    def __str__(self):
        return urlunparse(self.url)

    def is_resource(self):
        return (
            self.tag_type != 'a' and self.rel not in self._resource_rel_values)

    def is_internal(self, domain, base_url):
        'Whether this Link refers to a page in our target domain'
        resolved = urlparse(urljoin(base_url, urlunparse(self.url)))
        return resolved.netloc == domain


def extract_links(soup):
    # base = soup.find('base')
    # if base:
    #     base_url = base['href']
    for tag_type, link_attribute_name in Link.types.items():
        for tag in soup.find_all(tag_type):
            try:
                yield Link(
                    tag_type, tag[link_attribute_name], tag.get('rel'))
            except KeyError:
                log.debug('{!r} tag found with no {!r} attribute'.format(
                    tag_type, link_attribute_name))
