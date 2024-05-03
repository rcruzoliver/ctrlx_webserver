import ctypes

import ctrlxdatalayer
from ctrlxdatalayer.clib import C_DLR_RESULT

# ===================================================================
# variant.h  - Part I
# ===================================================================

# typedef void *DLR_VARIANT;
C_DLR_VARIANT = ctypes.c_void_p

# ===================================================================
# variant.h - Part II
# ===================================================================

# typedef enum DLR_VARIANT_TYPE
C_DLR_VARIANT_TYPE = ctypes.c_int32

# DLR_VARIANT DLR_variantCreate();
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCreate.argtypes = ()
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCreate.restype = C_DLR_VARIANT

# void DLR_variantDelete(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantDelete.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantDelete.restype = None

# DLR_RESULT DLR_variantSetBOOL8(DLR_VARIANT variant,   const bool value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetBOOL8.argtypes = (
    C_DLR_VARIANT, ctypes.c_bool)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetBOOL8.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetINT8(DLR_VARIANT variant,    const int8_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT8.argtypes = (
    C_DLR_VARIANT, ctypes.c_int8)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT8.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetUINT8(DLR_VARIANT variant,   const uint8_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT8.argtypes = (
    C_DLR_VARIANT, ctypes.c_uint8)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT8.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetINT16(DLR_VARIANT variant,   const int16_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT16.argtypes = (
    C_DLR_VARIANT, ctypes.c_int16)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT16.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetUINT16(DLR_VARIANT variant,  const uint16_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT16.argtypes = (
    C_DLR_VARIANT, ctypes.c_uint16)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT16.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetINT32(DLR_VARIANT variant,   const int32_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT32.argtypes = (
    C_DLR_VARIANT, ctypes.c_int32)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT32.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetUINT32(DLR_VARIANT variant,  const uint32_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT32.argtypes = (
    C_DLR_VARIANT, ctypes.c_uint32)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT32.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetINT64(DLR_VARIANT variant,   const int64_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT64.argtypes = (
    C_DLR_VARIANT, ctypes.c_int64)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetINT64.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetUINT64(DLR_VARIANT variant,  const uint64_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT64.argtypes = (
    C_DLR_VARIANT, ctypes.c_uint64)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetUINT64.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetFLOAT32(DLR_VARIANT variant, const float value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFLOAT32.argtypes = (
    C_DLR_VARIANT, ctypes.c_float)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFLOAT32.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetFLOAT64(DLR_VARIANT variant, const double value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFLOAT64.argtypes = (
    C_DLR_VARIANT, ctypes.c_double)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFLOAT64.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetSTRING(DLR_VARIANT variant,  const char* value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetSTRING.argtypes = (
    C_DLR_VARIANT, ctypes.c_char_p)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetSTRING.restype = C_DLR_RESULT

# 112
# DLR_RESULT DLR_variantSetARRAY_OF_BOOL8(DLR_VARIANT variant,   const bool* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_BOOL8.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_BOOL8.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_INT8(DLR_VARIANT variant,    const int8_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT8.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_int8), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT8.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_UINT8(DLR_VARIANT variant,   const uint8_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT8.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT8.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_INT16(DLR_VARIANT variant,   const int16_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT16.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_int16), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT16.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_UINT16(DLR_VARIANT variant,  const uint16_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT16.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_uint16), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT16.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_INT32(DLR_VARIANT variant,   const int32_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT32.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT32.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_UINT32(DLR_VARIANT variant,  const uint32_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT32.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT32.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_INT64(DLR_VARIANT variant,   const int64_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT64.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_INT64.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_UINT64(DLR_VARIANT variant,  const uint64_t* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT64.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_UINT64.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_FLOAT32(DLR_VARIANT variant, const float* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_FLOAT32.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_float), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_FLOAT32.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_FLOAT64(DLR_VARIANT variant, const double* value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_FLOAT64.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_FLOAT64.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_STRING(DLR_VARIANT variant,  const char** value, const size_t count);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_STRING.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_STRING.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetFlatbuffers(DLR_VARIANT variant, const int8_t* value, const size_t size);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFlatbuffers.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_int8), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetFlatbuffers.restype = C_DLR_RESULT

# bool     DLR_variantGetBOOL8(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetBOOL8.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetBOOL8.restype = ctypes.c_bool

# int8_t   DLR_variantGetINT8(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT8.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT8.restype = ctypes.c_int8

# uint8_t  DLR_variantGetUINT8(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT8.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT8.restype = ctypes.c_uint8

# int16_t  DLR_variantGetINT16(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT16.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT16.restype = ctypes.c_int16

# uint16_t DLR_variantGetUINT16(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT16.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT16.restype = ctypes.c_uint16

# int32_t  DLR_variantGetINT32(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT32.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT32.restype = ctypes.c_int32

# uint32_t DLR_variantGetUINT32(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT32.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT32.restype = ctypes.c_uint32

# int64_t  DLR_variantGetINT64(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT64.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetINT64.restype = ctypes.c_int64

# uint64_t DLR_variantGetUINT64(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT64.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetUINT64.restype = ctypes.c_uint64

# float    DLR_variantGetFLOAT32(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetFLOAT32.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetFLOAT32.restype = ctypes.c_float

# double   DLR_variantGetFLOAT64(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetFLOAT64.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetFLOAT64.restype = ctypes.c_double

# const char* DLR_variantGetSTRING(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetSTRING.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetSTRING.restype = ctypes.c_char_p

#  const bool*      DLR_variantGetArrayOfBOOL8(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfBOOL8.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfBOOL8.restype = ctypes.POINTER(
    ctypes.c_bool)

#  const int8_t*    DLR_variantGetArrayOfINT8(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT8.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT8.restype = ctypes.POINTER(
    ctypes.c_int8)

#  const uint8_t*   DLR_variantGetArrayOfUINT8(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT8.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT8.restype = ctypes.POINTER(
    ctypes.c_uint8)

#  const int16_t*   DLR_variantGetArrayOfINT16(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT16.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT16.restype = ctypes.POINTER(
    ctypes.c_int16)

#  const uint16_t*  DLR_variantGetArrayOfUINT16(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT16.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT16.restype = ctypes.POINTER(
    ctypes.c_uint16)

#  const int32_t*   DLR_variantGetArrayOfINT32(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT32.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT32.restype = ctypes.POINTER(
    ctypes.c_int32)

#  const uint32_t*  DLR_variantGetArrayOfUINT32(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT32.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT32.restype = ctypes.POINTER(
    ctypes.c_uint32)

#  const int64_t*   DLR_variantGetArrayOfINT64(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT64.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfINT64.restype = ctypes.POINTER(
    ctypes.c_int64)

#  const uint64_t*  DLR_variantGetArrayOfUINT64(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT64.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfUINT64.restype = ctypes.POINTER(
    ctypes.c_uint64)

#  const float*     DLR_variantGetArrayOfFLOAT32(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfFLOAT32.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfFLOAT32.restype = ctypes.POINTER(
    ctypes.c_float)

#  const double*    DLR_variantGetArrayOfFLOAT64(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfFLOAT64.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfFLOAT64.restype = ctypes.POINTER(
    ctypes.c_double)

