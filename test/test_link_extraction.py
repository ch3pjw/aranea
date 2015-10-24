from unittest import TestCase
import os
from urllib.parse import urlparse

from aranea.link_extraction import (
    extract_links, classify_url, UrlType, resolve)


class TestLinkExtraction(TestCase):
    urls = {
        UrlType.absolute: 'http://external.domain.com/path/index.html',
        UrlType.root_relative: 'relative.html',
        UrlType.document_relative: '/absolute/within/domain.html',
        UrlType.schema_agnostic: '//default.scheme.com/path/index.html',
    }

    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(here, 'fictional.example.com', 'index.html')
        with open(path) as f:
            cls.index = f.read()

    def test_extract_links(self):
        self.assertEqual(list(extract_links(self.index)), [])

    def test_classify_url(self):
        for url_type, url_string in self.urls:
            self.assertEqual(classify(urlparse(url_string)), url_type)
