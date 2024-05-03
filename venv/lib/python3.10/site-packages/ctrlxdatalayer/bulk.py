"""
class Bulk
Function calls are combined into a single call
"""
import ctypes
import datetime
import typing

import ctrlxdatalayer
from ctrlxdatalayer.bulk_util import _AsyncCreator, _BulkCreator, _Request
from ctrlxdatalayer.clib import userData_c_void_p
from ctrlxdatalayer.clib_bulk import (C_DLR_BULK, C_DLR_CLIENT_BULK_RESPONSE,
                                      C_VecBulkResponse)
from ctrlxdatalayer.clib_client import C_DLR_CLIENT
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT
from ctrlxdatalayer.client import Client, _CallbackPtr
from ctrlxdatalayer.variant import Result, Variant


class Response:
    """
    class Bulk Response
    """
    __slots__ = ['__address', '__result', '__data', '__timestamp']

    def __init__(self, addr: str, data: C_DLR_VARIANT, time: ctypes.c_uint64, result: Result):
        """init Response Bulk

        Args:
            addr (str): Address for the response
            data (C_DLR_VARIANT): Output data of the response
            time (ctypes.c_uint64): Timestamp of the response
            result (Result): Result of the response
        """
        self.__address = addr
        self.__result = result
        _, self.__data = Variant.copy(data)
        t = time if isinstance(time, int) else time.value
        self.__timestamp = Variant.from_filetime(t)

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
        close
        """
        self.__data.close()

    def get_address(self) -> str:
        """
        get_address

        Returns:
            str: Address for the response
        """
        return self.__address

    def get_result(self) -> Result:
        """get_result

        Returns:
            Result: Result of the response
        """
        return self.__result

    def get_data(self) -> Variant:
        """
        get_data

        Returns:
            Variant: Output data of the response
        """
        return self.__data

    def get_datetime(self) -> datetime.datetime:
        """
        get_datetime

        datetime object as timestamp (FILETIME) 64 bit 100ns since 1.1.1601 (UTC)

        Returns:
            datetime.datetime: Timestamp of the response
        """
        return self.__timestamp


ResponseCallback = typing.Callable[[
    typing.List[Response], userData_c_void_p], None]
"""ResponseCallback

    Returns:

"""


def _bulkGetCount(bulk: C_DLR_BULK) -> int:
    """_bulkGetCount

    Args:
        bulk (C_DLR_BULK): Reference to the bulk

    Returns:
        int: sizeof bulk
    """
    return ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetCount(bulk)


def _bulkGetResponseAddress(bulk: C_DLR_BULK, i: int) -> bytes:
    """_bulkGetResponseAddress

    Args:
        bulk(C_DLR_BULK): Reference to the bulk
        i(int): index[0..]

    Returns:
        bytes: address of response
    """
    return ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseAddress(bulk, ctypes.c_size_t(i))


def _bulkGetResponseData(bulk: C_DLR_BULK, i: int) -> C_DLR_VARIANT:
    """_bulkGetResponseData

    Args:
        bulk (C_DLR_BULK): Reference to the bulk
        i (int): index [0..]
    Returns:
        C_DLR_VARIANT: data of response
    """
    return ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseData(
        bulk, ctypes.c_size_t(i))


def _bulkGetResponseTimestamp(bulk: C_DLR_BULK, i: int) -> ctypes.c_uint64:
    """_bulkGetResponseTimestamp

    Args:
        bulk (C_DLR_BULK): Reference to the bulk
        i (int): index [0..]

    Returns:
        c_uint64: timestamp of response
    """
    return ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseTimestamp(
        bulk, ctypes.c_size_t(i))


def _bulkGetResponseResult(bulk: C_DLR_BULK, i: int) -> Result:
    """_bulkGetResponseResult

    Args:
        bulk (C_DLR_BULK): Reference to the bulk
        i (int): index [0..]

    Returns:
        Result: status of response
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkGetResponseResult(
        bulk, ctypes.c_size_t(i)))


