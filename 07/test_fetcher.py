import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from fetcher import fetch_url, run_worker, fetch_all


class TestFetcher(unittest.TestCase):
    def setUp(self):
        self.html_content = "<html><body>This is a test page</body></html>"

    @patch('aiohttp.ClientSession.get')
    @patch('aiohttp.ClientSession.__aenter__')
    @patch('aiohttp.ClientSession.__aexit__')
    async def test_fetch_url(self, mock_aexit, mock_aenter, mock_get):
        mock_aenter.return_value = AsyncMock()
        mock_aexit.return_value = AsyncMock()
        mock_get.return_value.__aenter__.return_value.text.return_value \
            = self.html_content

        url = 'https://example.com'
        result = await fetch_url(url, 3)

        mock_aenter.assert_called_once()
        mock_aexit.assert_called_once()
        mock_get.assert_called_once_with(url, timeout=5)
        self.assertEqual(result, '{"this": 1, "is": 1, "a": 1}')

    @patch('asyncio.Queue.get')
    @patch('asyncio.Queue.join')
    async def test_run_worker(self, mock_join, mock_get):
        queue = MagicMock()
        queue.get.side_effect = ['https://example.com', asyncio.CancelledError]

        await run_worker(queue, 3)

        mock_get.assert_called_with()
        mock_join.assert_called_once()

    @patch('asyncio.Queue.put_nowait')
    @patch('asyncio.create_task')
    @patch('aiohttp.ClientSession.__aenter__')
    @patch('aiohttp.ClientSession.__aexit__')
    async def test_fetch_all(self, mock_aexit, mock_aenter,
                             mock_create_task, mock_put_nowait):
        mock_aenter.return_value = AsyncMock()
        mock_aexit.return_value = AsyncMock()
        mock_create_task.return_value = MagicMock()

        urls_file = ['https://example.com', 'https://example.org']
        num_w = 2

        await fetch_all(urls_file, num_w, 3)

        mock_aenter.assert_called_once()
        mock_aexit.assert_called_once()
        mock_put_nowait.assert_any_call('https://example.com')
        mock_put_nowait.assert_any_call('https://example.org')
        self.assertEqual(mock_put_nowait.call_count, 2)
        self.assertEqual(mock_create_task.call_count, 2)


if __name__ == '__main__':
    asyncio.run(unittest.main())
