"""
Creates switches in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.entity as entity
import pyfimptoha.utils as utils

class Switch(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.entity_type = const.PLATFORM_SWITCH
        self.component_name = "Switch"
        self.entity_identifier = "switch"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "outlet",
            "schema": "template",
            "command_topic": self.command_topic,
            "state_topic": self.state_topic,
            "payload_on":  '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":true,"val_t":"bool"}',
            "payload_off": '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":false,"val_t":"bool"}',
            "value_template": '{{ value_json.val }}',
            "state_on": True,
            "state_off": False,
        })
        return comp

    def add_status(self, statuses):

        value = False

        if device.get("param") and device['param'].get('power'):
            value = device['param']['power'] == 'on'

        data = {
            "props": {},
            "serv": "out_bin_switch",
            "type": "cmd.binary.report",
            "val_t": "bool",
            "val": value
        }

        statuses.append(super().status(data))
