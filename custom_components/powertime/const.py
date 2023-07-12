"""Constants for the Powertime integration."""

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "powertime"
PLATFORMS = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(seconds=10)

NAME = "Powertime"
ISSUE_URL = "https://github.com/MorneSaunders360/Solar-Sunsynk/issues"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""