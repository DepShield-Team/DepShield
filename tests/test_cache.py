
import time
import unittest

from engine.cache import ResponseCache


class TestResponseCache(unittest.TestCase):

    def test_returns_stored_result(self):
        cache = ResponseCache()
        result = {"package": "requests", "status": "FOUND"}

        cache.set("requests", result)

        self.assertEqual(cache.get("requests"), result)

    def test_missing_key_returns_none(self):
        cache = ResponseCache()

        self.assertIsNone(cache.get("unknown-package"))

    def test_expired_entry_returns_none(self):
        cache = ResponseCache(ttl_seconds=1)
        cache.set("requests", {"status": "FOUND"})

        time.sleep(1.1)

        self.assertIsNone(cache.get("requests"))

    def test_clear_removes_entries(self):
        cache = ResponseCache()
        cache.set("requests", {"status": "FOUND"})

        cache.clear()

        self.assertIsNone(cache.get("requests"))

    def test_returned_result_cannot_modify_cached_result(self):
        cache = ResponseCache()
        cache.set("requests", {"status": "FOUND"})

        result = cache.get("requests")
        result["status"] = "CHANGED"

        self.assertEqual(cache.get("requests")["status"], "FOUND")


if __name__ == "__main__":
    unittest.main()
