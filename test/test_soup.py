from unittest import TestCase
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
        page = make_page(
            'http://fictional.example.com/index.html', self.index)
        self.assertEqual(page.urls, {
            '',  # FIXME: weed out empty anchor
            'relative.html',
            '_static/aiohttp-icon.ico',
            '//default.scheme.com/path/index.html',
            'client.html',
            'static/foo.png',
            'static/myscript.js',
            '/absolute/within/domain.html',
            'static/mystyle.css',
            'http://external.domain.com/path/index.html'}
        )
