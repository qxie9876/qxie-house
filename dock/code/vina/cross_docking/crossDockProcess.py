import re
import os
import getopt
import sys
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

def usage():
    "Print helpful, accurate usage statement to stdout."
    print("Usage: crossDockProcess.py -r rmsd.txt")
    print("     [-r]      rmsd.txt")

def getArgs():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:h", ["help"])
    except getopt.GetoptError as err:
        print (str(err)) 
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-r", "--rmsd.txt"):
            rmsd_path = a   
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"			
    return rmsd_path

if __name__ == '__main__':
    rmsd_path=getArgs()

pictures_path = 'results_matrix'
if not os.path.exists(pictures_path):
    os.mkdir(pictures_path)
    
def sear_name(string):
    x1 = re.compile('(?<=/).*?(?=_[0-9])')
    x2 = re.compile('(?<=_)[0-9].*?(?=\.)')
    f_name = re.findall(x1, string)
    s_name = re.findall(x2, string)
    return f_name[0], s_name[0]
names = []
rmsds = []
with open(rmsd_path,'r') as fh:
    allLines = fh.readlines()[1:]
for line in allLines:
    a = line.split() 
    f_name, s_name = sear_name(a[0])
    name_ls = [f_name,s_name]
    name = '@'.join(name_ls)
    rmsd = a[-1]
    names.append(name)
    rmsds.append(rmsd)

pro_ls = []
lig_ls = []
for name in names:
    x = re.compile('.*(?=@)')
    y = re.compile('(?<=@).*')
    pro = re.findall(x,name)
    lig = re.findall(y,name)
    pro_ls.append(pro[0])
    lig_ls.append(lig[0])
dicts_rmsd = dict(zip(names,rmsds))
df_non = pd.DataFrame(columns=set(lig_ls), index=set(pro_ls))

for name, rmsd in dicts_rmsd.items():
    print(name)
    x = re.compile('.*(?=@)')
    y = re.compile('(?<=@).*')
    pro = re.findall(x,name)
    lig = re.findall(y,name)
    df_non.loc[pro[0],lig[0]] = float(rmsd)

#print(df_non)
df_non.to_csv('result.csv')
df = pd.read_csv('result.csv',index_col=0)

#print(df)
ax = sns.heatmap(df,
                 annot=True,
                 vmin=0,vmax=7,
                 cmap=plt.cm.Blues,
                 fmt='.4f',
                 cbar=True,
                 square=True)
plt.xlabel('Ligand')
plt.ylabel('Protein')
plt.title('Cross Docking Rmsd Matrix')
plt.savefig(f'results_pictures.jpg')
