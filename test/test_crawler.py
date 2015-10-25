from unittest import TestCase
from unittest.mock import patch, Mock
import os
import asyncio
from urllib.parse import urlparse
from aiohttp import ClientSession

from aranea.crawler import crawl, get_page


def ready_future(result, loop):
    f = asyncio.Future(loop=loop)
    f.set_result(result)
    return f

url = 'http://example.com/index.html'
here = os.path.abspath(os.path.dirname(__file__))


class FileGetter:
    def __init__(self, domain, path):
        self.domain = domain
        self.path = path

    def get(self, url_string):
        url = urlparse(url_string)
        if url.netloc == self.domain:
            # FIXME: handle index.html on getting dir here!
            path = os.path.join(here, self.path, *url.path.split('/'))
            with open(path) as f:
                return f.read()
        else:
            raise KeyError('{!r} external to {!r}'.format(
                url_string, self.domain))


class TestCrawler(TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def _make_client(self, url, status, data):
        mock_client = Mock(spec=ClientSession)

        def get(requested_url):
            self.assertEqual(requested_url, url)
            # This mock is sadly rather permissive. A real response would have
            # been better, but aiohttp appears quite hard to mock:
            response = Mock(
                status=status, read=lambda: ready_future(data, self.loop))
            return ready_future(response, self.loop)
        mock_client.get.side_effect = get
        return mock_client

    def test_get_page_success(self):
        client = self._make_client(url, 200, 'hello world')
        data = self.loop.run_until_complete(get_page(client, url))
        self.assertEqual(data, 'hello world')

    def test_get_page_failure(self):
        client = self._make_client(url, 404, '')
        self.assertRaises(
            ValueError, self.loop.run_until_complete, get_page(client, url))


    @patch('aranea.crawler.get_page')
    def test_crawl(self, mock_get_page):
        # NB: this is far more of an integration test than a unit test. Breaking
        # it down into more unit-like elements might be a good idea.
        # We crawl the entirety of a dump of documentation from the internet
        file_getter = FileGetter(
            'aiohttp.readthedocs.org', 'aiohttp.readthedocs.org')
        mock_get_page.side_effect = asyncio.coroutine(
            lambda client, url: file_getter.get(url))
        pages = self.loop.run_until_complete(crawl(
            None, 'http://aiohttp.readthedocs.org/en/stable/index.html',
            loop=self.loop))
        self.assertEqual(
            pages['http://aiohttp.readthedocs.org/en/stable/index.html'],
            pages['http://aiohttp.readthedocs.org/en/stable/'])
