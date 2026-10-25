
import asyncio

from engine.verifier import verify_pypi_package
from engine.cache import ResponseCache


async def verify_dependencies(
    dependencies: list[dict],
    session,
    cache: ResponseCache,
) -> list[dict]:
    """Verify parsed dependencies concurrently."""

    tasks = [
        verify_pypi_package(item["package"], session, cache)
        for item in dependencies
    ]

    results = await asyncio.gather(*tasks)

    # Keep the original source line with each verification result.
    for dependency, result in zip(dependencies, results):
        result["line"] = dependency["line"]

    return results
