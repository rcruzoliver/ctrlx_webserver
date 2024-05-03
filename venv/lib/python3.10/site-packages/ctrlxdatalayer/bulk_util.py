"""
bulk util

"""
import ctypes
import typing

import ctrlxdatalayer
from ctrlxdatalayer.clib_bulk import (C_DLR_BULK, C_BulkRequest,
                                      C_VecBulkRequest)
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT
from ctrlxdatalayer.variant import Result, Variant, VariantRef, copy


class _Request:
    """
    class Bulk _Request
    """
    __slots__ = ['__address', '__data']

    def __init__(self, addr: str, data: Variant):
        """
        init Request parameters
        """
        self.__address = addr.encode('utf-8')  # !!
        self.__data = None if data is None else data.get_handle()

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
        pass

    def get_address(self) -> bytes:
        """
        get_address

        Returns:
            str: Address of the request
        """
        return self.__address

    def get_data(self) -> C_DLR_VARIANT:
        """
        get_data

        Returns:
            C_DLR_VARIANT: Input data of the request
        """
        return self.__data


def _bulkDelete(bulk: C_DLR_BULK):
    """_bulkDelete

    Args:
        bulk (C_DLR_BULK): Reference to the bulk
    """
    ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkDelete(bulk)


def _bulkCreate(size: int) -> C_DLR_BULK:
    """_bulkCreate

    Args:
        size (int): size of bulk requests

    Returns:
        C_DLR_BULK: Reference to the bulk
    """
    return ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkCreate(
        ctypes.c_size_t(size))


def _bulkSetRequestAddress(bulk: C_DLR_BULK, i: int, addr: bytes) -> Result:
    """_bulkSetRequestAddress

    Args:
        bulk (C_DLR_BULK): Reference to the bulk
        i (int): index [0..]
        addr (bytes): address

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkSetRequestAddress(
        bulk, ctypes.c_size_t(i), addr))


def _bulkSetRequestData(bulk: C_DLR_BULK, i: int, data: C_DLR_VARIANT):
    """_bulkSetRequestData

    Args:
        bulk (C_DLR_BULK): Reference to the bulk
        i (int): index [0..]
        data (C_DLR_VARIANT): Argument of read of write data

    Returns:
        Result: status of function call
    """
    return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_bulkSetRequestData(
        bulk, ctypes.c_size_t(i), data))


class _BulkCreator:
    """
    class _BulkCreator
    """
    __slots__ = ['__bulk']

    def __init__(self, reqs: typing.List[_Request]):
        """
        __init__

        Args:
            reqs (typing.List[_Request]): List of request
        """
        self.__bulk = None
        self.__create(reqs)

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
        if self.__bulk is None:
            return
        _bulkDelete(self.__bulk)
        self.__bulk = None

    def get_handle(self) -> C_DLR_BULK:
        """get_handle

        Returns:
            clib_client.C_DLR_BULK:  handle value of bulk 
        """
        return self.__bulk

    def __create(self, reqs: typing.List[_Request]):
        """__create

        Args:
            reqs (typing.List[_Request]): List of request

        Returns:
            clib_client.C_DLR_BULK: handle value of bulk 
        """
        req_len = len(reqs)
        bulk = _bulkCreate(req_len)

        i = 0
        for r in reqs:
            result = _bulkSetRequestAddress(bulk, i, r.get_address())
            if result != Result.OK:
                print(f"set address error {result}")
                return None
            if r.get_data() is not None:
                result = _bulkSetRequestData(bulk, i, r.get_data())
                if result != Result.OK:
                    print(f"set data error {result}")
                    return None
            i += 1
        self.__bulk = bulk


def _createBulkRequest(count: int):
    """def _createBulkRequest(count: int):

    Args:
        count (int): size of bulk requests

    Returns:
        ctypes.POINTER(C_VecBulkRequest): Reference to the bulk request 
    """
    return ctrlxdatalayer.clib.libcomm_datalayer.DLR_createBulkRequest(ctypes.c_size_t(count))


def _deleteBulkRequest(bulk_req):
    """def _deleteBulkRequest(count: int):

    Args:
        ctypes.POINTER(C_VecBulkRequest): Reference to the bulk request
    """
    ctrlxdatalayer.clib.libcomm_datalayer.DLR_deleteBulkRequest(bulk_req)


class _AsyncCreator:
    """
    class _AsyncCreator
    """
    __slots__ = ['__bulk_request']

    def __init__(self, reqs: typing.List[_Request]):
        """
        __init__

        Args:
            reqs (typing.List[_Request]): List of request
        """
        self.__bulk_request = None
        self.__create(reqs)

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
        if self.__bulk_request is not None:
            _deleteBulkRequest(self.__bulk_request)

    def get_bulk_request(self) -> ctypes.POINTER(C_VecBulkRequest):
        """get_bulk_request

        Returns:
            ctypes.POINTER: pointer of C_VecBulkRequest
        """
        return self.__bulk_request

    def __create(self, reqs: typing.List[_Request]):
        """__create

        Args:
            reqs (typing.List[_Request]): List of request

        Returns:
            clib_client.C_DLR_BULK: handle value of bulk 
        """
        req_len = len(reqs)
        bulkreq = _createBulkRequest(req_len)
        ptr = ctypes.cast(bulkreq[0].request, ctypes.POINTER(
            C_BulkRequest*req_len))
        i = 0
        for r in reqs:
            ptr[0][i].address = r.get_address()
            if r.get_data() is not None:
                copy(VariantRef(ptr[0][i].data), VariantRef(r.get_data()))
            i += 1
        self.__bulk_request = bulkreq
