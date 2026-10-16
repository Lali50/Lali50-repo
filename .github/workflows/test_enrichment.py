import unittest
from unittest.mock import patch

import main


SAMPLE_ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Critical ICS Advisory</title></head>
<body>
  <nav>Menu | Home | Contact</nav>
  <article>
    <h1>Critical Vulnerability Identified in Industrial Controllers</h1>
    <p>Security researchers and CERT teams across Central and Eastern Europe have confirmed active exploitation
    of a newly disclosed remote code execution flaw affecting industrial programmable logic controllers.</p>
    <p>According to technical telemetry released on Friday, unauthenticated threat actors can send crafted packets
    over TCP port 502 to overwrite firmware memory segments and disrupt substation automation workflows.</p>
    <p>Operators are strongly advised to segment operational technology networks immediately, apply vendor hotfixes
    prior to the upcoming maintenance window, and audit firewall rules for unauthorized external connections.</p>
  </article>
  <footer>Copyright 2026 Security News</footer>
</body>
</html>
"""


class TestSelectiveEnrichment(unittest.TestCase):

    def test_normalize_article_url_strips_tracking(self):
        raw = "https://www.Telex.hu/belfold/2026/10/16/teszt-cikk?utm_source=feed&utm_medium=rss&id=42#section1"
        norm = main.normalize_article_url(raw)
        self.assertEqual(norm, "https://telex.hu/belfold/2026/10/16/teszt-cikk?id=42")

    @patch("main.fetch_article_html")
    def test_enrich_short_rss_excerpt_from_webpage(self, mock_fetch):
        mock_fetch.return_value = (SAMPLE_ARTICLE_HTML, "ok", "HTTP 200")
        entry = {
            "link": "https://example.com/news/ics-flaw?utm_source=rss",
            "rss_text": "Short teaser sentence.",
            "rss_original_chars": 22,
            "rss_truncated": False,
            "rss_source_type": "rss_summary",
        }
        cache = {}
        result = main.enrich_article(entry, cache=cache, attempt_network=True)

        self.assertEqual(result["content_source"], "article_page")
        self.assertEqual(result["retrieval_status"], "success")
        self.assertGreater(result["supplied_chars"], 250)
        self.assertIn("programmable logic controllers", result["text"])
        self.assertIn("https://example.com/news/ics-flaw", cache)

    @patch("main.fetch_article_html")
    def test_cache_hit_does_not_refetch_network(self, mock_fetch):
        norm_url = main.normalize_article_url("https://example.com/news/cached-story")
        cached_text = " ".join(["Detailed cached article paragraph with plenty of analytical depth."] * 15)
        cache = {
            norm_url: {
                "fetched_at": 9999999999.0,
                "extracted_chars": len(cached_text),
                "text": cached_text,
            }
        }
        entry = {
            "link": "https://example.com/news/cached-story?utm_campaign=daily",
            "rss_text": "Short teaser.",
            "rss_original_chars": 13,
            "rss_truncated": False,
            "rss_source_type": "rss_summary",
        }
        result = main.enrich_article(entry, cache=cache, attempt_network=True)

        mock_fetch.assert_not_called()
        self.assertEqual(result["content_source"], "article_page")
        self.assertEqual(result["retrieval_status"], "cached")
        self.assertEqual(result["text"], cached_text)

    @patch("main.fetch_article_html")
    def test_restricted_or_blocked_page_falls_back_to_rss(self, mock_fetch):
        mock_fetch.return_value = (None, "restricted", "HTTP 403")
        entry = {
            "link": "https://paywalled.example.com/article",
            "rss_text": "Original RSS summary stays intact on 403.",
            "rss_original_chars": 41,
            "rss_truncated": False,
            "rss_source_type": "rss_summary",
        }
        result = main.enrich_article(entry, cache={}, attempt_network=True)

        self.assertEqual(result["content_source"], "rss_summary")
        self.assertEqual(result["retrieval_status"], "restricted")
        self.assertEqual(result["text"], "Original RSS summary stays intact on 403.")

    def test_selection_skips_substantial_rss_content(self):
        long_rss = "A" * (main.MIN_FEED_EXCERPT_CHARS + 200)
        candidates = [
            {
                "category": "Global Cyber & Threat Intel",
                "title": "Full Substack Essay",
                "link": "https://newsletter.threat.dev/p/full-post",
                "timestamp": 1700000000.0,
                "rss_text": long_rss,
                "rss_original_chars": len(long_rss),
                "rss_truncated": False,
                "rss_source_type": "rss_content",
            },
            {
                "category": "Hungarian Core & Geoeconomics",
                "title": "Short Telex Teaser",
                "link": "https://telex.hu/belfold/short-teaser",
                "timestamp": 1700000100.0,
                "rss_text": "Two sentence excerpt.",
                "rss_original_chars": 21,
                "rss_truncated": False,
                "rss_source_type": "rss_summary",
            },
        ]
        net_indices, cache_indices = main.select_enrichment_candidates(
            candidates,
            profile_data={"enabled": False},
            cache={},
            max_to_enrich=10,
        )
        self.assertEqual(net_indices, {1})
        self.assertEqual(cache_indices, set())


if __name__ == "__main__":
    unittest.main()
