# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课95-108"
OUTROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

JOBS = [
    # ch106
    (674, "chan-ch106/chan-ch106-01.png", (235,378,1565,1210), (950,530,1390,725)),
    (675, "chan-ch106/chan-ch106-02.png", (240,250,1560,1010), None),
    (675, "chan-ch106/chan-ch106-03.png", (240,1290,1560,2030), None),
    (676, "chan-ch106/chan-ch106-04.png", (240,580,1560,1310), None),
    (676, "chan-ch106/chan-ch106-05.png", (240,1350,1560,2090), None),
    (677, "chan-ch106/chan-ch106-06.png", (240,240,1560,1000), None),
    (677, "chan-ch106/chan-ch106-07.png", (240,1260,1560,2030), None),
    (678, "chan-ch106/chan-ch106-08.png", (240,240,1560,1010), None),
    (678, "chan-ch106/chan-ch106-09.png", (240,1040,1560,1810), None),
    (678, "chan-ch106/chan-ch106-10.png", (240,1840,1560,2290), None),
    (679, "chan-ch106/chan-ch106-11.png", (240,230,1560,1010), None),
    (679, "chan-ch106/chan-ch106-12.png", (240,1020,1560,1800), None),
    (679, "chan-ch106/chan-ch106-13.png", (240,1810,1560,2290), None),
    (680, "chan-ch106/chan-ch106-14.png", (240,230,1560,1010), None),
    (680, "chan-ch106/chan-ch106-15.png", (240,1020,1560,1800), None),
    (680, "chan-ch106/chan-ch106-16.png", (240,1810,1560,2290), None),
    (681, "chan-ch106/chan-ch106-17.png", (240,240,1560,1010), None),
    (681, "chan-ch106/chan-ch106-18.png", (240,1020,1560,1790), None),
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
