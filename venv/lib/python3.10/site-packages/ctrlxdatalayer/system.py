"""
    System class
"""
import ctrlxdatalayer
import ctrlxdatalayer.clib_system
from ctrlxdatalayer.converter import Converter
from ctrlxdatalayer.factory import Factory


class System:
    """
        Datalayer System Instance

        Hint: see python context manager for instance handling
    """
    __slots__ = ['__system', '__closed']

    def __init__(self, ipc_path: str):
        """
        Creates a datalayer system
        @param[in] ipc_path    Path for interprocess communication - use null pointer for automatic detection
        """
        b_ipc_path = ipc_path.encode('utf-8')
        self.__system = ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemCreate(
            b_ipc_path)
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
        closes the system instance
        """
        if self.__closed:
            return
        self.__closed = True
        self.stop(True)
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemDelete(self.__system)

    def get_handle(self):
        """
        handle value of system
        """
        return self.__system

    def start(self, bo_start_broker: bool):
        """
        Starts a datalayer system
        @param[in] bo_start_broker  Use true to start a broker. If you are a user of the datalayer - call with false!
        """
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemStart(
            self.__system, bo_start_broker)

    def stop(self, bo_force_provider_stop: bool) -> bool:
        """
        Stops a datalayer system
        @param[in] bo_force_provider_stop   Force stop off all created providers for this datalayer system
        @returns <bool> false if there is a client or provider active
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemStop(
            self.__system, bo_force_provider_stop)

    def factory(self) -> Factory:
        """
        Returns the factory to create clients and provider for the datalayer
        @returns <Factory>
        """
        c_factory = ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemFactory(
            self.__system)
        return Factory(c_factory)

    def json_converter(self) -> Converter:
        """
        Returns converter between JSON and Variant
        @returns <Converter>
        """
        c_converter = ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemJsonConverter(
            self.__system)
        return Converter(c_converter)

    def set_bfbs_path(self, path):
        """
        Sets the base path to bfbs files
        @param[in] path    Base path to bfbs files
        """
        b_path = path.encode('utf-8')
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_systemSetBfbsPath(
            self.__system, b_path)
