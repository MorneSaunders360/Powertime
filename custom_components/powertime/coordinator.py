"""Coordinator for Powertime integration."""
import logging

import aiohttp
from .powertimeapi import powertime_api

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER: logging.Logger = logging.getLogger(__package__)


class PowertimeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: powertime_api) -> None:
        """Initialize."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)
        self.api = client
        self.update_method = self._async_update_data
        self.data: dict[str, dict[str, float]] = {}

    async def _async_update_data(self):
        """Update data via library."""
        try:
            # {'Electricity Units': "776.80 Kwh's", 'Meter Number': '14438893399', 'Total Electricity': 'R2500.00', 'Date': '2023-06-27 18:08:39'}
            jsondata = await self.api.get_all_data()
            inverterdata: dict[str, any] = {}
            try: 
                inverterdata.update({"Electricity Units - History": jsondata.get("Electricity Units", 0)})
                inverterdata.update({"Total Electricity Amount - History": jsondata.get("Total Electricity", 0)})
                inverterdata.update({"Last Purchase Date": jsondata.get("Date", 0)})
                inverterdata.update({"Current Units Bought For Today": jsondata.get("Current Units", 0)})
                inverterdata.update({"Model": jsondata.get("Meter Number", 0)})
            except:
                _LOGGER.error("No data")
            _LOGGER.error(inverterdata)
            self.data.update({jsondata.get("Meter Number"): inverterdata})


            return self.data
        except (
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.ClientResponseError,
        ) as error:
            raise UpdateFailed(error) from error
