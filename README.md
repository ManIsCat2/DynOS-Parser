# How to use

Open a terminal, for example CMD in windows.

Copy the Bin file/Tex file that you wanna extract data from, and paste it in the DynOS-Parser Directory.

Use the `cd` command and move to the DynOS-Parser Directory.

Run this:
`py DynosMain.py extract=True actorbin=True file='BinName.bin'`

or if you have a Texture:
`py DynosMain.py extract=True texturebin=True file='TexName.tex'`

The program will make a Dump Directory in the current Directory, the data of the actor/texture will be in it.