class _ResponseMgr:
    """
    class _ResponseMgr
    """
    __slots__ = ['_response']

    def __init__(self):
        """
        __init__

        Args:
            bulk (clib_client.C_DLR_BULK): Bulk value
        """
        self._response: typing.List[Response] = []

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
        close
        """
        for r in self._response:
            r.close()
        self._response = []

    def get_response(self) -> typing.List[Response]:
        """
        get_response

        Returns:
            typing.List[Response]: List of response
        """
        return self._response


class _ResponseBulkMgr(_ResponseMgr):
    """
    class _ResponseBulkMgr
    """

    def __init__(self, bulk: C_DLR_BULK):
        """
        __init__

        Args:
            bulk (clib_client.C_DLR_BULK): Bulk value
        """
        super().__init__()

        size = _bulkGetCount(bulk)
        for i in range(size):
            addr = _bulkGetResponseAddress(bulk, i)
            data = _bulkGetResponseData(bulk, i)
            time = _bulkGetResponseTimestamp(bulk, i)
            result = _bulkGetResponseResult(bulk, i)
            obj = Response(addr.decode('utf-8'), data, time, result)
            self._response.append(obj)

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


class _ResponseAsynMgr(_ResponseMgr):
    """
    class _ResponseAsynMgr
    """

    __slots__ = ['_response', '__async_creator']

    def __init__(self, ac: _AsyncCreator):
        """__init__

        Args:
            ac (_AsyncCreator): help class
        """
        super().__init__()
        self._response = []
        self.__async_creator = ac

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

    def set_responses(self, responses: typing.List[Response]):
        """set_responses
        """
        self._response = responses

    def close(self):
        """close
        """
        self.__async_creator.close()
        self._response = []


def _clientBulkReadSync(client: C_DLR_CLIENT, bulk: C_DLR_BULK, token: bytes) -> Result:
    """_clientBulkReadSync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        bulk (C_DLR_BULK): Reference to the bulk
        token (bytes): Security access token for authentication as JWT payload

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkReadSync(client, bulk, token))


def _clientBulkWriteSync(client: C_DLR_CLIENT, bulk: C_DLR_BULK, token: bytes) -> Result:
    """_clientBulkWriteSync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        bulk (C_DLR_BULK): Reference to the bulk
        token (bytes): Security access token for authentication as JWT payload

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkWriteSync(client, bulk, token))


def _clientBulkBrowseSync(client: C_DLR_CLIENT, bulk: C_DLR_BULK, token: bytes) -> Result:
    """_clientBulkBrowseSync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        bulk (C_DLR_BULK): Reference to the bulk
        token (bytes): Security access token for authentication as JWT payload

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkBrowseSync(client, bulk, token))


def _clientBulkMetadataSync(client: C_DLR_CLIENT, bulk: C_DLR_BULK, token: bytes) -> Result:
    """_clientBulkMetadataSync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        bulk (C_DLR_BULK): Reference to the bulk
        token (bytes): Security access token for authentication as JWT payload

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkMetadataSync(client, bulk, token))


def _clientBulkCreateSync(client: C_DLR_CLIENT, bulk: C_DLR_BULK, token: bytes) -> Result:
    """_clientBulkCreateSync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        bulk (C_DLR_BULK): Reference to the bulk
        token (bytes): Security access token for authentication as JWT payload

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkCreateSync(client, bulk, token))


def _clientBulkDeleteSync(client: C_DLR_CLIENT, bulk: C_DLR_BULK, token: bytes) -> Result:
    """_clientBulkDeleteSync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        bulk (C_DLR_BULK): Reference to the bulk
        token (bytes): Security access token for authentication as JWT payload

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBulkDeleteSync(client, bulk, token))


def _clientReadBulkASync(client: C_DLR_CLIENT, request, token: bytes, cb: C_DLR_CLIENT_BULK_RESPONSE, userdata: userData_c_void_p) -> Result:
    """_clientReadBulkASync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        request (ctypes.POINTER(C_VecBulkRequest)): Requests
        token (bytes): Security access token for authentication as JWT payload
        cb (C_DLR_CLIENT_BULK_RESPONSE): Callback to call when function is finished
        userdata (userData_c_void_p): User data - will be returned in callback as userdata. 
                                      You can use this userdata to identify your request

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientReadBulkASync(client, request, token, cb, userdata))


