from Dynos import BinFile, String
import Dynos
import os
import shutil
import DynosCompress
import Gbi
from Gbi import C0, C1, NC0, NC1, DecodeColorCombiner, DecodeAlphaCombiner, color_comb_rgb, color_comb_alpha

dump_dir = "Dump"

def DoCombineMode(rgb1, alpha1, rgb2, alpha2, gfxFile):
        print("    gsDPSetCombineLERP(", 
            DecodeColorCombiner(CAST_U8(rgb1), 0), ", ", DecodeColorCombiner(CAST_U8(rgb1 >> 8), 0), ", ",DecodeColorCombiner(CAST_U8(rgb1 >> 16), 0),", ", DecodeColorCombiner(CAST_U8(rgb1 >> 24), 0),", ",
            DecodeAlphaCombiner(CAST_U8(alpha1), 0),", ", DecodeAlphaCombiner(CAST_U8(alpha1 >> 8), 0), ", ",DecodeAlphaCombiner(CAST_U8(alpha1 >> 16), 0), ", ",DecodeAlphaCombiner(CAST_U8(alpha1 >> 24), 0),", ",
            DecodeColorCombiner(CAST_U8(rgb2), 1),", ", DecodeColorCombiner(CAST_U8(rgb2 >> 8), 1),", ", DecodeColorCombiner(CAST_U8(rgb2 >> 16), 1), ", ",DecodeColorCombiner(CAST_U8(rgb2 >> 24), 1),", ",
            DecodeAlphaCombiner(CAST_U8(alpha2), 1),", ", DecodeAlphaCombiner(CAST_U8(alpha2 >> 8), 1), ", ",DecodeAlphaCombiner(CAST_U8(alpha2 >> 16), 1),", ", DecodeAlphaCombiner(CAST_U8(alpha2 >> 24), 1),
            "),"
        ,file=gfxFile,
        sep=""
        )



def CAST_U8(s):
    return s&0xff

def ReadName(binfile: BinFile) -> String:
    name = String()
    name.Read(binfile)
    return name

def ReadBytes(binfile:BinFile, bytes:int):
    return int.from_bytes(binfile.Read(bytes), 'little')

def ReadPNG(binfile: BinFile, name: String):
    sizeofpng = ReadBytes(binfile, 4)

    if sizeofpng > 0:
        pngData = binfile.Read(sizeofpng)
        with open(os.path.join(dump_dir, name.begin() + ".png"), "wb") as pngTexture:
            pngTexture.write(pngData)
        print("PNG data written to:", os.path.join(dump_dir, name.begin() + ".png"))
    else:
        print("No PNG data found for texture:", name.begin())

