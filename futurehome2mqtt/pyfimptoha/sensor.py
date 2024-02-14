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

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "battery",
            "state_class": const.STATE_CLASS_MEASUREMENT,
            "value_template": "{{ value_json.val | round(0) }}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('batteryPercentage'):
            value = self.device['param']['batteryPercentage']
            data = {
                "props": {
                    "unit": self.unit_of_measurement
                },
                "serv": "battery",
                "type": "evt.health.report",
                "val": value,
            }
            statuses.append(super().status(data))

class SensorLuminance(Sensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Illuminance"
        self.entity_identifier = "illuminance"
        self.unit_of_measurement = const.UOM_LUX
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "illuminance",
            "state_class": const.STATE_CLASS_MEASUREMENT,
            "value_template": "{{ value_json.val | round(0) }}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('illuminance'):
            value = self.device['param']['illuminance']
            data = {
                "props": {
                    "unit": self.unit_of_measurement
                },
                "serv": "sensor_lumin",
                "type": "evt.sensor.report",
                "val": value,
                "val_t": "float",
            }
            statuses.append(super().status(data))

class SensorTemperature(Sensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Temperature"
        self.entity_identifier = "temperature"
        self.unit_of_measurement = const.UOM_TEMPERATURE
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "temperature",
            "state_class": const.STATE_CLASS_MEASUREMENT,
            "value_template": "{{ value_json.val | round(2) }}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('temperature'):
            value = self.device['param']['temperature']
            data = {
                "props": {
                    "unit": self.unit_of_measurement
                },
                "serv": "sensor_temp",
                "type": "evt.sensor.report",
                "val": value,
                "val_t": "float",
            }
            statuses.append(super().status(data))

class SensorHumidity(Sensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Humidity"
        self.entity_identifier = "humidity"
        self.unit_of_measurement = const.UOM_PERCENTAGE
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "humidity",
            "state_class": const.STATE_CLASS_MEASUREMENT,
            "value_template": "{{ value_json.val | round(0) }}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('humidity'):
            value = self.device['param']['humidity']
            data = {
                "props": {
                    "unit": self.unit_of_measurement
                },
                "serv": "sensor_humid",
                "type": "evt.sensor.report",
                "val": value,
                "val_t": "float",
            }
            statuses.append(super().status(data))

class SensorAtmo(Sensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Pressure"
        self.entity_identifier = "pressure"
        self.unit_of_measurement = "hPa"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "atmospheric_pressure",
            "state_class": const.STATE_CLASS_MEASUREMENT,
            "value_template": "{{ value_json.val | round(1) }}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('pressure'):
            value = self.device['param']['pressure']
            data = {
                "props": {
                    "unit": self.unit_of_measurement
                },
                "serv": "sensor_atmo",
                "type": "evt.sensor.report",
                "val": value,
                "val_t": "float",
            }
            statuses.append(super().status(data))

class SensorPower(Sensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "Power"
        self.entity_identifier = "power"
        self.unit_of_measurement = "W"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "power",
            "state_class": const.STATE_CLASS_MEASUREMENT,
            "value_template": "{{ value_json.val | round(0) }}"
        })
        return comp

    def add_status(self, statuses):
        if self.device.get("param") and self.device['param'].get('wattage'):
            value = self.device['param']['wattage']
            data = {
                "props": {
                    "unit": self.unit_of_measurement
                },
                "serv": "sensor_power",
                "type": "evt.sensor.report",
                "val": value,
                "val_t": "float",
            }
            statuses.append(super().status(data))

class SensorCO2(Sensor):

    def __init__(self, mqtt, device, service, service_name):
        self.component_name = "CO2"
        self.entity_identifier = "co2"
        self.unit_of_measurement = "ppm"
        super().__init__(mqtt, device, service, service_name)

    def component(self):
        comp = super().component()
        comp.update({
            "device_class": "carbon_dioxide",
            "state_class": const.STATE_CLASS_MEASUREMENT,
            "value_template": "{{ value_json.val | round(0) }}"
        })
        return comp

    def add_status(self, statuses):
        print(f"Status for CO2 {self.device}")

        value = "Unknown"
        data = {
            "props": {
                "unit": self.unit_of_measurement
            },
            "serv": "sensor_co2",
            "type": "evt.sensor.report",
            "val": value,
            "val_t": "float",
        }
        statuses.append(super().status(data))
