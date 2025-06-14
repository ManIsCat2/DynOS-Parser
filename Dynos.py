# dynos.py

import struct

FUNCTION_CODE = 0x434E5546
POINTER_CODE = 0x52544E50
LUA_VAR_CODE = 0x5641554C
TEX_REF_CODE = 0x52584554

F32VTX_SENTINEL_0 = 0x3346
F32VTX_SENTINEL_1 = 0x5632
F32VTX_SENTINEL_2 = 0x5854

# Define the data types
DATA_TYPE_NONE = 0
DATA_TYPE_LIGHT = 1
DATA_TYPE_TEXTURE=2
DATA_TYPE_VERTEX=3
DATA_TYPE_DISPLAY_LIST=4
DATA_TYPE_GEO_LAYOUT=5
DATA_TYPE_ANIMATION_VALUE=6
DATA_TYPE_ANIMATION_INDEX=7
DATA_TYPE_ANIMATION=8
DATA_TYPE_ANIMATION_TABLE=9
DATA_TYPE_GFXDYNCMD=10
DATA_TYPE_COLLISION=11
DATA_TYPE_LEVEL_SCRIPT=12
DATA_TYPE_MACRO_OBJECT=13
DATA_TYPE_TRAJECTORY=14
DATA_TYPE_MOVTEX=15
DATA_TYPE_MOVTEXQC=16
DATA_TYPE_ROOMS=17
DATA_TYPE_LIGHT_T=18
DATA_TYPE_AMBIENT_T=19
DATA_TYPE_TEXTURE_LIST=20
DATA_TYPE_TEXTURE_RAW=21
DATA_TYPE_BEHAVIOR_SCRIPT=22
DATA_TYPE_UNUSED=23
DATA_TYPE_LIGHT_0=24

class BinFile:
    def __init__(self, file=None, filename="", ro=True):
        self.mOffset = 0
        self.mFile = file
        self.mFileName = filename
        self.mReadOnly = ro
        self.mData = None
        self.mSize = 0

    def Offset(self):
        return self.mOffset

    def SetOffset(self, offset):
        self.mOffset = offset

    def OpenR(self, name):
        self.mFile = open(name, "rb")
        self.mFileName = name
        self.mReadOnly = True
        self.mFile.seek(0, 2)  # Move to end of file
        self.mSize = self.mFile.tell()
        self.mFile.seek(0)  # Reset to start
        self.mData = self.mFile.read(self.mSize)
        self.mOffset = 0
        return self

    def Read(self, size):
        self.mFile.seek(self.mOffset)
        result = self.mFile.read(size)
        self.mOffset += size
        return result
    def ReadFloat(self):
        float_bytes = self.Read(4)
        return struct.unpack('<f', float_bytes)[0]
    def ReadInt16(self):
        int16_bytes = self.Read(2)
        return struct.unpack('<h', int16_bytes)[0]
    def ReadInt8(self):
        byte_value = self.Read(1)
        return int.from_bytes(byte_value, 'little')

    def Skip(self, amount):
        self.mOffset += amount

class String:
    def __init__(self, buffer=""):
        self.buffer = buffer

    def Read(self, binfile: BinFile):
        sizeofname = int.from_bytes(binfile.Read(1), 'little')
        self.buffer = binfile.Read(sizeofname).decode()

    def begin(self):
        return self.buffer