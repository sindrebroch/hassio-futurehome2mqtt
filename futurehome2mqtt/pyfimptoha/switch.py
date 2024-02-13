"""
Creates binary_sensors in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.utils as utils


def appliance_switch(
    device: typing.Any,
    mqtt,
    service_name,
    service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    identifier = f"fh_{address}_{service_name}"
    command_topic = f"pt:j1/mt:cmd{service['addr']}"
    state_topic   = f"pt:j1/mt:evt{service['addr']}"
    component = {
        "name": "Switch",
        "object_id": identifier,
        "unique_id": identifier,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "device_class": "outlet",
        "schema": "template",
        "command_topic": command_topic,
        "state_topic": state_topic,
        "payload_on":  '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":true,"val_t":"bool"}',
        "payload_off": '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":false,"val_t":"bool"}',
        "value_template": '{{ value_json.val }}',
        "state_on": True,
        "state_off": False,
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/switch/{identifier}/config", payload)

    # Queue statuses
    value = False
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
