"""
Class Sync Subscription
"""
import ctypes
import typing
import weakref

import ctrlxdatalayer
import ctrlxdatalayer.clib
import ctrlxdatalayer.subscription
from ctrlxdatalayer.clib import userData_c_void_p
from ctrlxdatalayer.clib_client import C_DLR_CLIENT_NOTIFY_RESPONSE, C_NotifyItem
from ctrlxdatalayer.variant import Result, Variant


class SubscriptionSync(ctrlxdatalayer.subscription.Subscription):
    """
    SubscriptionSync
    """
    __slots__ = ['__ptr_notify', '__closed', '__client', '__id']

    def __init__(self, client: ctrlxdatalayer.client.Client):
        """
        @param [in]  client    Reference to the client
        """
        self.__ptr_notify: ctrlxdatalayer.client._CallbackPtr
        self.__closed = False
        self.__client = weakref.ref(client)
        self.__id = ""

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
        """
        on_close
        """
        self.close()

    def id(self) -> str:
        """
        Subscription ID

        @return <str> id
        """
        return self.__id

    def __create_sub_callback(self, cb: ctrlxdatalayer.subscription.ResponseNotifyCallback):
        """
        callback management
        """
        cb_ptr = ctrlxdatalayer.client._CallbackPtr()
        self.__ptr_notify = cb_ptr

        def _cb(status: ctrlxdatalayer.clib.C_DLR_RESULT, items: ctypes.POINTER(C_NotifyItem),
                count: ctypes.c_uint32, userdata: ctypes.c_void_p):
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
        return self.__create_sub_callback(cb)

    def close(self):
        """
        closes the client instance
        """
        if self.__closed:
            return
        self.__closed = True
        self.unsubscribe_all()
        self.__ptr_notify = None
        self.__client = None

    def _create(self, prop: Variant, cnb: ctrlxdatalayer.subscription.ResponseNotifyCallback,
                userdata: userData_c_void_p = None) -> Result:
        """
        Set up a subscription
        @param[in]  ruleset   Variant that describe ruleset of subscription as subscription.fbs
        @param[in]  publishCallback  Callback to call when new data is available
        @param[in]  userdata  User data - will be returned in publishCallback as userdata. You can use this userdata to identify your subscription
        @result <Result> status of function cal
        """
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientCreateSubscriptionSync(
            self.__client().get_handle(), prop.get_handle(),
            self.__create_sub_callback(cnb), userdata, self.__client().get_token()))
        if r == Result.OK:
            self.__id = ctrlxdatalayer.subscription.get_id(prop)
        return r

    def subscribe(self, address: str) -> Result:
        """
        Adds a node to a subscription id
        @param[in]  address   Address of a node, that should be added to the given subscription.
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeSync(
            self.__client().get_handle(), b_id, b_address))

    def unsubscribe(self, address: str) -> Result:
        """
        Removes a node from a subscription id
        @param[in]  address   Address of a node, that should be removed to the given subscription.
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeSync(
            self.__client().get_handle(), b_id, b_address))

    def subscribe_multi(self, address: typing.List[str]) -> Result:
        """
        Adds a list of nodes to a subscription id
        @param[in]  address   List of Addresses of a node, that should be added to the given subscription.
        @param[in]  count     Count of addresses.
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = (ctypes.c_char_p * len(address))(*
                                                     [d.encode('utf-8') for d in address])
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientSubscribeMultiSync(
            self.__client().get_handle(), b_id, b_address, len(address)))

    def unsubscribe_multi(self, address: typing.List[str]) -> Result:
        """
        Removes a set of nodes from a subscription id
        @param[in]  address   Set of addresses of nodes, that should be removed to the given subscription.
        @result <Result> status of function call
        """
        b_id = self.id().encode('utf-8')
        b_address = (ctypes.c_char_p * len(address))(*
                                                     [d.encode('utf-8') for d in address])
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeMultiSync(
            self.__client().get_handle(), b_id, b_address, len(address)))

    def unsubscribe_all(self) -> Result:
        """
        Removes subscription id completely
        @result <Result> status of function call
        """
        if self.__client is None:
            return
        self.__client()._unregister_sync(self)
        b_id = self.id().encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_clientUnsubscribeAllSync(
            self.__client().get_handle(), b_id))