#  const char**     DLR_variantGetArrayOfSTRING(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfSTRING.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetArrayOfSTRING.restype = ctypes.POINTER(
    ctypes.c_char_p)

# DLR_VARIANT_TYPE DLR_variantGetType(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetType.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetType.restype = C_DLR_VARIANT_TYPE

#  uint8_t* DLR_variantGetData(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetData.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetData.restype = ctypes.POINTER(
    ctypes.c_byte)

#  size_t DLR_variantGetSize(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetSize.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetSize.restype = ctypes.c_size_t

#  size_t DLR_variantGetCount(DLR_VARIANT variant);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount.argtypes = (
    C_DLR_VARIANT,)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantGetCount.restype = ctypes.c_size_t

#  DLR_RESULT DLR_variantCheckConvert(DLR_VARIANT variant, DLR_VARIANT_TYPE type);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCheckConvert.argtypes = (
    C_DLR_VARIANT, C_DLR_VARIANT_TYPE)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCheckConvert.restype = C_DLR_RESULT

#  DLR_RESULT DLR_variantCopy(DLR_VARIANT dest, DLR_VARIANT src);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCopy.argtypes = (
    C_DLR_VARIANT, C_DLR_VARIANT)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantCopy.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetTimestamp(DLR_VARIANT variant,  const uint64_t value);
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetTimestamp.argtypes = (
    C_DLR_VARIANT, ctypes.c_uint64)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetTimestamp.restype = C_DLR_RESULT

# DLR_RESULT DLR_variantSetARRAY_OF_TIMESTAMP(DLR_VARIANT variant, const uint64_t* value, const size_t count)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_TIMESTAMP.argtypes = (
    C_DLR_VARIANT, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t)
ctrlxdatalayer.clib.libcomm_datalayer.DLR_variantSetARRAY_OF_TIMESTAMP.restype = C_DLR_RESULT
