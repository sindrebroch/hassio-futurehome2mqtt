"""
Creates light in Home Assistant based on FIMP services
"""

import json
import typing

import pyfimptoha.const as const
import pyfimptoha.entity as entity
import pyfimptoha.utils as utils

class LightEntity(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.entity_type = const.PLATFORM_LIGHT
        super().__init__(mqtt, device, service, service_name)

class Light(LightEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Light"
        self.entity_identifier = "light"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "command_topic": self.command_topic,
            "state_topic": self.state_topic,
            "command_on_template": """
                    {
                    "props":{},
                    "serv":"out_lvl_switch",
                    "tags":[]
                    {%- if brightness -%}
                    , "type":"cmd.lvl.set",
                    "val":{{ (brightness / 2.55) | int }},
                    "val_t":"int"
                    {%- else -%}
                    , "type":"cmd.binary.set",
                    "val":true,
                    "val_t":"bool"
                    {%- endif -%}
                    }
                """,
            "command_off_template": """
                    {"props":{},
                    "serv":"out_lvl_switch",
                    "tags":[],
                    "type":"cmd.binary.set",
                    "val":false,
                    "val_t":"bool"}
                """,
            "schema": "template",
            "state_template": "{% if value_json.val %} on {% else %} off {% endif %}",
            "brightness_template": "{% if value_json.val_t %}{{ (value_json.val * 2.55) | int }}{% endif %}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('power'):
            power = self.device['param']['power']
            if power == "off":
                data = {
                    "props": {},
                    "serv": "out_lvl_switch",
                    "type": "cmd.binary.report",
                    "val_t": "bool",
                    "val": False
                }
            else:
                dim_value = self.device['param']['dimValue']
                data = {
                    "props": {},
                    "serv": "out_bin_switch",
                    "type": "cmd.binary.set",
                    "val_t": "int",
                    "val": dim_value
                }

            statuses.append(super().status(data))


class LightSwitch(LightEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Light Switch"
        self.entity_identifier = "light"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "command_topic": self.command_topic,
            "state_topic": self.state_topic,
            "schema": "template",
            "payload_on": '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":true,"val_t":"bool"}',
            "payload_off": '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":false,"val_t":"bool"}',
            "command_on_template": """
                {
                "props":{},
                "serv":"out_bin_switch",
                "tags":[],
                "type":"cmd.binary.set",
                "val":true,
                "val_t":"bool"
                }
            """,
            "command_off_template": """
                {
                "props":{},
                "serv":"out_bin_switch",
                "tags":[],
                "type":"cmd.binary.set",
                "val":false,
                "val_t":"bool"
                }
            """,
            "state_template": "{% if value_json.val %} on {% else %} off {% endif %}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('power'):
            value = self.device['param']['power']
            data = {
                "props": {},
                "serv": "out_bin_switch",
                "type": "cmd.binary.report",
                "val_t": "bool",
                "val": True if value == 'on' else False
            }

            statuses.append(super().status(data))
