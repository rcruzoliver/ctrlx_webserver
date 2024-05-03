import ctypes

import ctrlxdatalayer
from ctrlxdatalayer.clib import (C_DLR_CONVERTER, C_DLR_RESULT,
                                 address_c_char_p, userData_c_void_p)
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT


class C_NotifyItem(ctypes.Structure):
    """ NotifyItem """
    _fields_ = [('data', C_DLR_VARIANT),
                ('info', C_DLR_VARIANT)]


# typedef void* DLR_CLIENT;
C_DLR_CLIENT = ctypes.c_void_p

# typedef void(*DLR_CLIENT_RESPONSE)(DLR_RESULT, DLR_VARIANT, void*);
C_DLR_CLIENT_RESPONSE = ctypes.CFUNCTYPE(
    None, ctypes.c_int32, ctypes.c_void_p, ctypes.c_void_p)  # None: return void

# typedef void(*DLR_CLIENT_NOTIFY_RESPONSE)(DLR_RESULT, NotifyItem*, uint32_t, void*);
C_DLR_CLIENT_NOTIFY_RESPONSE = ctypes.CFUNCTYPE(
    None, C_DLR_RESULT, ctypes.POINTER(C_NotifyItem), ctypes.c_uint32, ctypes.c_void_p)

# void DLR_clientDelete(DLR_CLIENT client);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientDelete.argtypes = (C_DLR_CLIENT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientDelete.restype = None

