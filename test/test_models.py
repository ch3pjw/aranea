from unittest import TestCase

from aranea.models import Link, Page

internal_domain = 'example.com'
base_url = 'http://' + internal_domain
example_url = base_url + '/path'
external_domain = 'another-domain.com'
external_base_url = '//' + external_domain


class TestLink(TestCase):
    def test_str(self):
        l = Link('a', example_url, rel=[])
        self.assertEqual(str(l), example_url)

    def test_repr(self):
        l = Link('a', example_url, rel=[])
        self.assertIn(example_url, repr(l))

    def test_eq(self):
        l = lambda: Link('a', example_url, rel=[])
        self.assertEqual(l(), l())
        self.assertNotEqual(l(), Link('img', example_url, rel=[]))
        self.assertNotEqual(l(), Link('a', external_base_url, rel=[]))
        self.assertNotEqual(l(), Link('a', example_url, rel=['icon']))
        self.assertNotEqual(l(), 'hello world')

    def test_is_resource(self):
        l = Link('a', example_url, rel=[])
        self.assertFalse(l.is_resource())
        l = Link('link', example_url, rel=['next'])
        self.assertFalse(l.is_resource())
        l = Link('link', example_url, rel=['stylesheet'])
        self.assertTrue(l.is_resource())
        l = Link('link', example_url, rel=['shortcut', 'icon'])
        self.assertTrue(l.is_resource())
        l = Link('img', example_url, rel=[])
        self.assertTrue(l.is_resource())
        # NB: we could exhaustively check combinations of tag_type and rel, but
        # we'd pretty much just be checking that the code was how we wrote it,
        # which doesn't offer much of a useful check.

    def test_is_internal(self):
        l = Link('a', example_url + '/sub_path', rel=[])
        self.assertTrue(l.is_internal(internal_domain, ''))
        self.assertFalse(l.is_internal(external_domain, ''))
        self.assertTrue(l.is_internal(internal_domain, '//ignored.com'))
        self.assertFalse(l.is_internal(external_domain, '//ignored.com'))
        l = Link('a', '/root/relative', rel=[])
        self.assertTrue(l.is_internal(internal_domain, base_url))
        self.assertFalse(l.is_internal(
            internal_domain, external_base_url))
        # NB: we have to be careful that we're not just testing urljoin's logic
        # for resolving relative paths!


class TestPage(TestCase):
    def test_eq(self):
        base1 = 'http://base1'
        base2 = 'http://base2'
        p1 = Page(
            'my_url', base1, [Link('a', 'http://abs.o/lute', rel=[])])
        p2 = Page(
            'my_url', base2, [Link('a', 'http://abs.o/lute', rel=[])])
        self.assertEqual(p1, p2)
        p1 = Page('my_url', base1, [Link('a', '/rel.html', rel=[])])
        p1 = Page('my_url', base2, [Link('a', '/rel.html', rel=[])])
        self.assertNotEqual(p1, p2)

    def test_url_iter(self):
        s1 = base_url + '/some/doc.html'
        l1 = Link('a', s1, rel=[])
        s2 = external_base_url + '/another/doc.html'
        l2 = Link('a', s2, rel=[])
        s3 = 'relative/link.html'
        l3 = Link('a', s3, rel=[])
        s4 = external_base_url + '/some/image.png'
        l4 = Link('img', s4, rel=[])
        p = Page(example_url, base_url, (l1, l2, l3, l4))
        self.assertEqual(p.resource_urls, {'http:' + s4})
        self.assertEqual(p.internal_urls, {s1, base_url + '/' + s3})
        p = Page(example_url, external_base_url, (l1, l2, l3, l4))
        self.assertEqual(p.resource_urls, {s4})
        self.assertEqual(p.internal_urls, {s1})
