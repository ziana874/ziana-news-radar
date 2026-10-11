"""Offline smoke tests; no news is fabricated or committed."""
import importlib.util
import json
import os
import sys
import time
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

try:
    import feedparser  # noqa: F401
except ImportError:
    sys.modules['feedparser'] = types.SimpleNamespace(parse=lambda _: None)

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('news_update', ROOT/'src'/'update.py')
news = importlib.util.module_from_spec(spec)
spec.loader.exec_module(news)

class Tests(unittest.TestCase):
    def test_sources(self):
        feeds = json.loads((ROOT/'feeds.json').read_text())
        self.assertEqual(len(feeds), 20)
        self.assertEqual(set(x['category'] for x in feeds), set(news.GROUPS))
        self.assertTrue(all(x['url'].startswith('https://') for x in feeds))

    def test_canonical_drops_trackers_but_keeps_ids(self):
        self.assertEqual(news.canonical('https://EXAMPLE.com/a?utm_source=foo&id=123&fbclid=abc'), 'https://example.com/a?id=123')
        self.assertEqual(news.canonical('javascript:alert(1)'), '')

    def test_html_stripping(self):
        self.assertEqual(news.clean_text('<h2>新闻</h2><script>evil()</script>'), '新闻')

    def test_feed_parse_without_external_network(self):
        entry = {'title': 'Australian skilled visa changes announced',
                 'link': 'https://example.com/visa?id=2&utm_medium=rss',
                 'summary': '<p>Policy proposal; effective date not confirmed.</p>',
                 'published_parsed': time.gmtime()}
        resp = Mock(status_code=200, content=b'<rss/>')
        resp.raise_for_status.return_value = None
        parsed = types.SimpleNamespace(entries=[entry])
        source = {'category': 'immigration', 'name': 'Test source', 'url':'https://example.com/rss', 'kind': 'index'}
        with patch.object(news.requests, 'get', return_value=resp), patch.object(news.feedparser, 'parse', return_value=parsed):
            items, stats = news.parse_source(source)
        self.assertTrue(stats['ok'])
        self.assertEqual(items[0]['policy_status'], '待核验')
        self.assertEqual(items[0]['url'], 'https://example.com/visa?id=2')
        self.assertFalse(items[0]['ai_generated'])

    def test_ai_without_key_does_not_pretend_chinese_summary(self):
        with patch.dict(os.environ, {'GEMINI_API_KEY': ''}):
            result = news.ai_summarize([])
        self.assertFalse(result['enabled'])
        self.assertFalse(result['succeeded'])

if __name__ == '__main__':
    unittest.main()
