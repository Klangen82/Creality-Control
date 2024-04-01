from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from datetime import timedelta
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Creality Control sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        CrealitySensor(coordinator, "printStatus", "Status"),
        CrealitySensor(coordinator, "filename", "Filename"),
        CrealityTimeLeftSensor(coordinator, "printRemainTime", "Time Left"),
        CrealitySensor(coordinator, "progress", "Progress", unit_of_measurement="%"),
        CrealitySensor(coordinator, "curSliceLayer", "Current Layer"),
        CrealitySensor(coordinator, "sliceLayerCount", "Total Layers"),
        CrealitySensor(coordinator, "printExposure", "Print Exposure", unit_of_measurement="s"),
        CrealitySensor(coordinator, "layerThickness", "Layer Thickness", unit_of_measurement="mm"),
        CrealitySensor(coordinator, "printHeight", "Rising Height", unit_of_measurement="mm"),
        CrealitySensor(coordinator, "bottomExposureNum", "Bottom Layers"),
        CrealitySensor(coordinator, "initExposure", "Initial Exposure", unit_of_measurement="s"),
        CrealitySensor(coordinator, "delayLight", "Turn off Delay", unit_of_measurement="s"),
        CrealitySensor(coordinator, "eleSpeed", "Motor Speed", unit_of_measurement="mm/s"),
        CrealitySensor(coordinator, "resin", "Resin"),
        # Add any additional sensors you need here
    ]
    async_add_entities(sensors)

class CrealitySensor(CoordinatorEntity, Entity):
    """Defines a single Creality sensor."""

    def __init__(self, coordinator, data_key, name_suffix, unit_of_measurement=None):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.data_key = data_key
        self._attr_name = f"Creality {name_suffix}"
        self._attr_unique_id = f"{coordinator.config['host']}_{data_key}"
        self._unit_of_measurement = unit_of_measurement

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._attr_name

    @property
    def unique_id(self):
        """Return a unique identifier for this sensor."""
        return self._attr_unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        # Special handling for the "Progress" sensor to calculate its value
        if self.data_key == "progress":
            cur_layer = self.coordinator.data.get("curSliceLayer", 0)
            total_layers = self.coordinator.data.get("sliceLayerCount", 0)
            try:
                progress = (float(cur_layer) / float(total_layers)) * 100 if total_layers else 0
                return round(progress, 2)
            except ValueError:  # In case of non-integer values
                return 0
        return self.coordinator.data.get(self.data_key, "Unknown")

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement if defined."""
        return self._unit_of_measurement

    @property
    def device_info(self):
        """Return information about the device this sensor is part of."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.config['host'])},
            "name": "Creality Printer",
            "manufacturer": "Creality",
            "model": "Creality Printer",  # Update with your model, have not found a way to get this information
        }

class CrealityTimeLeftSensor(CrealitySensor):
    """Specialized sensor class for handling 'Time Left' data."""

    @property
    def state(self):
        """Return the state of the sensor, converting time to HH:MM:SS format."""
        time_left = int(self.coordinator.data.get(self.data_key, 0))
        return str(timedelta(seconds=time_left))