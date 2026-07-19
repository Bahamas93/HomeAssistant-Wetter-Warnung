"""Base entity for GeoSphere Warn."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL


class GeoSphereEntity(CoordinatorEntity):
    """Base GeoSphere entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator) -> None:
        """Initialize entity."""
        super().__init__(coordinator)

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    coordinator.gkz,
                )
            },
            manufacturer=MANUFACTURER,
            model=MODEL,
            name=f"GeoSphere {coordinator.gkz}",
            configuration_url="https://warnungen.zamg.at",
        )

    @property
    def available(self) -> bool:
        """Return True if coordinator has data."""
        return self.coordinator.last_update_success

    @property
    def status(self):
        """Shortcut to the current warning status."""
        return self.coordinator.data

    @property
    def highest(self):
        """Return highest warning."""
        return self.status.highest

    @property
    def warnings(self):
        """Return all warnings."""
        return self.status.warnings

    @property
    def extra_state_attributes(self):
        """Common attributes."""

        if self.highest is None:
            return {
                "active": False,
                "warning_count": 0,
            }

        return {
            "active": self.status.active,
            "warning_count": self.status.count,
            "warnid": self.highest.warnid,
            "level": self.highest.level,
            "level_name": self.highest.level_name,
            "type": self.highest.wtype,
            "start": self.highest.start.isoformat(),
            "end": self.highest.end.isoformat(),
        }
