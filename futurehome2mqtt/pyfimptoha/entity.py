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

    entity_type: str

    address: str
    name: str
    room: str
    model: str
    identifier: str
    state_topic: str

    def __init__(self, mqtt, device):
        print("Init Entity")
        self.mqtt = mqtt
        self.address = device["fimp"]["address"]
        self.name = device["client"]["name"]
        self.room = device["room"]
        self.model = utils.get_model(device)

    def publish(self):
        print("Publish Entity", self.entity_type, self.identifier)
        topic = f"homeassistant/{self.entity_type}/{self.identifier}/config"
        # payload = json.dumps(component)
        # mqtt.publish(topic, payload)

    def status(self):
        print("Status Entity")
        # payload = json.dumps(data)
        # status = (self.state_topic, payload)
        return {
            "name": "test"
        }