"""
Class Converter
"""
import ctypes
from enum import Enum

import ctrlxdatalayer
import ctrlxdatalayer.clib_converter
from ctrlxdatalayer.variant import Result, Variant

C_DLR_CONVERTER = ctypes.c_void_p


class C_DLR_SCHEMA(Enum):
    """
    Type of Converter
    """
    METADATA = 0
    REFLECTION = 1
    MEMORY = 2
    MEMORY_MAP = 3
    TOKEN = 4
    PROBLEM = 5
    DIAGNOSIS = 6


class Converter:
    """
        Converter interface
    """
    __slots__ = ['__converter']

    def __init__(self, c_converter: C_DLR_CONVERTER):
        """
            generate converter
        """
        self.__converter = c_converter

    def get_handle(self):
        """
        handle value of Converter:

        """
        return self.__converter

    def converter_generate_json_simple(self, data: Variant, indent_step: int):
        """
        This function generate a JSON string out of a Variant witch have a simple data type
        @param[in]  data        Variant which contains data with simple data type
        @param[in]  indentStep  Indentation length for json string
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Generated JSON as Variant (string)
        """
        json = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGenerateJsonSimple(
            self.__converter, data.get_handle(), json.get_handle(), indent_step))
        return result, json

    def converter_generate_json_complex(self, data: Variant, ty: Variant, indent_step: int):
        """
        This function generate a JSON string out of a Variant with complex type (flatbuffers) and the metadata of this data
        @param[in]  data        Variant which contains data of complex data type (flatbuffers) if data is empty (VariantType::UNKNOWN) type is converted to json schema
        @param[in]  type        Variant which contains type of data (Variant with flatbuffers BFBS)
        @param[in]  indentStep  Indentation length for json string
        @returns tuple  (Result, Variant)
        @return <Result>, status of function call,
        @return <Variant>, Generated JSON as Variant (string)
        """
        json = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGenerateJsonComplex(
            self.__converter, data.get_handle(), ty.get_handle(), json.get_handle(), indent_step))
        return result, json

    def parse_json_simple(self, json: str):
        """
        This function generates a Variant out of a JSON string containing the (simple) data
        @param[in]  json        Data of the Variant as a json string
        @returns tuple  (Result, Variant, Variant)
        @return <Result>,  status of function call,
        @return <Variant>, Variant which contains the data
        @return <Variant>, Error as Variant (string)
        """
        b_json = json.encode('utf-8')
        data = Variant()
        err = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterParseJsonSimple(
            self.__converter, b_json, data.get_handle(), err.get_handle()))
        return result, data, err

    def parse_json_complex(self, json: str, ty: Variant):
        """
        This function generates a Variant out of a JSON string containing the (complex) data
        @param[in]  json        Data of the Variant as a json string
        @param[in]  type        Variant which contains type of data (Variant with bfbs flatbuffer content)
        @returns tuple  (Result, Variant, Variant)
        @return <Result>,  status of function call,
        @return <Variant>, Variant which contains the data
        @return <Variant>, Error as Variant (string)
        """
        b_json = json.encode('utf-8')
        data = Variant()
        err = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterParseJsonComplex(
            self.__converter, b_json, ty.get_handle(), data.get_handle(), err.get_handle()))
        return result, data, err

    def get_schema(self, schema: C_DLR_SCHEMA):
        """
        This function returns the type (schema)
        @param[in]  schema      Requested schema
        @returns tuple  (Result, Variant)
        @return <Result>,  status of function call,
        @return <Variant>, Variant which contains the type (schema)
        """
        data = Variant()
        result = Result(ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGetSchema(
            self.__converter, schema.value, data.get_handle()))
        return result, data
