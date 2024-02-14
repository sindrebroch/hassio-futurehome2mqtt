"""
Creates sensors in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.const as const
import pyfimptoha.entity as entity
import pyfimptoha.utils as utils

class Sensor(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.entity_type = const.PLATFORM_SENSOR
        super().__init__(mqtt, device, service, service_name)

class SensorBattery(Sensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Battery"
        self.entity_identifier = "battery"
        self.unit_of_measurement = const.UOM_PERCENTAGE
        super().__init__(mqtt, device, service, service_name)
        print(f"Service - {service}")
        print(f"Service name - {service_name}")

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "battery",
            "value_template": "{{ value_json.val | round(0) }}"
        })
        return comp

    def status(self):

        status = None

        if device.get("param") and device['param'].get('batteryPercentage'):
            value = device['param']['batteryPercentage']
            data = {
                "props": {
                    "unit": self.unit_of_measurement
                },
                "serv": "battery",
                "type": "evt.health.report",
                "val": value,
            }
            return super().status(data)

        return status

def battery(
    device: typing.Any,
    mqtt,
    service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    identifier = f"fh_{address}_battery"
    state_topic = f"pt:j1/mt:evt{service['addr']}"
    unit_of_measurement = const.UOM_PERCENTAGE
    component = {
        "name": "Batteri",
        "object_id": identifier,
        "unique_id": identifier,
        "state_topic": state_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "device_class": "battery",
        "unit_of_measurement": unit_of_measurement,
        "value_template": "{{ value_json.val | round(0) }}"
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/sensor/{identifier}/config", payload)

    # Queue statuses
    status = None
    if device.get("param") and device['param'].get('batteryPercentage'):
        value = device['param']['batteryPercentage']
        data = {
            "props": {
                "unit": unit_of_measurement
            },
            "serv": "battery",
            "type": "evt.health.report",
            "val": value,
        }

        payload = json.dumps(data)
        status = (state_topic, payload)
    return status

def sensor_lumin(
    device: typing.Any,
    mqtt,
    service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    identifier = f"fh_{address}_illuminance"
    state_topic = f"pt:j1/mt:evt{service['addr']}"
    unit_of_measurement = const.UOM_LUX
    component = {
        "name": "Belysningsstyrke",
        "object_id": identifier,
        "unique_id": identifier,
        "state_topic": state_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "device_class": "illuminance",
        "unit_of_measurement": unit_of_measurement,
        "value_template": "{{ value_json.val | round(0) }}"
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/sensor/{identifier}/config", payload)

    # Queue statuses
    status = None
    if device.get("param") and device['param'].get('illuminance'):
        value = device['param']['illuminance']
        data = {
            "props": {
                "unit": unit_of_measurement
            },
            "serv": "sensor_lumin",
            "type": "evt.sensor.report",
            "val": value,
            "val_t": "float",
        }

        payload = json.dumps(data)
        status = (state_topic, payload)
    return status

def sensor_temp(
    device: typing.Any,
    mqtt,
    service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    identifier = f"fh_{address}_temperature"
    state_topic = f"pt:j1/mt:evt{service['addr']}"
    unit_of_measurement = const.UOM_TEMPERATURE
    component = {
        "name": "Temperatur",
        "object_id": identifier,
        "unique_id": identifier,
        "state_topic": state_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "device_class": "temperature",
        "unit_of_measurement": unit_of_measurement,
        "value_template": "{{ value_json.val | round(0) }}"
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/sensor/{identifier}/config", payload)

    # Queue statuses
    status = None
    if device.get("param") and device['param'].get('temperature'):
        value = device['param']['temperature']
        data = {
            "props": {
                "unit": unit_of_measurement
            },
            "serv": "sensor_temp",
            "type": "evt.sensor.report",
            "val": value,
            "val_t": "float",
        }
        payload = json.dumps(data)
        status = (state_topic, payload)
    return status

def sensor_humid(
    device: typing.Any,
    mqtt,
    service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    identifier = f"fh_{address}_humidity"
    state_topic = f"pt:j1/mt:evt{service['addr']}"
    unit_of_measurement = const.UOM_PERCENTAGE
    component = {
        "name": "Luftfuktighet",
        "object_id": identifier,
        "unique_id": identifier,
        "state_topic": state_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "device_class": "humidity",
        "unit_of_measurement": unit_of_measurement,
        "value_template": "{{ value_json.val | round(0) }}"
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/sensor/{identifier}/config", payload)

    # Queue statuses
    status = None
    if device.get("param") and device['param'].get('humidity'):
        value = device['param']['humidity']
        data = {
            "props": {
                "unit": unit_of_measurement
            },
            "serv": "sensor_humid",
            "type": "evt.sensor.report",
            "val": value,
            "val_t": "float",
        }
        payload = json.dumps(data)
        status = (state_topic, payload)
    return status


def meter_elec(
    device: typing.Any,
    mqtt,
    service,
):
    address = device["fimp"]["address"]
    name = device["client"]["name"]
    room = device["room"]
    model = utils.get_model(device)

    is_energy = device.get("param") and device['param'].get('energy')
    is_wattage = device.get("param") and device['param'].get('wattage')

    device_class = const.DEVICE_CLASS_ENERGY if is_energy else const.DEVICE_CLASS_POWER
    state_class = const.STATE_CLASS_INCREASING if is_energy else const.STATE_CLASS_MEASUREMENT
    unit_of_measurement = const.UOM_ENERGY if is_energy else const.UOM_POWER

    identifier = f"fh_{address}_meter_elec"
    state_topic = f"pt:j1/mt:evt{service['addr']}"
    component = {
        "name": "Forbruk",
        "object_id": identifier,
        "unique_id": identifier,
        "state_topic": state_topic,
        "device": { 
            "name": name,
            "identifiers": address,
            "model": model,
            "suggested_area": room if room is not None else "Unknown"
        },
        "device_class": device_class,
        "state_class": state_class,
        "unit_of_measurement": unit_of_measurement,
        "value_template": "{{ value_json.val }}"
    }
    payload = json.dumps(component)
    mqtt.publish(f"homeassistant/sensor/{identifier}/config", payload)

    # Queue statuses
    status = None
    if is_energy:
        value = device['param']['energy']
        data = {
            "props": {
                "unit": unit_of_measurement
            },
            "serv": "meter_elec",
            "type": "evt.meter.report",
            "val": value,
        }
        payload = json.dumps(data)
        status = (state_topic, payload)
    elif is_wattage:
        value = device['param']['wattage']
        data = {
            "props": {
                "unit": unit_of_measurement
            },
            "serv": "meter_elec",
            "type": "evt.meter.report",
            "val": value,
        }
        payload = json.dumps(data)
        status = (state_topic, payload)

    return status
