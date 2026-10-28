"""Fotos oficiales de Xocios Lab (capturas en src-lab/, de fragranceoutlet.com) -> ../img/lab2/<id>.webp sobre blanco."""
from PIL import Image
import numpy as np, glob, os
from scipy import ndimage
O='../img/lab2/'; os.makedirs(O,exist_ok=True)
for f in glob.glob('src-lab/*.png'):
    a=np.asarray(Image.open(f).convert('RGB'))
    m=ndimage.binary_dilation(a.min(2)<240,iterations=3); ys,xs=np.where(m)
    c=Image.fromarray(a[max(0,ys.min()-6):ys.max()+7,max(0,xs.min()-6):xs.max()+7])
    s=max(c.size); sq=Image.new('RGB',(int(s*1.08),int(s*1.08)),'white'); sq.paste(c,((sq.width-c.width)//2,(sq.height-c.height)//2))
    sq.thumbnail((900,900),Image.LANCZOS); sq.save(O+os.path.basename(f)[:-4]+'.webp','WEBP',quality=88,method=6)
print(len(os.listdir(O)))
