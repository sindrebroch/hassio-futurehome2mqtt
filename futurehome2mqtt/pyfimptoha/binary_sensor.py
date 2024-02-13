"""
Creates binary_sensors in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.entity as entity
import pyfimptoha.utils as utils


class BinarySensor(entity.CustomEntity):

    def __init__(self, mqtt, device):
        super().__init__(mqtt, device)
        self.entity_type = "binary_sensor"

class BinarySensorPresence(BinarySensor):

    def __init__(
        self, 
        mqtt, 
        device, 
        service
    ):
        print("BinarySensorPresence init")
        self.component_name = "Motion"
        self.entity_identifier =  "sensor_presence"
        self.state_topic = f"pt:j1/mt:evt{service['addr']}"
        super().__init__(mqtt, device)

    def component(self):
        print("BinarySensorPresence component")
        return super().component().update({
            "device_class": "motion",
            "payload_off": False,
            "payload_on": True,
            "value_template": "{{ value_json.val }}",
        })

    def publish(self):
        print("BinarySensorPresence publish")
        super().publish()

    def status(self):
        print("BinarySensorPresence status")
        
        value = False
        if device.get("param") and device['param'].get('presence'):
            value = device['param']['presence']
        
        data = {
            "props": {},
            "serv": "sensor_presence",
            "type": "evt.presence.report",
            "val_t": "bool",
            "val": value
        }
        return super().status(data)
        
def sensor_presence(
    device: typing.Any,
    mqtt,
    service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    identifier = f"fh_{address}_sensor_presence"
    state_topic = f"pt:j1/mt:evt{service['addr']}"
    component = {
        "name": "Bevegelse",
        "object_id": identifier,
        "unique_id": identifier,
        "state_topic": state_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "device_class": "motion",
        "payload_off": False,
        "payload_on": True,
        "value_template": "{{ value_json.val }}",
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/binary_sensor/{identifier}/config", payload)

    # Queue statuses
    value = False
    if device.get("param") and device['param'].get('presence'):
        value = device['param']['presence']
    data = {
        "props": {},
        "serv": "sensor_presence",
        "type": "evt.presence.report",
        "val_t": "bool",
        "val": value
    }
    payload = json.dumps(data)
    status = (state_topic, payload)
    return status
