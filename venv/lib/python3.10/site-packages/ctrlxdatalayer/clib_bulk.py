import ctypes

import ctrlxdatalayer
import ctrlxdatalayer.clib_client
from ctrlxdatalayer.clib import C_DLR_RESULT, address_c_char_p
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT


class C_BulkRequest(ctypes.Structure):
    """ BulkRequest """
    _fields_ = [('address', address_c_char_p),
                ('data', C_DLR_VARIANT)]


class C_VecBulkRequest(ctypes.Structure):
    """ Vector of bulk request """
    _fields_ = [('count', ctypes.c_size_t),
                ('request', ctypes.POINTER(C_BulkRequest))]


class C_BulkResponse(ctypes.Structure):
    """ BulkResponse """
    _fields_ = [('address', address_c_char_p),
                ('data', C_DLR_VARIANT),
                ('result', C_DLR_RESULT),
                ('timestamp', ctypes.c_uint64)]


class C_VecBulkResponse(ctypes.Structure):
    """ Vector of bulk response """
    _fields_ = [('count', ctypes.c_size_t),
                ('response', ctypes.POINTER(C_BulkResponse))]


# typedef void* DLR_BULK;
C_DLR_BULK = ctypes.c_void_p

# typedef void(*DLR_CLIENT_BULK_RESPONSE)(DLR_VEC_BULK_RESPONSE * response, void * userdata)
C_DLR_CLIENT_BULK_RESPONSE = ctypes.CFUNCTYPE(None,                             # None: return void
                                              ctypes.POINTER(C_VecBulkResponse), ctypes.c_void_p)

# DLR_RESULT DLR_bulkCreate(size_t count)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkCreate.argtypes = [
    ctypes.c_size_t]
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkCreate.restype = C_DLR_BULK

# void DLR_bulkDelete(DLR_BULK bulk);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkDelete.argtypes = [
    C_DLR_BULK]
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkDelete.restype = None

# size_t DLR_bulkGetCount(DLR_BULK bulk)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetCount.argtypes = [
    C_DLR_BULK]
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetCount.restype = ctypes.c_size_t

# DLR_RESULT DLR_bulkSetRequestAddress(DLR_BULK bulk, size_t index, char* address)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkSetRequestAddress.argtypes = (
    C_DLR_BULK, ctypes.c_size_t, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkSetRequestAddress.restype = C_DLR_RESULT

# DLR_RESULT DLR_bulkSetRequestData(DLR_BULK bulk, size_t index, char* address)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkSetRequestData.argtypes = (
    C_DLR_BULK, ctypes.c_size_t, C_DLR_VARIANT)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkSetRequestData.restype = C_DLR_RESULT

# char * DLR_bulkGetResponseAddress(DLR_BULK bulk, size_t index)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseAddress.argtypes = (
    C_DLR_BULK, ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseAddress.restype = ctypes.c_char_p

# DLR_VARIANT DLR_bulkGetResponseData(DLR_BULK bulk, size_t index)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseData.argtypes = (
    C_DLR_BULK, ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseData.restype = C_DLR_VARIANT

# uint64_t DLR_bulkGetResponseTimestamp(DLR_BULK bulk, size_t index)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseTimestamp.argtypes = (
    C_DLR_BULK, ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseTimestamp.restype = ctypes.c_uint64

# DLR_RESULT DLR_bulkGetResponseResult(DLR_BULK bulk, size_t index)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseResult.argtypes = (
    C_DLR_BULK, ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseResult.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBulkReadSync(DLR_CLIENT client, DLR_BULK bulk, const char* token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkReadSync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, C_DLR_BULK, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkReadSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBulkWriteSync(DLR_CLIENT client, DLR_BULK bulk, const char* token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkWriteSync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, C_DLR_BULK, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkWriteSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBulkBrowseSync(DLR_CLIENT client, DLR_BULK bulk, const char* token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkBrowseSync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, C_DLR_BULK, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkBrowseSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBulkCreateSync(DLR_CLIENT client, DLR_BULK bulk, const char* token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkCreateSync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, C_DLR_BULK, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkCreateSync.restype = C_DLR_RESULT

# DLR_RESULT libcomm_datalayer(DLR_CLIENT client, DLR_BULK bulk, const char* token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkDeleteSync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, C_DLR_BULK, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkDeleteSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBulkMetadataSync(DLR_CLIENT client, DLR_BULK bulk, const char* token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkMetadataSync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, C_DLR_BULK, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkMetadataSync.restype = C_DLR_RESULT

############################# Async ############################################
# DLR_RESULT DLR_createBulkRequest(size_t count)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_createBulkRequest.argtypes = [
    ctypes.c_size_t]
ctrlxdatalayer.clib.libcomm_datalayer.DLR_createBulkRequest.restype = ctypes.POINTER(
    C_VecBulkRequest)

# DLR_RESULT DLR_deleteBulkRequest(DLR_VEC_BULK_REQUEST** request)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_deleteBulkRequest.argtypes = [
    (ctypes.POINTER(ctypes.POINTER(C_VecBulkRequest)))]
ctrlxdatalayer.clib.libcomm_datalayer.DLR_deleteBulkRequest.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientReadBulkASync(DLR_CLIENT client, const DLR_VEC_BULK_REQUEST* request, const char* token, DLR_CLIENT_BULK_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadBulkASync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, ctypes.POINTER(
        C_VecBulkRequest), ctypes.c_char_p, C_DLR_CLIENT_BULK_RESPONSE, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadBulkASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientWriteBulkASync(DLR_CLIENT client, const DLR_VEC_BULK_REQUEST* request, const char* token, DLR_CLIENT_BULK_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteBulkASync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, ctypes.POINTER(
        C_VecBulkRequest), ctypes.c_char_p, C_DLR_CLIENT_BULK_RESPONSE, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteBulkASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientCreateBulkASync(DLR_CLIENT client, const DLR_VEC_BULK_REQUEST* request, const char* token, DLR_CLIENT_BULK_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateBulkASync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, ctypes.POINTER(
        C_VecBulkRequest), ctypes.c_char_p, C_DLR_CLIENT_BULK_RESPONSE, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateBulkASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientDeleteBulkASync(DLR_CLIENT client, const DLR_VEC_BULK_REQUEST* request, const char* token, DLR_CLIENT_BULK_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientDeleteBulkASync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, ctypes.POINTER(
        C_VecBulkRequest), ctypes.c_char_p, C_DLR_CLIENT_BULK_RESPONSE, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientDeleteBulkASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBrowseBulkASync(DLR_CLIENT client, const DLR_VEC_BULK_REQUEST* request, const char* token, DLR_CLIENT_BULK_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseBulkASync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, ctypes.POINTER(
        C_VecBulkRequest), ctypes.c_char_p, C_DLR_CLIENT_BULK_RESPONSE, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseBulkASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientMetadataBulkASync(DLR_CLIENT client, const DLR_VEC_BULK_REQUEST* request, const char* token, DLR_CLIENT_BULK_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataBulkASync.argtypes = (
    ctrlxdatalayer.clib_client.C_DLR_CLIENT, ctypes.POINTER(
        C_VecBulkRequest), ctypes.c_char_p, C_DLR_CLIENT_BULK_RESPONSE, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataBulkASync.restype = C_DLR_RESULT
