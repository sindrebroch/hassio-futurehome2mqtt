"""
Utils for FIMP services
"""

import typing

def get_model(device: typing.Any):
    try:
        return device["modelAlias"]
    except KeyError:
        return device["model"]