def _clientBrowseBulkASync(client: C_DLR_CLIENT, request, token: bytes, cb: C_DLR_CLIENT_BULK_RESPONSE, userdata: userData_c_void_p) -> Result:
    """_clientBrowseBulkASync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        request (ctypes.POINTER(C_VecBulkRequest)): Requests
        token (bytes): Security access token for authentication as JWT payload
        cb (C_DLR_CLIENT_BULK_RESPONSE): Callback to call when function is finished
        userdata (userData_c_void_p): User data - will be returned in callback as userdata. 
                                      You can use this userdata to identify your request

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientBrowseBulkASync(client, request, token, cb, userdata))


def _clientMetadataBulkASync(client: C_DLR_CLIENT, request, token: bytes, cb: C_DLR_CLIENT_BULK_RESPONSE, userdata: userData_c_void_p) -> Result:
    """_clientMetadataBulkASync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        request (ctypes.POINTER(C_VecBulkRequest)): Requests
        token (bytes): Security access token for authentication as JWT payload
        cb (C_DLR_CLIENT_BULK_RESPONSE): Callback to call when function is finished
        userdata (userData_c_void_p): User data - will be returned in callback as userdata. 
                                      You can use this userdata to identify your request

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientMetadataBulkASync(client, request, token, cb, userdata))


def _clientWriteBulkASync(client: C_DLR_CLIENT, request, token: bytes, cb: C_DLR_CLIENT_BULK_RESPONSE, userdata: userData_c_void_p) -> Result:
    """_clientWriteBulkASync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        request (ctypes.POINTER(C_VecBulkRequest)): Requests
        token (bytes): Security access token for authentication as JWT payload
        cb (C_DLR_CLIENT_BULK_RESPONSE): Callback to call when function is finished
        userdata (userData_c_void_p): User data - will be returned in callback as userdata. 
                                      You can use this userdata to identify your request

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientWriteBulkASync(client, request, token, cb, userdata))


def _clientCreateBulkASync(client: C_DLR_CLIENT, request, token: bytes, cb: C_DLR_CLIENT_BULK_RESPONSE, userdata: userData_c_void_p) -> Result:
    """_clientCreateBulkASync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        request (ctypes.POINTER(C_VecBulkRequest)): Requests
        token (bytes): Security access token for authentication as JWT payload
        cb (C_DLR_CLIENT_BULK_RESPONSE): Callback to call when function is finished
        userdata (userData_c_void_p): User data - will be returned in callback as userdata. 
                                      You can use this userdata to identify your request

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateBulkASync(client, request, token, cb, userdata))


