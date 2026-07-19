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

from .const import DOMAIN, WARNING_TYPES
from .entity import GeoSphereEntity


@dataclass(frozen=True, kw_only=True)
class GeoSphereBinarySensorDescription(BinarySensorEntityDescription):
    """GeoSphere binary sensor description."""

    warning_type: int


DESCRIPTIONS: tuple[GeoSphereBinarySensorDescription, ...] = (
    GeoSphereBinarySensorDescription(
        key="wind",
        name="Wind",
        warning_type=1,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:weather-windy",
    ),
    GeoSphereBinarySensorDescription(
        key="snow",
        name="Snow",
        warning_type=2,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:snowflake",
    ),
    GeoSphereBinarySensorDescription(
        key="rain",
        name="Rain",
        warning_type=3,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:weather-rainy",
    ),
    GeoSphereBinarySensorDescription(
        key="cold",
        name="Cold",
        warning_type=4,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:thermometer-low",
    ),
    GeoSphereBinarySensorDescription(
        key="thunderstorm",
        name="Thunderstorm",
        warning_type=5,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:weather-lightning",
    ),
    GeoSphereBinarySensorDescription(
        key="heat",
        name="Heat",
        warning_type=6,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:thermometer-high",
    ),
    GeoSphereBinarySensorDescription(
        key="ice",
        name="Ice",
        warning_type=7,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:snowflake-alert",
    ),
    GeoSphereBinarySensorDescription(
        key="fog",
        name="Fog",
        warning_type=8,
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:weather-fog",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GeoSphere binary sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        GeoSphereBinarySensor(coordinator, description)
        for description in DESCRIPTIONS
    )


class GeoSphereBinarySensor(
    GeoSphereEntity,
    BinarySensorEntity,
):
    """GeoSphere binary sensor."""

    entity_description: GeoSphereBinarySensorDescription

    def __init__(self, coordinator, description) -> None:
        """Initialize binary sensor."""

        super().__init__(coordinator)

        self.entity_description = description

        self._attr_unique_id = (
            f"{coordinator.gkz}_{description.key}"
        )

    @property
    def is_on(self) -> bool:
        """Return True if this warning type is active."""

        return any(
            warning.wtype == self.entity_description.warning_type
            for warning in self.warnings
        )
