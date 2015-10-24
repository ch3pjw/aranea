from unittest import TestCase

from aranea.links import Link


class TestLinks(TestCase):
    internal_domain = 'example.com'
    base_url = 'http://' + internal_domain
    example_url = base_url + '/path'
    external_domain = 'another-domain.com'
    external_base_url = '//' + external_domain

    def test_str(self):
        l = Link('a', self.example_url, rel=None)
        self.assertEqual(str(l), self.example_url)

    def test_is_resource(self):
        l = Link('a', self.example_url, rel=None)
        self.assertFalse(l.is_resource())
        l = Link('link', self.example_url, rel='next')
        self.assertFalse(l.is_resource())
        l = Link('link', self.example_url, rel='stylesheet')
        self.assertTrue(l.is_resource())
        l = Link('img', self.example_url, rel=None)
        self.assertTrue(l.is_resource())
        # NB: we could exhaustively check combinations of tag_type and rel, but
        # we'd pretty much just be checking that the code was how we wrote it,
        # which doesn't offer much of a useful check.

    def test_is_internal(self):
        l = Link('a', self.example_url + '/sub_path', rel=None)
        self.assertTrue(l.is_internal(self.internal_domain, ''))
        self.assertFalse(l.is_internal(self.external_domain, ''))
        self.assertTrue(l.is_internal(self.internal_domain, '//ignored.com'))
        self.assertFalse(l.is_internal(self.external_domain, '//ignored.com'))
        l = Link('a', '/root/relative', rel=None)
        self.assertTrue(l.is_internal(self.internal_domain, self.base_url))
        self.assertFalse(l.is_internal(
            self.internal_domain, self.external_base_url))
        # NB: we have to be careful that we're not just testing urljoin's logic
        # for resolving relative paths!
