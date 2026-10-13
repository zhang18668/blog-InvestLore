# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课95-108"
OUTROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

JOBS = [
    # ch98
    (651, "chan-ch98/chan-ch98-01.png", (235,378,1565,1020), (555,650,1050,850)),
    (651, "chan-ch98/chan-ch98-02.png", (240,1470,1560,2230), None),
    (652, "chan-ch98/chan-ch98-03.png", (240,220,1560,920), None),
    (652, "chan-ch98/chan-ch98-04.png", (240,950,1560,1650), None),
    (653, "chan-ch98/chan-ch98-05.png", (240,240,1560,980), None),
    (653, "chan-ch98/chan-ch98-06.png", (240,1230,1560,1960), None),
    (654, "chan-ch98/chan-ch98-07.png", (240,290,1560,990), (730,660,1060,850)),
    (655, "chan-ch98/chan-ch98-08.png", (240,220,1560,960), None),
    (655, "chan-ch98/chan-ch98-09.png", (240,990,1560,1680), None),
    (655, "chan-ch98/chan-ch98-10.png", (240,1720,1560,2290), None),
]

for page, rel, box, ad in JOBS:
    im = Image.open(os.path.join(SRC, f"p{page:03d}.png")).convert("RGB")
    cr = im.crop(box)
    if ad:
        l,t,r,b = ad
        l-=box[0]; t-=box[1]; r-=box[0]; b-=box[1]
        l=max(0,l); t=max(0,t); r=min(cr.width,r); b=min(cr.height,b)
        d=ImageDraw.Draw(cr)
        d.rectangle([l,t,r,b], fill=(255,255,255))
    outp=os.path.join(OUTROOT, rel)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    cr.save(outp)
    print("saved", rel, cr.size)
