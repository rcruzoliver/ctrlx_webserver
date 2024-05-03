"""
    Variant class
"""
import ctypes
import datetime
import typing
from enum import Enum

import ctrlxdatalayer
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT

FILE_TIME_EPOCH = datetime.datetime(1601, 1, 1)
# FILETIME counts 100 nanoseconds intervals = 0.1 microseconds, so 10 of those are 1 microsecond
FILE_TIME_MICROSECOND = 10


class Result(Enum):
    """
        Result(Enum)

        status of function call
    """
    OK = 0
    OK_NO_CONTENT = 0x00000001
    FAILED = 0x80000001
    # application
    INVALID_ADDRESS = 0x80010001
    UNSUPPORTED = 0x80010002
    OUT_OF_MEMORY = 0x80010003
    LIMIT_MIN = 0x80010004
    LIMIT_MAX = 0x80010005
    TYPE_MISMATCH = 0x80010006
    SIZE_MISMATCH = 0x80010007
    INVALID_FLOATINGPOINT = 0x80010009
    INVALID_HANDLE = 0x8001000A
    INVALID_OPERATION_MODE = 0x8001000B
    INVALID_CONFIGURATION = 0x8001000C
    INVALID_VALUE = 0x8001000D
    SUBMODULE_FAILURE = 0x8001000E
    TIMEOUT = 0x8001000F
    ALREADY_EXISTS = 0x80010010
    CREATION_FAILED = 0x80010011
    VERSION_MISMATCH = 0x80010012
    DEPRECATED = 0x80010013
    PERMISSION_DENIED = 0x80010014
    NOT_INITIALIZED = 0x80010015
    MISSING_ARGUMENT = 0x80010016
    TOO_MANY_ARGUMENTS = 0x80010017
    RESOURCE_UNAVAILABLE = 0x80010018
    COMMUNICATION_ERROR = 0x80010019
    TOO_MANY_OPERATIONS = 0x8001001A
    WOULD_BLOCK = 0x8001001B

    # communication
    COMM_PROTOCOL_ERROR = 0x80020001
    COMM_INVALID_HEADER = 0x80020002
    # client
    CLIENT_NOT_CONNECTED = 0x80030001
    # provider
    # broker
    # realtime related error codes
    RT_NOT_OPEN = 0x80060001
    RT_INVALID_OBJECT = 0x80060002
    RT_WRONG_REVISION = 0x80060003
    RT_NO_VALID_DATA = 0x80060004
    RT_MEMORY_LOCKED = 0x80060005
    RT_INVALID_MEMORY_MAP = 0x80060006
    RT_INVALID_RETAIN = 0x80060007
    RT_INVALID_ERROR = 0x80060008
    RT_MALLOC_FAILED = 0x80060009

    # security
    sec_noSEC_NO_TOKEN_token = 0x80070001
    SEC_INVALID_SESSION = 0x80070002
    SEC_INVALID_TOKEN_CONTENT = 0x80070003
    SEC_UNAUTHORIZED = 0x80070004
    SEC_PAYMENT_REQUIRED = 0x80070005

    @classmethod
    def _missing_(cls, value):
        """
        _missing_ function
        """
        i = 0xFFFFFFFF & value
        if i == 0x00000001:
            return cls(i)
        if i == 0x80000001:
            return cls(i)
        if (i >= 0x80010001) and (i <= Result.WOULD_BLOCK.value):
            return cls(i)
        if (i >= 0x80020001) and (i <= 0x80020002):
            return cls(i)
        if i == 0x80030001:
            return cls(i)
        if (i >= 0x80060001) and (i <= Result.RT_MALLOC_FAILED.value):
            return cls(i)
        if (i >= 0x80070001) and (i <= Result.SEC_PAYMENT_REQUIRED.value):
            return cls(i)
        return value


class VariantType(Enum):
    """
        VariantType(Enum)

        type of variant
    """
    UNKNON = 0
    BOOL8 = 1
    INT8 = 2
    UINT8 = 3
    INT16 = 4
    UINT16 = 5
    INT32 = 6
    UINT32 = 7
    INT64 = 8
    UINT64 = 9
    FLOAT32 = 10
    FLOAT64 = 11
    STRING = 12
    ARRAY_BOOL8 = 13
    ARRAY_INT8 = 14
    ARRAY_UINT8 = 15
    ARRAY_INT16 = 16
    ARRAY_UINT16 = 17
    ARRAY_INT32 = 18
    ARRAY_UINT32 = 19
    ARRAY_INT64 = 20
    ARRAY_UINT64 = 21
    ARRAY_FLOAT32 = 22
    ARRAY_FLOAT64 = 23
    ARRAY_STRING = 24
    RAW = 25
    FLATBUFFERS = 26
    TIMESTAMP = 27
    ARRAY_OF_TIMESTAMP = 28


