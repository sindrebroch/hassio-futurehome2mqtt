"""
Creates covers in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.const as const
import pyfimptoha.utils as utils

class Blind(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.entity_type = const.PLATFORM_COVER
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


def blind(
        device: typing.Any,
        mqtt,
        service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    identifier = f"fh_{address}_blind"
    command_topic = f"pt:j1/mt:cmd{service['addr']}"

    payload_close = """
        {
            "props":{},
            "serv":"out_lvl_switch",
            "tags":[],
            "type":"cmd.lvl.set",
            "val_t":"int",
            "ver":"1",
            "val": 0
        }
    """

    state_topic = f"pt:j1/mt:evt{service['addr']}"
    set_position_topic = f"pt:j1/mt:cmd{service['addr']}"
    component = {
        "name": "Persienne",
        "object_id": identifier,
        "unique_id": identifier,
        "command_topic": command_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "payload_close": payload_close,
        "payload_open": payload_close.replace('"ver":"1"', '"ver":"100"'),
        "set_position_topic": set_position_topic,
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
        # read position
        "position_topic": state_topic,
        "position_template": "{{ value_json.val | round(0) }}",
        "state_topic": "home-assistant/cover/state",
        "value_template": "valuee {{ value_json.val | round(0) }}"
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/cover/{identifier}/config", payload)

    # Queue statuses
    status = None
    if device.get("param") and isinstance(device['param'].get('position'), int):
        value = device['param']['position']
        data = {
            "props": {},
            "serv": "out_lvl_switch",
            "type": "evt.lvl.report",
            "val": value,
        }

        payload = json.dumps(data)
        status = (state_topic, payload)
    return status