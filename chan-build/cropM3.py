# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课95-108"
OUTROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

JOBS = [
    # ch99
    (656, "chan-ch99/chan-ch99-01.png", (235,378,1565,1020), (555,650,1050,850)),
    (656, "chan-ch99/chan-ch99-02.png", (230,1730,1560,2290), None),
    (657, "chan-ch99/chan-ch99-03.png", (450,450,1180,1010), None),
    (657, "chan-ch99/chan-ch99-04.png", (450,1480,1180,2040), None),
    (658, "chan-ch99/chan-ch99-05.png", (230,470,1560,1070), None),
    (658, "chan-ch99/chan-ch99-06.png", (230,1220,1560,1830), None),
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
