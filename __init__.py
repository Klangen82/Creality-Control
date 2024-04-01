import aiohttp
import async_timeout
import json
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from base64 import b64encode
from binascii import unhexlify

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = aiohttp.ClientSession()
    coordinator = CrealityDataCoordinator(hass, session, entry.data)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, 'sensor'))
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, 'button'))
    return True

class CrealityDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, session, config):
        self.session = session
        self.config = config
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=30))

    async def _async_update_data(self):
        data = await self.fetch_data()
        if data is None:
            raise UpdateFailed("Failed to fetch data from the Creality printer.")
        return data

    async def fetch_data(self):
        uri = f"ws://{self.config['host']}:{self.config['port']}/"
        token = self.generate_token(self.config['password'])
        async with self.session.ws_connect(uri) as ws:
            await ws.send_json({"cmd": "GET_PRINT_STATUS", "token": token})
            async with async_timeout.timeout(10):
                msg = await ws.receive_json()
                if msg:
                    return msg
                else:
                    _LOGGER.error("Failed to receive data")
                    return None

    def generate_token(self, password):
        key = unhexlify("6138356539643638")
        cipher = DES.new(key[:8], DES.MODE_ECB)
        padded_password = pad(password.encode(), DES.block_size)
        encrypted_password = cipher.encrypt(padded_password)
        token = b64encode(encrypted_password).decode('utf-8')
        return token

    async def send_command(self, command):
        """Send a command to the printer."""
        uri = f"ws://{self.config['host']}:{self.config['port']}/"
        token = self.generate_token(self.config['password'])
        
        try:
            async with self.session.ws_connect(uri) as ws:
                await ws.send_json({"cmd": command, "token": token})
                _LOGGER.info(f"Sent command {command} to the printer")
                response = await ws.receive()
                
                if response.type == aiohttp.WSMsgType.TEXT:
                    response_data = json.loads(response.data)
                    if response_data.get("cmd") == command and response_data.get("status") == command:
                        _LOGGER.info(f"Command {command} executed successfully.")
                    else:
                        _LOGGER.error(f"Printer responded with unexpected data: {response_data}")
                else:
                    _LOGGER.error(f"Failed to receive valid response for command {command}")
                    
        except Exception as e:
            _LOGGER.error(f"Failed to send command {command}: {e}")
