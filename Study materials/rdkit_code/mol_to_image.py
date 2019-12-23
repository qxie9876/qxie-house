# 将分子转换成图片并显示

from rdkit import Chem
from rdkit.Chem import Draw # 将mol转成图片
from itertools import islice # 创建迭代器，对迭代器内容进行切片处理
from IPython.display import Image, display, HTML

# 显示图片
def display_images(filenames):
    """Helper to pretty-print images."""
    for filename in filenames:
        display(Image(filename))

# 将分子转成png格式
def mols_to_pngs(mols, basename="test"):
    """Helper to write RDKit mols to png files."""
    filenames = []
    for i, mol in enumerate(mols):
        filename = "MUV_%s%d.png" % (basename, i)
        Draw.MolToFile(mol, filename)
        filenames.append(filename)
    return filenames

num_to_display = 12
molecules = []
for _, data in islice(dataset.iterrows(), num_to_display):
    molecules.append(Chem.MolFromSmiles(data["smiles"]))
display_images(mols_to_pngs(molecules))