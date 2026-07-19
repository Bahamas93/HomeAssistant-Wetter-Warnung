"""Sensor platform for GeoSphere Warn."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import GeoSphereEntity


@dataclass(frozen=True, kw_only=True)
class GeoSphereSensorDescription(SensorEntityDescription):
    """GeoSphere sensor description."""

    value_fn: Callable[[dict[str, Any]], Any]


SENSORS = (
    GeoSphereSensorDescription(
        key="highest_level",
        name="Warning Level",
        icon="mdi:alert",
        value_fn=lambda data: data["highest_level"],
    ),
    GeoSphereSensorDescription(
        key="highest_color",
        name="Warning Color",
        icon="mdi:palette",
        value_fn=lambda data: data["highest_color"],
    ),
    GeoSphereSensorDescription(
        key="highest_type",
        name="Warning Type",
        icon="mdi:weather-lightning",
        value_fn=lambda data: data["highest_type"],
    ),
    GeoSphereSensorDescription(
        key="warning_count",
        name="Warning Count",
        icon="mdi:counter",
        value_fn=lambda data: data["warning_count"],
    ),
    GeoSphereSensorDescription(
        key="warning_start",
        name="Warning Start",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: (
            datetime.fromtimestamp(data["warnings"][0]["start"])
            if data["warnings"]
            else None
        ),
    ),
    GeoSphereSensorDescription(
        key="warning_end",
        name="Warning End",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: (
            datetime.fromtimestamp(data["warnings"][0]["end"])
            if data["warnings"]
            else None
        ),
    ),
)
