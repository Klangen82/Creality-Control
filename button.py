from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry  
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Creality Control buttons from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        CrealityControlButton(coordinator, "Pause/Resume Print", "PRINT_PAUSE"),
        CrealityControlButton(coordinator, "Stop Print", "PRINT_STOP"),
    ])

class CrealityControlButton(ButtonEntity):
    """Defines a Creality Control button."""

    def __init__(self, coordinator, name, command):
        super().__init__()
        self.coordinator = coordinator
        self._attr_name = name
        self._command = command
        self._attr_unique_id = f"{coordinator.config['host']}_{command}"

    async def async_press(self):
        """Handle the button press."""
        await self.coordinator.send_command(self._command)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.config['host'])},
            "name": "Creality Printer",
            "manufacturer": "Creality",
            # Add any other device info as needed
        }
