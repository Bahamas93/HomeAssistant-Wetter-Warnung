"""API client for GeoSphere warnings."""

from __future__ import annotations

import aiohttp

from .const import API_URL, LEVELS, WARNING_TYPES


class GeoSphereApi:

    def __init__(
        self,
        session: aiohttp.ClientSession,
        gkz: str,
    ) -> None:

        self._session = session
        self._gkz = str(gkz)

    async def async_get_warning(self) -> dict:

        async with self._session.get(
            API_URL,
            headers={"accept": "application/json"},
        ) as response:

            response.raise_for_status()

            data = await response.json()

        warnings = []

        for feature in data.get("features", []):

            props = feature.get("properties", {})

            if self._gkz not in props.get("gemeinden", []):
                continue

            level = props.get("wlevel", 0)
            wtype = props.get("wtype", 0)

            warnings.append(
                {
                    "warnid": props.get("warnid"),
                    "level": level,
                    "color": LEVELS.get(level, "unknown"),
                    "type": wtype,
                    "type_name": WARNING_TYPES.get(
                        wtype,
                        f"Unknown ({wtype})",
                    ),
                    "start": int(props["start"]),
                    "end": int(props["end"]),
                }
            )

        if not warnings:
            return {
                "active": False,
                "highest_level": 0,
                "highest_color": "green",
                "highest_type": None,
                "highest_type_name": None,
                "warning_count": 0,
                "warnings": [],
            }

        highest = max(
            warnings,
            key=lambda warning: warning["level"],
        )

        return {
            "active": True,
            "highest_level": highest["level"],
            "highest_color": highest["color"],
            "highest_type": highest["type"],
            "highest_type_name": highest["type_name"],
            "warning_count": len(warnings),
            "warnings": warnings,
        }
