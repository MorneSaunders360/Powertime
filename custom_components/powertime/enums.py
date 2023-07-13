"""Parent class for PowertimeNames enum."""
from enum import Enum, unique


@unique
class PowertimeNames(str, Enum):
    """Device names used by Powertime."""

    ElectricityUnitsHistory = "Electricity Units - History"
    TotalElectricityAmountHistory = "Total Electricity Amount - Histor"
    LastPurchaseDate = "Last Purchase Date"
    CurrentUnitsBoughtForToday = "Current Units Bought For Today"