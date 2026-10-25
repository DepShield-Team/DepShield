
import aiohttp
from urllib.parse import quote

from engine.cache import ResponseCache


PYPI_API_URL = "https://pypi.org/pypi/{}/json"


async def verify_pypi_package(
    package_name: str,
    session: aiohttp.ClientSession,
    cache: ResponseCache,
) -> dict:
    """Verify whether a package exists on PyPI."""

    # Step 1: Normalize the package name.
    package_name = package_name.strip().lower()

    if not package_name:
        return {
            "package": package_name,
            "status": "REGISTRY_ERROR",
            "message": "Package name cannot be empty.",
        }

    # Step 2: Check the cache before making an HTTP request.
    cache_key = f"pypi:{package_name}"
    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return cached_result

    # Step 3: Construct the PyPI API URL.
    encoded_name = quote(package_name, safe="")
    url = PYPI_API_URL.format(encoded_name)

    try:
        # Step 4: Send an asynchronous HTTP request.
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:

            if response.status == 200:
                data = await response.json()
                info = data.get("info", {})

                result = {
                    "package": package_name,
                    "status": "FOUND",
                    "version": info.get("version"),
                    "summary": info.get("summary"),
                }

            elif response.status == 404:
                result = {
                    "package": package_name,
                    "status": "NOT_FOUND",
                    "message": "Package does not exist on PyPI.",
                }

            else:
                return {
                    "package": package_name,
                    "status": "REGISTRY_ERROR",
                    "message": f"PyPI returned HTTP {response.status}.",
                }

    except (aiohttp.ClientError, TimeoutError, ValueError) as error:
        return {
            "package": package_name,
            "status": "REGISTRY_ERROR",
            "message": str(error),
        }

    # Step 5: Cache only successful, conclusive results.
    cache.set(cache_key, result)

    return result
