"""The Powertime integration."""
from __future__ import annotations

from .powertimeapi import powertime_api

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS
from .coordinator import PowertimeDataUpdateCoordinator

# import logging
# _LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Sunsynk from a config entry."""
    
    client = powertime_api(entry.data[CONF_USERNAME],entry.data[CONF_PASSWORD],hass)
    coordinator = PowertimeDataUpdateCoordinator(hass, client=client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))


    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
