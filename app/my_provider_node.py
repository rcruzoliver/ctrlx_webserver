# SPDX-FileCopyrightText: Bosch Rexroth AG
#
# SPDX-License-Identifier: MIT

import ctrlxdatalayer
from comm.datalayer import DisplayFormat, Metadata, NodeClass
from ctrlxdatalayer.provider import Provider
from ctrlxdatalayer.provider_node import (
    ProviderNode,
    ProviderNodeCallbacks,
    NodeCallback,
)
from ctrlxdatalayer.variant import Result, Variant

from appdata.app_data_control import AppDataControl


class MyProviderNode:
    """MyProviderNode"""

    def __init__(self, provider: Provider, address: str, initialValue: Variant):
        """__init__"""
        self._cbs = ProviderNodeCallbacks(
            self.__on_create,
            self.__on_remove,
            self.__on_browse,
            self.__on_read,
            self.__on_write,
            self.__on_metadata,
        )
        self._app_data_control = AppDataControl()

        self._providerNode = ProviderNode(self._cbs)

        self._provider = provider
        self._address = address
        self._data = initialValue

    def register_node(self):
        """register_node"""
        return self._provider.register_node(self._address, self._providerNode)

    def unregister_node(self):
        """unregister_node"""
        self._provider.unregister_node(self._address)
        #self._metadata.close()
        self._data.close()

    def set_value(self, value: Variant):
        """set_value"""
        self._data = value

    def __on_create(
        self,
        userdata: ctrlxdatalayer.clib.userData_c_void_p,
        address: str,
        data: Variant,
        cb: NodeCallback,
    ):
        """__on_create"""
        print("__on_create()", "address:", address, "userdata:", userdata, flush=True)
        cb(Result.OK, data)

    def __on_remove(
        self,
        userdata: ctrlxdatalayer.clib.userData_c_void_p,
        address: str,
        cb: NodeCallback,
    ):
        """__on_remove"""
        print("__on_remove()", "address:", address, "userdata:", userdata, flush=True)
        cb(Result.UNSUPPORTED, None)

    def __on_browse(
        self,
        userdata: ctrlxdatalayer.clib.userData_c_void_p,
        address: str,
        cb: NodeCallback,
    ):
        """__on_browse"""
        print("__on_browse()", "address:", address, "userdata:", userdata, flush=True)
        with Variant() as new_data:
            new_data.set_array_string([])
            cb(Result.OK, new_data)

    def __on_read(
        self,
        userdata: ctrlxdatalayer.clib.userData_c_void_p,
        address: str,
        data: Variant,
        cb: NodeCallback,
    ):
        """__on_read"""            
        print(
            "__on_read()",
            "address:",
            address,
            "data:",
            self._data,
            "userdata:",
            userdata,
            flush=True,
        )
        new_data = self._data
        cb(Result.OK, new_data)

    def __on_write(
        self,
        userdata: ctrlxdatalayer.clib.userData_c_void_p,
        address: str,
        data: Variant,
        cb: NodeCallback,
    ):
        
        if(address=="webserver/app-cmd"):
            resultVariant = Variant()
            if(data.get_string()=="save"):
                if self._app_data_control.set_default():
                    resultVariant.set_string("save done")
                    _ , data = resultVariant.clone()
                else:
                    resultVariant.set_string("save error")
                    _ , data = resultVariant.clone()
            elif(data.get_string()=="load"):
                if self._app_data_control.load():
                    resultVariant.set_string("load done")
                    _ , data = resultVariant.clone()
                else:
                    resultVariant.set_string("load error")
                    _ , data = resultVariant.clone()
            else:
                resultVariant.set_string("command unknown") 
                _ , data = resultVariant.clone()
                        
        """__on_write"""
        print(
            "__on_write()",
            "address:",
            address,
            "data:",
            data,
            "userdata:",
            userdata,
            flush=True,
        )

        if self._data.get_type() != data.get_type():
            cb(Result.TYPE_MISMATCH, None)
            return

        result, self._data = data.clone()
        cb(Result.OK, self._data)

    def __on_metadata(
        self,
        userdata: ctrlxdatalayer.clib.userData_c_void_p,
        address: str,
        cb: NodeCallback,
    ):
        """__on_metadata"""
        print("__on_metadata()", "address:", address, flush=True)
        cb(Result.FAILED, None) #cb(Result.OK, self._metadata)  # Take metadata from metadata.mddb