
import unittest
from unittest.mock import AsyncMock, patch

from engine.cache import ResponseCache
from engine.pipeline import verify_dependencies


class TestDependencyPipeline(unittest.IsolatedAsyncioTestCase):

    async def test_verifies_dependencies_and_preserves_line_numbers(self):
        dependencies = [
            {"package": "requests", "line": 2},
            {"package": "flask", "line": 5},
        ]

        fake_results = [
            {"package": "requests", "status": "FOUND"},
            {"package": "flask", "status": "NOT_FOUND"},
        ]

        with patch(
            "engine.pipeline.verify_pypi_package",
            new_callable=AsyncMock,
        ) as mock_verify:
            mock_verify.side_effect = fake_results

            results = await verify_dependencies(
                dependencies,
                session=None,
                cache=ResponseCache(),
            )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "FOUND")
        self.assertEqual(results[0]["line"], 2)
        self.assertEqual(results[1]["status"], "NOT_FOUND")
        self.assertEqual(results[1]["line"], 5)
        self.assertEqual(mock_verify.await_count, 2)


if __name__ == "__main__":
    unittest.main()
