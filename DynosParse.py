from Dynos import BinFile, String, ReadName, ReadBytes, DynosPointerRead
import Dynos
import os
import shutil
import DynosCompress
import Gbi
from Gbi import C0, C1, NC0, NC1, DecodeColorCombiner, DecodeAlphaCombiner, color_comb_rgb, color_comb_alpha

dump_dir = "Dump"

def CAST_S16(value):
    value = int(value)
    value = value & 0xFFFF
    if value > 32767:
        value -= 65536
    return value

def CAST_U8(s):
    return s&0xff

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

def ReadPNG(binfile: BinFile, name: String, extract:bool, gfxFile=None, actor=False):
    sizeofpng = ReadBytes(binfile, 4)
    if extract:
        if actor:
            output = (
            f"u8 {name.begin()}[] = "
            "{"
            )
            print(output, file=gfxFile)
    if sizeofpng > 0:
        if extract:
            pngData = binfile.Read(sizeofpng)
            with open(os.path.join(dump_dir, name.begin() + ".png"), "wb") as pngTexture:
                pngTexture.write(pngData)
                print("PNG data written to:", os.path.join(dump_dir, name.begin() + ".png"))
            if actor:
                print(f"    #include \"actors/Dump/{name.begin()}.inc.c\"", file=gfxFile)
    else:
        print("No PNG data found for texture:", name.begin())
        if actor and extract:
            print(f"    0", file=gfxFile)
    if extract:
        if actor:
            print("};\n", file=gfxFile)

def ParseLights1(binfile: BinFile, gfxFile, extract):
    name = ReadName(binfile)
    light = binfile.Read(24)
    if extract:
        output = (
            f"Lights1 {name.begin()} = gdSPDefLights1(\n"
            f"   0x{light[0]:x}, 0x{light[1]:x}, 0x{light[2]:x},\n"
            f"   0x{light[12]:x}, 0x{light[13]:x}, 0x{light[14]:x},"
            f" 0x{light[16]:x}, 0x{light[17]:x}, 0x{light[18]:x},\n"
            ");\n"
        )
        print(output, file=gfxFile)
    print("Light Found:", name.begin())

def ParseLight0(binfile: BinFile, gfxFile, extract):
    name = ReadName(binfile)
    print("Light 0 Found:", name.begin())

def ParseLightT(binfile: BinFile, gfxFile, extract):
    name = ReadName(binfile)
    print("Light T Found:", name.begin())

def ParseAmbientT(binfile: BinFile, gfxFile, extract):
    name = ReadName(binfile)
    print("Ambient T Found:", name.begin())

def ParseTexture(binfile: BinFile, gfxFile, extract):
    name = ReadName(binfile)
    print("Texture Found:", name.begin())
    ReadPNG(binfile, name, extract, gfxFile=gfxFile, actor=True)
    
def IsUsingF32Vtx(ob):
    return ob[0] == Dynos.F32VTX_SENTINEL_0 and ob[1] == Dynos.F32VTX_SENTINEL_1 and ob[2] == Dynos.F32VTX_SENTINEL_2

def ParseVertex(binfile: BinFile, gfxFile, extract):
    name = ReadName(binfile)
    isUsingF32Vtx = False
    vtxSize = ReadBytes(binfile, 4)
    if extract:
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
        
        if extract:
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
    if extract:
        print("};\n", file=gfxFile)
    print("Vertex Found:", name.begin())