# DLR_RESULT DLR_clientPingSync(DLR_CLIENT client);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientPingSync.argtypes = (C_DLR_CLIENT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientPingSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientCreateSync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientRemoveSync(DLR_CLIENT client, const char* address, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientRemoveSync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientRemoveSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBrowseSync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseSync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientReadSync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadSync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientWriteSync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteSync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientMetadataSync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataSync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientPingASync(DLR_CLIENT client, DLR_CLIENT_RESPONSE callback, void *userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientPingASync.argtypes = (
    C_DLR_CLIENT, C_DLR_CLIENT_RESPONSE, userData_c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientPingASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientCreateASync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token, DLR_CLIENT_RESPONSE callback, void *userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateASync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, userData_c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientRemoveASync(DLR_CLIENT client, const char* address, const char* token, DLR_CLIENT_RESPONSE callback, void *userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientRemoveASync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, userData_c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientRemoveASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientBrowseASync(DLR_CLIENT client, const char* address, const char* token, DLR_CLIENT_RESPONSE callback, void *userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseASync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, userData_c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientReadASync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token, DLR_CLIENT_RESPONSE callback, void *userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadASync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, userData_c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientWriteASync(DLR_CLIENT client, const char* address, DLR_VARIANT variant, const char* token, DLR_CLIENT_RESPONSE callback, void *userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteASync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_void_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, userData_c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteASync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientMetadataASync(DLR_CLIENT client, const char* address, const char* token, DLR_CLIENT_RESPONSE callback, void *userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataASync.argtypes = (
    C_DLR_CLIENT, address_c_char_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, userData_c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataASync.restype = C_DLR_RESULT

token_c_char_p = ctypes.c_char_p

# DLR_RESULT DLR_clientCreateSubscriptionSync(DLR_CLIENT client, DLR_VARIANT ruleset, DLR_CLIENT_NOTIFY_RESPONSE publishCallback, void* userdata, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSubscriptionSync.argtypes = (
    C_DLR_CLIENT, C_DLR_VARIANT, C_DLR_CLIENT_NOTIFY_RESPONSE, userData_c_void_p, token_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSubscriptionSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientSubscribeSync(DLR_CLIENT client, const char* id, const char* address);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeSync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p, address_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientSubscribeMultiSync(DLR_CLIENT client, const char* id, const char** address, uint32_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeMultiSync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p,  ctypes.POINTER(address_c_char_p), ctypes.c_uint32)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeMultiSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientUnsubscribeSync(DLR_CLIENT client, const char* id, const char* address);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeSync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientUnsubscribeMultiSync(DLR_CLIENT client, const char* id, const char** address, uint32_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeMultiSync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p, ctypes.POINTER(address_c_char_p), ctypes.c_uint32)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeMultiSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientUnsubscribeAllSync(DLR_CLIENT client, const char* id);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAllSync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAllSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientCreateSubscriptionAsync(DLR_CLIENT client, DLR_VARIANT ruleset, DLR_CLIENT_NOTIFY_RESPONSE publishCallback, DLR_CLIENT_RESPONSE callback, void* userdata, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSubscriptionAsync.argtypes = (
    C_DLR_CLIENT, C_DLR_VARIANT, C_DLR_CLIENT_NOTIFY_RESPONSE, C_DLR_CLIENT_RESPONSE, userData_c_void_p, token_c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSubscriptionAsync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientSubscribeAsync(DLR_CLIENT client, const char* id, const char* address, DLR_CLIENT_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeAsync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, ctypes.c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeAsync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientSubscribeMultiAsync(DLR_CLIENT client, const char* id, const char** address, uint32_t count, DLR_CLIENT_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeMultiAsync.argtypes = (C_DLR_CLIENT, ctypes.c_char_p, ctypes.POINTER(
    ctypes.c_char_p), ctypes.c_uint32, C_DLR_CLIENT_RESPONSE, ctypes.c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeMultiAsync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientUnsubscribeAsync(DLR_CLIENT client, const char* id, const char* address, DLR_CLIENT_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAsync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, ctypes.c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAsync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientUnsubscribeMultiAsync(DLR_CLIENT client, const char* id, const char** address, uint32_t count, DLR_CLIENT_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeMultiAsync.argtypes = (C_DLR_CLIENT, ctypes.c_char_p, ctypes.POINTER(
    ctypes.c_char_p), ctypes.c_uint32, C_DLR_CLIENT_RESPONSE, ctypes.c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeMultiAsync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientUnsubscribeAllAsync(DLR_CLIENT client, const char* id, DLR_CLIENT_RESPONSE callback, void* userdata);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAllAsync.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p, C_DLR_CLIENT_RESPONSE, ctypes.c_void_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAllAsync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientSetTimeout(DLR_CLIENT client, DLR_TIMEOUT_SETTING timeout, uint32_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSetTimeout.argtypes = (
    C_DLR_CLIENT, ctypes.c_int32, ctypes.c_uint32)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSetTimeout.restype = C_DLR_RESULT

# bool DLR_clientIsConnected(DLR_CLIENT client);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientIsConnected.argtypes = (
    C_DLR_CLIENT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientIsConnected.restype = ctypes.c_bool

# void DLR_clientSetAuthToken(DLR_CLIENT client, const char* token);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSetAuthToken.argtypes = (
    C_DLR_CLIENT, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSetAuthToken.restype = None

# const char* DLR_clientGetAuthToken(DLR_CLIENT client);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientGetAuthToken.argtypes = (
    C_DLR_CLIENT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientGetAuthToken.restype = ctypes.c_char_p

# DLR_RESULT DLR_clientReadJsonSync(DLR_CLIENT client, DLR_CONVERTER converter, const char * address, DLR_VARIANT json, int32_t indentStep, const char * token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadJsonSync.argtypes = (
    C_DLR_CLIENT, C_DLR_CONVERTER, ctypes.c_char_p, C_DLR_VARIANT, ctypes.c_int32, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadJsonSync.restype = C_DLR_RESULT

# DLR_RESULT DLR_clientWriteJsonSync(DLR_CLIENT client, DLR_CONVERTER converter, const char * address, const char * json, DLR_VARIANT error, const char * token)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteJsonSync.argtypes = (
    C_DLR_CLIENT, C_DLR_CONVERTER, ctypes.c_char_p, ctypes.c_char_p, C_DLR_VARIANT, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteJsonSync.restype = C_DLR_RESULT


