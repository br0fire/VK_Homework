import asyncio
import unittest
from unittest.mock import MagicMock, patch
from fetcher import fetch_url, run_worker, fetch_all
# from asynctest import CoroutineMock
import aiohttp

from io import StringIO

class TestFetcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.html_content = "<html><body>This is a test page</body></html>"

    async def test_fetch_url(self):
        mock = aiohttp.ClientSession
        mock.get = MagicMock()
        mock.get.return_value.__aenter__.return_value.status = 200
        mock.get.return_value.__aenter__.return_value.text.return_value = self.html_content

        url = 'https://example.com'
        result = await fetch_url(mock, url, 3)
        self.assertEqual(result[1], {"this": 1, "is": 1, "a": 1})

    @patch("fetcher.fetch_url")
    @patch('aiohttp.ClientSession')
    async def test_run_worker(self, mock_session,mock_fetch_url):
        url = "example.org"
        queue = asyncio.Queue()
        mock_fetch_url.return_value = (url, {"this": 1, "is": 1, "a": 1})

        with patch('sys.stdout', new=StringIO()) as fake_out:
            task = asyncio.create_task(run_worker(mock_session, queue, 3))
            await queue.put(url)
            await queue.join()
            self.assertEqual(fake_out.getvalue(), f"{url}: {{\"this\": 1, \"is\": 1, \"a\": 1}}\n")
            mock_fetch_url.assert_called_once_with(mock_session, url, 3)
        task.cancel()

    @patch("fetcher.fetch_url")
    @patch('aiohttp.ClientSession')
    async def test_run_worker_error(self, mock_session, mock_fetch_url):
        url = "example.org"
        queue = asyncio.Queue()
        error_message = "404 Not Found"
        mock_fetch_url.side_effect = Exception(error_message)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            task = asyncio.create_task(run_worker(mock_session, queue, 3))

            await queue.put(url)
            await queue.join()
            url = "example.org"
            mock_fetch_url.assert_called_once_with(mock_session, url, 3)
            self.assertEqual(f"Error processing URL {url}: {error_message}\n", fake_out.getvalue())
        task.cancel()

        


if __name__ == '__main__':
    asyncio.run(unittest.main())
