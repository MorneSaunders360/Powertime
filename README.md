# Powertime ![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)

A Home Assistant integration to track your Powertime Last Purchase .


# Features
1. Supports real-time monitoring of your Solar Powertime system's parameters.
2. Allows you to adjust the settings of your system remotely through Home Assistant.
3. New: Now supports adjusting solar settings remotely through the set_solar_settings service.


# HACS Install 
1. Access HACS: Open Home Assistant and click on HACS in the sidebar.
2. Go to Integrations: Navigate to the Integrations tab.
3. Add Custom Repository: Click on the menu in the top right corner (three vertical dots), then select Custom Repositories.
4. Enter Details: In the new window, you need to input the necessary information about the custom integration you want to add
5. Add custom repository URL: Paste the URL of the repository you want to add.
6. Select category: Choose 'Integration' from the category dropdown menu.
7. Add: Click the Add button to confirm. This action should add the custom integration to HACS.
8. Select "+ Explore & Download Repositories" and search for "Powertime"
9. Select "Powertime" and "Download this repository with HACS"
10. Once downloaded, go to settings, then devices and services
11. Click on add intergration and search for 'Solar Powertime'
12. Follow the prompt with user name and then password, wait for 2 minutes and your data should be loaded
13. Setup cards and automations

# Service Usage
1. To monitor your system, use the provided sensors in your Home Assistant dashboard.


# Sensors
 Go to developer tool thne select the states tab. Then filter the entities by searching for solar and you will be able to see all the sensors available.
 ![image](https://user-images.githubusercontent.com/109594480/233350555-f44916c6-9522-4cb0-9994-9d195711cd99.png)

