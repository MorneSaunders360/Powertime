"""Parent class for SunsynkNames enum."""
from enum import Enum, unique


@unique
class PowertimeNames(str, Enum):
    """Device names used by Powertime."""

    ElectricityUnits = "Electricity Units"
    TotalElectricity = "Total Electricity"
    LastPurchaseDate = "Last Purchase Date"