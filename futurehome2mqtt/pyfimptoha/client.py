import json
import time

import pyfimptoha.fimp as fimp
import pyfimptoha.homeassistant as homeassistant
import pyfimptoha.mode as mode


class Client:
    _devices = [] # discovered fimp devices
    _mqtt = None
    _topic_discover = "pt:j1/mt:rsp/rt:app/rn:homeassistant/ad:flow1"
    _topic_receive_mode = "pt:j1/mt:rsp/rt:app/rn:homeassistant/ad:mode"
    _topic_fimp_event = "pt:j1/mt:evt/rt:dev/rn:zw/ad:1/"
    _topic_ha_status = "homeassistant/status"
    _verbose = False

    def __init__(
            self,
            mqtt=None,
            debug=False
    ):
        self._verbose = debug

        if mqtt:
            self._mqtt = mqtt
            mqtt.on_message = self.on_message

        self.start()

    def start(self):
        mqtt = self._mqtt

        # Request FIMP mode
        mqtt.subscribe(self._topic_receive_mode)
        fimp.send_mode_request(mqtt)

        # Request FIMP devices
        mqtt.subscribe(self._topic_discover)
        fimp.send_discovery_request(mqtt)

        # Subscribe to home assistant status where ha announces restarts
        self._mqtt.subscribe(self._topic_ha_status)

    def on_message(self, client, userdata, msg):
        """
        The callback for when a message is received from the server.
        """
        payload = str(msg.payload.decode("utf-8"))

        # Discover FIMP devices and create HA components out of them
        if msg.topic == self._topic_discover:
            data = json.loads(payload)
            homeassistant.create_components(
                devices=data["val"]["param"]["device"],
                mqtt=self._mqtt,
            )
        elif msg.topic == self._topic_receive_mode:
            # Create mode sensor  (home, away, sleep and vacation)
            data = json.loads(payload)
            mode.create(
                mqtt=self._mqtt,
                data=data,
            )
        elif msg.topic == self._topic_ha_status and payload == "online":
            # Home Assistant was restarted - Push everything again
            self.start()
