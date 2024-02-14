import json
import typing

import pyfimptoha.utils as utils


class CustomEntity():

    mqtt: typing.Any
    device: typing.Any
    service: typing.Any
    service_name: str

    entity_type: str
    entity_identifier: str
    unit_of_measurement: str or None = None

    id: str
    thing: str
    functionality: str
    address: str
    name: str
    room: str
    model: str
    component_name: str

    identifier: str
    command_topic: str
    state_topic: str

    def __init__(self, mqtt, device, service, service_name):
        self.mqtt = mqtt
        self.device = device
        self.service = service
        self.service_name = service_name

        self.id = device["id"]
        self.name = device["client"]["name"]
        self.thing = device["thing"]
        self.address = device["fimp"]["address"]
        self.functionality = device["functionality"]
        self.room = utils.get_room(device)
        self.model = utils.get_model(device)
        
        self.identifier =  f"fh_{self.address}_{self.entity_identifier}"
        self.command_topic = f"pt:j1/mt:cmd{service['addr']}"
        self.state_topic   = f"pt:j1/mt:evt{service['addr']}"

        # self.debug()
        self.publish()

    def debug(self):
        print(f"-----")
        print(f"Debug: {self.name}")
        print(f"- ID: {self.id}")
        print(f"- Thing: {self.thing}")
        print(f"- Address: {self.address}")
        print(f"- Room: {self.room}")
        print(f"- Model: {self.model}")
        print(f"- Functionality: {self.functionality}")
        print(f"- Entity type: {self.entity_type}")
        print(f"- Entity identifier: {self.entity_identifier}")
        print(f"- Identifier: {self.identifier}")
        print(f"- UOM: {self.unit_of_measurement}")
        print(f"- Device: {self.device}")
        print(f"- Service name: {self.service_name}")
        print(f"- Service: {self.service}")
        
    def publish(self):
        self.mqtt.publish(
            f"homeassistant/{self.entity_type}/{self.identifier}/config", 
            json.dumps(self.component())
        )

    def component(self):
        return {
            "name": self.component_name,
            "object_id": self.identifier,
            "unique_id": self.identifier,
            "state_topic": self.state_topic,
            "unit_of_measurement": self.unit_of_measurement,
            "device": { 
                "name": self.name,
                "identifiers": self.address,
                "model": self.model,
                "suggested_area": self.room
            }
        }

    def status(self, data):
        payload = json.dumps(data)
        status = (self.state_topic, payload)
        return status

class UnknownEntity(CustomEntity):

    unsupported_services: [
        "dev_sys", 
        "indicator_ctrl", 
        "version",
        "basic",
        "alarm_emergency",
        "alarm_burglar",
        "alarm_power",
        "thermostat",
        "media_player",
    ]

    def __init__(self, mqtt, device, service, service_name):
        if service_name not in unsupported_services:
            print(f"- Service {service_name} not yet implemented")
            print(f"- Device {device}")
