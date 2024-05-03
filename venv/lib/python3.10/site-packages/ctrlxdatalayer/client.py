"""
class Client
"""
import ctypes
import typing
from enum import Enum

import ctrlxdatalayer
import ctrlxdatalayer.clib
import ctrlxdatalayer.subscription
from ctrlxdatalayer.clib import userData_c_void_p
from ctrlxdatalayer.clib_client import C_DLR_CLIENT, C_DLR_CLIENT_RESPONSE
from ctrlxdatalayer.converter import Converter
from ctrlxdatalayer.variant import Result, Variant, VariantRef

ResponseCallback = typing.Callable[[
    Result, typing.Optional[Variant], ctrlxdatalayer.clib.userData_c_void_p], None]


class _CallbackPtr:
    """
        Callback wrapper
    """
    __slots__ = ['_ptr']

    def __init__(self):
        """
        init _CallbackPtr
        """
        self._ptr: typing.Optional[ctypes._CFuncPtr] = None

    def set_ptr(self, ptr):
        """
        setter CallbackPtr
        """
        self._ptr = ptr

    def get_ptr(self):
        """
        getter CallbackPtr
        """
        return self._ptr


class TimeoutSetting(Enum):
    """
    Settings of different timeout values
    """
    IDLE = 0
    PING = 1
    Reconnect = 2


