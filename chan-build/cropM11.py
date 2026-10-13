# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课95-108"
OUTROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

JOBS = [
    # ch108
    (689, "chan-ch108/chan-ch108-01.png", (235,378,1565,1160), (950,540,1380,730)),
    (689, "chan-ch108/chan-ch108-02.png", (180,1520,1300,2230), None),
    (690, "chan-ch108/chan-ch108-03.png", (230,270,1300,1030), None),
    (690, "chan-ch108/chan-ch108-04.png", (200,1470,1400,1930), None),
    (691, "chan-ch108/chan-ch108-05.png", (230,360,1400,960), None),
    (691, "chan-ch108/chan-ch108-06.png", (240,1420,1560,2200), None),
    (692, "chan-ch108/chan-ch108-07.png", (240,250,1560,1030), None),
    (692, "chan-ch108/chan-ch108-08.png", (240,1200,1560,1980), None),
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
