import ctypes

import ctrlxdatalayer
from ctrlxdatalayer.clib_client import C_DLR_CLIENT
from ctrlxdatalayer.clib_provider import C_DLR_PROVIDER

# ===================================================================
# factory.h
# ===================================================================

# typedef void *DLR_FACTORY;
C_DLR_FACTORY = ctypes.c_void_p
remote_c_char_p = ctypes.c_char_p

# DLR_CLIENT DLR_factoryCreateClient(DLR_FACTORY factory, const char* remote);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_factoryCreateClient.argtypes = (
    C_DLR_FACTORY, remote_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_factoryCreateClient.restype = C_DLR_CLIENT

# DLR_PROVIDER DLR_factoryCreateProvider(DLR_FACTORY factory, const char* remote);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_factoryCreateProvider.argtypes = (
    C_DLR_FACTORY, remote_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_factoryCreateProvider.restype = C_DLR_PROVIDER
