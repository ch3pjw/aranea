from unittest import TestCase
from unittest.mock import patch, Mock
import asyncio
from aiohttp import ClientSession

from aranea.crawler import crawl, get_page


def ready_future(result, loop):
    f = asyncio.Future(loop=loop)
    f.set_result(result)
    return f

url = 'http://example.com/index.html'


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
        raise NotImplementedError()
