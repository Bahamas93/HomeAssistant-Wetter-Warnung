from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class GeoSphereEntity(CoordinatorEntity):

    @property
    def device_info(self):

        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.gkz,
                )
            },
            manufacturer="GeoSphere Austria",
            name="GeoSphere Warnungen",
            model="Warning API",
            configuration_url="https://warnungen.zamg.at",
        )
