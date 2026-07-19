"""GeoSphere Warn API."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import aiohttp

from .const import API_URL, LEVEL_NAMES


@dataclass(slots=True)
class Warning:
    """Eine einzelne Warnung."""

    warnid: str
    level: int
    level_name: str
    wtype: int
    start: datetime
    end: datetime


@dataclass(slots=True)
class WarningStatus:
    """Alle Warnungen der Gemeinde."""

    active: bool
    highest: Warning | None
    warnings: list[Warning]

    @property
    def count(self) -> int:
        return len(self.warnings)


class GeoSphereApi:
    """GeoSphere API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        gkz: str,
    ) -> None:

        self._session = session
        self._gkz = str(gkz)

    async def async_get_warnings(self) -> WarningStatus:
        """Liest alle Warnungen für die konfigurierte Gemeinde."""

        async with self._session.get(
            API_URL,
            headers={"accept": "application/json"},
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:

            response.raise_for_status()

            payload: dict[str, Any] = await response.json()

        warnings: list[Warning] = []

        for feature in payload.get("features", []):

            props = feature.get("properties", {})

            if self._gkz not in props.get("gemeinden", []):
                continue

            level = int(props.get("wlevel", 0))

            warnings.append(
                Warning(
                    warnid=props["warnid"],
                    level=level,
                    level_name=LEVEL_NAMES.get(level, "unknown"),
                    wtype=int(props["wtype"]),
                    start=datetime.fromtimestamp(
                        int(props["start"])
                    ),
                    end=datetime.fromtimestamp(
                        int(props["end"])
                    ),
                )
            )

        if warnings:

            highest = max(
                warnings,
                key=lambda warning: warning.level,
            )

        else:

            highest = None

        return WarningStatus(
            active=bool(warnings),
            highest=highest,
            warnings=warnings,
        )
