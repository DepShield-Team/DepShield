
import time
from typing import Any


CACHE_TTL_SECONDS = 24 * 60 * 60  # 24 hours


class ResponseCache:
    """Simple in-memory cache with a time-to-live for each entry."""

    def __init__(self, ttl_seconds: int = CACHE_TTL_SECONDS):
        if ttl_seconds <= 0:
            raise ValueError("TTL must be greater than zero.")

        self.ttl_seconds = ttl_seconds
        self._entries: dict[str, tuple[float, dict[str, Any]]] = {}

    def get(self, key: str) -> dict[str, Any] | None:
        """Return a cached result, or None if missing or expired."""
        entry = self._entries.get(key)

        if entry is None:
            return None

        expires_at, result = entry

        if time.monotonic() >= expires_at:
            del self._entries[key]
            return None

        # Return a copy so callers cannot modify the cached result.
        return result.copy()

    def set(self, key: str, result: dict[str, Any]) -> None:
        """Store a result until its TTL expires."""
        expires_at = time.monotonic() + self.ttl_seconds
        self._entries[key] = (expires_at, result.copy())

    def clear(self) -> None:
        """Remove all cached entries."""
        self._entries.clear()