class Variant:
    """
        Variant is a container for a many types of data.

        Hint: see python context manager for instance handling
    """

    __slots__ = ['_variant', '__closed']

    def __init__(self, c_variant: C_DLR_VARIANT = None):
        """
        generate Variant
        """
        self.__closed = False
        if c_variant is None:
            self._variant = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCreate()
        else:
            self.__closed = True
            self._variant = c_variant

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
        closes the variant instance
        """
        if self.__closed:
            return
        self.__closed = True
        ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantDelete(self._variant)

    def get_handle(self):
        """
        handle value of variant
        """
        return self._variant

    def get_type(self) -> VariantType:
        """
        Returns the type of the variant
        @returns <VariantType>
        """
        return VariantType(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetType(self._variant))

    def get_data(self) -> bytearray:
        """
        Returns the pointer to the data of the variant
        @returns array of bytes
        """
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetSize(
            self._variant)
        c_data = ctypes.string_at(
            ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetData(self._variant), length)
        return bytearray(c_data)

    def get_size(self) -> int:
        """
        @returns size of the type in bytes
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetSize(self._variant)

    def get_count(self) -> int:
        """
        Returns the count of elements in the variant (scalar data types = 1, array = count of elements in array)
        @returns count of a type
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(self._variant)

    def check_convert(self, datatype: VariantType) -> Result:
        """
        Checks whether the variant can be converted to another type
        @returns <Result>, status of function call
        """
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCheckConvert(
            self._variant, datatype.value))

    @staticmethod
    def copy(c_variant: C_DLR_VARIANT):
        """
        copies the content of a variant to another variant
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, copy of variant
        """
        dest = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCopy(
            dest._variant, c_variant))
        return result, dest

    def clone(self):
        """
        clones the content of a variant to another variant
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, clones of variant
        """
        return Variant.copy(self._variant)

    def get_bool8(self) -> bool:
        """
        Returns the value of the variant as a bool (auto convert if possible) otherwise 0
        @returns [True, False]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetBOOL8(self._variant)

    def get_int8(self) -> int:
        """
        Returns the value of the variant as an int8 (auto convert if possible) otherwise 0
        @returns [-128, 127]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT8(self._variant)

    def get_uint8(self) -> int:
        """
        Returns the value of the variant as an uint8 (auto convert if possible) otherwise 0
        @returns [0, 255]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT8(self._variant)

    def get_int16(self) -> int:
        """
        Returns the value of the variant as an int16 (auto convert if possible) otherwise 0
        @returns [-32768, 32767]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT16(self._variant)

    def get_uint16(self) -> int:
        """
        Returns the value of the variant as an uint16 (auto convert if possible) otherwise 0
        @returns [0, 65.535]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT16(self._variant)

    def get_int32(self) -> int:
        """
        Returns the value of the variant as an int32 (auto convert if possible) otherwise 0
        @returns [-2.147.483.648, 2.147.483.647]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT32(self._variant)

    def get_uint32(self) -> int:
        """
        Returns the value of the variant as an Uint32 (auto convert if possible) otherwise 0
        @returns [0, 4.294.967.295]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT32(self._variant)

    def get_int64(self) -> int:
        """
        Returns the value of the variant as an int64 (auto convert if possible) otherwise 0
        @returns [-9.223.372.036.854.775.808, 9.223.372.036.854.775.807]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT64(self._variant)

    def get_uint64(self) -> int:
        """
        Returns the value of the variant as an uint64 (auto convert if possible) otherwise 0
        @returns [0, 18446744073709551615]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT64(self._variant)

    def get_float32(self) -> float:
        """
        Returns the value of the variant as a float (auto convert if possible) otherwise 0
        @returns [1.2E-38, 3.4E+38]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetFLOAT32(self._variant)

    def get_float64(self) -> float:
        """
        Returns the value of the variant as a double (auto convert if possible) otherwise 0
        @returns [2.3E-308, 1.7E+308]
        """
        return ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetFLOAT64(self._variant)

    def get_string(self) -> str:
        """
        Returns the array of bool8 if the type is an array of bool otherwise null
        @returns string
        """
        if self.check_convert(VariantType.STRING) != Result.OK:
            return None
        b = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetSTRING(
            self._variant)
        if b is None:
            return b
        return b.decode('utf-8')

    def get_flatbuffers(self) -> bytearray:
        """
        Returns the flatbuffers if the type is a flatbuffers otherwise null
        @returns flatbuffer (bytearray)
        """
        if self.check_convert(VariantType.FLATBUFFERS) != Result.OK:
            return None

        return self.get_data()

    def get_datetime(self) -> datetime.datetime:
        """datetime object as timestamp (FILETIME) 64 bit 100ns since 1.1.1601 (UTC)

        Returns:
            datetime.datetime: datetime object
        """
        d = self.get_uint64()
        return Variant.from_filetime(d)

    def get_array_bool8(self) -> typing.List[bool]:
        """
        Returns the array of int8 if the type is an array of int8 otherwise null
        @returns array of bool8
        """
        if self.check_convert(VariantType.ARRAY_BOOL8) != Result.OK:
            return None

        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfBOOL8(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_int8(self) -> typing.List[int]:
        """
        Returns the array of int8 if the type is an array of int8 otherwise null
        @returns array of int8
        """
        if self.check_convert(VariantType.ARRAY_INT8) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT8(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_uint8(self) -> typing.List[int]:
        """
        Returns the array of uint8 if the type is an array of uint8 otherwise null
        @returns array of uint8
        """
        if self.check_convert(VariantType.ARRAY_UINT8) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT8(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_int16(self) -> typing.List[int]:
        """
        Returns the array of int16 if the type is an array of int16 otherwise null
        @returns array of int16
        """
        if self.check_convert(VariantType.ARRAY_INT16) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT16(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_uint16(self) -> typing.List[int]:
        """
        Returns the array of uint16 if the type is an array of uint16 otherwise null
        @returns array of uint16
        """
        if self.check_convert(VariantType.ARRAY_UINT16) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT16(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_int32(self) -> typing.List[int]:
        """
        Returns the array of int32 if the type is an array of int32 otherwise null
        @returns array of int32
        """
        if self.check_convert(VariantType.ARRAY_INT32) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT32(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_uint32(self) -> typing.List[int]:
        """
        Returns the array of uint32 if the type is an array of uint32 otherwise null
        @returns array of uint32
        """
        if self.check_convert(VariantType.ARRAY_UINT32) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT32(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_int64(self) -> typing.List[int]:
        """
        Returns the array of int64 if the type is an array of int64 otherwise null
        @returns array of int64
        """
        if self.check_convert(VariantType.ARRAY_INT64) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT64(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_uint64(self) -> typing.List[int]:
        """
        Returns the array of uint64 if the type is an array of uint64 otherwise null
        @returns array of uint64
        """
        if self.check_convert(VariantType.ARRAY_UINT64) != Result.OK and self.check_convert(VariantType.ARRAY_OF_TIMESTAMP) != Result.OK:
            return None

        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT64(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_float32(self) -> typing.List[float]:
        """
        Returns the array of float if the type is an array of float otherwise null
        @returns array of float32
        """
        if self.check_convert(VariantType.ARRAY_FLOAT32) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfFLOAT32(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_float64(self) -> typing.List[float]:
        """
        Returns the array of double if the type is an array of double otherwise null
        @returns array of float64
        """
        if self.check_convert(VariantType.ARRAY_FLOAT64) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfFLOAT64(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i] for i in range(length)]

    def get_array_string(self) -> typing.List[str]:
        """
        Returns the type of the variant
        @returns array of strings
        """
        if self.check_convert(VariantType.ARRAY_STRING) != Result.OK:
            return None
        c_data = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfSTRING(
            self._variant)
        length = ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount(
            self._variant)
        return [c_data[i].decode('utf-8') for i in range(length)]

    def get_array_datetime(self) -> typing.List[datetime.datetime]:
        """datetime objects as timestamp (FILETIME) 64 bit 100ns since 1.1.1601 (UTC)

        Returns:
            array of datetime.datetime: datetime object
        """
        vals = self.get_array_uint64()
        return [Variant.from_filetime(ft) for ft in vals]

    def set_bool8(self, data: bool) -> Result:
        """
        Set a bool value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetBOOL8(self._variant, data))

    def set_int8(self, data: int) -> Result:
        """
        Set an int8 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT8(self._variant, data))

    def set_uint8(self, data: int) -> Result:
        """
        Set a uint8 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT8(self._variant, data))

    def set_int16(self, data: int) -> Result:
        """
        Set an int16 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT16(self._variant, data))

    def set_uint16(self, data: int) -> Result:
        """
        Set a uint16 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT16(self._variant, data))

    def set_int32(self, data: int) -> Result:
        """
        Set an int32 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT32(self._variant, data))

    def set_uint32(self, data: int) -> Result:
        """
        Set a uint32 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT32(self._variant, data))

    def set_int64(self, data: int) -> Result:
        """
        Set an int64 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT64(self._variant, data))

    def set_uint64(self, data: int) -> Result:
        """
        Set a uint64 value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT64(self._variant, data))

    def set_float32(self, data: float) -> Result:
        """
        Set a float value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFLOAT32(self._variant, data))

    def set_float64(self, data: float) -> Result:
        """
        Set a double value
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFLOAT64(self._variant, data))

    def set_string(self, data: str) -> Result:
        """
        Set a string
        @returns <Result>, status of function call
        """
        b_data = data.encode('utf-8')
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetSTRING(self._variant, b_data))

    def set_flatbuffers(self, data: bytearray) -> Result:
        """
        Set a flatbuffers
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        buf = (ctypes.c_byte * len(data)).from_buffer(data)
        c_data = ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte))
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFlatbuffers(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_timestamp(self, data: int) -> Result:
        """
        Set a timestamp value
        data <int>: timestamp (FILETIME) 64 bit 100ns since 1.1.1601 (UTC)
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetTimestamp(self._variant, data))

    def set_datetime(self, dt: datetime) -> Result:
        """Set a timestamp value as datetime object

        Args:
            dt (datetime): datetime object

        Returns:
            Result: status of function call
        """
        ft = Variant.to_filetime(dt)
        return self.set_timestamp(ft)

    @staticmethod
    def from_filetime(filetime) -> datetime:
        """convert filetime to datetime

        Args:
            filetime (int): (FILETIME) 64 bit 100ns since 1.1.1601 (UTC)

        Returns:
            datetime: datetime object
        """
        #microseconds_since_file_time_epoch = filetime // FILE_TIME_MICROSECOND
        return FILE_TIME_EPOCH + datetime.timedelta(microseconds=(filetime // FILE_TIME_MICROSECOND))

    @staticmethod
    def to_filetime(dt: datetime) -> int:
        """convert datetime to filetime

        Args:
            dt (datetime): datetime to convert

        Returns:
            int: (FILETIME) 64 bit 100ns since 1.1.1601 (UTC)
        """
        microseconds_since_file_time_epoch = (
            dt - FILE_TIME_EPOCH) // datetime.timedelta(microseconds=1)
        return microseconds_since_file_time_epoch * FILE_TIME_MICROSECOND

    def set_array_bool8(self, data: typing.List[bool]) -> Result:
        """
        Set array of bool8
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_bool * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_BOOL8(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_int8(self, data: typing.List[int]) -> Result:
        """
        Set array of int8
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_int8 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT8(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_uint8(self, data: typing.List[int]) -> Result:
        """
        Set array of uint8
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_uint8 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT8(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_int16(self, data: typing.List[int]) -> Result:
        """
        Set array of int16
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_int16 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT16(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_uint16(self, data: typing.List[int]) -> Result:
        """
        Set array of uint16
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_uint16 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT16(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_int32(self, data: typing.List[int]) -> Result:
        """
        Set array of int32
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_int32 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT32(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_uint32(self, data: typing.List[int]) -> Result:
        """
        Set array of uint32
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_uint32 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT32(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_int64(self, data: typing.List[int]) -> Result:
        """
        Set array of int64
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_int64 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT64(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_uint64(self, data: typing.List[int]) -> Result:
        """
        Set array of uint64
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_uint64 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT64(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_float32(self, data: typing.List[float]) -> Result:
        """
        Set array of float32
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_float * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_FLOAT32(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_float64(self, data: typing.List[float]) -> Result:
        """
        Set array of float64
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_double * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_FLOAT64(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_string(self, data: typing.List[str]) -> Result:
        """
        Set array of strings
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_char_p * len(data))(*
                                               [d.encode('utf-8') for d in data])
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_STRING(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_timestamp(self, data: typing.List[int]) -> Result:
        """
        Set array of timestamp (uint64)
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        c_data = (ctypes.c_uint64 * len(data))(*data)
        r = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_TIMESTAMP(
            self._variant, c_data, len(data)))
        del c_data
        return r

    def set_array_datetime(self, data: typing.List[datetime.datetime]) -> Result:
        """
        Set array of datetime
        @returns <Result>, status of function call
        """
        if self.__closed:
            return Result.NOT_INITIALIZED
        return self.set_array_timestamp([Variant.to_filetime(d) for d in data])


def copy(dest: Variant, src: Variant):
    """
    copies the content of a variant to another variant
    @returns tuple  (Result, Variant)
    @return <Result>, status of function call,
    """
    result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCopy(
        dest.get_handle(), src.get_handle()))
    return result


class VariantRef(Variant):
    """
        Variant Helper interface,
        Important: store not an instance of VariantRef, uses the clone/copy function
    """

    def __init__(self, c_variant: C_DLR_VARIANT = None):
        """
        generate Variant
        """
        super().__init__(c_variant)

    def __del__(self):
        """
        __del__
        """
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__
        """
        pass
