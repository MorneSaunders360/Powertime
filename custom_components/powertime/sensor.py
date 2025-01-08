"""Powertime Sensor definitions."""
from typing import List

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, PERCENTAGE, UnitOfPower
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PowertimeDataUpdateCoordinator
from .entity import PowertimeSensorDescription
from .enums import PowertimeNames
SENSOR_DESCRIPTIONS: List[PowertimeSensorDescription] = [
    PowertimeSensorDescription(
        key=PowertimeNames.ElectricityUnitsHistory,
        name="Electricity Units - History",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PowertimeSensorDescription(
        key=PowertimeNames.CurrentUnitsBoughtForToday,
        name="Current Units Bought For Today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PowertimeSensorDescription(
        key=PowertimeNames.TotalElectricityAmountHistory,
        name="Total Electricity Amount - History",
        native_unit_of_measurement=None,
        device_class=None,
        state_class=None,
    ),
    PowertimeSensorDescription(
        key=PowertimeNames.LastPurchaseDate,
        name="Last Purchase Date",
        native_unit_of_measurement=None,
        device_class=None,
        state_class=None,
    ),
]

async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Defer sensor setup to the shared sensor module."""

    coordinator: PowertimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: List[PowertimeSensor] = []

    key_supported_states = {
        description.key: description for description in SENSOR_DESCRIPTIONS
    }

    for serial in coordinator.data:
        for description in key_supported_states:
            entities.append(
                PowertimeSensor(
                    coordinator, entry, serial, key_supported_states[description]
                )
            )
    async_add_entities(entities)

    return


class PowertimeSensor(CoordinatorEntity, SensorEntity):
    """Powertime Sensor."""

    def __init__(self, coordinator, config, serial, key_supported_states):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config = config
        self._name = key_supported_states.name
        self._native_unit_of_measurement = key_supported_states.native_unit_of_measurement
        self._device_class=key_supported_states.device_class
        self._state_class=key_supported_states.state_class
        self._serial = serial
        self._coordinator = coordinator

        for invertor in coordinator.data:
            serial = invertor
            if self._serial == serial:
                self._attr_device_info = DeviceInfo(
                    entry_type=DeviceEntryType.SERVICE,
                    identifiers={(DOMAIN, serial)},
                    manufacturer="Powertime",
                    model=coordinator.data[invertor]["Model"],
                    name=f"Powertime Statistics : {serial}",
                )

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self._config.entry_id}_{self._serial} - {self._name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._serial}_{self._name}"

    @property
    def native_value(self):
        """Return the state of the resources."""
        return self._coordinator.data[self._serial][self._name]

    @property
    def native_unit_of_measurement(self):
        """Return the native unit of measurement of the sensor."""
        return self._native_unit_of_measurement

    @property
    def device_class(self):
        """Return the device_class of the sensor."""
        return self._device_class

    @property
    def state_class(self):
        """Return the state_class of the sensor."""
        return self._state_class
