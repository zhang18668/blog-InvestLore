# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课95-108"
OUTROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

JOBS = [
    # ch101
    (664, "chan-ch101/chan-ch101-01.png", (235,378,1565,1075), (250,655,740,855)),
    (664, "chan-ch101/chan-ch101-02.png", (250,1280,1560,1960), None),
    (665, "chan-ch101/chan-ch101-03.png", (250,240,1560,950), None),
    (665, "chan-ch101/chan-ch101-04.png", (250,960,1560,1670), None),
    (666, "chan-ch101/chan-ch101-05.png", (250,240,1560,950), None),
    (666, "chan-ch101/chan-ch101-06.png", (250,1180,1560,1880), None),
    (667, "chan-ch101/chan-ch101-07.png", (250,240,1560,950), None),
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
