"""
Utils for FIMP services
"""

import typing

def get_type(device: typing.Any):
    try:
        _type = device['type']['type']
    except KeyError:
        _type = None
    return _type

def get_model(device: typing.Any):
    try:
        return device["modelAlias"]
    except KeyError:
        return device["model"]

def get_room(device: typing.Any):
    room = device["room"]
    return room if room is not None else "Unknown"

