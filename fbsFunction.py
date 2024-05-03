from motion.core.fbtypes.KinActualValues import KinActualValues
import motion.core.fbtypes.KinCmdMoveData #import KinCmdMoveData
import motion.core.fbtypes.DynamicLimits 
import flatbuffers

from ctrlxdatalayer.variant import Result, Variant, VariantType

from motion.core.fbtypes.KinActualValues import (
    KinActualValues    
)

from motion.core.fbtypes.KinCmdMoveData import (
    KinCmdMoveDataStartKinPosVector,
    KinCmdMoveDataAddKinPos,
    KinCmdMoveDataAddLim,
    KinCmdMoveDataAddCoordSys,
    KinCmdMoveDataStart,
    KinCmdMoveDataEnd
)

from motion.core.fbtypes.DynamicLimits import (
    DynamicLimitsAddVel,
    DynamicLimitsAddAcc,
    DynamicLimitsAddDec,
    DynamicLimitsAddJrkAcc,
    DynamicLimitsAddJrkDec,
    DynamicLimitsStart,
    DynamicLimitsEnd
)

from motion.core.fbtypes.AxsCmdAddToKinData import (
    AxsCmdAddToKinDataAddKinName,
    AxsCmdAddToKinDataAddBuffered,
    AxsCmdAddToKinDataStart,
    AxsCmdAddToKinDataEnd
)

from motion.core.fbtypes.BrakeLimit import (
    BrakeLimit
)

from motion.core.fbtypes.KinCmdAbortData import (
    KinCmdAbortDataAddType,
    KinCmdAbortDataEnd,
    KinCmdAbortDataStart
)

from robot.core.fbtypes.RobotActualValues import (
    RobotActualValuesAddActualPosX,
    RobotActualValuesAddActualPosY,
    RobotActualValuesAddActualPosZ,
    RobotActualValuesEnd,
    RobotActualValuesStart
)



def getActualValues(data: Variant):
    root = KinActualValues.GetRootAsKinActualValues(data.get_flatbuffers(), 0)
    
    return(root.ActualPos(0), root.ActualPos(1), root.ActualPos(2))


def setRobotActualValues(x ,y, z):
    builder = flatbuffers.Builder(1024)
    
    RobotActualValuesStart(builder)
    RobotActualValuesAddActualPosX(builder, x),
    RobotActualValuesAddActualPosY(builder, y),
    RobotActualValuesAddActualPosZ(builder, z),
    robot_actual_values = RobotActualValuesEnd(builder)
    
    builder.Finish(robot_actual_values)
    variantFlatbuffers = Variant()
    variantFlatbuffers.set_flatbuffers(builder.Output())
    
    return variantFlatbuffers


def addToKin(kin: str, buffered: bool):
    builder = flatbuffers.Builder(1024)
    kinfb = builder.CreateString(kin)
    
    AxsCmdAddToKinDataStart(builder)
    AxsCmdAddToKinDataAddKinName(builder, kinfb)
    AxsCmdAddToKinDataAddBuffered(builder, buffered)
    axs_cmd_abort_data = AxsCmdAddToKinDataEnd(builder)
    
    builder.Finish(axs_cmd_abort_data)
    variantFlatbuffers = Variant()
    variantFlatbuffers.set_flatbuffers(builder.Output())
    
    return variantFlatbuffers


def kinCmdAbortData():
    builder = flatbuffers.Builder(1024)
    
    KinCmdAbortDataStart(builder)
    KinCmdAbortDataAddType(builder, BrakeLimit.LAST_COMMANDED_LIMITS)
    kin_cmd_abort_data = KinCmdAbortDataEnd(builder)
    
    builder.Finish(kin_cmd_abort_data)
    variantFlatbuffers = Variant()
    variantFlatbuffers.set_flatbuffers(builder.Output())
    
    return variantFlatbuffers


def setDynamicLimits(builder, limVel: float, limAcc: float, limDec: float, limJrkAcc: float, limJrkDec: float):
    
    print(limVel, limAcc, limDec)
    DynamicLimitsStart(builder)
    DynamicLimitsAddVel(builder, limVel) 
    DynamicLimitsAddAcc(builder, limAcc)
    DynamicLimitsAddDec(builder, limDec)
    DynamicLimitsAddJrkAcc(builder, limJrkAcc)
    DynamicLimitsAddJrkDec(builder, limJrkDec)   
    dynamic_limit = DynamicLimitsEnd(builder)
    
    return dynamic_limit


def setKinCmdMove(pos: [float], coor_sys: str, limVel: float, limAcc: float, limDec: float, limJrkAcc: float, limJrkDec: float):
    builder = flatbuffers.Builder(1024)
    
    lim = setDynamicLimits(builder ,limVel, limAcc, limDec, limJrkAcc, limJrkDec)
    
    KinCmdMoveDataStartKinPosVector(builder, 16)
    
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(0.0)
    builder.PrependFloat64(float(pos[2])) #target position of z
    builder.PrependFloat64(float(pos[1])) #target position of y
    builder.PrependFloat64(float(pos[0])) #target position of x
    
    kin_pos = builder.EndVector(16)
    
    fb_coorsys = builder.CreateString(coor_sys)
    
    KinCmdMoveDataStart(builder)
   
    KinCmdMoveDataAddKinPos(builder, kin_pos)
    KinCmdMoveDataAddLim(builder, lim)
    KinCmdMoveDataAddCoordSys(builder, fb_coorsys)
   
    kin_cmd_move_data = KinCmdMoveDataEnd(builder)
   
    builder.Finish(kin_cmd_move_data)
    variantFlatbuffers = Variant()
    variantFlatbuffers.set_flatbuffers(builder.Output())
    
    return variantFlatbuffers   