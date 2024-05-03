import ctypes

import ctrlxdatalayer
from ctrlxdatalayer.clib_factory import C_DLR_FACTORY
from ctrlxdatalayer.converter import C_DLR_CONVERTER

# typedef void *DLR_SYSTEM;
C_DLR_SYSTEM = ctypes.c_void_p

ipcPath_c_char_p = ctypes.c_void_p
# DLR_SYSTEM DLR_systemCreate(const char* ipcPath);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemCreate.argtypes = (ctypes.c_char_p,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemCreate.restype = C_DLR_SYSTEM

# void DLR_systemDelete(DLR_SYSTEM system);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemDelete.argtypes = (C_DLR_SYSTEM,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemDelete.restype = None

# DLR_FACTORY DLR_systemFactory(DLR_SYSTEM system);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemFactory.argtypes = (C_DLR_SYSTEM,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemFactory.restype = C_DLR_FACTORY

# DLR_CONVERTER DLR_systemJsonConverter(DLR_SYSTEM system);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemJsonConverter.argtypes = (
    C_DLR_SYSTEM,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemJsonConverter.restype = C_DLR_CONVERTER

boStartBroker_c_bool = ctypes.c_bool
# void DLR_systemStart(DLR_SYSTEM system, bool boStartBroker);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemStart.argtypes = (
    C_DLR_SYSTEM, boStartBroker_c_bool)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemStart.restype = None

boForceProviderStop_c_bool = ctypes.c_bool
# bool DLR_systemStop(DLR_SYSTEM system, bool boForceProviderStop);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemStop.argtypes = (
    C_DLR_SYSTEM, boForceProviderStop_c_bool)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemStop.restype = ctypes.c_bool

path_c_char_p = ctypes.c_char_p
# void DLR_systemSetBfbsPath(DLR_SYSTEM system, const char* path);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemSetBfbsPath.argtypes = (
    C_DLR_SYSTEM, path_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemSetBfbsPath.restype = None
