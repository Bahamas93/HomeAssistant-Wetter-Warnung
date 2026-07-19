"""Config flow for GeoSphere Warn."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_GKZ, DEFAULT_NAME, DOMAIN


class GeoSphereConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            gkz = user_input[CONF_GKZ].strip()

            if not gkz.isdigit() or len(gkz) != 5:
                errors["base"] = "invalid_gkz"
            else:
                await self.async_set_unique_id(gkz)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"{DEFAULT_NAME} ({gkz})",
                    data={
                        CONF_GKZ: gkz,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_GKZ): str,
                }
            ),
            errors=errors,
        )
