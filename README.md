# Creality Control Integration for Home Assistant

This custom integration allows Home Assistant users to monitor and control their Creality 3D printers. It offers capabilities such as viewing current print status and sending pause/resume and stop commands directly from the Home Assistant interface.

## Features

- **Print Status Monitoring**: Track the status of ongoing prints, including progress, remaining time, current layer, and more.
- **Print Control**: Directly pause/resume and stop prints from within Home Assistant.
- **Notifications**: Configure Home Assistant to notify you about print completions or issues (additional configuration required).

## Prerequisites

- A compatible Creality 3D printer connected to your network.
- Home Assistant Core 2021.6.0 or newer.

## Installation

1. Clone this repository or download the latest release.
2. Copy the `creality_control` folder to your `custom_components` directory in your Home Assistant configuration directory.
3. Restart Home Assistant to recognize the new integration.
4. Navigate to **Configuration** > **Integrations** and click **+ Add Integration**.
5. Search for "Creality Control" and input your printer's details as prompted.

## Configuration

You will need the following information to set up the integration:

- **Host**: IP address of your Creality printer.
- **Port**: Network port for the printer (default: `18188`).
- **Password**: Your printer's password, if set.

## Important Considerations

- **Printer Online**: Ensure your printer is online and connected to the same network as Home Assistant for successful integration.
- **Control Limitations**: Pause/Resume and Stop commands are only functional when there is an active print job. Home Assistant does not support uploading print files or starting prints due to limitations.

## Support

For support, questions, or contributions, please visit the [GitHub issue tracker](https://github.com/Klangen82/Creality-Control/issues).

## Disclaimer

This integration is not officially affiliated with Creality. Use it at your own risk. Always ensure your printer's firmware is up to date with the latest version recommended by Creality.

## License

This Home Assistant integration is released under the [MIT License](LICENSE).
