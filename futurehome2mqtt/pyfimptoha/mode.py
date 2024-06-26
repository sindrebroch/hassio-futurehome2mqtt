import json
import time


def create(mqtt, data):
    """ Futurehome mode switch is stored as a sensor with the values
    home, away, sleep and vaction

    How to read mode switch (home, away, sleep, vacation)
    Topic: pt:j1/mt:evt/rt:app/rn:vinculum/ad:1
    {
    "ctime": "....",
    "serv": "vinculum",
    "val": {
        "component": "hub",
        "id": "mode",
        "param": {
            "current": "home",
            "prev": "home"
        }
    },
    "val_t": "object",
    "ver": "1"
    }
    """

    print(f"- Mode data: {data}")

    _mode = data.get("val").get("param").get("house").get("mode")

    value_template = \
        "{% if value_json.val.id == 'mode' %}{{ value_json.val.param.current }}" \
        "{% else %}{{states('sensor.fh_mode')}}{% endif %}"

    identifier = "fh_mode"
    state_topic = "pt:j1/mt:evt/rt:app/rn:vinculum/ad:1"
    component = {
        "icon": "mdi:hexagon",
        "name": "Modus",
        "device": {
            "name": "Futurehome",
            "identifiers": identifier,
        },
        "object_id": identifier,
        "unique_id": identifier,
        "state_topic": state_topic,
        "value_template": value_template,
    }

    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/sensor/{identifier}/config", payload)
    print(f"Creating mode sensor")

    mqtt.loop()
    time.sleep(1)
    print(f"Publishing mode status \"{_mode}\"")
    payload = {
        "val": {
            "id": "mode",
            "param": {
                "current": _mode
            }
        }
    }
    payload = json.dumps(payload)
    mqtt.publish(state_topic, payload)
