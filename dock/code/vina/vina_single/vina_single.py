'''
Created on Nov 27, 2019

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
    print("Usage: vina_single.py -l <file> -r <file> -c 'num,num,num' -s 'num,num,num' -e num -n num -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/")

    print("	Optional parameters:")
    print("     [-l]         ligands          file")
    print("     [-r]         protein          file")
    print("     [-c]         center           'x, y, z'")
    print("     [-s]         size             'x, y, z'")
    print("     [-e]         exhaustiveness   num")
    print("     [-n]         maxinum number of binding modes to generate")
    print("     [-p]         AutodockTools' path")
    print("     [-h]         print command usage")

def getArgs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:r:c:s:e:n:p:h", ["help"])
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
        elif o in ("-c", "--center"):
            center = a
        elif o in ("-s", "--size"):
            size = a		
        elif o in ("-e", "--exhaustiveness"):
            exhaustiveness = a	
        elif o in ("-n", "--num_modes"):
            num_modes = a
        elif o in ("-p", "--path_pre"):
            path_pre = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"
			
    return (ligFile, proFile, center, size, exhaustiveness, num_modes, path_pre)    

if __name__ == '__main__':
    (ligFile, proFile, center, size, exhaustiveness, num_modes, path_pre)=getArgs()

def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print('success: ',ret)
    else:
        print('error: ',ret)

center = center.split(",")
size = size.split(",")

res_path = 'result'

if not os.path.exists(res_path):
    os.mkdir(res_path)

# vina pre_process
proname = proFile.split('.')[0]
ligname = ligFile.split('.')[0]

# Convert protein file format to pdbqt
print(f'\n--------------- deal with {proFile} --------------\n')
command = (['pythonsh',
            f"{path_pre}prepare_receptor4.py",
            '-r',proFile,
            '-o',f'{res_path}/{proname}_protein.pdbqt',
            '-A','hydrogens',
            '-U','nphs'])
runcmd(command)

# Convert ligand file format to pdbqt
print(f'\n--------------- deal with {ligFile} --------------\n')
command2 = (['pythonsh',
            f"{path_pre}prepare_ligand4.py",
            '-l',ligFile,
            '-o',f'{res_path}/{ligname}_ligand.pdbqt',
            '-A','hydrogens'])
runcmd(command2)
       
# vina对接
print("\n--------------- vina start ----------------\n")
command3 = (["vina",
             "--receptor", f"{res_path}/{proname}_protein.pdbqt",
             "--ligand", f"{res_path}/{ligname}_ligand.pdbqt",
             "--center_x", center[0],
             "--center_y", center[1],
             "--center_z", center[2],
             "--size_x", size[0],
             "--size_y", size[1],
             "--size_z", size[2],
             "--exhaustiveness",exhaustiveness,
             "--num_modes", num_modes,
             "--out", f"{res_path}/{proname}_{ligname}_vina.pdbqt",
             "--log", f"{res_path}/{proname}_{ligname}_vina.txt"])
runcmd(command3)    
print('\n------ Store results in result folder ------')
