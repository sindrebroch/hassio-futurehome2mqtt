import json
import time

import paho.mqtt.client as client

import pyfimptoha.binary_sensor as bs
import pyfimptoha.const as const
import pyfimptoha.cover as cover
import pyfimptoha.sensor as sensor
import pyfimptoha.switch as switch
import pyfimptoha.light as light
import pyfimptoha.lock as lock
import pyfimptoha.utils as utils

def create_components(
    devices: list,
    mqtt: client,
):
    """
    Creates HA components out of FIMP devices by pushing them to HA using mqtt discovery
    """

    print('Received list of devices from FIMP. FIMP reported %s devices' % (len(devices)))

    statuses = []

    for device in devices:
        id = device["id"]
        thing = device["thing"]
        address = device["fimp"]["address"]
        name = device["client"]["name"]
        functionality = device["functionality"]
        room = device["room"]
        model = utils.get_model(device)

        print(f"Creating: {address} - {name}")
        print(f"- IDs: {id} - {thing} - {address}")
        print(f"- Room: {room}")
        print(f"- Model: {model}")
        print(f"- Functionality: {functionality}")
        print(f"- Device: {device}")

        for service_name, service in device["services"].items():
            status = None
            _type = utils.get_type(device)


            match service_name:
                case const.SERVICE_SENSOR_PRESENCE:
                    entity = bs.BinarySensorPresence(mqtt, device, service, service_name)
                    status = entity.status()
                    statuses.append(status) if status
                case "battery":
                    entity = sensor.SensorBattery(mqtt, device, service, service_name)
                    status = entity.status()
                    statuses.append(status) if status



            if _type == "blinds" and service_name == "out_lvl_switch":
                print(f"- Service: {service_name} (as blind/cover)")
                status = cover.blind(
                    device=device,
                    mqtt=mqtt,
                    service=service,
                )
            elif service_name == "meter_elec":
                print(f"- Service: {service_name}")
                status = sensor.meter_elec(
                    device=device,
                    mqtt=mqtt,
                    service=service,
                )
            elif service_name == "sensor_lumin":
                print(f"- Service: {service_name}")
                status = sensor.sensor_lumin(
                    device=device,
                    mqtt=mqtt,
                    service=service,
                )
            elif service_name == "sensor_temp":
                print(f"- Service: {service_name}")
                status = sensor.sensor_temp(
                    device=device,
                    mqtt=mqtt,
                    service=service,
                )
            elif service_name == "sensor_humid":
                print(f"- Service: {service_name}")
                status = sensor.sensor_humid(
                    device=device,
                    mqtt=mqtt,
                    service=service,
                )
            elif service_name == "sensor_power":
                print(f"- Service: {service_name}")
            elif service_name == "sensor_atmo":
                print(f"- Service: {service_name}")
            elif service_name == "media_player":
                print(f"- Service: {service_name}")
            elif service_name == "basic":
                print(f"- Service: {service_name}")
            elif service_name == "thermostat":
                print(f"- Service: {service_name}")
            elif service_name == "vinculum":
                print(f"- Service: {service_name}")
            elif service_name == "user_code":
                print(f"- Service: {service_name}")
            elif service_name == "technology_specific":
                print(f"- Service: {service_name}")
            elif service_name == "alarm_burglar":
                print(f"- Service: {service_name}")
            elif service_name == "alarm_emergency":
                print(f"- Service: {service_name}")
            elif service_name == "alarm_lock":
                print(f"- Service: {service_name}")
            elif service_name == "dev_sys":
                print(f"- Service: {service_name}")
            elif service_name == "version":
                print(f"- Service: {service_name}")

            if status:
                statuses.append(status)

            # Door lock
            elif _type == "door_lock":
                print(f"- Service: {service_name}")
                status = lock.door_lock(
                    device=device,
                    mqtt=mqtt,
                    service=service,
                )
                if status:
                    statuses.append(status)

            # Lights
            elif functionality == "lighting":
                status = None
                if service_name == "out_lvl_switch":
                    print(f"- Service: {functionality} - {service_name}")
                    status = light.out_lvl_switch(
                        service_name=service_name,
                        device=device,
                        mqtt=mqtt,
                        service=service,
                    )
                elif service_name == "out_bin_switch":
                    print(f"- Service: {functionality} - {service_name}")
                    status = light.out_bin_switch(
                        service_name=service_name,
                        device=device,
                        mqtt=mqtt,
                        service=service,
                    )

                if status:
                    statuses.append(status)

            # Appliance
            elif functionality == "appliance":
                # Binary switch
                if service_name == "out_bin_switch":
                    print(f"- Service: {functionality} - {service_name}")
                    status = switch.appliance_switch(
                        device=device,
                        mqtt=mqtt,
                        service_name=service_name,
                        service=service,
                    )
                pass

    mqtt.loop()
    time.sleep(2)
    print("Publishing statuses...")
    for state in statuses:
        topic = state[0]
        payload = state[1]
        mqtt.publish(topic, payload)
        print(topic)
    print("Finished pushing statuses...")
