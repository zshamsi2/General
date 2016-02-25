import os.path
import glob

for pdbF in glob.glob('*.pdb'):
	l = pdbF.split('.pdb')[0]
	print l
	inF = open("tleap"+ l +".in" , 'w')
	inF.write("source leaprc.ff14SB\n")
	inF.write("source leaprc.gaff \n")
	inF.write("loadamberparams frcmod.ionsjc_tip3p \n")
	inF.write("loadamberparams STI.frcmod \n")
	inF.write("loadoff STI.lib \n")
	inF.write("pdb = loadpdb "+pdbF+"\n")
	inF.write("saveamberparm pdb "+l+".prmtop "+l+"00.rst\n")
	inF.write("quit")
	inF.close()
