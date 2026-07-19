from datetime import timedelta

DOMAIN = "geosphere_warn"

CONF_GKZ = "gkz"

API_URL = "https://warnungen.zamg.at/wsapp/api/getWarnstatus"

UPDATE_INTERVAL = timedelta(minutes=5)

LEVELS = {
    0: "green",
    1: "yellow",
    2: "orange",
    3: "red",
}
