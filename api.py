"""GeoSphere Warn API."""

from __future__ import annotations

from typing import Any

import aiohttp

from .const import API_URL, LEVELS


class GeoSphereApi:
    """Client for the GeoSphere warning API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        gkz: str,
    ) -> None:
        self._session = session
        self._gkz = str(gkz)

    async def async_get_warnings(self) -> dict[str, Any]:
        """Return all warnings for the configured municipality."""

        async with self._session.get(
            API_URL,
            headers={"accept": "application/json"},
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:

            response.raise_for_status()

            payload = await response.json()

        warnings: list[dict[str, Any]] = []

        for feature in payload.get("features", []):

            properties = feature.get("properties", {})

            if self._gkz not in properties.get("gemeinden", []):
                continue

            level = int(properties.get("wlevel", 0))

            warning = {
                "warnid": properties.get("warnid"),
                "type": int(properties.get("wtype", 0)),
                "level": level,
                "color": LEVELS.get(level, "unknown"),
                "start": int(properties.get("start", 0)),
                "end": int(properties.get("end", 0)),
            }

            warnings.append(warning)

        if not warnings:

            return {
                "active": False,
                "highest_level": 0,
                "highest_color": "green",
                "highest_type": None,
                "warning_count": 0,
                "warnings": [],
            }

        highest = max(
            warnings,
            key=lambda item: item["level"],
        )

        return {
            "active": True,
            "highest_level": highest["level"],
            "highest_color": highest["color"],
            "highest_type": highest["type"],
            "warning_count": len(warnings),
            "warnings": warnings,
        }