def _clientDeleteBulkASync(client: C_DLR_CLIENT, request, token: bytes, cb: C_DLR_CLIENT_BULK_RESPONSE, userdata: userData_c_void_p) -> Result:
    """_clientDeleteBulkASync

    Args:
        client (C_DLR_CLIENT): Reference to the client
        request (ctypes.POINTER(C_VecBulkRequest)): Requests
        token (bytes): Security access token for authentication as JWT payload
        cb (C_DLR_CLIENT_BULK_RESPONSE): Callback to call when function is finished
        userdata (userData_c_void_p): User data - will be returned in callback as userdata. 
                                      You can use this userdata to identify your request

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientDeleteBulkASync(client, request, token, cb, userdata))


class BulkReadRequest:
    """Struct for BulkReadRequest
    Address for the request
    Read argument of the request
    """

    def __init__(self, address: str, data: Variant = None):
        """Struct for BulkReadRequest

        Args:
            address (str): Address for the request
            data (Variant, optional): Argument of the request. Defaults to None.
        """
        self.address = address
        self.data = data


class BulkWriteRequest:
    """Struct for BulkWriteRequest
    Address for the request
    Write data of the request
    """

    def __init__(self, address: str, data: Variant):
        """BulkWriteRequest

        Args:
            address (str): Address for the request
            data (Variant): Write data of the request
        """
        self.address = address
        self.data = data


class BulkCreateRequest:
    """Struct for BulkCreateRequest
    Address for the request
    Write data of the request
    """

    def __init__(self, address: str, data: Variant = None):
        """BulkCreateRequest

        Args:
            address (str): Address for the request
            data (Variant): Write data of the request
        """
        self.address = address
        self.data = data


class Bulk:
    """
    class Bulk
    """
    __slots__ = ['_client', '_requests', '__resp_mgr', '__ptr_resp', '__on_cb']

    def __init__(self, c: Client):
        """__init__

        Args:
            c (Client): Client
        """
        self._client = c
        self._requests: typing.List[_Request] = []
        self.__resp_mgr = None
        self.__ptr_resp: _CallbackPtr
        self.__on_cb = False

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
        close
        """
        self._client = None
        self._requests = []
        self.__close_mgr()

    def __create_response_callback(self, cb: ResponseCallback):
        """
        callback management
        """
        self.__on_cb = False
        cb_ptr = _CallbackPtr()
        self.__ptr_resp = cb_ptr

        def _cb(bulk_resp: ctypes.POINTER(C_VecBulkResponse), userdata: ctypes.c_void_p):
            """
            datalayer calls this function
            """
            if bulk_resp is None:
                cb(None, userdata)
                self.__on_cb = True
                return
            ptr = bulk_resp[0]
            resps = []
            for i in range(ptr.count):
                addr = ptr.response[i].address
                data = ptr.response[i].data
                time = ptr.response[i].timestamp
                result = ptr.response[i].result
                resp = Response(addr.decode('utf-8'),
                                data, time, Result(result))
                resps.append(resp)
            self.__resp_mgr.set_responses(resps)
            cb(resps, userdata)
            self.__on_cb = True

        cb_ptr.set_ptr(C_DLR_CLIENT_BULK_RESPONSE(_cb))
        return cb_ptr.get_ptr()

    def _test_callback(self, cb: ResponseCallback):
        """
            internal use
        """
        return self.__create_response_callback(cb)

    def _add(self, address: str, data: Variant = None):
        """
        add bulk request
        """
        req = _Request(address, data)
        self._requests.append(req)

    def read(self, request: typing.List[BulkReadRequest], cb: ResponseCallback = None, userdata: userData_c_void_p = None) -> Result:
        """
        read

        Bulk read request to read multiple nodes with a single request.
        With cb is None, read is called synchronously

        Args:
            request (typing.List[BulkReadRequest]): list of requests
            cb (ResponseCallback, optional): Callback to call when function is finished. Defaults to None.
            userdata (optional): User data - will be returned in callback as userdata. You can use this userdata to identify your request

        Returns:
            Result: status of function call
        """
        self._requests = []
        for r in request:
            self._add(r.address, r.data)
        self.__close_mgr()
        if cb is not None:
            return self._read_async(cb, userdata)
        return self._read_sync()

    def _read_async(self, cb: ResponseCallback, userdata: userData_c_void_p) -> Result:
        """_read_async

        Returns:
            Result: status of function call
        """
        bulk = _AsyncCreator(self._requests)
        result = _clientReadBulkASync(self._client.get_handle(),
                                      bulk.get_bulk_request(),
                                      self._client.get_token(),
                                      C_DLR_CLIENT_BULK_RESPONSE(
                                          self.__create_response_callback(cb)),
                                      userdata)
        self.__resp_mgr = _ResponseAsynMgr(bulk)
        return result

    def _read_sync(self) -> Result:
        """_read_sync

        Returns:
            Result: status of function call
        """
        with _BulkCreator(self._requests) as bulk:
            result = _clientBulkReadSync(
                self._client.get_handle(), bulk.get_handle(), self._client.get_token())
            if result != Result.OK:
                return result
            self.__resp_mgr = _ResponseBulkMgr(bulk.get_handle())
            return result

    def write(self, request: typing.List[BulkWriteRequest], cb: ResponseCallback = None, userdata: userData_c_void_p = None) -> Result:
        """
        write

        Bulk write request to write multiple nodes with a single request
        With cb is None, write is called synchronously

        Args:
            request (typing.List[BulkWriteRequest]): list of requests
            cb (ResponseCallback, optional): callback  Callback to call when function is finished. Defaults to None.
            userdata (optional): User data - will be returned in callback as userdata. You can use this userdata to identify your request

        Returns:
            Result: status of function call
        """
        self._requests = []
        for r in request:
            self._add(r.address, r.data)
        self.__close_mgr()
        if cb is not None:
            return self._write_async(cb, userdata)
        return self._write_sync()

    def _write_sync(self) -> Result:
        """_write_sync

        Returns:
            Result: status of function call
        """
        with _BulkCreator(self._requests) as bulk:
            result = _clientBulkWriteSync(
                self._client.get_handle(), bulk.get_handle(), self._client.get_token())
            if result != Result.OK:
                return result
            self.__resp_mgr = _ResponseBulkMgr(bulk.get_handle())
            return result

    def _write_async(self, cb: ResponseCallback, userdata: userData_c_void_p) -> Result:
        """_write_async

        Returns:
            Result: status of function call
        """
        bulk = _AsyncCreator(self._requests)
        result = _clientWriteBulkASync(self._client.get_handle(),
                                       bulk.get_bulk_request(),
                                       self._client.get_token(),
                                       C_DLR_CLIENT_BULK_RESPONSE(
            self.__create_response_callback(cb)),
            userdata)
        self.__resp_mgr = _ResponseAsynMgr(bulk)
        return result

    def browse(self, request: typing.List[str], cb: ResponseCallback = None, userdata: userData_c_void_p = None) -> Result:
        """
        browse

        Bulk browse request to browse multiple nodes with a single request
        With cb is None, browse is called synchronously

        Args:
            request (typing.List[str]): list of requests
            cb (ResponseCallback, optional): callback  Callback to call when function is finished. Defaults to None.
            userdata (optional): User data - will be returned in callback as userdata. You can use this userdata to identify your request

        Returns:
            Result: status of function call
        """
        self._requests = []
        for r in request:
            self._add(r, None)
        self.__close_mgr()
        if cb is not None:
            return self._browse_async(cb, userdata)

        return self._browse_sync()

    def _browse_async(self, cb: ResponseCallback, userdata: userData_c_void_p) -> Result:
        """_browse_async

        Returns:
            Result: status of function call
        """
        bulk = _AsyncCreator(self._requests)
        result = _clientBrowseBulkASync(self._client.get_handle(),
                                        bulk.get_bulk_request(),
                                        self._client.get_token(),
                                        C_DLR_CLIENT_BULK_RESPONSE(
            self.__create_response_callback(cb)),
            userdata)
        self.__resp_mgr = _ResponseAsynMgr(bulk)
        return result

    def _browse_sync(self) -> Result:
        """_browse_sync

        Returns:
            Result: status of function call
        """
        with _BulkCreator(self._requests) as bulk:
            result = _clientBulkBrowseSync(
                self._client.get_handle(), bulk.get_handle(), self._client.get_token())
            if result != Result.OK:
                return result
            self.__resp_mgr = _ResponseBulkMgr(bulk.get_handle())
            return result

    def metadata(self, request: typing.List[str], cb: ResponseCallback = None, userdata: userData_c_void_p = None) -> Result:
        """
        metadata

        Bulk metadata request to metadata multiple nodes with a single request
        With cb is None, metadata is called synchronously

        Args:
            request (typing.List[str]): list of requests
            cb (ResponseCallback, optional): callback  Callback to call when function is finished. Defaults to None.
            userdata (optional): User data - will be returned in callback as userdata. You can use this userdata to identify your request

        Returns:
            Result: status of function call
        """
        self._requests = []
        for r in request:
            self._add(r, None)
        self.__close_mgr()
        if cb is not None:
            return self._metadata_async(cb, userdata)

        return self._metadata_sync()

    def _metadata_async(self, cb: ResponseCallback, userdata: userData_c_void_p) -> Result:
        """_metadata_async

        Returns:
            Result: status of function call
        """
        bulk = _AsyncCreator(self._requests)
        result = _clientMetadataBulkASync(self._client.get_handle(),
                                          bulk.get_bulk_request(),
                                          self._client.get_token(),
                                          C_DLR_CLIENT_BULK_RESPONSE(
            self.__create_response_callback(cb)),
            userdata)
        self.__resp_mgr = _ResponseAsynMgr(bulk)
        return result

    def _metadata_sync(self) -> Result:
        """_metadata_sync

        Returns:
            Result: status of function call
        """
        with _BulkCreator(self._requests) as bulk:
            result = _clientBulkMetadataSync(
                self._client.get_handle(), bulk.get_handle(), self._client.get_token())
            if result != Result.OK:
                return result
            self.__resp_mgr = _ResponseBulkMgr(bulk.get_handle())
            return result

    def create(self, request: typing.List[BulkCreateRequest], cb: ResponseCallback = None, userdata: userData_c_void_p = None) -> Result:
        """
        create

        Bulk create request to create multiple nodes with a single request
        With cb is None, create is called synchronously

        Args:
            request (typing.List[BulkCreateRequest]): list of requests
            cb (ResponseCallback, optional): callback  Callback to call when function is finished. Defaults to None.
            userdata (optional): User data - will be returned in callback as userdata. You can use this userdata to identify your request

        Returns:
            Result: status of function call
        """
        self._requests = []
        for r in request:
            self._add(r.address, r.data)
        self.__close_mgr()
        if cb is not None:
            return self._create_async(cb, userdata)
        return self._create_sync()

    def _create_sync(self) -> Result:
        """_create_sync

        Returns:
            Result: status of function call
        """
        with _BulkCreator(self._requests) as bulk:
            result = _clientBulkCreateSync(
                self._client.get_handle(), bulk.get_handle(), self._client.get_token())
            if result != Result.OK:
                return result
            self.__resp_mgr = _ResponseBulkMgr(bulk.get_handle())
            return result

    def _create_async(self, cb: ResponseCallback, userdata: userData_c_void_p) -> Result:
        """_create_async

        Returns:
            Result: status of function call
        """
        bulk = _AsyncCreator(self._requests)
        result = _clientCreateBulkASync(self._client.get_handle(),
                                        bulk.get_bulk_request(),
                                        self._client.get_token(),
                                        C_DLR_CLIENT_BULK_RESPONSE(
            self.__create_response_callback(cb)),
            userdata)
        self.__resp_mgr = _ResponseAsynMgr(bulk)
        return result

    def delete(self, request: typing.List[str], cb: ResponseCallback = None, userdata: userData_c_void_p = None) -> Result:
        """
        delete

        Bulk delete request to delete multiple nodes with a single request
        With cb is None, delete is called synchronously

        Args:
            request (typing.List[str]): list of requests
            cb (ResponseCallback, optional): callback  Callback to call when function is finished. Defaults to None.
            userdata (optional): User data - will be returned in callback as userdata. You can use this userdata to identify your request

        Returns:
            Result: status of function call
        """
        self._requests = []
        for r in request:
            self._add(r, None)
        self.__close_mgr()
        if cb is not None:
            return self._delete_async(cb, userdata)
        return self._delete_sync()

    def _delete_sync(self) -> Result:
        """_delete_sync

        Returns:
            Result: status of function call
        """
        with _BulkCreator(self._requests) as bulk:
            result = _clientBulkDeleteSync(
                self._client.get_handle(), bulk.get_handle(), self._client.get_token())
            if result != Result.OK:
                return result
            self.__resp_mgr = _ResponseBulkMgr(bulk.get_handle())
            return result

    def _delete_async(self, cb: ResponseCallback, userdata: userData_c_void_p) -> Result:
        """_delete_async

        Returns:
            Result: status of function call
        """
        bulk = _AsyncCreator(self._requests)
        result = _clientDeleteBulkASync(self._client.get_handle(),
                                        bulk.get_bulk_request(),
                                        self._client.get_token(),
                                        C_DLR_CLIENT_BULK_RESPONSE(
            self.__create_response_callback(cb)),
            userdata)
        self.__resp_mgr = _ResponseAsynMgr(bulk)
        return result

    def get_response(self) -> typing.List[Response]:
        """
        get_response

        Returns:
            typing.List[Response]: List of response
        """
        if self.__resp_mgr is None:
            return []
        return self.__resp_mgr.get_response()

    def __close_mgr(self):
        """__close_mgr
        """
        if self.__resp_mgr is not None:
            self.__resp_mgr.close()
        self.__resp_mgr = None
