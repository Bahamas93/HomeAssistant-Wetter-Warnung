"""Sensor platform for GeoSphere Warn."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN

LEVELS = {
    0: "green",
    1: "yellow",
    2: "orange",
    3: "red",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            WarningLevelSensor(coordinator),
            WarningColorSensor(coordinator),
            WarningTypeSensor(coordinator),
            WarningCountSensor(coordinator),
            WarningStartSensor(coordinator),
            WarningEndSensor(coordinator),
        ]
    )


class BaseWarningSensor(CoordinatorEntity, SensorEntity):

    _attr_has_entity_name = True

    def __init__(self, coordinator):

        super().__init__(coordinator)


class WarningLevelSensor(BaseWarningSensor):

    _attr_name = "Level"
    _attr_unique_id = "geosphere_warning_level"

    @property
    def native_value(self):

        return self.coordinator.data["highest_level"]


class WarningColorSensor(BaseWarningSensor):

    _attr_name = "Color"
    _attr_unique_id = "geosphere_warning_color"

    @property
    def native_value(self):

        return self.coordinator.data["highest_color"]


class WarningTypeSensor(BaseWarningSensor):

    _attr_name = "Type"
    _attr_unique_id = "geosphere_warning_type"

    @property
    def native_value(self):

        return self.coordinator.data["highest_type_name"]


class WarningCountSensor(BaseWarningSensor):

    _attr_name = "Warning Count"
    _attr_unique_id = "geosphere_warning_count"

    @property
    def native_value(self):

        return self.coordinator.data["warning_count"]


class WarningStartSensor(BaseWarningSensor):

    _attr_name = "Start"
    _attr_unique_id = "geosphere_warning_start"
    _attr_device_class = "timestamp"

    @property
    def native_value(self):

        warnings = self.coordinator.data["warnings"]

        if not warnings:
            return None

        return datetime.fromtimestamp(warnings[0]["start"])


class WarningEndSensor(BaseWarningSensor):

    _attr_name = "End"
    _attr_unique_id = "geosphere_warning_end"
    _attr_device_class = "timestamp"

    @property
    def native_value(self):

        warnings = self.coordinator.data["warnings"]

        if not warnings:
            return None

        return datetime.fromtimestamp(warnings[0]["end"])
