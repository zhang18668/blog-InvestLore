# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课95-108"
OUTROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

JOBS = [
    # ch102
    (668, "chan-ch102/chan-ch102-01.png", (235,378,1565,1080), (250,655,740,855)),
    (669, "chan-ch102/chan-ch102-02.png", (240,380,1560,1080), None),
    (669, "chan-ch102/chan-ch102-03.png", (240,1100,1560,1810), (250,1450,740,1650)),
]

for page, rel, box, ad in JOBS:
    im = Image.open(os.path.join(SRC, f"p{page:03d}.png")).convert("RGB")
    cr = im.crop(box)
    if ad:
        l,t,r,b = ad
        l-=box[0]; t-=box[1]; r-=box[0]; b-=box[1]
        l=max(0,l); t=max(0,t); r=min(cr.width,r); b=min(cr.height,b)
        ImageDraw.Draw(cr).rectangle([l,t,r,b], fill=(255,255,255))
    outp=os.path.join(OUTROOT, rel)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    cr.save(outp)
    print("saved", rel, cr.size)
