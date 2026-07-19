"""DataUpdateCoordinator for GeoSphere Warn."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import GeoSphereApi
from .const import DOMAIN, CONF_GKZ, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class GeoSphereWarnCoordinator(DataUpdateCoordinator):
    """Coordinator for GeoSphere warning data."""

    def __init__(self, hass: HomeAssistant, gkz: str) -> None:
        """Initialize coordinator."""

        self.api = GeoSphereApi(
            async_get_clientsession(hass),
            gkz,
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from GeoSphere."""

        try:
            return await self.api.async_get_warning()

        except Exception as err:
            raise UpdateFailed(err) from err
