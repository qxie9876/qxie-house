'''
Created on Dec 15, 2019

@author: xieqin
@mail: 987671584@qq.com
'''
# single protein and single ligand docking
import re
import os
import getopt
import sys
import subprocess

def usage():
    "Print helpful, accurate usage statement to stdout."
    print("Usage: vina_screening.py -l <file.sd> -r <file.mol2> -n 50")

    print("	Optional parameters:")
    print("     [-l]         ligands           file")
    print("     [-r]         protein          *.mol2 file")
    print("     [-n]         maxinum number of binding modes to generate")

def getArgs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:r:n:h", ["help"])
    except getopt.GetoptError as err:
	# print help information and exit:
        print (str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
		
    for o, a in opts:
        if o in ("-l", "--ligands"):
            ligFile = a   
        elif o in ("-r", "--receptor"):
            proFile = a 	
        elif o in ("-n", "--num_modes"):
            num_modes = a 	
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"
			
    return (ligFile, proFile, num_modes)    

if __name__ == '__main__':
    (ligFile, proFile, num_modes)=getArgs()

def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print('success: ',ret)
    else:
        print('error: ',ret)

proname = proFile.split('.')[0]
ligname = ligFile.split('.')[0]

# pre_process
fh = open(f'{proname}_{ligname}.prm','w')
fh.write(f'RBT_PARAMETER_FILE_V1.00\
            \nTIRLE {proname}\
            \nRECEPTOR_FILE   {proFile}\
            \nRECEPTOR_TOPOL_FILE  {proname}.psf\
            \nRECEPTOR_COORD_FILE  {proname}.crd\
            \nRECEPTOR_FLEX 3.0\
            \nRECEPTOR_DIHEDRAL_STEP 10.0\
            \n\nSECTION LIGAND\
            \n        TRANS_MODE FREE\
            \n        ROT_MODE FREE\
            \n        DIHEDRAL_MODE FIXED\
            \nEND_SECTION\
            \n\nSECTION MAPPER\
            \n        SITE_MAPPER RbtLigandSiteMapper\
            \n        VOL_INCR 0.0\
            \n        GRIDSTEP 0.5\
            \n        RADIUS 6.0\
            \n        REF_MOL  {ligFile}\
            \n        SMALL_SPHERE 1.0\
            \n        TRACE 1\
            \n        MIN_VOLUME 100\
            \n        MAX_CAVITIES 1\
            \nEND_SECTION\
            \n\nSECTION CAVITY\
            \n        SCORING_FUNCTION        RbtCavityGridSF\
            \n        WEIGHT                  1.0\
            \nEND_SECTION')
fh.close()

# dock
cmd_cav = ['rbcavity', '-r', f'{proname}_{ligname}.prm', '-was','-d']

cmd_rdock = ['rbdock', '-i', ligFile, '-o', f'{proname}_{ligname}',
             '-r', f'{proname}_{ligname}.prm', '-p', 'dock.prm',
             '-n', num_modes]
runcmd(cmd_cav)
runcmd(cmd_rdock)

# post_process
subprocess.call(f'sdsort -n -fSCORE.INTER -s {proname}_{ligname}.sd > {proname}_{ligname}_sort.sd',shell=True)
subprocess.call(f'sdreport -t {proname}_{ligname}_sort.sd >{proname}_{ligname}_sort.txt',shell=True)