def ParseDisplayList(binfile: BinFile, gfxFile, extract):
    name = ReadName(binfile)
    gfxSize = ReadBytes(binfile, 4)
    ptrname=None
    vertexSize=0
    if extract:
        print(f"Gfx {name.begin()}[] = " "{", file=gfxFile)

    for _ in range(gfxSize):
        words0 = ReadBytes(binfile, 4)
        words1 = ReadBytes(binfile, 4)
        if words1 == Dynos.POINTER_CODE: 
            ptrname = ReadName(binfile)
            words1 = ptrdata = ReadBytes(binfile, 4)
        if extract:
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
                print(f"    gsSP2Triangles({str(NC0(words0, 16, 8) // 2)}, {str(NC0(words0, 8, 8) // 2)}, {str(NC0(words0, 0, 8) // 2)}, 0, {str(NC1(words1, 16, 8) // 2)}, {str(NC1(words1, 8, 8) // 2)}, {str(NC1(words1, 0, 8) // 2)}, 0),", file=gfxFile)
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
            elif opcode == Gbi.G_DL:
                if NC0(words0, 16, 1) == 0:
                    print(f"    gsSPDisplayList({ptrname.begin()}),", file=gfxFile)
                else:
                    print(f"    gsSPBranchList({ptrname.begin()}),", file=gfxFile)
                    vertexSize=0
            elif opcode == Gbi.G_ENDDL:
                print("    gsSPEndDisplayList(),", file=gfxFile)
                vertexSize=0
            elif opcode == Gbi.G_VTX:
                print(f"    gsSPVertex({ptrname.begin()} + {str(vertexSize)}, {C0(words0, 12, 8)}, {str(NC0(words0, 1, 7) - NC0(words0, 12, 8))}),", file=gfxFile)
                vertexSize+=NC0(words0, 12, 8)
            elif opcode == Gbi.G_MOVEMEM:
                mvlength = int(NC0(words0, 8, 8) * 8 / 24 - 1)
                if NC0(words0, 0, 8) == 10:
                    if mvlength == 1:
                        print(f"    gsSPLight(&{ptrname.begin()}.l, {mvlength}),", file=gfxFile)
                    elif mvlength == 2:
                        print(f"    gsSPLight(&{ptrname.begin()}.a, {mvlength}),", file=gfxFile)
            elif opcode == Gbi.G_COPYMEM:
                mvlength = int(NC0(words0, 8, 8) * 8 / 24 - 1)
                if NC0(words0, 0, 8) == 10:
                    print(f"    gsSPCopyLightEXT({int(NC0(words0,8, 8) * 8 / 24 - 1)}, {int(NC0(words0,16, 8) * 8 / 24 - 1)}),", file=gfxFile)
    if extract:
        print("};\n", file=gfxFile)
    print("DisplayList Found:", name.begin())
    if ptrname:
        print("DisplayList ptr Found:",ptrname.begin())

