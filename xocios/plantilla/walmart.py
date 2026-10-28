"""Fotos oficiales de producto desde walmart.co.cr (capturas en src-wm/, por código de barras).
Recorta cada producto sobre blanco (sin quitar fondo) y escribe ../img/p3/<id>.webp."""
from PIL import Image
import numpy as np, glob, re, os
from scipy import ndimage
import sys
S=sys.argv[1] if len(sys.argv)>1 else 'src-wm/'; O='../img/p3/'; os.makedirs(O,exist_ok=True)
pages=open(S+'pages.txt').read().strip().split(';')
shots=sorted(glob.glob(S+'screenshot-*.png'),key=lambda f:int(re.search(r'-(\d+)\.png$',f).group(1)))
assert len(shots)==len(pages),(len(shots),len(pages))
def trim(a):
    m=a.min(2)<238
    m=ndimage.binary_dilation(m,iterations=3)
    lab,n=ndimage.label(m)
    if n==0: return a
    sizes=ndimage.sum(m,lab,range(1,n+1))
    keep=[i+1 for i,s in enumerate(sizes) if s>=sizes.max()*0.06]
    mm=np.isin(lab,keep)
    ys,xs=np.where(mm)
    return a[max(0,ys.min()-4):ys.max()+5, max(0,xs.min()-4):xs.max()+5]
n=0
for f,spec in zip(shots,pages):
    t,ids=spec.split(':'); ids=ids.split(',')
    im=np.asarray(Image.open(f).convert('RGB')); W=im.shape[1]; h=W//2
    for k,i in enumerate(ids):
        if t=='t': cell=im[:, k*h:(k+1)*h]
        else: cell=im[(k//2)*h:(k//2+1)*h, (k%2)*h:(k%2+1)*h]
        if i=='SKIP': continue
        c=Image.fromarray(trim(cell[3:-3,3:-3]))
        c.thumbnail((900,900),Image.LANCZOS)
        c.save(O+i+'.webp','WEBP',quality=88,method=6); n+=1
print(n)
