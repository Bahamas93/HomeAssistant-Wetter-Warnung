DOMAIN = "geosphere_warn"

CONF_GKZ = "gkz"

SCAN_INTERVAL = 300

API_URL = "https://warnungen.zamg.at/wsapp/api/getWarnstatus"

LEVELS = {
    0: "green",
    1: "yellow",
    2: "orange",
    3: "red",
}

# Die Zuordnung der wtype-Werte bitte noch anhand der
# offiziellen GeoSphere-Dokumentation verifizieren.
WARNING_TYPES = {
    1: "Wind",
    2: "Snow",
    3: "Rain",
    4: "Cold",
    5: "Thunderstorm",
    6: "Heat",
    7: "Ice",
    8: "Fog",
}
