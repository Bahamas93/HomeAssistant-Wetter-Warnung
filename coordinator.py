from __future__ import annotations

import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import GeoSphereApi
from .const import UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class GeoSphereCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, gkz):

        self.gkz = gkz

        self.api = GeoSphereApi(
            async_get_clientsession(hass),
            gkz,
        )

        super().__init__(
            hass,
            _LOGGER,
            name="GeoSphere",
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):

        try:
            return await self.api.async_get_warning()

        except Exception as err:
            raise UpdateFailed(err) from err
