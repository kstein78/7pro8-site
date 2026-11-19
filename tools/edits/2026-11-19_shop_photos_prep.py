import os,sys
from PIL import Image,ImageOps,ImageFilter
src='/mnt/user-data/uploads/Цех'
OUT='out'
picks={'IMG_1231.jpg':'assembly-team.jpg','IMG_1375.jpg':'partition-frame.jpg','IMG_1540.jpg':'composite-moulding.jpg',
       'IMG_1668.jpg':'3d-printing.jpg','IMG_1398.jpg':'kits-in-work.jpg'}
blur={'IMG_1231.jpg':[(1398,695,1445,835),(278,878,388,908),(278,945,388,1035),(845,695,897,713),(845,738,897,768)],
      'IMG_1398.jpg':[(655,880,760,908),(655,930,760,1012),(950,1112,1118,1152),(1050,1008,1086,1036)]}
for f,name in picks.items():
    im=ImageOps.exif_transpose(Image.open(os.path.join(src,f))).convert('RGB')
    im=im.resize((1800,round(im.height*1800/im.width)),Image.LANCZOS)
    for b in blur.get(f,[]):
        reg=im.crop(b).filter(ImageFilter.GaussianBlur(6)); im.paste(reg,b)
    im.save(os.path.join(OUT,name),quality=86,optimize=True,progressive=True)
    print(name,im.size,os.path.getsize(os.path.join(OUT,name))//1024,'KB')
