"""
Class Async Subscription
"""
import ctypes
import time
import typing
import weakref

import ctrlxdatalayer
import ctrlxdatalayer.subscription
from ctrlxdatalayer.clib import C_DLR_RESULT, userData_c_void_p
from ctrlxdatalayer.clib_client import (C_DLR_CLIENT_NOTIFY_RESPONSE,
                                        C_DLR_CLIENT_RESPONSE, C_NotifyItem)
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT
from ctrlxdatalayer.variant import Result, Variant, VariantRef


class SubscriptionAsync(ctrlxdatalayer.subscription.Subscription):
    """
    SubscriptionAsync
    """
    __slots__ = ['__ptr_notify', '__ptr_resp',
                 '__closed', '__client', '__id', '__on_cb']

    def __init__(self, client: ctrlxdatalayer.client.Client):
        """
        @param[in]  client    Reference to the client
        """
        self.__ptr_notify: ctrlxdatalayer.client._CallbackPtr
        self.__ptr_resp: ctrlxdatalayer.client._CallbackPtr
        self.__closed = False
        self.__client = weakref.ref(client)
        self.__id = ""
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

    def on_close(self):
        """ on_close """
        self.close()

    def id(self) -> str:
        """
        Subscription ID
        """
        return self.__id

    def close(self):
        """
        closes the client instance
        """
        if self.__closed:
            return
        self.__closed = True
        self.__close_sub()
        self.__ptr_notify = None
        self.__ptr_resp = None
        self.__client = None

    def __close_sub(self):
        print("close_sub:", self.__id)

        if self.__id is None or self.__id == "":
            return

        def __cb_close(result: Result, data: typing.Optional[Variant], userdata: ctrlxdatalayer.clib.userData_c_void_p):
            print("async close all: ", result, int(userdata))

        self.unsubscribe_all(__cb_close, 1879)
        self.wait_on_response_cb()

    def __create_sub_notify_callback(self, cb: ctrlxdatalayer.subscription.ResponseNotifyCallback):
        """
        callback management
        """
        cb_ptr = ctrlxdatalayer.client._CallbackPtr()
        self.__ptr_notify = cb_ptr

        def _cb(status: C_DLR_RESULT, items: ctypes.POINTER(C_NotifyItem), count: ctypes.c_uint32, userdata: ctypes.c_void_p):
            """
            datalayer calls this function
            """
            r = Result(status)
            if r == Result.OK:
                notify_items = []
                for x in range(0, count):
                    n = ctrlxdatalayer.subscription.NotifyItem(
                        items[x].data, items[x].info)
                    notify_items.append(n)
                cb(r, notify_items, userdata)
                del notify_items
                return
            cb(r, None, userdata)

        cb_ptr.set_ptr(C_DLR_CLIENT_NOTIFY_RESPONSE(_cb))
        return cb_ptr.get_ptr()

    def _test_notify_callback(self, cb: ctrlxdatalayer.subscription.ResponseNotifyCallback):
        """
            internal use
        """
        return self.__create_sub_notify_callback(cb)

    def __create_response_callback(self, cb: ctrlxdatalayer.client.ResponseCallback):
        """
        callback management
        """
        self.__on_cb = False
        cb_ptr = ctrlxdatalayer.client._CallbackPtr()
        self.__ptr_resp = cb_ptr

        def _cb(status: C_DLR_RESULT, data: C_DLR_VARIANT, userdata: ctypes.c_void_p):
            """
            datalayer calls this function
            """
            r = Result(status)
            if r == Result.OK:
                v = VariantRef(data)
                cb(r, v, userdata)
                self.__on_cb = True
                return
            cb(r, None, userdata)
            self.__on_cb = True

        cb_ptr.set_ptr(C_DLR_CLIENT_RESPONSE(_cb))
        return cb_ptr.get_ptr()

    def _test_response_callback(self, cb: ctrlxdatalayer.client.ResponseCallback):
        """
            internal use
        """
        return self.__create_response_callback(cb)

    def _create(self, prop: Variant, cnb: ctrlxdatalayer.subscription.ResponseNotifyCallback, cb: ctrlxdatalayer.client.ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Set up a subscription
        @param[in]  ruleset   Variant that describe ruleset of subscription as subscription.fbs
        @param[in]  publishCallback Callback to call when new data is available
        @param[in]  callback  Callback to be called when subscription is created
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request and subscription
        @param[in]  token     Security access &token for authentication as JWT payload
        @result <Result> status of function call
        """
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSubscriptionAsync(
            self.__client().get_handle(),
            prop.get_handle(),
            self.__create_sub_notify_callback(cnb),
            self.__create_response_callback(cb),
            userdata,
            self.__client().get_token()))
        if r == Result.OK:
            self.__id = ctrlxdatalayer.subscription.get_id(prop)
        return r

    def subscribe(self, address: str, cb: ctrlxdatalayer.client.ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Set up a subscription to a node
        @param[in]  address   Address of the node to add a subscription to
        @param[in]  callback  Callback to called when data is subscribed
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeAsync(
            self.__client().get_handle(),
            b_id,
            b_address,
            self.__create_response_callback(cb),
            userdata))

    def unsubscribe(self, address: str, cb: ctrlxdatalayer.client.ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Removes a node from a subscription id
        @param[in]  address   Address of a node, that should be removed to the given subscription.
        @param[in]  callback  Callback to called when data is subscribed
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAsync(
            self.__client().get_handle(),
            b_id,
            b_address,
            self.__create_response_callback(cb),
            userdata))

    def subscribe_multi(self, address: typing.List[str], cb: ctrlxdatalayer.client.ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Set up a subscription to multiple nodes
        @param[in]  address   Set of addresses of nodes, that should be removed to the given subscription.
        @param[in]  count     Count of addresses.
        @param[in]  callback  Callback to called when data is subscribed
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = (ctypes.c_char_p * len(address))(*
                                                     [d.encode('utf-8') for d in address])
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeMultiAsync(
            self.__client().get_handle(),
            b_id,
            b_address,
            len(address),
            self.__create_response_callback(cb),
            userdata))

    def unsubscribe_multi(self, address: typing.List[str], cb: ctrlxdatalayer.client.ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Removes a set of nodes from a subscription id
        @param[in]  address   Address of a node, that should be removed to the given subscription.
        @param[in]  callback  Callback to called when data is subscribed
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = (ctypes.c_char_p * len(address))(*
                                                     [d.encode('utf-8') for d in address])
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeMultiAsync(
            self.__client().get_handle(),
            b_id,
            b_address,
            len(address),
            self.__create_response_callback(cb),
            userdata))

    def unsubscribe_all(self, cb: ctrlxdatalayer.client.ResponseCallback, userdata: userData_c_void_p = None) -> Result:
        """
        Removes all subscriptions from a subscription id
        @param[in]  callback  Callback to called when data is subscribed
        @param[in]  userdata  User data - will be returned in callback as userdata. You can use this userdata to identify your request
        @result <Result> status of function call
        """
        if self.__client is None:
            return
        self.__client()._unregister_sync(self)
        b_id = self.id().encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAllAsync(
            self.__client().get_handle(),
            b_id,
            self.__create_response_callback(cb),
            userdata))

    def wait_on_response_cb(self, wait: int = 5) -> bool:
        """ wait_on_response_cb """
        if wait <= 0:
            wait = 5
        n = 0
        while not self.__on_cb and n < wait:
            n = n + 1
            time.sleep(1)
        return self.__on_cb
