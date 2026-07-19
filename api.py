import aiohttp

from .const import API_URL


class GeoSphereApi:

    def __init__(self, session, gkz):

        self._session = session
        self._gkz = str(gkz)

    async def async_get_warning(self):

        async with self._session.get(API_URL) as response:

            response.raise_for_status()

            data = await response.json()

        highest = None

        for feature in data["features"]:

            props = feature["properties"]

            if self._gkz in props["gemeinden"]:

                level = props["wlevel"]

                if highest is None or level > highest["wlevel"]:
                    highest = props

        return highest
