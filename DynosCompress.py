import os
import struct
import zlib
from Dynos import BinFile

DYNOS_BIN_COMPRESS_MAGIC = 0x4E4942534F4E5944

def DynosFileCompressed(f):
    magic = struct.unpack('<Q', f.read(8))[0]
    return magic == DYNOS_BIN_COMPRESS_MAGIC

def DynosDecompressBin(filename):
    uncompressed_filename = "Data/uncompressed.bin"

    with open(filename, "rb") as f:
        if not DynosFileCompressed(f):
            print("Not a compressed file. Returning original file.")
            return BinFile().OpenR(filename)  # return original filename if not compressed

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