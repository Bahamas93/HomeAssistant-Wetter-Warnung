"""GeoSphere Warn API."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import aiohttp

from .const import API_URL


@dataclass(slots=True)
class Warning:
    """Eine Warnung für eine Gemeinde."""

    warnid: str
    level: int
    wtype: int
    start: datetime
    end: datetime


class GeoSphereApi:
    """API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        gkz: str,
    ) -> None:
        self._session = session
        self._gkz = str(gkz)

    async def async_get_warnings(self) -> list[Warning]:
        """Liefert alle Warnungen für die konfigurierte Gemeinde."""

        async with self._session.get(
            API_URL,
            headers={"accept": "application/json"},
        ) as response:
            response.raise_for_status()
            payload: dict[str, Any] = await response.json()

        warnings: list[Warning] = []

        for feature in payload.get("features", []):
            props = feature.get("properties", {})

            if self._gkz not in props.get("gemeinden", []):
                continue

            warnings.append(
                Warning(
                    warnid=props["warnid"],
                    level=int(props["wlevel"]),
                    wtype=int(props["wtype"]),
                    start=datetime.fromtimestamp(int(props["start"])),
                    end=datetime.fromtimestamp(int(props["end"])),
                )
            )

        return warnings
