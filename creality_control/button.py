from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_platform
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Creality Control buttons from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    buttons = []

    # Check the printer type to populate the appropriate buttons
    if entry.data.get("printer_type") == "wifi_box":
        buttons.extend([
            CrealityControlButton(coordinator, f"Pause Print", "PRINT_PAUSE"),
            CrealityControlButton(coordinator, f"Resume Print", "PRINT_RESUME"),
            CrealityControlButton(coordinator, f"Stop Print", "PRINT_STOP"),
        ])
    else:  # Default to your original Halot resin printer buttons
        buttons.extend([
            CrealityControlButton(coordinator, "Pause/Resume Print", "PAUSE_RESUME"),
            CrealityControlButton(coordinator, "Stop Print", "STOP_PRINT"),
        ])

    async_add_entities(buttons)

    # Retrieve the current entity platform
    platform = entity_platform.current_platform.get()
    if platform:
        # Service to send any command to the printer.
        platform.async_register_entity_service(
            "send_command",
            {
                vol.Required("entity_id"): cv.entity_ids,
                vol.Required("command"): cv.string,
            },
            "async_send_command"
        )

class CrealityControlButton(ButtonEntity):
    """Defines a Creality Control button."""

    def __init__(self, coordinator, name, command_key):
        super().__init__()
        self.coordinator = coordinator
        self._name = name
        self._command_key = command_key
        # Update the format of the unique ID and name to be more descriptive
        self._attr_name = f"{name} on {coordinator.host}"
        self._attr_unique_id = f"creality_{coordinator.host.replace('.', '_')}_{command_key.lower()}"

    async def async_press(self):
        """Handle the button press."""
        if self.coordinator.config.get("printer_type") == "wifi_box":
            await self.coordinator.send_command(self._command_key)
        else:
            # Handle the command for the Halot resin printer
            if self._command_key == "PAUSE_RESUME":
                command = "PRINT_PAUSE"  # Adjust as needed for your actual command
            elif self._command_key == "STOP_PRINT":
                command = "PRINT_STOP"  # Adjust as needed
            await self.coordinator.send_command(command)
        
    async def async_send_command(self, command):
        """Send a specific command to the printer."""
        _LOGGER.info(f"Sending command: {command}")
        await self.coordinator.send_command(command)

    @property
    def device_info(self):
        """Return device info for the Creality printer."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.config['host'])},
            "name": self.coordinator.config.get('model', 'Creality Printer'),
            "manufacturer": "Creality",
        }
