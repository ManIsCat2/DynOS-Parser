import DynosParse
from Dynos import BinFile
import sys
import os, shutil

dump_dir = "Dump"
anim_dir = dump_dir+"/"+"anims"

def main(texturebin=False, actorbin=False, file = "", extract=False):
	Binfile:BinFile = BinFile().OpenR(file)
	if os.path.exists(dump_dir):
		shutil.rmtree(dump_dir)
	if os.path.exists(anim_dir):
		shutil.rmtree(anim_dir)
	os.makedirs(dump_dir, exist_ok=True)
	os.makedirs(anim_dir, exist_ok=True)

	if actorbin:
		gfxFile = open(os.path.join(dump_dir, "model.inc.c"), "w")
		geoFile = open(os.path.join(dump_dir, "geo.inc.c"), "w")
		animFile = open(anim_dir+"/"+"anims.inc.c", "w")
	if texturebin:
		DynosParse.ParseTextureBinary(Binfile, extract)
	elif actorbin:
		DynosParse.ParseActorBinary(Binfile, gfxFile, extract, geoFile, animFile)

def EvalArg(name, arg):
	try:
		return eval(arg)
	except:
		raise Exception(f"Argument {name} unable to be evaluated with arg {arg}")

if __name__=='__main__':
	argD = {}
	args = ''
	"""if any(h in sys.argv for h in ["-h", "help", "--help"]):
		print(HelpMsg)
		if any(h in sys.argv for h in ["-v", "verbose", "--verbose"]):
			print(Verbose)
		sys.exit()"""
	for arg in sys.argv[1:]:
		args+=arg+" "
	try:
		#the utmosts of cringes
		for arg in sys.argv:
			if arg=='DynosMain.py':
				continue
			arg = arg.split('=')
			argD[arg[0]]=EvalArg(arg[0], arg[1])
	except:
		raise 'bad arguments'
	main(**argD)