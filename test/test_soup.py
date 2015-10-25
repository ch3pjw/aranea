from unittest import TestCase
from collections import Sequence
import os

from aranea.soup import make_page


class TestSoup(TestCase):
    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(here, 'fictional.example.com', 'index.html')
        with open(path) as f:
            cls.index = f.read()

    def test_make_soup(self):
        base_url = 'http://fictional.example.com'
        page = make_page(base_url + '/index.html', self.index)
        self.assertEqual(page.urls, {
            base_url + '/index.html',  # From '#' anchor
            base_url + '/relative.html',
            base_url + '/static/myicon.ico',
            'http://default.scheme.com/path/index.html',
            base_url + '/next_page.html',
            base_url + '/static/foo.png',
            base_url + '/static/myscript.js',
            base_url + '/absolute/within/domain.html',
            base_url + '/static/mystyle.css',
            'http://external.domain.com/path/index.html'}
        )
        for link in page.links:
            self.assertIsInstance(link.rel, Sequence)
