"""
Creates sensors in Home Assistant based on FIMP services
"""
import json
import typing

import pyfimptoha.const as const
import pyfimptoha.entity as entity
import pyfimptoha.utils as utils

class SensorMeterElec(entity.CustomEntity):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "MeterElec"
        self.entity_identifier = "meter_elec"

        # print(f"Meter elec {device}")

        # unit = device["props"]["unit"]
        # self.unit_of_measurement = "W"
        # super().__init__(mqtt, device, service, service_name)

        # device_class = const.DEVICE_CLASS_ENERGY if is_energy else const.DEVICE_CLASS_POWER
        # state_class = const.STATE_CLASS_INCREASING if is_energy else const.STATE_CLASS_MEASUREMENT
        # unit_of_measurement = const.UOM_ENERGY if is_energy else const.UOM_POWER

    #def component(self):
    #    comp = super().component()
    #    return comp

    #def add_status(self, statuses):
    #    print("Add status")

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



# https://github.com/futurehomeno/fimp-api/blob/15ddaea376f050003bfcc668613573c18df4dd0a/device_services/generic/meter.md#service-names
# dc_i
# dc_p
# dc_u
# e_export
# e_export_apparent
# e_export_react
# e_import
# e_import_apparent
# e_import_react
# e1_export
# e1_import
# e2_export
# e2_import
# e3_export
# e3_import
# freq
# i
# i_export
# i1
# i1_export
# i2
# i2_export
# i3
# i3_export
# p_export
# p_export_apparent
# p_export_react
# p_factor
# p_factor_export
# p_import
# p_import_apparent
# p_import_react
# p1
# p1_export
# p1_export_apparent
# p1_export_react
# p1_factor
# p1_factor_export
# p1_import_apparent
# p1_import_react
# p2
# p2_export
# p2_export_apparent
# p2_export_react
# p2_factor
# p2_factor_export
# p2_import_apparent
# p2_import_react
# p3
# p3_export
# p3_export_apparent
# p3_export_react
# p3_factor
# p3_factor_export
# p3_import_apparent
# p3_import_react
# u
# u_export
# u1
# u1_export
# u2
# u2_export
# u3
# u3_export

# "val": {
#     "e_export": 0,
#     "e_import": 29685.4,
#     "i1": 3.8,
#     "i2": 0,
#     "i3": 5.5,
#     "last_e_export": 0,
#     "last_e_import": 11.436662,
#     "p_export": 0,
#     "p_export_max": 0,
#     "p_export_min": 0,
#     "p_import": 1608,
#     "p_import_avg": 1060.5,
#     "p_import_max": 3656,
#     "p_import_min": 311,
#     "u1": 233.2,
#     "u2": 230.5,
#     "u3": 230.8
# },