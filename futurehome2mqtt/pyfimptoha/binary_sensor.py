"""
Creates binary_sensors in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.const as const
import pyfimptoha.entity as entity
import pyfimptoha.utils as utils


class BinarySensor(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.entity_type = const.PLATFORM_BINARY_SENSOR
        super().__init__(mqtt, device, service, service_name)

class BinarySensorPresence(BinarySensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Motion"
        self.entity_identifier = "sensor_presence"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": const.DEVICE_CLASS_MOTION,
            "payload_off": False,
            "payload_on": True,
            "value_template": "{{ value_json.val }}",
        })
        return comp

    def add_status(self, statuses):

        # todo unknown
        value = False

        if self.device.get("param") and self.device['param'].get('presence'):
            value = self.device['param']['presence']
        
        data = {
            "props": {},
            "serv": "sensor_presence",
            "type": "evt.presence.report",
            "val_t": "bool",
            "val": value
        }

        statuses.append(super().status(data))
