"""
Creates lock in Home Assistant based on FIMP services
"""

import json
import typing

import pyfimptoha.const as const
import pyfimptoha.entity as entity
import pyfimptoha.utils as utils

class DoorLock(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.entity_type = const.PLATFORM_LOCK
        self.component_name = "Door Lock"
        self.entity_identifier = "door_lock"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "payload_lock": '{"props":{},"serv":"door_lock","tags":[],"type":"cmd.lock.set","val":true,"val_t":"bool"}',
            "payload_unlock": '{"props":{},"serv":"door_lock","tags":[],"type":"cmd.lock.set","val":false,"val_t":"bool"}',
            "value_template": '{{ iif(value_json.val["is_secured"], "LOCKED", "UNLOCKED", None) }}',
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('lockState'):
            value = self.device['param']['lockState']
        
            data = {
                "props": {},
                "serv": "door_lock",
                "type": "evt.lock.report",
                "val_t": "bool_map",
                "val": {
                    "is_secured": True if value == 'locked' else False,
                }
            }

            statuses.append(super().status(data))
