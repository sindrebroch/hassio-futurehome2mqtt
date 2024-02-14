"""
Creates binary_sensors in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.const as const
import pyfimptoha.entity as entity
import pyfimptoha.utils as utils


class BinarySensor(entity.CustomEntity):

    def __init__(self, mqtt, device):
        print("BinarySensor init")
        self.entity_type = const.PLATFORM_BINARY_SENSOR
        super().__init__(mqtt, device)

class BinarySensorPresence(BinarySensor):

    def __init__(self, mqtt, device, service, service_name):
        print("BinarySensorPresence init")
        self.component_name = "Motion"
        self.entity_identifier = const.SERVICE_SENSOR_PRESENCE
        self.state_topic = f"pt:j1/mt:evt{service['addr']}"
        super().__init__(mqtt, device)
        print(f"Service - {service}")
        print(f"Service name - {service_name}")

    def component(self):
        return super().component().update({
            "device_class": utils.DEVICE_CLASS_MOTION,
            "payload_off": False,
            "payload_on": True,
            "value_template": "{{ value_json.val }}",
        })

    def status(self):

        value = False
        if self.device.get("param") and self.device['param'].get('presence'):
            value = self.device['param']['presence']
        
        data = {
            "props": {},
            "serv": const.SERVICE_SENSOR_PRESENCE,
            "type": "evt.presence.report",
            "val_t": "bool",
            "val": value
        }

        return super().status(data)
