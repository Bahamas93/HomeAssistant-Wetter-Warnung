async def _async_update_data(self):
    try:
        return await self.api.async_get_warning()
    except Exception as err:
        raise UpdateFailed(err) from err