def ParseLights1(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    light = binfile.Read(24)
    
    output = (
        f"Lights1 {name.begin()} = gdSPDefLights1(\n"
        f"   0x{light[0]:x}, 0x{light[1]:x}, 0x{light[2]:x},\n"
        f"   0x{light[12]:x}, 0x{light[13]:x}, 0x{light[14]:x},"
        f" 0x{light[16]:x}, 0x{light[17]:x}, 0x{light[18]:x},\n"
        ");\n"
    )
    print(output, file=gfxFile)
    print("Light Found:", name.begin())

def ParseLight0(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    print("Light 0 Found:", name.begin())

def ParseLightT(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    print("Light T Found:", name.begin())

def ParseAmbientT(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    print("Ambient T Found:", name.begin())

def ParseTexture(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    output = (
        f"u8 {name.begin()}[] = "
        "{\n"
        f"#include \"actors/Dump/{name.begin()}.inc.c\"\n"
        "};\n"
        
    )
    print(output, file=gfxFile)
    print("Texture Found:", name.begin())
    ReadPNG(binfile, name)
    
def IsUsingF32Vtx(ob):
    return ob[0] == Dynos.F32VTX_SENTINEL_0 and ob[1] == Dynos.F32VTX_SENTINEL_1 and ob[2] == Dynos.F32VTX_SENTINEL_2

def ParseVertex(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    isUsingF32Vtx = False
    vtxSize = ReadBytes(binfile, 4)
    
    print(f"static const Vtx {name.begin()}[{vtxSize}] = " "{", file=gfxFile)
    
    for i in range(vtxSize):
        pos = [0, 0, 0]
        if isUsingF32Vtx:
            pos[0] = binfile.ReadFloat()
            pos[1] = binfile.ReadFloat()
            pos[2] = binfile.ReadFloat()
        else:
            pos[0] = binfile.ReadInt16()
            pos[1] = binfile.ReadInt16()
            pos[2] = binfile.ReadInt16()

        flag = binfile.ReadInt16()
        texcoord = [binfile.ReadInt16(), binfile.ReadInt16()]
        normals = [binfile.ReadInt8(), binfile.ReadInt8(), binfile.ReadInt8()]
        alpha = ReadBytes(binfile, 1)
        
        print("    {{{p1, p2, p3}, fl, {t1, t2}, {n1, n2, n3, n4}}},".
                replace("p1", str(pos[0])).
                replace("p2", str(pos[1])).
                replace("p3", str(pos[2])).
                replace("fl", str(flag)).
                replace("t1", str(texcoord[0])).
                replace("t2", str(texcoord[1])).
                replace("n1", str(normals[0])).
                replace("n2", str(normals[1])).
                replace("n3", str(normals[2])).
                replace("n4", str(alpha))
              , file=gfxFile
              )
        
        if (not isUsingF32Vtx and i == 0 and IsUsingF32Vtx(pos)):
            vtxSize-=1 
            i-=1
            isUsingF32Vtx = True
    print("};\n", file=gfxFile)
    print("Vertex Found:", name.begin())

def ParseDisplayList(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    gfxSize = ReadBytes(binfile, 4)
    ptrname=None
    print(f"Gfx {name.begin()}[] = " "{", file=gfxFile)
    for _ in range(gfxSize):
        words0 = ReadBytes(binfile, 4)
        words1 = ReadBytes(binfile, 4)
        if words1 == Dynos.POINTER_CODE: 
            ptrname = ReadName(binfile)
            words1 = ptrdata = ReadBytes(binfile, 4)
        opcode:int = words0>>24
        if opcode == Gbi.G_RDPPIPESYNC:
            print("    gsDPPipeSync(),", file=gfxFile)
        elif opcode == Gbi.G_RDPLOADSYNC:
            print("    gsDPLoadSync(),", file=gfxFile)
        elif opcode == Gbi.G_RDPTILESYNC:
            print("    gsDPTileSync(),", file=gfxFile)
        elif opcode == Gbi.G_SETCOMBINE:
           DoCombineMode(
                color_comb_rgb  (NC0(words0,20, 4), NC1(words1,28, 4), NC0(words0,15, 5), NC1(words1,15, 3), 0),
                color_comb_alpha(NC0(words0,12, 3), NC1(words1,12, 3), NC0(words0,9, 3),  NC1(words1,9, 3),  0),
                color_comb_rgb  (NC0(words0,5, 4),  NC1(words1,24, 4), NC0(words0,0, 5),  NC1(words1,6, 3),  1),
                color_comb_alpha(NC1(words1,21, 3), NC1(words1,3, 3),  NC1(words1,18, 3), NC1(words1,0, 3),  1),
                gfxFile
            )
        elif opcode == Gbi.G_TEXTURE:
            print(f"    gsSPTexture({C1(words1, 16, 16)}, {C1(words1, 0, 16)}, {C0(words0, 11, 3)}, {C0(words0, 8, 3)}, {C0(words0, 1, 7)}),", file=gfxFile)
        elif opcode == Gbi.G_TRI2:
            print(f"    gsSP2Triangles({str(NC0(words0, 16, 8) // 2)}, {str(NC0(words0, 8, 8) // 2)}, {str(NC0(words0, 0, 8) // 2)}, 0, {str(NC1(words1, 16, 8) // 2)}, {str(NC1(words1, 8, 8) // 2)}, {str(NC1(words1, 0, 8) // 2)}),", file=gfxFile)
        elif opcode == Gbi.G_TRI1:
            print(f"    gsSP1Triangle({str(NC0(words0, 16, 8) // 2)}, {str(NC0(words0, 8, 8) // 2)}, {str(NC0(words0, 0, 8) // 2)}, 0),", file=gfxFile)
        elif opcode == Gbi.G_LOADBLOCK:
            print(f"    gsDPLoadBlock({C1(words1, 24, 3)}, {C0(words0, 12, 12)}, {C0(words0, 0, 12)}, {C1(words1, 12, 12)}, {C1(words1, 0, 12)}),", file=gfxFile)
        elif opcode == Gbi.G_LOADTILE:
            print(f"    gsDPLoadTile({C1(words1, 24, 3)}, {C0(words0, 12, 12)}, {C0(words0, 0, 12)}, {C1(words1, 12, 12)}, {C1(words1, 0, 12)}),", file=gfxFile)
        elif opcode == Gbi.G_SETTILE:
            print(f"    gsDPSetTile({C0(words0, 21, 3)}, {C0(words0, 19, 2)}, {C0(words0, 9, 9)}, {C0(words0, 0, 9)}, {C1(words1, 24, 3)}, {C1(words1, 20, 4)}, {C1(words1, 18, 2)}, {C1(words1, 14, 4)}, {C1(words1, 10, 4)}, {C1(words1, 8, 2)}, {C1(words1, 4, 4)}, {C1(words1, 0, 4)}),", file=gfxFile)
        elif opcode == Gbi.G_SETTILESIZE:
            print(f"    gsDPSetTileSize({C1(words1, 24, 3)}, {C0(words0, 12, 12)}, {C0(words0, 0, 12)}, {C1(words1, 12, 12)}, {C1(words1, 0, 12)}),", file=gfxFile)
        elif opcode == Gbi.G_LOADTLUT:
            print(f"    gsDPLoadTLUTCmd({C1(words1, 24, 3)}, {C1(words1, 14, 10)}),", file=gfxFile)
        elif opcode == Gbi.G_SETTIMG:
            print(f"    gsDPSetTextureImage({C0(words0, 21, 3)}, {C0(words0, 19, 2)}, 1, {ptrname.begin()}),", file=gfxFile)
        elif opcode == Gbi.G_SETENVCOLOR:
            print(f"    gsDPSetEnvColor({C1(words1, 24, 8)}, {C1(words1, 16, 8)}, {C1(words1, 8, 8)}, {C1(words1, 0, 8)}),", file=gfxFile)
        elif opcode == Gbi.G_SETPRIMCOLOR:
            print(f"    gsDPSetPrimColor(0, 0, {C1(words1, 24, 8)}, {C1(words1, 16, 8)}, {C1(words1, 8, 8)}, {C1(words1, 0, 8)}),", file=gfxFile)
        elif opcode == Gbi.G_GEOMETRYMODE:
            print(f"    gsSPGeometryMode({str(((~NC0(words0, 0, 24))& 0xFFFFFFFF) &~ 4278190080)}, {str(words1)})", file=gfxFile)   
            
    print("};\n", file=gfxFile)
    print("DisplayList Found:", name.begin())
    if ptrname:
        print("DisplayList ptr Found:",ptrname.begin())

def ParseGeoLayout(binfile: BinFile, gfxFile):
    name = ReadName(binfile)
    geoSize = ReadBytes(binfile, 4)
    
    for _ in range(geoSize):
        value = ReadBytes(binfile, 4)
        if value == Dynos.FUNCTION_CODE: 
            funcindex = ReadBytes(binfile, 4)
        elif value == Dynos.POINTER_CODE: 
            ptrname = ReadName(binfile)
            ptrdata = ReadBytes(binfile, 4)
    print("GeoLayout Found:", name.begin())

def ParseAnimation(binfile: BinFile):
    print("Animation data parsed.")

def ParseGfxDynCmd(binfile: BinFile):
    print("Graphics Dynamic Command data parsed.")

def ParseTextureBinary(binfile: BinFile):
    binfile.Read(1)

    name = ReadName(binfile)
    print("Texture Found:", name.begin())
    ReadPNG(binfile, name)

def ParseActorBinary(binfile: BinFile, gfxFile):
    _binfile = DynosCompress.DynosDecompressBin(binfile.mFileName)
    parse_functions = {
        Dynos.DATA_TYPE_LIGHT: ParseLights1,
        Dynos.DATA_TYPE_LIGHT_0: ParseLight0,
        Dynos.DATA_TYPE_LIGHT_T: ParseLightT,
        Dynos.DATA_TYPE_AMBIENT_T: ParseAmbientT,
        Dynos.DATA_TYPE_TEXTURE: ParseTexture,
        Dynos.DATA_TYPE_VERTEX: ParseVertex,
        Dynos.DATA_TYPE_DISPLAY_LIST: ParseDisplayList,
        Dynos.DATA_TYPE_GEO_LAYOUT: ParseGeoLayout,
        Dynos.DATA_TYPE_ANIMATION: ParseAnimation,
        Dynos.DATA_TYPE_GFXDYNCMD: ParseGfxDynCmd,
    }

    while True:
        dataType = ReadBytes(_binfile, 1)
        
        if dataType in parse_functions:
            parse_functions[dataType](_binfile, gfxFile)
        else:
            break