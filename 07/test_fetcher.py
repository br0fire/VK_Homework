import asyncio
import unittest
from unittest.mock import Mock, patch
from io import StringIO
from fetcher import fetch_all


class TestFetcher(unittest.TestCase):

    def test_fetch_all(self):
        mock_session = Mock()
        mock_session.get.return_value.text.return_value = \
            "<html><body><p>hello world</p></body></html>"
        mock_session.get.return_value.status = 200

        with patch('aiohttp.ClientSession', return_value=mock_session):
            urls_file = StringIO("http://example.com\nhttps://example.org")
            num_workers = 2
            k = 3

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(fetch_all(urls_file,
                                                       num_workers, k))

            self.assertEqual(result, None)
            mock_session.get.assert_any_call("http://example.com", timeout=5)
            mock_session.get.assert_any_call("https://example.org", timeout=5)


if __name__ == '__main__':
    unittest.main()