def ParseGeoLayout(binfile: BinFile, gfxFile, extract, geoFile):
    name = ReadName(binfile)
    geoSize = ReadBytes(binfile, 4)
    ptrname=None
    if extract:
        print(f"const GeoLayout {name.begin()}[] = " "{", file=geoFile)
    
    for _ in range(geoSize):
        value = ReadBytes(binfile, 4)
        ptrname = DynosPointerRead(value, binfile)
        if extract:
            fileoffset = binfile.Offset()
            geoOp = CAST_U8(value)
            
            valueSH8 = value >> 8
            valueSH16 = value >> 16
            valueAsU8 = value & 0XFF
            
            if geoOp == 0x01:
                print("    GEO_END(),", file=geoFile)
            elif geoOp == 0x0b:
                print("    GEO_NODE_START(),", file=geoFile)
            elif geoOp == 0x03:
                print("    GEO_RETURN(),", file=geoFile)
            elif geoOp == 0x04:
                print("    GEO_OPEN_NODE(),", file=geoFile)
            elif geoOp == 0x05:
                print("    GEO_CLOSE_NODE(),", file=geoFile)
            elif geoOp == 0x15:
                value = ReadBytes(binfile, 4)
                ptrname = DynosPointerRead(value, binfile, True)
                if ptrname=="NULL":
                    pass
                else:
                    print(f"    GEO_DISPLAY_LIST({valueSH8}, ",file=geoFile, end="")
                    print(f"{ptrname.begin()}),",file=geoFile)
                binfile.SetOffset(fileoffset)
            elif geoOp == 0x16:
                print(f"    GEO_SHADOW({valueSH16}, ",file=geoFile, end="")
                value = ReadBytes(binfile, 4)
                print(f"{CAST_U8(value)}, {value>>16}),",file=geoFile)
                binfile.SetOffset(fileoffset)
            elif geoOp == 0x1d:
                if (valueSH8 & 0xff) & 0x80 != 0: 
                    print(f"    GEO_SCALE_WITH_DL({CAST_U8(valueSH8&~0x80)}, ",file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    print(f"{value}, ",file=geoFile)
                    value = ReadBytes(binfile, 4)
                    ptrname = DynosPointerRead(value, binfile)
                    print(f"{ptrname.begin()}),",file=geoFile)
                    binfile.SetOffset(fileoffset)
                else:
                    print(f"    GEO_SCALE({CAST_U8(valueSH8)}, ",file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    print(f"{value}),",file=geoFile)
                    binfile.SetOffset(fileoffset)
            elif geoOp == 0x20:
                print(f"    GEO_CULLING_RADIUS({valueSH16}),", file=geoFile)
            elif geoOp == 0x02:
                print(f"    GEO_BRANCH({valueSH8}, ",file=geoFile, end="")
                value = ReadBytes(binfile, 4)
                ptrname = DynosPointerRead(value, binfile)
                print(f"{ptrname.begin()}),",file=geoFile)
                binfile.SetOffset(fileoffset)
            elif geoOp == 0x13:
                print(f"    GEO_ANIMATED_PART({CAST_U8(valueSH8)}, {CAST_S16(valueSH16)}, ", file=geoFile, end="")
                value = ReadBytes(binfile, 4)
                print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile, end="")
                value = ReadBytes(binfile, 4)
                ptrname = DynosPointerRead(value, binfile, True)
                if ptrname=="NULL":
                    print(f"{ptrname}),",file=geoFile)
                else:
                    print(f"{ptrname.begin()}),",file=geoFile)
                binfile.SetOffset(fileoffset)
            elif geoOp == 0x12:
                if (CAST_U8(valueSH8)) &0x80 != 0:
                    print(f"    GEO_ROTATION_NODE_WITH_DL({CAST_U8(valueSH8)&~0x80}, {CAST_S16(valueSH16)}, ", file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    ptrname = DynosPointerRead(value, binfile, True)
                    if ptrname=="NULL":
                        print(f"{ptrname}),",file=geoFile)
                    else:
                        print(f"{ptrname.begin()}),",file=geoFile)
                    binfile.SetOffset(fileoffset)
                else:
                    print(f"    GEO_ROTATION_NODE({CAST_U8(valueSH8)}, {CAST_S16(valueSH16)}, ", file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}),", file=geoFile)
                    binfile.SetOffset(fileoffset)
            elif geoOp == 0x10:
                isTrans = CAST_U8(valueSH8) & 0x10 != 0
                isRot = CAST_U8(valueSH8) & 0x20 != 0
                isRotY = CAST_U8(valueSH8) & 0x30 != 0
                isDL = CAST_U8(valueSH8) & 0x80 != 0
                if (not isTrans and not isRot and not isRotY):
                    if not isDL:
                        print(f"    GEO_TRANSLATE_ROTATE({CAST_U8(valueSH8)}, ", file=geoFile,end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile,end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile,end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}),", file=geoFile)
                        binfile.SetOffset(fileoffset)
                    else:
                        print(f"    GEO_TRANSLATE_ROTATE_WITH_DL({(CAST_U8(valueSH8)&~0x80)}, ", file=geoFile,end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile,end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile,end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile,end="")
                        value = ReadBytes(binfile, 4)
                        ptrname = DynosPointerRead(value, binfile, True)
                        if ptrname=="NULL":
                            print(f"{ptrname}),",file=geoFile)
                        else:
                            print(f"{ptrname.begin()}),",file=geoFile)
                        binfile.SetOffset(fileoffset)
                if (isTrans):
                    if not isDL:
                        print(f"    GEO_TRANSLATE({CAST_U8(valueSH8)&~0x10}, {CAST_S16(valueSH16)}, ", end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}),")
                        binfile.SetOffset(fileoffset)
                    else:
                        print(f"    GEO_TRANSLATE({(CAST_U8(valueSH8)&~0x10)&~0x80}, {CAST_S16(valueSH16)}, ", end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ",end="")
                        value = ReadBytes(binfile, 4)
                        ptrname = DynosPointerRead(value, binfile, True)
                        if ptrname=="NULL":
                            print(f"{ptrname}),",file=geoFile)
                        else:
                            print(f"{ptrname.begin()}),",file=geoFile)
                        binfile.SetOffset(fileoffset)
                elif (isRot):
                    if not isDL:
                        print(f"    GEO_ROTATE({CAST_U8(valueSH8)&~0x20}, {CAST_S16(valueSH16)}, ", end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}),")
                        binfile.SetOffset(fileoffset)
                    else:
                        print(f"    GEO_ROTATE({(CAST_U8(valueSH8)&~0x20)&~0x80}, {CAST_S16(valueSH16)}, ", end="")
                        value = ReadBytes(binfile, 4)
                        print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ",end="")
                        value = ReadBytes(binfile, 4)
                        ptrname = DynosPointerRead(value, binfile, True)
                        if ptrname=="NULL":
                            print(f"{ptrname}),",file=geoFile)
                        else:
                            print(f"{ptrname.begin()}),",file=geoFile)
                        binfile.SetOffset(fileoffset)
                elif (isRotY):
                    if not isDL:
                        print(f"    GEO_ROTATE_Y({CAST_U8(valueSH8)&~0x30}, {CAST_S16(valueSH16)}),")
                        binfile.SetOffset(fileoffset)
                    else:
                        print(f"    GEO_ROTATE_Y({(CAST_U8(valueSH8)&~0x30)&~0x80}, {CAST_S16(valueSH16)}, ", end="")
                        value = ReadBytes(binfile, 4)
                        ptrname = DynosPointerRead(value, binfile, True)
                        if ptrname=="NULL":
                            print(f"{ptrname}),",file=geoFile)
                        else:
                            print(f"{ptrname.begin()}),",file=geoFile)
                        binfile.SetOffset(fileoffset)
            elif geoOp == 0x11:
                isDL = CAST_U8(valueSH8) & 0x80 != 0
                if isDL:
                    print(f"    GEO_TRANSLATE_NODE({CAST_U8(valueSH8)&~0x80}, {CAST_S16(valueSH16)}, ", file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}, ", file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    ptrname = DynosPointerRead(value, binfile, True)
                    if ptrname=="NULL":
                        print(f"{ptrname}),",file=geoFile)
                    else:
                        print(f"{ptrname.begin()}),",file=geoFile)
                    binfile.SetOffset(fileoffset)
                else:
                    print(f"    GEO_TRANSLATE_NODE({CAST_U8(valueSH8)}, {CAST_S16(valueSH16)}, ", file=geoFile, end="")
                    value = ReadBytes(binfile, 4)
                    print(f"{CAST_S16(value)}, {CAST_S16(value>>16)}),", file=geoFile)
            elif geoOp == 0x18:
                print(f"    GEO_ASM({CAST_S16(valueSH16)}, ", file=geoFile, end="")
                value = ReadBytes(binfile, 4)
                ptrname = DynosPointerRead(value, binfile)
                print(f"{ptrname}),",file=geoFile)
                binfile.SetOffset(fileoffset)
            elif geoOp == 0x0e:
                print(f"    GEO_SWITCH_CASE({CAST_S16(valueSH16)}, ", file=geoFile, end="")
                value = ReadBytes(binfile, 4)
                ptrname = DynosPointerRead(value, binfile)
                print(f"{ptrname}),",file=geoFile)
                binfile.SetOffset(fileoffset)
    if extract:
        print("};\n", file=geoFile)
    print("GeoLayout Found:", name.begin())

def ParseAnimation(binfile: BinFile):
    print("Animation data parsed.")

def ParseGfxDynCmd(binfile: BinFile):
    print("Graphics Dynamic Command data parsed.")

def ParseTextureBinary(binfile: BinFile, extract:bool):
    binfile.Read(1)

    name = ReadName(binfile)
    print("Texture Found:", name.begin())
    ReadPNG(binfile, name, extract)

def ParseActorBinary(binfile: BinFile, gfxFile, extract, geoFile):
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
            if dataType != Dynos.DATA_TYPE_GEO_LAYOUT:
                parse_functions[dataType](_binfile, gfxFile, extract)
            else:
                parse_functions[dataType](_binfile, gfxFile, extract, geoFile)
        else:
            break