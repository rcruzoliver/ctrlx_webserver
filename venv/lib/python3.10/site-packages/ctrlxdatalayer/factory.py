"""
    Factory class
"""
import ctrlxdatalayer
from ctrlxdatalayer.clib_factory import C_DLR_FACTORY
from ctrlxdatalayer.client import Client
from ctrlxdatalayer.provider import Provider


class Factory:
    """ Factory class """

    __slots__ = ['__factory']

    def __init__(self, c_factory: C_DLR_FACTORY):
        """
        generate Factory
        """
        self.__factory = c_factory

    def get_handle(self):
        """
        handle value of Factory
        """
        return self.__factory

    def create_client(self, remote: str) -> Client:
        """
        Creates a client for accessing data of the system
        @param[in] remote     Remote address of the data layer
        @returns <Client>
        """
        b_remote = remote.encode('utf-8')
        c_client = ctrlxdatalayer.clib.libcomm_datalayer.DLR_factoryCreateClient(
            self.__factory, b_remote)
        return Client(c_client)

    def create_provider(self, remote: str) -> Provider:
        """
        Creates a provider to provide data to the datalayer
        @param[in] remote     Remote address of the data layer
        @returns <Provider>
        """
        b_remote = remote.encode('utf-8')
        c_provider = ctrlxdatalayer.clib.libcomm_datalayer.DLR_factoryCreateProvider(
            self.__factory, b_remote)
        return Provider(c_provider)
