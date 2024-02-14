import json
import time

import paho.mqtt.client as client

import pyfimptoha.const as const
import pyfimptoha.utils as utils

from pyfimptoha.binary_sensor import BinarySensorPresence
from pyfimptoha.cover import Cover
from pyfimptoha.entity import UnknownEntity
from pyfimptoha.light import Light, LightSwitch
from pyfimptoha.lock import DoorLock
from pyfimptoha.meter_elec import SensorMeterElec
from pyfimptoha.sensor import (
    SensorAtmo,
    SensorBattery,
    SensorHumidity,
    SensorLuminance,
    SensorTemperature,
    SensorPower,
    SensorPrice,
    SensorCO2,
)
from pyfimptoha.switch import Switch

def create_components( devices: list, mqtt: client ):
    """
    Creates HA components out of FIMP devices by pushing them to HA using mqtt discovery
    """

    print('Received list of devices from FIMP. FIMP reported %s devices' % (len(devices)))

    statuses = []

    for device in devices:
        address = device["fimp"]["address"]
        name = device["client"]["name"]
        print(f"Device: {address} - {name}")

        for service_name, service in device["services"].items():
            status = None
            _type = utils.get_type(device)

            # https://github.com/futurehomeno/fimp-api/blob/master/device_services/device_services.md
            match service_name:
                case "sensor_presence":
                    entity = BinarySensorPresence(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "sensor_lumin":
                    entity = SensorLuminance(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "sensor_temp":
                    entity = SensorTemperature(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "sensor_humid":
                    entity = SensorHumidity(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "sensor_atmo":
                    entity = SensorAtmo(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "sensor_power":
                    entity = SensorPower(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "sensor_co2":
                    entity = SensorCO2(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "sensor_price":
                    entity = SensorPrice(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "battery":
                    entity = SensorBattery(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "door_lock":
                    entity = DoorLock(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "meter_elec":
                    SensorMeterElec(mqtt, device, service, service_name)
                case "out_lvl_switch":
                    match _type:
                        case "blinds":
                            Cover(mqtt, device, service, service_name)
                            entity.add_status(statuses)
                        case "light":
                            Light(mqtt, device, service, service_name)
                            entity.add_status(statuses)
                        # None
                        case _:
                            UnknownEntity(mqtt, device, service, service_name)
                case "out_bin_switch":
                    match _type:
                        case "appliance" | None:
                            Switch(mqtt, device, service, service_name)
                            entity.add_status(statuses)
                        case "light":
                            LightSwitch(mqtt, device, service, service_name)
                            entity.add_status(statuses)
                case _:
                    UnknownEntity(mqtt, device, service, service_name)

    mqtt.loop()
    time.sleep(2)
    print("Publishing statuses...")
    for state in statuses:
        topic = state[0]
        payload = state[1]
        mqtt.publish(topic, payload)
        print(topic)
    print("Finished pushing statuses...")
