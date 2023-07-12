"""Parent class for SunsynkNames enum."""
from enum import Enum, unique


@unique
class PowertimeNames(str, Enum):
    """Device names used by Powertime."""

    SolarProduction = "Solar Production"
    SolarToBattery = "Solar to Battery"
    SolarToGrid = "Solar to Grid"
    SolarToLoad = "Solar to Load"