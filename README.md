# Home Assistant add-on: Futurehome FIMP to MQTT

Based on the work of [runelangseid](https://github.com/runelangseid/hassio-futurehome2mqtt)

## About

This [Futurehome FIMP](https://github.com/futurehomeno/fimp-api) to MQTT add-on allows you to integrate the Futurehome
Smarthub with Home Assistant by using the local MQTT broker inside the hub.

This addon configure devices and their capabilities from Future Home in Home Assistant using MQTT Discovery.

## Supported Futurehome devices

- 

### 1. Home Assistant MQTT

Home Assistant must use the MQTT broker provided by the Futurehome Smart hub

### 2. Install add-on

1) Add this repo as an add-on repository
2) Install the addon 'Futurehome FIMP to MQTT'
3) Configure the addon with the same parameters as before
4) Start it. Supported devices should appear in the Home Assistant UI
