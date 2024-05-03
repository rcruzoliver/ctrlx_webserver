import ctypes

import ctrlxdatalayer
from ctrlxdatalayer.clib import C_DLR_RESULT, address_c_char_p
from ctrlxdatalayer.clib_provider_node import (C_DLR_PROVIDER_NODE,
                                               C_DLR_PROVIDER_NODE_CALLBACKS)
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT

# ===================================================================
# provider.h
# ===================================================================

# typedef void *DLR_PROVIDER;
C_DLR_PROVIDER = ctypes.c_void_p

# void DLR_providerDelete(DLR_PROVIDER provider);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerDelete.argtypes = (
    C_DLR_PROVIDER,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerDelete.restype = None

pathname_c_char_p = ctypes.c_char_p

# DLR_RESULT DLR_providerRegisterType(DLR_PROVIDER provider, const char* address, const char* pathname);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterType.argtypes = (
    C_DLR_PROVIDER, address_c_char_p, pathname_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterType.restype = C_DLR_RESULT

# DLR_RESULT DLR_providerUnregisterType(DLR_PROVIDER provider, const char* address);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerUnregisterType.argtypes = (
    C_DLR_PROVIDER, address_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerUnregisterType.restype = C_DLR_RESULT

# DLR_RESULT DLR_providerRegisterNode(DLR_PROVIDER provider, const char* address, DLR_PROVIDER_NODE node);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterNode.argtypes = (
    C_DLR_PROVIDER, address_c_char_p, C_DLR_PROVIDER_NODE)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterNode.restype = C_DLR_RESULT

# DLR_RESULT DLR_providerUnregisterNode(DLR_PROVIDER provider, const char* address);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerUnregisterNode.argtypes = (
    C_DLR_PROVIDER, address_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerUnregisterNode.restype = C_DLR_RESULT

# DLR_RESULT DLR_providerSetTimeoutNode(DLR_PROVIDER provider, DLR_PROVIDER_NODE node, uint32_t timeoutMS);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerSetTimeoutNode.argtypes = (
    C_DLR_PROVIDER, C_DLR_PROVIDER_NODE, ctypes.c_uint32)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerSetTimeoutNode.restype = C_DLR_RESULT

# DLR_RESULT DLR_providerStart(DLR_PROVIDER provider);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerStart.argtypes = (
    C_DLR_PROVIDER,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerStart.restype = C_DLR_RESULT

# DLR_RESULT DLR_providerStop(DLR_PROVIDER provider);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerStop.argtypes = (
    C_DLR_PROVIDER,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerStop.restype = C_DLR_RESULT

# bool DLR_providerIsConnected(DLR_PROVIDER provider);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerIsConnected.argtypes = (
    C_DLR_PROVIDER,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerIsConnected.restype = ctypes.c_bool

# const DLR_VARIANT DLR_providerGetToken(DLR_PROVIDER provider);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerGetToken.argtypes = (
    C_DLR_PROVIDER,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerGetToken.restype = C_DLR_VARIANT

# DLR_RESULT DLR_providerRegisterTypeVariant(DLR_PROVIDER provider, const char* address, DLR_VARIANT data);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterTypeVariant.argtypes = (
    C_DLR_PROVIDER, address_c_char_p, C_DLR_VARIANT)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterTypeVariant.restype = C_DLR_RESULT
