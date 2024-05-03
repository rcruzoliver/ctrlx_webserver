import ctypes
import os.path
import platform

# check architecture
arch = platform.machine()
print("System architecture: ", arch)

# load libraries
ctypes.CDLL("libsystemd.so.0", mode=ctypes.RTLD_GLOBAL)
ctypes.CDLL("libzmq.so.5", mode=ctypes.RTLD_GLOBAL)

libcomm_datalayer = None
libcomm_datalayer = ctypes.CDLL("libcomm_datalayer.so")
# typedef enum DLR_RESULT
C_DLR_RESULT = ctypes.c_int32

# typedef void *DLR_CONVERTER;
C_DLR_CONVERTER = ctypes.c_void_p

userData_c_void_p = ctypes.c_void_p
address_c_char_p = ctypes.c_char_p
