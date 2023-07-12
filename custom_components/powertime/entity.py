"""Parent class for Powertime devices."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntityDescription


@dataclass
class PowertimeSensorDescription(SensorEntityDescription):
    """Class to describe an Powertime sensor."""

    native_value: Callable[
        [str | int | float], str | int | float
    ] | None = lambda val: val
