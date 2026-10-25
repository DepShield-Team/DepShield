
import unittest
from unittest.mock import AsyncMock

import aiohttp

from engine.cache import ResponseCache
from engine.verifier import verify_pypi_package


class FakeResponse:
    def __init__(self, status, data=None):
        self.status = status
        self.data = data or {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return False

    async def json(self):
        return self.data


class TestPyPIVerifier(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.cache = ResponseCache()
        self.session = unittest.mock.MagicMock()

    async def test_existing_package(self):
        self.session.get.return_value = FakeResponse(
            200,
            {
                "info": {
                    "version": "2.32.0",
                    "summary": "Python HTTP library",
                }
            },
        )

        result = await verify_pypi_package(
            "requests", self.session, self.cache
        )

        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["package"], "requests")
        self.assertEqual(result["version"], "2.32.0")

    async def test_missing_package_returns_not_found(self):
        self.session.get.return_value = FakeResponse(404)

        result = await verify_pypi_package(
            "nonexistent-package-xyz-123", self.session, self.cache
        )

        self.assertEqual(result["status"], "NOT_FOUND")

    async def test_cached_result_avoids_second_request(self):
        self.session.get.return_value = FakeResponse(
            200, {"info": {"version": "1.0", "summary": "Test"}}
        )

        first = await verify_pypi_package(
            "requests", self.session, self.cache
        )
        second = await verify_pypi_package(
            "requests", self.session, self.cache
        )

        self.assertEqual(first, second)
        self.assertEqual(self.session.get.call_count, 1)

    async def test_network_error_returns_registry_error(self):
        self.session.get.side_effect = aiohttp.ClientError("Network failed")

        result = await verify_pypi_package(
            "requests", self.session, self.cache
        )

        self.assertEqual(result["status"], "REGISTRY_ERROR")

    async def test_package_name_is_normalized(self):
        self.session.get.return_value = FakeResponse(
            200, {"info": {"version": "1.0", "summary": "Test"}}
        )

        result = await verify_pypi_package(
            "  Requests  ", self.session, self.cache
        )

        self.assertEqual(result["package"], "requests")


if __name__ == "__main__":
    unittest.main()
