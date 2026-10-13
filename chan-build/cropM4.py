# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课95-108"
OUTROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

JOBS = [
    # ch100
    (659, "chan-ch100/chan-ch100-01.png", (235,378,1565,1020), (555,650,1050,850)),
    (660, "chan-ch100/chan-ch100-02.png", (240,250,1560,1010), None),
    (660, "chan-ch100/chan-ch100-03.png", (240,1260,1560,2010), None),
    (661, "chan-ch100/chan-ch100-04.png", (240,250,1560,1010), None),
    (661, "chan-ch100/chan-ch100-05.png", (240,1370,1560,2130), None),
    (662, "chan-ch100/chan-ch100-06.png", (240,250,1560,980), None),
    (662, "chan-ch100/chan-ch100-07.png", (240,990,1560,1730), None),
    (663, "chan-ch100/chan-ch100-08.png", (240,250,1560,1000), None),
    (663, "chan-ch100/chan-ch100-09.png", (240,1010,1560,1780), None),
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
