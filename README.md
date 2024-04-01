# Creality Control Integration for Home Assistant
This custom integration for Home Assistant allows you to monitor and control your Creality 3D printer directly from Home Assistant's interface. With it, you can keep an eye on your current print's status, pause/resume prints, and stop them altogether. This integration aims to bring convenience and remote monitoring capabilities to your 3D printing setup.

Features
Print Status Monitoring: Check the current status of your print, including progress, print time left, current layer, and more.
Control Commands: Pause/Resume and Stop your prints directly from Home Assistant.
Notification Support: Get notified about print completions or issues right within Home Assistant (requires additional configuration).
Requirements
A Creality 3D printer that is compatible with the integration.
The printer must be connected to the same network as your Home Assistant instance.
Home Assistant Core 2021.6.0 or later.
Installation
Download the latest release of the Creality Control integration.
Unzip the release and copy the creality_control directory into the custom_components directory of your Home Assistant installation.
Restart Home Assistant to load the new integration.
Go to Configuration > Integrations in the UI and click on the + Add Integration button.
Search for Creality Control and follow the on-screen instructions to configure the integration with your printer's details.
Configuration
During the integration setup, you will be prompted to enter the following details:

Host: The IP address of your Creality printer.
Port: The port used by your Creality printer for network communication (default is 18188).
Password: The password for your Creality printer, if applicable.
Important Notes
Printer Online Requirement: The printer needs to be online and connected to the network to be added successfully to Home Assistant. Ensure your printer is powered on and properly connected to the same network as your Home Assistant instance before attempting to add the integration.
Control Command Limitations: The pause/resume and stop controls can only be used when a print job has started. Due to Home Assistant's limitations, it's not currently possible to upload prints or initiate print jobs from Home Assistant.
Support
For support, questions, or contributions, please visit the GitHub issue tracker for this integration.

Disclaimer
This integration is not officially affiliated with Creality. Use it at your own risk. Always ensure your printer's firmware is up to date with the latest version recommended by Creality.

License
This Home Assistant integration is released under the MIT License.
