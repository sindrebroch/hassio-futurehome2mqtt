import json
import typing

import pyfimptoha.utils as utils

class Device():
    name: str
    identifieres: str or typing.Any
    model: str
    suggested_area: str

class Component():
    name: str
    object_id: str
    unique_id: str
    state_topic: str
    device: Device
    device_class: str

class CustomEntity():

    mqtt: typing.Any

    device: typing.Any

    entity_type: str
    entity_identifier: str

    address: str
    name: str
    room: str
    model: str
    identifier: str
    state_topic: str
    component_name: str

    def __init__(self, mqtt, device):
        print("CustomEntity init")
        self.mqtt = mqtt
        self.device = device
        self.address = device["fimp"]["address"]
        self.name = device["client"]["name"]
        self.room = utils.get_room(device)
        self.model = utils.get_model(device)
        self.identifier =  f"fh_{self.address}_{self.entity_identifier}"

    def publish(self):
        print("CustomEntity publish")
        self.mqtt.publish(
            f"homeassistant/{self.entity_type}/{self.identifier}/config", 
            json.dumps(self.component())
        )

    def component(self):
        print("CustomEntity component")
        return {
            "name": self.component_name,
            "object_id": self.identifier,
            "unique_id": self.identifier,
            "state_topic": self.state_topic,
            "device": { 
                "name": self.name,
                "identifiers": self.address,
                "model": self.model,
                "suggested_area": self.room
            }
        }

    def status(self, data):
        print("CustomEntity status")
        payload = json.dumps(data)
        status = (self.state_topic, payload)
        return status
