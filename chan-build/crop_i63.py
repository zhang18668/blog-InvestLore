# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课60-66"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

SPECS = [
    ("f466.png", "chan-ch63/chan-ch63-01.png", (250, 390, 1540, 1090), [(490, 300, 1130, 470)]),
    ("f467.png", "chan-ch63/chan-ch63-02.png", (245, 240, 1545, 935), []),
    ("f467.png", "chan-ch63/chan-ch63-03.png", (245, 990, 1545, 1685), []),
]

for src, rel, box, whites in SPECS:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    crop = im.crop(box)
    d = ImageDraw.Draw(crop)
    for (wl, wt, wr, wb) in whites:
        d.rectangle((wl, wt, wr, wb), fill=(255, 255, 255))
    outp = os.path.join(DST, rel)
    crop.save(outp)
    print("saved", rel, crop.size)
