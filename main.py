#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Bosch Rexroth AG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flask import Flask, render_template, jsonify, request, Blueprint
import os

import faulthandler
import signal
import sys
import time

import ctrlxdatalayer
from ctrlxdatalayer.variant import Result, Variant, VariantType

from fbsFunction import (
    getActualValues,
    setRobotActualValues,
    addToKin,
    removeFromKin,
    kinCmdAbortData,
    setKinCmdMove    
)

import datalayerProvider

if 'SNAP' in os.environ:
    root_path = os.getenv("SNAP")
    connection_string = "ipc://"
else:
    root_path = os.getcwd()
    connection_string = "tcp://boschrexroth:boschrexroth@10.0.2.2?sslport=8443"

template_path = root_path + '/templates'
static_path = root_path + '/static'

# Binary sampleSchema file
bfbs_file = root_path + "/bfbs/robotActualValues.bfbs"

# Binary metadata file
mddb_file = root_path + "/mddb/metadata.mddb"

# addresses of provided values
address_base = "sdk-py-provider/"

bp = Blueprint('lin-rob',__name__, static_folder=static_path, template_folder=template_path)

datalayer_system = ctrlxdatalayer.system.System("")
datalayer_system.start(False)

datalayer_client = datalayer_system.factory().create_client(connection_string)
datalayer_provider = datalayer_system.factory().create_provider(connection_string)

if datalayer_client is None or datalayer_provider is None:
    print("WARNING Connecting", connection_string, "failed.")
    datalayer_system.stop(False)
    sys.exit(1)

result = datalayer_provider.start()
if result != Result.OK:
    print(
       "ERROR Starting ctrlX Data Layer Provider failed with:",
        result,
        flush=True,
    )

datalayerProvider.register_fbs(datalayer_provider, "types/robot/core/fbtypes/RobotActualValues/RobotActualValues", bfbs_file)
datalayerProvider.register_mddb(datalayer_provider, mddb_file)
    
# Create nodes
provider_node_fbs = datalayerProvider.provide_fbs(datalayer_provider, "actual-value")
provider_node_str = datalayerProvider.provide_string(datalayer_provider, "app-cmd")

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/datalayer/get-actual-values', methods=['GET'])
def get_actual_value():
    result, data = datalayer_client.read_sync("motion/kin/Kinematics/state/values/actual")

    if (result!=Result.OK ):
        pos_x, pos_y, pos_z = getActualValues(data)
    
    variantFlatbuffers = setRobotActualValues(pos_x, pos_y, pos_z)
    
    result = datalayer_client.write_sync("sdk-py-provider/actual-value", variantFlatbuffers)
    
    return jsonify({"message": [pos_x,pos_y,pos_z,11,12,True]})

# API to fetch robot status
@bp.route('/api/datalayer/fetch-robot-status', methods=['GET'])
def get_robot_status():
    #motion/kin/Robot/state/opstate/plcopen
    result,data = datalayer_client.read_sync("motion/kin/Kinematics/state/opstate/plcopen")
    
    return jsonify({"status": data.get_string()})

#API to set the power status of the machine
@bp.route('/api/datalayer/set-power', methods=['POST'])
def set_power_value():
    variantBoolean = Variant()
    variantBoolean.set_bool8(True)
    result = datalayer_client.create_sync("motion/axs/AxisX/cmd/power",variantBoolean)
    
    variantBoolean = Variant()
    variantBoolean.set_bool8(True)
    result = datalayer_client.create_sync("motion/axs/AxisY/cmd/power",variantBoolean)
    
    variantBoolean = Variant()
    variantBoolean.set_bool8(True)
    result = datalayer_client.create_sync("motion/axs/AxisZ/cmd/power",variantBoolean)    
    
    variantBoolean = Variant()
    variantBoolean.set_bool8(True)
    result = datalayer_client.create_sync("motion/kin/Kinematics/cmd/group-ena", variantBoolean)
    
    variantFlatbuffersX = addToKin("Kinematics", False)
    variantFlatbuffersY = addToKin("Kinematics", False)
    variantFlatbuffersZ = addToKin("Kinematics", False)
    
    result = datalayer_client.create_sync("motion/axs/AxisX/cmd/add-to-kin",variantFlatbuffersX)
    result = datalayer_client.create_sync("motion/axs/AxisY/cmd/add-to-kin",variantFlatbuffersY)
    result = datalayer_client.create_sync("motion/axs/AxisZ/cmd/add-to-kin",variantFlatbuffersZ)  
    
    return jsonify({"message": "Values changed!!"})

@bp.route('/api/datalayer/set-power-off', methods=['POST'])
def set_power_value_off():

    variantBoolean = Variant()
    variantBoolean.set_bool8(True)
    result = datalayer_client.create_sync("motion/kin/Kinematics/cmd/group-dis", variantBoolean)

    variantFlatbuffersX = removeFromKin("Kinematics", False)
    variantFlatbuffersY = removeFromKin("Kinematics", False)
    variantFlatbuffersZ = removeFromKin("Kinematics", False)
    
    result = datalayer_client.create_sync("motion/axs/AxisX/cmd/rem-frm-kin",variantFlatbuffersX)
    result = datalayer_client.create_sync("motion/axs/AxisY/cmd/rem-frm-kin",variantFlatbuffersY)
    result = datalayer_client.create_sync("motion/axs/AxisZ/cmd/rem-frm-kin",variantFlatbuffersZ)  

    variantBoolean = Variant()
    variantBoolean.set_bool8(False)
    result = datalayer_client.create_sync("motion/axs/AxisX/cmd/power",variantBoolean)
    
    variantBoolean = Variant()
    variantBoolean.set_bool8(False)
    result = datalayer_client.create_sync("motion/axs/AxisY/cmd/power",variantBoolean)
    
    variantBoolean = Variant()
    variantBoolean.set_bool8(False)
    result = datalayer_client.create_sync("motion/axs/AxisZ/cmd/power",variantBoolean)    
    

    
    return jsonify({"message": "Values changed!!"})

#API to stop kinematics
@bp.route('/api/datalayer/stop-kinematics', methods=['POST'])
def set_kinematics_status():
    
    variantFlatbuffers = kinCmdAbortData()
   
    result = datalayer_client.create_sync("motion/kin/Kinematics/cmd/abort", variantFlatbuffers)
    
    return jsonify({"message": "Values changed!!"})

#API to set the target values
@bp.route('/api/datalayer/set-target-values', methods=['POST'])
def set_target_value():
    data=request.json
    print(data)
    
    variantFlatbuffers = setKinCmdMove([float(data['x']), float(data['y']), float(data['z'])], "WCS", 10*float(data['speed']), 100, 100, 1, 1)
   
    result = datalayer_client.create_sync("motion/kin/Kinematics/cmd/move-abs", variantFlatbuffers)
    
    print(data)
    
    return jsonify({"message": "Values changed!!"})

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/lin-rob')

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0', ssl_context='adhoc')