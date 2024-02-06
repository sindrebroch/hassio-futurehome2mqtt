"""
Creates light in Home Assistant based on FIMP services
"""

import json
import typing


def out_lvl_switch(
        service_name: str,
        device: typing.Any,
        mqtt,
        service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = device["model"]

    identifier = f"fh_{address}_{service_name}"
    command_topic = f"pt:j1/mt:cmd{service['addr']}"
    state_topic   = f"pt:j1/mt:evt{service['addr']}"
    component = {
        "name": "Lys",
        "object_id": identifier,
        "unique_id": identifier,
        "brightness_scale": 100,
        "command_topic": command_topic,
        "state_topic": state_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
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
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/light/{identifier}/config", payload)

    # Queue statuses
    status = None
    if device.get("param") and device['param'].get('power'):
        power = device['param']['power']
        if power == "off":
            data = {
                "props": {},
                "serv": "out_lvl_switch",
                "type": "cmd.binary.report",
                "val_t": "bool",
                "val": False
            }
        else:
            dim_value = device['param']['dimValue']
            data = {
                "props": {},
                "serv": "out_bin_switch",
                "type": "cmd.binary.set",
                "val_t": "int",
                "val": dim_value
            }
        payload = json.dumps(data)
        status = (state_topic, payload)
    return status


def out_bin_switch(
        service_name: str,
        device: typing.Any,
        mqtt,
        service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = device["model"]

    identifier = f"fh_{address}_{service_name}"
    command_topic = f"pt:j1/mt:cmd{service['addr']}"
    state_topic   = f"pt:j1/mt:evt{service['addr']}"
    component = {
        "name": "Switch",
        "object_id": identifier,
        "unique_id": identifier,
        "command_topic": command_topic,
        "state_topic": state_topic,
        "schema": "template",
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
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
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/light/{identifier}/config", payload)

    # Queue statuses
    status = None
    if device.get("param") and device['param'].get('power'):
        power = device['param']['power']
        data = {
            "props": {},
            "serv": "out_bin_switch",
            "type": "cmd.binary.report",
            "val_t": "bool",
            "val": True if power == 'on' else False
        }

        payload = json.dumps(data)
        status = (state_topic, payload)
    return status
