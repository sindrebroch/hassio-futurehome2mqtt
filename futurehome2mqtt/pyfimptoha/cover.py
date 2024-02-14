"""
Creates covers in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.const as const
import pyfimptoha.utils as utils

class Cover(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.entity_type = const.PLATFORM_COVER
        self.component_name = "Cover"
        self.entity_identifier = "cover"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "command_topic": self.command_topic,
            "set_position_topic": self.command_topic,
            "payload_close": {
                "props":{},
                "serv":"out_lvl_switch",
                "tags":[],
                "type":"cmd.lvl.set",
                "val_t":"int",
                "ver":"1",
                "val": 0
            },
            "payload_open": {
                "props":{},
                "serv":"out_lvl_switch",
                "tags":[],
                "type":"cmd.lvl.set",
                "val_t":"int",
                "ver":"100",
                "val": 0
            },
            "set_position_template": """
                {
                    "props":{},
                    "serv":"out_lvl_switch",
                    "tags":[],
                    "type":"cmd.lvl.set",
                    "val_t":"int",
                    "ver":"1",
                    "val": {{ position }}
                }
            """,
            "position_topic": self.state_topic,
            "position_template": "{{ value_json.val | round(0) }}",
            "state_topic": "home-assistant/cover/state",
            "value_template": "valuee {{ value_json.val | round(0) }}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('position'):
            value = self.device['param']['position']
        
            data = {
                "props": {},
                "serv": "out_lvl_switch",
                "type": "evt.lvl.report",
                "val": value,
            }

            statuses.append(super().status(data))
