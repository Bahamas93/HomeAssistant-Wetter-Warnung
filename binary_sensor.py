"""Binary sensor platform for GeoSphere Warn."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import GeoSphereEntity


@dataclass(frozen=True, kw_only=True)
class GeoSphereBinarySensorDescription(BinarySensorEntityDescription):
    """GeoSphere binary sensor description."""

    warning_type: int


WARNING_TYPES = {
    1: "wind",
    2: "snow",
    3: "rain",
    4: "cold",
    5: "thunderstorm",
    6: "heat",
    7: "ice",
    8: "fog",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for wtype, name in WARNING_TYPES.items():

        entities.append(
            GeoSphereBinarySensor(
                coordinator,
                GeoSphereBinarySensorDescription(
                    key=name,
                    name=name.replace("_", " ").title(),
                    warning_type=wtype,
                    device_class=BinarySensorDeviceClass.PROBLEM,
                    icon="mdi:alert",
                ),
            )
        )

    async_add_entities(entities)


class GeoSphereBinarySensor(
    GeoSphereEntity,
    BinarySensorEntity,
):

    entity_description: GeoSphereBinarySensorDescription

    def __init__(
        self,
        coordinator,
        description,
    ) -> None:

        super().__init__(coordinator)

        self.entity_description = description

        self._attr_unique_id = (
            f"{coordinator.gkz}_{description.key}"
        )

    @property
    def is_on(self) -> bool:

        for warning in self.coordinator.data["warnings"]:

            if warning["type"] == self.entity_description.warning_type:
                return True

        return False

    @property
    def extra_state_attributes(self):

        return {
            "warnings": self.coordinator.data["warnings"],
        }
