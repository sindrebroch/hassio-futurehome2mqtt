import json

import paho.mqtt.client as mqtt

VINCULUM_TOPIC = "pt:j1/mt:cmd/rt:app/rn:vinculum/ad:1"

def send_discovery_request(client: mqtt):
    """Load FIMP devices from MQTT broker"""

    path = "pyfimptoha/data/fimp_discover.json"
    with open(path) as json_file:
        data = json.load(json_file)
        payload = json.dumps(data)
        print('Asking FIMP to expose all devices...')
        client.publish(VINCULUM_TOPIC, payload)


def send_mode_request(client: mqtt):
    """Request Futurehome mode"""

    payload = {
        "props": {},
        "serv": "vinculum",
        "tags": [],
        "type": "cmd.pd7.request",
        "val_t": "object",
        "ver": "1",
        "val": {
            "cmd": "get",
            "param": { "components": [ "house" ] }
        },
        "resp_to": "pt:j1/mt:rsp/rt:app/rn:homeassistant/ad:mode"
    }
    payload = json.dumps(payload)
    print('Requesting current mode status')
    client.publish(VINCULUM_TOPIC, payload)


# Used for tests
def load_json_device(self, filename):
    data = "{}"

    path = "data/%s" % filename
    with open(path) as json_file:
        data = json.load(json_file)

    # self._devices.append(data)
    return data
