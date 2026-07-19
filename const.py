"""Constants for the GeoSphere Warn integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "geosphere_warn"

CONF_GKZ = "gkz"

DEFAULT_NAME = "GeoSphere Warn"

API_URL = "https://warnungen.zamg.at/wsapp/api/getWarnstatus"

UPDATE_INTERVAL = timedelta(minutes=5)

MANUFACTURER = "GeoSphere Austria"

MODEL = "Weather Warning API"

ATTR_WARNINGS = "warnings"
ATTR_WARNING_COUNT = "warning_count"
ATTR_HIGHEST = "highest"

LEVEL_GREEN = 0
LEVEL_YELLOW = 1
LEVEL_ORANGE = 2
LEVEL_RED = 3

LEVEL_NAMES = {
    LEVEL_GREEN: "green",
    LEVEL_YELLOW: "yellow",
    LEVEL_ORANGE: "orange",
    LEVEL_RED: "red",
}

LEVEL_ICONS = {
    LEVEL_GREEN: "mdi:shield-check",
    LEVEL_YELLOW: "mdi:alert",
    LEVEL_ORANGE: "mdi:alert-outline",
    LEVEL_RED: "mdi:alert-octagon",
}

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
