#!/usr/bin/env python3

# SPDX-FileCopyrightText: Bosch Rexroth AG
#
# SPDX-License-Identifier: MIT

import os
import signal
import sys
import time

import ctrlxdatalayer
import flatbuffers
from ctrlxdatalayer.variant import Result, Variant

from app.my_provider_node import MyProviderNode
from robot.core.fbtypes.RobotActualValues import (
    RobotActualValuesAddActualPosX,
    RobotActualValuesAddActualPosY,
    RobotActualValuesAddActualPosZ,
    RobotActualValuesEnd,
    RobotActualValuesStart,
)

# addresses of provided values
address_base = "webserver/"

def register_fbs(provider: ctrlxdatalayer.provider, name: str, path: str):
    # Register Flatbuffer type
    # ATTENTION: Use same type as in csv file
    result = provider.register_type(name, path)
    if result != Result.OK:
        print(
            "WARNING Registering",
            name,
            "failed with:",
            result,
            flush=True,
        )

def register_mddb(provider: ctrlxdatalayer.provider, path: str):    
    # Register Metadata Database
    result = provider.register_type("datalayer", path)
    print(result)
    if result != Result.OK:
        print(
            "WARNING Registering", path, "failed with:", result, flush=True
        )

def provide_fbs(provider: ctrlxdatalayer.provider, name: str):
    """provide_fbs"""
    # Create `FlatBufferBuilder`instance. Initial Size 1024 bytes (grows automatically if needed)
    builder = flatbuffers.Builder(1024)

    # Serialize InertialValue data (InertialValue.py auto generated from sampleSchema.fbs by flatc compiler)
    RobotActualValuesStart(builder)
    RobotActualValuesAddActualPosX(builder, 0.0),
    RobotActualValuesAddActualPosY(builder, 0.0),
    RobotActualValuesAddActualPosZ(builder, 0.0),
    robotActualvalues = RobotActualValuesEnd(builder)

    # Closing operation
    builder.Finish(robotActualvalues)
    variantFlatbuffers = Variant()
    result = variantFlatbuffers.set_flatbuffers(builder.Output())
    if result != ctrlxdatalayer.variant.Result.OK:
        print("ERROR creating variant flatbuffers failed with:", result, flush=True)
        return

    # Create and register flatbuffers provider node
    print("Creating flatbuffers provider node " + address_base + name, flush=True)
    provider_node_fbs = MyProviderNode(
        provider, address_base + name, variantFlatbuffers
    )
    result = provider_node_fbs.register_node()
    if result != ctrlxdatalayer.variant.Result.OK:
        print(
            "ERROR Registering node " + address_base + name + " failed with:",
            result,
            flush=True,
        )

    return provider_node_fbs


def provide_string(provider: ctrlxdatalayer.provider, name: str):
    """provide_string"""
    # Create and register simple string provider node
    print("Creating string  provider node " + address_base + name, flush=True)
    variantString = Variant()
    variantString.set_string("waiting for input")
    provider_node_str = MyProviderNode(provider, address_base + name, variantString)
    result = provider_node_str.register_node()
    if result != ctrlxdatalayer.variant.Result.OK:
        print(
            "ERROR Registering node " + address_base + name + " failed with:",
            result,
            flush=True,
        )

    return provider_node_str