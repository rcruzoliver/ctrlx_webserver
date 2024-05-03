"""
Class Provider Node
"""
import ctypes
import typing

import ctrlxdatalayer
from ctrlxdatalayer.clib import C_DLR_RESULT
from ctrlxdatalayer.clib_provider_node import (C_DLR_PROVIDER_NODE_CALLBACK,
                                         C_DLR_PROVIDER_NODE_CALLBACKDATA,
                                         C_DLR_PROVIDER_NODE_CALLBACKS,
                                         C_DLR_PROVIDER_NODE_FUNCTION,
                                         C_DLR_PROVIDER_NODE_FUNCTION_DATA,
                                         C_DLR_VARIANT, address_c_char_p,
                                         userData_c_void_p)
from ctrlxdatalayer.variant import Result, Variant, VariantRef

NodeCallback = typing.Callable[[Result, typing.Optional[Variant]], None]
NodeFunction = typing.Callable[[userData_c_void_p, str, NodeCallback], None]
NodeFunctionData = typing.Callable[[
    userData_c_void_p, str, Variant, NodeCallback], None]


class _CallbackPtr:
    """
        _CallbackPtr helper
    """

    __slots__ = ['_ptr']

    def __init__(self):
        """
        init _CallbackPtr
        """
        self._ptr: typing.Optional[ctypes._CFuncPtr] = None

    def set_ptr(self, ptr):
        """
        setter _CallbackPtr
        """
        self._ptr = ptr

    def get_ptr(self):
        """
        getter _CallbackPtr
        """
        return self._ptr


class ProviderNodeCallbacks:
    """
        Provider Node callbacks  interface
    """
    __slots__ = ['on_create', 'on_remove', 'on_browse',
                 'on_read', 'on_write', 'on_metadata']

    def __init__(self,
                 on_create: NodeFunctionData,
                 on_remove: NodeFunction,
                 on_browse: NodeFunction,
                 on_read: NodeFunctionData,
                 on_write: NodeFunctionData,
                 on_metadata: NodeFunction):
        """
        init ProviderNodeCallbacks
        """
        self.on_create = on_create
        self.on_remove = on_remove
        self.on_browse = on_browse
        self.on_read = on_read
        self.on_write = on_write
        self.on_metadata = on_metadata


class ProviderNode:
    """
        Provider node interface for providing data to the system

        Hint: see python context manager for instance handling
    """
    __slots__ = ['__ptrs', '__c_cbs', '__closed', '__provider_node']

    def __init__(self, cbs: ProviderNodeCallbacks, userdata: userData_c_void_p = None):
        """
        init ProviderNode
        """
        self.__ptrs: typing.List[_CallbackPtr] = []
        self.__c_cbs = C_DLR_PROVIDER_NODE_CALLBACKS(
            userdata,
            self.__create_function_data(cbs.on_create),
            self.__create_function(cbs.on_remove),
            self.__create_function(cbs.on_browse),
            self.__create_function_data(cbs.on_read),
            self.__create_function_data(cbs.on_write),
            self.__create_function(cbs.on_metadata),
        )
        self.__closed = False
        self.__provider_node = ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerNodeCreate(
            self.__c_cbs)

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

    def __del__(self):
        """
        __del__
        """
        self.close()

    def close(self):
        """
        closes the node instance
        """
        if self.__closed:
            return
        self.__closed = True
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerNodeDelete(
            self.__provider_node)
        self.__ptrs.clear()
        self.__c_cbs = None

    def get_handle(self):
        """
        handle value of ProviderNode
        """
        return self.__provider_node

    def __create_callback(self,
                          c_cb: C_DLR_PROVIDER_NODE_CALLBACK,
                          c_cbdata: C_DLR_PROVIDER_NODE_CALLBACKDATA) -> NodeCallback:
        """
        create callback
        """
        def cb(result: Result, data: typing.Optional[Variant]):
            """ cb """
            if data is None:
                c_cb(c_cbdata, result.value, None)
            else:
                c_cb(c_cbdata, result.value, data.get_handle())
        return cb

    def __create_function(self, func: NodeFunction):
        """
        create callback management
        """
        cb_ptr = _CallbackPtr()
        self.__ptrs.append(cb_ptr)

        def _func(c_userdata: userData_c_void_p,
                  c_address: address_c_char_p,
                  c_cb: C_DLR_PROVIDER_NODE_CALLBACK,
                  c_cbdata: C_DLR_PROVIDER_NODE_CALLBACKDATA) -> C_DLR_RESULT:
            """
            datalayer calls this function
            """
            address = c_address.decode('utf-8')
            cb = self.__create_callback(c_cb, c_cbdata)
            func(c_userdata, address, cb)
            return Result.OK.value
        cb_ptr.set_ptr(C_DLR_PROVIDER_NODE_FUNCTION(_func))
        return cb_ptr.get_ptr()

    def __create_function_data(self, func: NodeFunctionData):
        """
        create callback management
        """
        cb_ptr = _CallbackPtr()
        self.__ptrs.append(cb_ptr)

        def _func(c_userdata: userData_c_void_p,
                  c_address: address_c_char_p,
                  c_data: C_DLR_VARIANT,
                  c_cb: C_DLR_PROVIDER_NODE_CALLBACK,
                  c_cbdata: C_DLR_PROVIDER_NODE_CALLBACKDATA) -> C_DLR_RESULT:
            """
            datalayer calls this function
            """
            address = c_address.decode('utf-8')
            data = VariantRef(c_data)
            cb = self.__create_callback(c_cb, c_cbdata)
            func(c_userdata, address, data, cb)
            return Result.OK.value
        cb_ptr.set_ptr(C_DLR_PROVIDER_NODE_FUNCTION_DATA(_func))
        return cb_ptr.get_ptr()

    def _test_function(self, func: NodeFunction):
        """
            internal use
        """
        return self.__create_function(func)

    def _test_function_data(self, func: NodeFunctionData):
        """
            internal use
        """
        return self.__create_function_data(func)
