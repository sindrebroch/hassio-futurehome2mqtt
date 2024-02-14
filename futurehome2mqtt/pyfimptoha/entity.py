import json
import typing

import pyfimptoha.utils as utils


class CustomEntity():

    mqtt: typing.Any

    device: typing.Any

    entity_type: str
    entity_identifier: str

    id: str
    thing: str
    functionality: str
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

        self.id = device["id"]
        self.name = device["client"]["name"]
        self.thing = device["thing"]
        self.address = device["fimp"]["address"]
        self.functionality = device["functionality"]
        self.room = utils.get_room(device)
        self.model = utils.get_model(device)
        self.identifier =  f"fh_{self.address}_{self.entity_identifier}"

        self.debug()
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
        print(f"- Device: {self.device}")

    def publish(self):
        t = self.component()
        print(f"component {t}")
        self.mqtt.publish(
            f"homeassistant/{self.entity_type}/{self.identifier}/config", 
            json.dumps(t)
        )

    def component(self):
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
        payload = json.dumps(data)
        status = (self.state_topic, payload)
        return status
