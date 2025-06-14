def C0(_WordsW0, pos, width):  return str((_WordsW0 >> (pos)) & ((1 << width) - 1))
def C1(_WordsW1, pos, width): return str((_WordsW1 >> (pos)) & ((1 << width) - 1))
def NC0(_WordsW0, pos, width):  return ((_WordsW0 >> (pos)) & ((1 << width) - 1))
def NC1(_WordsW1, pos, width): return ((_WordsW1 >> (pos)) & ((1 << width) - 1))

G_NOOP		=	0x00
G_RDPHALF_2	=	0xf1
G_SETOTHERMODE_H=	0xe3
G_SETOTHERMODE_L=	0xe2
G_RDPHALF_1	=	0xe1
G_SPNOOP	=	0xe0
G_ENDDL		=	0xdf
G_DL		=	0xde
G_LOAD_UCODE	=	0xdd
G_MOVEMEM		=0xdc
G_MOVEWORD	=	0xdb
G_MTX		=	0xda
G_GEOMETRYMODE	=	0xd9
G_POPMTX	=	0xd8
G_TEXTURE	=	0xd7
G_DMA_IO	=	0xd6
G_SPECIAL_1	=	0xd5
G_SPECIAL_2	=	0xd4
G_SPECIAL_3	=	0xd3

G_COPYMEM	=	0xd2

G_VTX		=	0x01
G_MODIFYVTX		=0x02
G_CULLDL	=	0x03
G_BRANCH_Z		=0x04
G_TRI1		=	0x05
G_TRI2		=	0x06
G_QUAD		=	0x07
G_LINE3D=		0x08

#RDP
G_SETCIMG	=	0xff	
G_SETZIMG		=0xfe	
G_SETTIMG	=	0xfd	
G_SETCOMBINE	=	0xfc	
G_SETENVCOLOR	=	0xfb	
G_SETPRIMCOLOR	=	0xfa	
G_SETBLENDCOLOR	=	0xf9	
G_SETFOGCOLOR	=	0xf8	
G_SETFILLCOLOR	=	0xf7	
G_FILLRECT		=0xf6	
G_SETTILE		=0xf5	
G_LOADTILE	=	0xf4	
G_LOADBLOCK	=	0xf3	
G_SETTILESIZE	=	0xf2	
G_LOADTLUT		=0xf0	
G_RDPSETOTHERMODE	=0xef	
G_SETPRIMDEPTH		=0xee
G_SETSCISSOR		=0xed	
G_SETCONVERT		=0xec	
G_SETKEYR		=0xeb	
G_SETKEYGB	=	0xea	
G_RDPFULLSYNC=		0xe9	
G_RDPTILESYNC=		0xe8	
G_RDPPIPESYNC=		0xe7	
G_RDPLOADSYNC=		0xe6	
G_TEXRECTFLIP=		0xe5	
G_TEXRECT	=	0xe4	

# Color combiner constants
G_CCMUX_COMBINED = 0
G_CCMUX_TEXEL0 = 1
G_CCMUX_TEXEL1 = 2
G_CCMUX_PRIMITIVE = 3
G_CCMUX_SHADE = 4
G_CCMUX_ENVIRONMENT = 5
G_CCMUX_CENTER = 6
G_CCMUX_SCALE = 6
G_CCMUX_COMBINED_ALPHA = 7
G_CCMUX_TEXEL0_ALPHA = 8
G_CCMUX_TEXEL1_ALPHA = 9
G_CCMUX_PRIMITIVE_ALPHA = 10
G_CCMUX_SHADE_ALPHA = 11
G_CCMUX_ENV_ALPHA = 12
G_CCMUX_LOD_FRACTION = 13
G_CCMUX_PRIM_LOD_FRAC = 14
G_CCMUX_NOISE = 7
G_CCMUX_K4 = 7
G_CCMUX_K5 = 15
G_CCMUX_1 = 6
G_CCMUX_0 = 31

# Alpha combiner constants
G_ACMUX_COMBINED = 0
G_ACMUX_TEXEL0 = 1
G_ACMUX_TEXEL1 = 2
G_ACMUX_PRIMITIVE = 3
G_ACMUX_SHADE = 4
G_ACMUX_ENVIRONMENT = 5
G_ACMUX_LOD_FRACTION = 0
G_ACMUX_PRIM_LOD_FRAC = 6
G_ACMUX_1 = 6
G_ACMUX_0 = 7

CC_0 = 0
CC_TEXEL0 = 1
CC_TEXEL1 = 2
CC_PRIM = 3
CC_SHADE = 4
CC_ENV = 5
CC_TEXEL0A = 6
CC_LOD = 7
CC_1 = 8
CC_TEXEL1A = 9
CC_COMBINED = 10
CC_COMBINEDA = 11
CC_PRIMA = 12
CC_SHADEA = 13
CC_ENVA = 14
CC_NOISE = 15
CC_ENUM_MAX = 16 

def color_comb_component_a(v, cycle):
    if v == G_CCMUX_COMBINED:
        return CC_COMBINED if cycle else CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    elif v == G_CCMUX_1:
        return CC_1
    elif v == G_CCMUX_0:
        return CC_0
    elif v == G_CCMUX_COMBINED_ALPHA:
        return CC_COMBINEDA if cycle else CC_0
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    else:
        return CC_0

def color_comb_component_b(v, cycle):
    if v == G_CCMUX_COMBINED:
        return CC_COMBINED if cycle else CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    elif v == G_CCMUX_0:
        return CC_0
    elif v == G_CCMUX_COMBINED_ALPHA:
        return CC_COMBINEDA if cycle else CC_0
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    else:
        return CC_0

