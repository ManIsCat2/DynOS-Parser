import os
import struct
import zlib
from Dynos import BinFile

DYNOS_BIN_COMPRESS_MAGIC = 0x4E4942534F4E5944  # Equivalent to 0x4E4942534F4E5944llu

def DynosCompressedCondition(condition, function, filename, message):
    if not condition:
        print(f"ERROR: {function}: File \"{filename}\": {message}")
        return False
    return True

def DynosFileCompressed(filename):
    with open(filename, "rb") as f:
        magic = struct.unpack('<Q', f.read(8))[0]  # Read the magic number
        return magic == DYNOS_BIN_COMPRESS_MAGIC

def DynosDecompressBin(filename):
    uncompressed_filename = "Dump/uncompressed.bin"

    with open(filename, "rb") as f:
        # Read the magic number
        magic = struct.unpack('<Q', f.read(8))[0]
        if magic != DYNOS_BIN_COMPRESS_MAGIC:
            print("Not a compressed file. Returning original file.")
            return BinFile().OpenR(filename)  # Return original filename if not compressed

        print(f"Decompressing file \"{filename}\"...")

        length_uncompressed = struct.unpack('<Q', f.read(8))[0]

        compressed_data = f.read()

        # decompress the data
        uncompressed_data = zlib.decompress(compressed_data)

        if len(uncompressed_data) != length_uncompressed:
            print("ERROR: Decompressed data size does not match expected size.")
            return None
        with open(uncompressed_filename, "wb") as out_file:
            out_file.write(uncompressed_data)

    print(f"Uncompressed data written to \"{uncompressed_filename}\".")
    return BinFile().OpenR(uncompressed_filename)