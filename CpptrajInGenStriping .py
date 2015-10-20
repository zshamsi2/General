# This script generates cpptraj input files for stiping water from trajectories. (the frist step for addaptive sampling 
# and featurization)
# For using the script, raw trajectories should be stored in 'rawMdcrd', and have the naming format of 
# "A1_SampleR4_32_md4-17.mdcrd" as an example. Also topology files should be in 'top' with the name of "A1_SampleR4_32.top"

import os.path
import glob

for mdF in glob.glob('rawMdcrd/*.mdcrd'):
	l = mdF.split('/')[-1]
	topN = l.split('_md')[0]
	# topN = l.split('MD')[0]
	mdN = l.strip('.mdcrd')
	print topN, mdN

	inF = open("cppIn"+ mdN +".in" , 'w')
	inF.write("parm top/" + topN + ".top \n")
        inF.write("trajin " + mdF + "\n")
	
	inF.write("strip :WAT \n")
	inF.write("strip :Na+\n")
	inF.write("strip :Cl- \n")
	inF.write("strip @H* \n")

	inF.write("autoimage origin \n")
	inF.write("trajout " + mdN + ".mdcrd mdcrd\n" )
	inF.write("go \n")
	inF.write("quit")
	inF.close()
	
##################################################################################
# run generated input files with the simple command:
# for i in `ls cppIn_*`; do cpptraj < $i; done
# for the next step you need to have the striped topology files:
# as an example of ccptraj
# parm mol.water.parm7
# parmstrip :WAT
###parmbox nobox 
#parmwrite out strip.mol.nobox.parm7
##################################################################################
# msmb AtomPairsFeaturizer --out pair_features --pair_indices AtomIndices.txt --top ala2.pdb --trjs "*.dcd"
