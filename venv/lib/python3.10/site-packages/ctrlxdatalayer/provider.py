"""
Class Provider
"""
import ctrlxdatalayer
from ctrlxdatalayer.clib_provider import C_DLR_PROVIDER
from ctrlxdatalayer.provider_node import ProviderNode
from ctrlxdatalayer.variant import Result, Variant


class Provider:
    """
        Provider interface to manage provider nodes
        Hint: see python context manager for instance handling
    """

    __slots__ = ['__provider', '__closed']

    def __init__(self, c_provider: C_DLR_PROVIDER):
        """
        generate Provider
        """
        self.__provider: C_DLR_PROVIDER = c_provider
        self.__closed = False

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
        closes the provider instance
        """
        if self.__closed:
            return
        self.__closed = True
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerStop(self.__provider)
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerDelete(
            self.__provider)

    def register_type(self, address: str, pathname: str) -> Result:
        """
        Register a type to the datalayer
        @param[in]  address   Address of the node to register (no wildcards allowed)
        @param[in]  pathname  Path to flatbuffer bfbs
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        b_pathname = pathname.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterType(self.__provider, b_address, b_pathname))

    def unregister_type(self, address: str) -> Result:
        """
        Unregister a type from the datalayer
        @param[in]  address   Address of the node to register (wildcards allowed)
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerUnregisterType(self.__provider, b_address))

    def register_node(self, address: str, node: ProviderNode) -> Result:
        """
        Register a node to the datalayer
        @param[in]  address   Address of the node to register (wildcards allowed)
        @param[in]  node      Node to register
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterNode(self.__provider, b_address, node.get_handle()))

    def unregister_node(self, address: str) -> Result:
        """
        Unregister a node from the datalayer
        @param[in]  address   Address of the node to register (wildcards allowed)
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerUnregisterNode(self.__provider, b_address))

    def set_timeout_node(self, node: ProviderNode, timeout_ms: int) -> Result:
        """
        Set timeout for a node for asynchron requests (default value is 1000ms)
        @param[in]  node      Node to set timeout for
        @param[in]  timeoutMS Timeout in milliseconds for this node
        @returns <Result>, status of function call
        """
        if node is None:
            return Result.FAILED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerSetTimeoutNode(self.__provider, node.get_handle(), timeout_ms))

    def start(self) -> Result:
        """
        Start the provider
        @returns <Result>, status of function call
        """
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerStart(self.__provider))

    def stop(self) -> Result:
        """
        Stop the provider
        @returns <Result>, status of function call
        """
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerStop(self.__provider))

    def is_connected(self) -> bool:
        """
        returns whether provider is connected
        @returns status of connection
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerIsConnected(self.__provider)

    def get_token(self) -> Variant:
        """
        return the current token of the current request.You can call this function during your onRead, onWrite, ... methods of your ProviderNodes. If there is no current request the method return an empty token
        @returns <Variant> current token
        """
        return Variant(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerGetToken(self.__provider))

    def register_type_variant(self, address: str, data: Variant) -> Result:
        """
        Register a type to the datalayer
        @param[in]  address   Address of the node to register (no wildcards allowed)
        @param[in]  data      Variant with flatbuffer type
        @returns <Result>, status of function call
        """
        b_address = address.encode('utf-8')
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_providerRegisterTypeVariant(self.__provider, b_address, data.get_handle()))