def color_comb_component_c(v, cycle):
    if v == G_CCMUX_COMBINED:
        return CC_COMBINED if cycle else CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    elif v == G_CCMUX_COMBINED_ALPHA:
        return CC_COMBINEDA if cycle else CC_0
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    elif v == G_CCMUX_LOD_FRACTION:
        return CC_LOD
    elif v == G_CCMUX_0:
        return CC_0
    else:
        return CC_0

def color_comb_component_d(v, cycle):
    if v == G_CCMUX_COMBINED:
        return CC_COMBINED if cycle else CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    elif v == G_CCMUX_1:
        return CC_1
    elif v == G_CCMUX_0:
        return CC_0
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    else:
        return CC_0

def color_comb_rgb(a, b, c, d, cycle):
    return (color_comb_component_a(a, cycle)
            | (color_comb_component_b(b, cycle) << 8)
            | (color_comb_component_c(c, cycle) << 16)
            | (color_comb_component_d(d, cycle) << 24))

def color_comb_component_a_alpha(v, cycle):
    if v == G_CCMUX_COMBINED_ALPHA:
        return CC_COMBINEDA if cycle else CC_0
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    elif v == G_CCMUX_1:
        return CC_1
    elif v == G_CCMUX_0:
        return CC_0
    elif v == G_CCMUX_COMBINED:
        return CC_COMBINED if cycle else CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    else:
        return CC_0

def color_comb_component_b_alpha(v, cycle):
    if v == G_CCMUX_COMBINED_ALPHA:
        return CC_COMBINEDA if cycle else CC_0
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    elif v == G_CCMUX_1:
        return CC_1
    elif v == G_CCMUX_0:
        return CC_0
    elif v == G_CCMUX_COMBINED:
        return CC_COMBINED if cycle else CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    else:
        return CC_0

def color_comb_component_c_alpha(v, cycle):
    if v == G_CCMUX_LOD_FRACTION:
        return CC_LOD
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    elif v == G_CCMUX_0:
        return CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    else:
        return CC_0

def color_comb_component_d_alpha(v, cycle):
    if v == G_CCMUX_COMBINED_ALPHA:
        return CC_COMBINEDA if cycle else CC_0
    elif v == G_CCMUX_TEXEL0_ALPHA:
        return CC_TEXEL0A
    elif v == G_CCMUX_TEXEL1_ALPHA:
        return CC_TEXEL1A
    elif v == G_CCMUX_PRIMITIVE_ALPHA:
        return CC_PRIMA
    elif v == G_CCMUX_SHADE_ALPHA:
        return CC_SHADEA
    elif v == G_CCMUX_ENV_ALPHA:
        return CC_ENVA
    elif v == G_CCMUX_1:
        return CC_1
    elif v == G_CCMUX_0:
        return CC_0
    elif v == G_CCMUX_COMBINED:
        return CC_COMBINED if cycle else CC_0
    elif v == G_CCMUX_TEXEL0:
        return CC_TEXEL0
    elif v == G_CCMUX_TEXEL1:
        return CC_TEXEL1
    elif v == G_CCMUX_PRIMITIVE:
        return CC_PRIM
    elif v == G_CCMUX_SHADE:
        return CC_SHADE
    elif v == G_CCMUX_ENVIRONMENT:
        return CC_ENV
    else:
        return CC_0

def color_comb_alpha(a, b, c, d, cycle):
    return (color_comb_component_a_alpha(a, cycle)
            | (color_comb_component_b_alpha(b, cycle) << 8)
            | (color_comb_component_c_alpha(c, cycle) << 16)
            | (color_comb_component_d_alpha(d, cycle) << 24))

def DecodeColorCombiner(CC, cycle):
    if CC == CC_COMBINED:
        return "COMBINED" if cycle else "0"
    elif CC == CC_TEXEL0:
        return "TEXEL0"
    elif CC == CC_TEXEL1:
        return "TEXEL1"
    elif CC == CC_PRIM:
        return "PRIMITIVE"
    elif CC == CC_SHADE:
        return "SHADE"
    elif CC == CC_ENV:
        return "ENVIRONMENT"
    elif CC == CC_COMBINEDA:
        return "COMBINED_ALPHA" if cycle else "0"
    elif CC == CC_TEXEL0A:
        return "TEXEL0_ALPHA"
    elif CC == CC_TEXEL1A:
        return "TEXEL1_ALPHA"
    elif CC == CC_PRIMA:
        return "PRIMITIVE_ALPHA"
    elif CC == CC_SHADEA:
        return "SHADE_ALPHA"
    elif CC == CC_ENVA:
        return "ENV_ALPHA"
    elif CC == CC_1:
        return "1"
    elif CC == CC_0:
        return "0"
    else:
        return "0"

def DecodeAlphaCombiner(CC, cycle):
    if CC == CC_COMBINED:
        return "COMBINED" if cycle else "0"
    elif CC == CC_TEXEL0:
        return "TEXEL0"
    elif CC == CC_TEXEL1:
        return "TEXEL1"
    elif CC == CC_PRIM:
        return "PRIMITIVE"
    elif CC == CC_SHADE:
        return "SHADE"
    elif CC == CC_ENV:
        return "ENVIRONMENT"
    elif CC == CC_TEXEL0A:
        return "TEXEL0_ALPHA"
    elif CC == CC_TEXEL1A:
        return "TEXEL1_ALPHA"
    elif CC == CC_PRIMA:
        return "PRIMITIVE_ALPHA"
    elif CC == CC_SHADEA:
        return "SHADE_ALPHA"
    elif CC == CC_ENVA:
        return "ENV_ALPHA"
    elif CC == CC_1:
        return "1"
    elif CC == CC_0:
        return "0"
    else:
        return "0"