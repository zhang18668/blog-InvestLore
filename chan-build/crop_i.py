# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课60-66"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

# specs: (src_page, out_rel, box=(l,t,r,b), whiten=[(l,t,r,b),...])
SPECS = [
    # 课60 f444
    ("f444.png", "chan-ch60/chan-ch60-01.png", (235, 375, 1555, 1010), [(760, 580, 1380, 800)]),
    ("f444.png", "chan-ch60/chan-ch60-02.png", (230, 1400, 1410, 2130), []),
    # 课60 f445
    ("f445.png", "chan-ch60/chan-ch60-03.png", (290, 640, 1490, 985), []),
    ("f445.png", "chan-ch60/chan-ch60-04.png", (245, 1580, 1540, 2280), []),
    # 课60 f446
    ("f446.png", "chan-ch60/chan-ch60-05.png", (245, 865, 1540, 1565), []),
    ("f446.png", "chan-ch60/chan-ch60-06.png", (245, 1745, 1540, 2395), []),
    # 课60 f447
    ("f447.png", "chan-ch60/chan-ch60-07.png", (245, 235, 1540, 935), []),
    ("f447.png", "chan-ch60/chan-ch60-08.png", (245, 965, 1540, 1635), []),
    ("f447.png", "chan-ch60/chan-ch60-09.png", (245, 1665, 1540, 2295), []),
    # 课60 f448
    ("f448.png", "chan-ch60/chan-ch60-10.png", (245, 245, 1540, 935), []),
    ("f448.png", "chan-ch60/chan-ch60-11.png", (245, 965, 1540, 1635), []),
    ("f448.png", "chan-ch60/chan-ch60-12.png", (245, 1665, 1540, 2295), []),
    # 课60 f449
    ("f449.png", "chan-ch60/chan-ch60-13.png", (245, 235, 1540, 935), []),
    ("f449.png", "chan-ch60/chan-ch60-14.png", (245, 1325, 1540, 2025), []),
    # 课60 f450
    ("f450.png", "chan-ch60/chan-ch60-15.png", (245, 385, 1540, 1185), []),
    ("f450.png", "chan-ch60/chan-ch60-16.png", (245, 1215, 1540, 1915), []),
]

for src, rel, box, whites in SPECS:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    crop = im.crop(box)
    cl, ct, cr, cb = box
    d = ImageDraw.Draw(crop)
    for (wl, wt, wr, wb) in whites:
        d.rectangle((wl - cl, wt - ct, wr - cl, wb - ct), fill=(255, 255, 255))
    outp = os.path.join(DST, rel)
    crop.save(outp)
    print("saved", rel, crop.size)
