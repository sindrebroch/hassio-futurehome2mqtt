import json
import time

import paho.mqtt.client as client

import pyfimptoha.const as const
import pyfimptoha.cover as cover
import pyfimptoha.switch as switch
import pyfimptoha.light as light
import pyfimptoha.lock as lock
import pyfimptoha.utils as utils

from pyfimptoha.binary_sensor import BinarySensorPresence
from pyfimptoha.entity import UnknownEntity
from pyfimptoha.lock import DoorLock
from pyfimptoha.meter_elec import SensorMeterElec
from pyfimptoha.sensor import (
    SensorAtmo,
    SensorBattery,
    SensorHumidity,
    SensorLuminance,
    SensorTemperature,
    SensorPower,
)

def create_components( devices: list, mqtt: client ):
    """
    Creates HA components out of FIMP devices by pushing them to HA using mqtt discovery
    """

    print('Received list of devices from FIMP. FIMP reported %s devices' % (len(devices)))

    statuses = []

    for device in devices:
        id = device["id"]
        thing = device["thing"]
        address = device["fimp"]["address"]
        name = device["client"]["name"]
        functionality = device["functionality"]
        room = device["room"]
        model = utils.get_model(device)

        #print(f"Creating: {address} - {name}")
        #print(f"- IDs: {id} - {thing} - {address}")
        #print(f"- Room: {room}")
        #print(f"- Model: {model}")
        #print(f"- Functionality: {functionality}")
        #print(f"- Device: {device}")

        for service_name, service in device["services"].items():
            status = None
            _type = utils.get_type(device)


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
                case "battery":
                    entity = SensorBattery(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "door_lock":
                    entity = DoorLock(mqtt, device, service, service_name)
                    entity.add_status(statuses)
                case "meter_elec":
                    SensorMeterElec(mqtt, device, service, service_name)
                case _:
                    UnknownEntity(mqtt, device, service, service_name)

            if _type == "blinds" and service_name == "out_lvl_switch":
                print(f"- Service: {service_name} (as blind/cover)")
                status = cover.blind(
                    device=device,
                    mqtt=mqtt,
                    service=service,
                )
            if status:
                statuses.append(status)

            # Lights
            elif functionality == "lighting":
                status = None
                if service_name == "out_lvl_switch":
                    print(f"- Service: {functionality} - {service_name}")
                    status = light.out_lvl_switch(
                        service_name=service_name,
                        device=device,
                        mqtt=mqtt,
                        service=service,
                    )
                elif service_name == "out_bin_switch":
                    print(f"- Service: {functionality} - {service_name}")
                    status = light.out_bin_switch(
                        service_name=service_name,
                        device=device,
                        mqtt=mqtt,
                        service=service,
                    )

                if status:
                    statuses.append(status)

            # Appliance
            elif functionality == "appliance":
                # Binary switch
                if service_name == "out_bin_switch":
                    print(f"- Service: {functionality} - {service_name}")
                    status = switch.appliance_switch(
                        device=device,
                        mqtt=mqtt,
                        service_name=service_name,
                        service=service,
                    )
                pass

    mqtt.loop()
    time.sleep(2)
    print("Publishing statuses...")
    for state in statuses:
        topic = state[0]
        payload = state[1]
        mqtt.publish(topic, payload)
        print(topic)
    print("Finished pushing statuses...")
