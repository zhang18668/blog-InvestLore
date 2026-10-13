# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课60-66"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

SPECS = [
    ("f485.png", "chan-ch66/chan-ch66-01.png", (250, 380, 1540, 1090), (20, 0, 540, 105)),
]

for src, rel, box, w in SPECS:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    crop = im.crop(box)
    d = ImageDraw.Draw(crop)
    d.rectangle(w, fill=(255, 255, 255))
    outp = os.path.join(DST, rel)
    crop.save(outp)
    print("saved", rel, crop.size)
