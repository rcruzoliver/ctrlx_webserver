import ctypes
from enum import Enum

import ctrlxdatalayer
from ctrlxdatalayer.clib import C_DLR_RESULT
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT

# ===================================================================
# converter.h
# ===================================================================

# typedef void *DLR_CONVERTER;
#C_DLR_CONVERTER = ctypes.c_void_p

void_p_converter = ctypes.c_void_p
variant_p_data = C_DLR_VARIANT
variant_p_type = C_DLR_VARIANT
variant_p_json = C_DLR_VARIANT
int32_indentStep = ctypes.c_int32

# DLR_RESULT DLR_converterGenerateJsonSimple(DLR_CONVERTER converter, const DLR_VARIANT data, DLR_VARIANT json, int32_t indentStep);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGenerateJsonSimple.argtypes = (
    void_p_converter, variant_p_data, variant_p_json, int32_indentStep)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGenerateJsonSimple.restype = C_DLR_RESULT

# DLR_RESULT DLR_converterGenerateJsonComplex(DLR_CONVERTER converter, const DLR_VARIANT data, const DLR_VARIANT type, DLR_VARIANT json, int32_t indentStep);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGenerateJsonComplex.argtypes = (
    void_p_converter, variant_p_data, variant_p_type, variant_p_json, int32_indentStep)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGenerateJsonComplex.restype = C_DLR_RESULT

variant_p_error = C_DLR_VARIANT

# DLR_RESULT DLR_converterParseJsonSimple(DLR_CONVERTER converter, const char* json, DLR_VARIANT data, DLR_VARIANT error);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterParseJsonSimple.argtypes = (
    void_p_converter, ctypes.c_char_p, variant_p_data, variant_p_error)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterParseJsonSimple.restype = C_DLR_RESULT

variant_p_type = C_DLR_VARIANT

# DLR_RESULT DLR_converterParseJsonComplex(DLR_CONVERTER converter, const char* json, const DLR_VARIANT type, DLR_VARIANT data, DLR_VARIANT error);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterParseJsonComplex.argtypes = (
    void_p_converter, ctypes.c_char_p, variant_p_type, variant_p_data, variant_p_error)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterParseJsonComplex.restype = C_DLR_RESULT


# DLR_RESULT DLR_converterGetSchema(DLR_CONVERTER converter, DLR_SCHEMA schema, DLR_VARIANT data);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGetSchema.argtypes = (
    void_p_converter, ctypes.c_uint32, variant_p_data)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_converterGetSchema.restype = C_DLR_RESULT
