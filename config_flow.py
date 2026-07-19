from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME

from .const import DOMAIN, CONF_GKZ


class GeoSphereConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):

        errors = {}

        if user_input is not None:

            await self.async_set_unique_id(user_input[CONF_GKZ])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"GeoSphere {user_input[CONF_GKZ]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_GKZ): str,
                    vol.Optional(CONF_NAME, default="GeoSphere Warn"): str,
                }
            ),
            errors=errors,
        )
