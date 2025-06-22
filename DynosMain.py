import DynosRead
from Dynos import BinFile
import sys
import os, shutil

dump_dir = "Data"
anim_dir = dump_dir+"/"+"anims"

def main(file = "", texture=False, actor=False, extract=False, write=False):
	if os.name == 'nt':  #windows
		os.system('cls')
	else:
		os.system('clear') #linux

	if file == "":
		print("ERROR: No file selected.")
		return
	if not texture and not actor and not extract and not write:
		print("ERROR?: Nothing to do!")
		return
	Binfile:BinFile = None
	texFile = None
	if texture and write:
		texFile = open(file, "rb")
	else:
		Binfile = BinFile().OpenR(file)
	if os.path.exists(dump_dir):
		shutil.rmtree(dump_dir)
	if os.path.exists(anim_dir):
		shutil.rmtree(anim_dir)
	os.makedirs(dump_dir, exist_ok=True)

	if texture:
		DynosRead.ReadTextureBinary(Binfile, extract)
	elif actor:
		gfxFile = open(os.path.join(dump_dir, "model.inc.c"), "w")
		geoFile = open(os.path.join(dump_dir, "geo.inc.c"), "w")
		os.makedirs(anim_dir, exist_ok=True)
		animFile = open(anim_dir+"/"+"anims.inc.c", "w")
		DynosRead.ReadActorBinary(Binfile, gfxFile, extract, geoFile, animFile)