class Client:
    """
    Client interface for accessing data from the system

    Hint: see python context manager for instance handling
    """
    # problem with weakref.ref
    #__slots__ = ['__closed', '__client', '__token', '__ptrs', '__subs']

    def __init__(self, c_client: C_DLR_CLIENT):
        """
        @param[in]  client    Reference to the client
        """
        self.__closed = False
        self.__client: C_DLR_CLIENT = c_client
        self.__token = None
        self.__ptrs: typing.List[_CallbackPtr] = []
        self.__subs: typing.List[ctrlxdatalayer.subscription.Subscription] = [
        ]

    def __enter__(self):
        """
        use the python context manager
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        use the python context manager
        """
        self.close()

    def close(self):
        """
        closes the client instance
        """
        if self.__closed:
            return
        self.__closed = True
        self.__close_all_subs()
        self.__subs.clear()

        ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientDelete(self.__client)
        self.__ptrs.clear()
        del self.__subs
        del self.__ptrs
        self.__token = None

    def get_handle(self):
        """
        handle value of Client
        """
        return self.__client

    def get_token(self):
        """
        internal token
        """
        return self.__token

    def __create_callback(self, cb: ResponseCallback):
        """
        callback management
        """
        cb_ptr = _CallbackPtr()
        self.__ptrs.append(cb_ptr)

        def _cb(c_result: ctrlxdatalayer.clib.C_DLR_RESULT,
                c_data: ctypes.c_void_p, c_userdata: ctypes.c_void_p):
            """
            datalayer calls this function
            """
            if c_data is None:
                cb(Result(c_result), None, c_userdata)
            else:
                data = VariantRef(c_data)
                cb(Result(c_result), data, c_userdata)
            cb_ptr.set_ptr(None)  # remove cyclic dependency
            self.__ptrs.remove(cb_ptr)

        cb_ptr.set_ptr(C_DLR_CLIENT_RESPONSE(_cb))
        return cb_ptr.get_ptr()

    def _test_callback(self, cb: ResponseCallback):
        """
            internal use
        """
        return self.__create_callback(cb)

    def set_timeout(self, timeout: TimeoutSetting, value: int) -> Result:
        """
        Set client timeout value
        @param[in]  timeout   Timeout to set (see DLR_TIMEOUT_SETTING)
        @param[in]  value     Value to set
        @returns <Result>, status of function call
        """
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSetTimeout(
            self.__client, timeout.value, value))

    def is_connected(self) -> bool:
        """
        returns whether provider is connected
        @returns <bool> status of connection
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientIsConnected(self.__client)

    def set_auth_token(self, token: str):
        """
        Set persistent security access token for authentication as JWT payload
        @param[in]  token  Security access &token for authentication
        """
        if token is None:
            raise TypeError('token is invalid')
        self.__token = token.encode('utf-8')
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSetAuthToken(
            self.__client, self.__token)

    def get_auth_token(self) -> str:
        """
        returns persistent security access token for authentication
        @returns <str> security access token for authentication
        """
        token = ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientGetAuthToken(
            self.__client)
        self.__token = token
        return token.decode('utf-8')

    def ping_sync(self) -> Result:
        """
        Ping the next hop. This function is synchronous: It will wait for the answer.
        @returns <Result> status of function call
        """
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientPingSync(self.__client))

    def create_sync(self, address: str, data: Variant):
        """
        Create an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to create object in
        @param[in]  variant      Data of the object
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call
        @return <Variant>, variant result of write
        """
        b_address = address.encode('utf-8')
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSync(
            self.__client, b_address, data.get_handle(), self.__token))
        return result, data

    def remove_sync(self, address: str) -> Result:
        """
        Remove an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to remove
        @returns <Result> status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientRemoveSync(
            self.__client, b_address, self.__token))

    def browse_sync(self, address: str):
        """
        Browse an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to browse
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Children of the node. Data will be provided as Variant array of strings.
        """
        b_address = address.encode('utf-8')
        data = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseSync(
            self.__client, b_address, data.get_handle(), self.__token))
        return result, data

    def read_sync(self, address: str):
        """
        Read an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to read
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Data of the node
        """
        data = Variant()
        return self.read_sync_args(address, data)

    def read_sync_args(self, address: str, args: Variant):
        """
        Read an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to read
        @param[in,out] args   Read arguments data of the node
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Data of the node
        """
        b_address = address.encode('utf-8')
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadSync(
            self.__client, b_address, args.get_handle(), self.__token))
        return result, args

    def write_sync(self, address: str, data: Variant):
        """
        Write an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to write
        @param[in] variant New data of the node
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, result of write
        """
        b_address = address.encode('utf-8')
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteSync(
            self.__client, b_address, data.get_handle(), self.__token))
        return result, data

    def metadata_sync(self, address: str):
        """
        Read metadata of an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to read metadata of
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Metadata of the node. Data will be provided as Variant flatbuffers with metadata.fbs data type.
        """
        b_address = address.encode('utf-8')
        data = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataSync(
            self.__client, b_address, data.get_handle(), self.__token))
        return result, data

    def ping_async(self, cb: ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Ping the next hop. This function is asynchronous. It will return immediately. Callback will be called if function call is finished.
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result> status of function call
        """
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientPingASync(
            self.__client, self.__create_callback(cb), userdata))

    def create_async(self, address: str, data: Variant,
                     cb: ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Create an object. This function is asynchronous. It will return immediately. Callback will be called if function call is finished. Result data may be provided in callback function.
        @param[in]  address   Address of the node to create object in
        @param[in]  data      Data of the object
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result> status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateASync(
            self.__client, b_address, data.get_handle(),
            self.__token, self.__create_callback(cb), userdata))

    def remove_async(self, address: str,
                     cb: ResponseCallback,
                     userdata: userData_c_void_p = None) -> Result:
        """
        Remove an object. This function is asynchronous. It will return immediately. Callback will be called if function call is finished. Result data may be provided in callback function.
        @param[in]  address   Address of the node to remove
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result> status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientRemoveASync(self.__client,
                                                                            b_address,
                                                                            self.__token,
                                                                            self.__create_callback(
                                                                                cb),
                                                                            userdata))

    def browse_async(self, address: str,
                     cb: ResponseCallback,
                     userdata: userData_c_void_p = None) -> Result:
        """
        Browse an object. This function is asynchronous. It will return immediately. Callback will be called if function call is finished. Result data may be provided in callback function.
        @param[in]  address   Address of the node to browse
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result> status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseASync(
            self.__client, b_address, self.__token, self.__create_callback(cb), userdata))

    def read_async(self, address: str,
                   cb: ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Read an object. This function is asynchronous. It will return immediately. Callback will be called if function call is finished. Result data may be provided in callback function.
        @param[in]  address   Address of the node to read
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result>, status of function call
        """
        with Variant() as args:
            return self.read_async_args(address, args, cb, userdata)

    def read_async_args(self, address: str, args: Variant,
                        cb: ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Read an object. This function is asynchronous. It will return immediately. Callback will be called if function call is finished. Result data may be provided in callback function.
        @param[in]  address   Address of the node to read
        @param[in]  args      Read arguments data of the node
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadASync(self.__client,
                                                                          b_address,
                                                                          args.get_handle(),
                                                                          self.__token,
                                                                          self.__create_callback(
                                                                              cb),
                                                                          userdata))

    def write_async(self, address: str,
                    data: Variant, cb: ResponseCallback,
                    userdata: userData_c_void_p = None) -> Result:
        """
        Write an object. This function is synchronous: It will wait for the answer.
        @param[in]  address   Address of the node to read metadata
        @param[in]  data      Data of the object
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteASync(self.__client,
                                                                           b_address,
                                                                           data.get_handle(),
                                                                           self.__token,
                                                                           self.__create_callback(
                                                                               cb),
                                                                           userdata))

    def metadata_async(self, address: str,
                       cb: ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Read metadata of an object. This function is asynchronous. It will return immediately. Callback will be called if function call is finished. Result data may be provided in callback function.
        @param[in]  address   Address of the node to read metadata
        @param[in]  callback  Callback to call when function is finished
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataASync(self.__client,
                                                                              b_address,
                                                                              self.__token,
                                                                              self.__create_callback(
                                                                                  cb),
                                                                              userdata))

    def _unregister_sync(self, sub: ctrlxdatalayer.subscription.Subscription):
        """ _unregister_sync """
        if sub in self.__subs:
            self.__subs.remove(sub)

    def create_subscription_sync(self, prop: Variant,
                                 cnb: ctrlxdatalayer.subscription.ResponseNotifyCallback,
                                 userdata: userData_c_void_p = None):
        """
        Set up a subscription
        @param[in]  ruleset   Variant that describe ruleset of subscription as subscription.fbs
        @param[in]  publishCallback  Callback to call when new data is available
        @param[in]  userdata  User data - will be returned in publishCallback as userdata. You can use this userdata to identify your subscription
        @result <Result>, status of function cal
        """
        sub = ctrlxdatalayer.subscription_sync.SubscriptionSync(self)
        r = sub._create(prop, cnb, userdata)
        if r == Result.OK:
            self.__subs.append(sub)
        return r, sub

    def create_subscription_async(self,
                                  prop: Variant,
                                  cnb: ctrlxdatalayer.subscription.ResponseNotifyCallback,
                                  cb: ResponseCallback,
                                  userdata: userData_c_void_p = None):
        """
        Set up a subscription
        @param[in]  ruleset   Variant that describe ruleset of subscription as subscription.fbs
        @param[in]  publishCallback  Callback to call when new data is available
        @param[in]  userdata  User data - will be returned in publishCallback as userdata. You can use this userdata to identify your subscription
        @result <Result>, status of function cal
        """
        sub = ctrlxdatalayer.subscription_async.SubscriptionAsync(self)
        r = sub._create(prop, cnb, cb, userdata)
        if r == Result.OK:
            self.__subs.append(sub)
        return r, sub

    def __close_all_subs(self):
        """ __close_all_subs """
        subs = self.__subs.copy()
        self.__subs.clear()
        for x in subs:
            x.on_close()

    def read_json_sync(self,
                       conv: Converter,
                       address: str,
                       indent: int,
                       data: Variant() = None):
        """
        This function reads a values as a JSON string
        @param[in]  converter   Reference to the converter (see System json_converter())
        @param[in]  address     Address of the node to read
        @param[in]  indentStep  Indentation length for json string
        @param[in]  json        Generated JSON as Variant (string)
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Generated JSON as Variant (string)
        """
        b_address = address.encode('utf-8')
        if data is None:
          data = Variant()

        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadJsonSync(
            self.__client, conv.get_handle(), b_address, data.get_handle(), indent, self.__token))
        return result, data

    def write_json_sync(self,
                        conv: Converter,
                        address: str,
                        json: str):
        """
        This function writes a JSON value
        @param[in]     converter   Reference to the converter (see System json_converter())
        @param[in]     address     Address of the node to write
        @param[in]     json        JSON value to write
        @param[in,out] error       Error of conversion as variant string
        @return result status of the function
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Error of conversion as variant string
        """
        b_address = address.encode('utf-8')
        b_json = json.encode('utf-8')
        error = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteJsonSync(
            self.__client, conv.get_handle(), b_address, b_json, error.get_handle(), self.__token))
        return result, error

    def create_bulk(self):
        """
        Setup a bulk object

        Returns:
            Bulk: Bulk object
        """
        bulk = ctrlxdatalayer.bulk.Bulk(self)
        return bulk
