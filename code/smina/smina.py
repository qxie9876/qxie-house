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
    print("Usage: smina.py -l <file> -r <file.pdbqt> -c 'num,num,num' -s 'num,num,num' -e num -n num")

    print("	Optional parameters:")
    print("     [-l]         ligands           file")
    print("     [-r]         protein          *.pdbqt file")
    print("     [-c]         center           'x, y, z'")
    print("     [-s]         size             'x, y, z'")
    print("     [-e]         exhaustiveness   num")
    print("     [-n]         maxinum number of binding modes to generate")
    print("     [-h]         print command usage")

def getArgs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:r:c:s:e:n:h", ["help"])
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
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"
			
    return (ligFile, proFile, center, size, exhaustiveness, num_modes)    

if __name__ == '__main__':
    (ligFile, proFile, center, size, exhaustiveness, num_modes)=getArgs()

def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print('success: ',ret)
    else:
        print('error: ',ret)

center = center.split(",")
size = size.split(",")

# smina pre_process
proname = proFile.split('.')[0]
ligname = ligFile.split('.')[0]
       
# smina对接
print("\n--------------- smina start ----------------\n")
command = (["smina",
             "--receptor", proFile,
             "--ligand", ligFile,
             "--center_x", center[0],
             "--center_y", center[1],
             "--center_z", center[2],
             "--size_x", size[0],
             "--size_y", size[1],
             "--size_z", size[2],
             "--exhaustiveness",exhaustiveness,
             "--num_modes", num_modes,
             "--out", f"{proname}_{ligname}.pdbqt",
             "--log", f"{proname}_{ligname}.txt"])
runcmd(command)    
