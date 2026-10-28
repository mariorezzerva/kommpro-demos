"""Fondo blanco puro: los píxeles casi blancos conectados al borde pasan a #fff, con transición suave."""
from PIL import Image
import numpy as np, glob, sys
from scipy import ndimage
n=0
for f in sorted(glob.glob('../img/p3/*.webp')+glob.glob('../img/lab2/*.webp')):
    im=Image.open(f).convert('RGB'); a=np.asarray(im).astype(float)
    mn=a.min(2); near=mn>=226
    lab,_=ndimage.label(near)
    edge=np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])); edge=edge[edge>0]
    bg=np.isin(lab,edge)
    # transición: distancia al fondo para mezclar 2 px
    d=ndimage.distance_transform_edt(~bg)
    w=np.clip(1-(d-0.5)/2.5,0,1)[...,None]*(~bg)[...,None]
    out=a*(1-w)+255*w; out[bg]=255
    Image.fromarray(out.clip(0,255).astype('uint8')).save(f,'WEBP',quality=90,method=6); n+=1
print(n)
