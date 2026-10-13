# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课60-66"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

SPECS = [
    ("f469.png", "chan-ch64/chan-ch64-01.png", (250, 400, 1540, 1090), [(490, 270, 1130, 440)]),
    ("f469.png", "chan-ch64/chan-ch64-02.png", (245, 1080, 1545, 1730), []),
    ("f470.png", "chan-ch64/chan-ch64-03.png", (245, 235, 1545, 935), []),
    ("f470.png", "chan-ch64/chan-ch64-04.png", (245, 965, 1545, 1645), []),
    ("f470.png", "chan-ch64/chan-ch64-05.png", (245, 1665, 1545, 2335), []),
    ("f471.png", "chan-ch64/chan-ch64-06.png", (245, 680, 1545, 1375), []),
    ("f471.png", "chan-ch64/chan-ch64-07.png", (245, 1410, 1545, 2105), []),
    ("f472.png", "chan-ch64/chan-ch64-08.png", (245, 235, 1545, 935), []),
    ("f472.png", "chan-ch64/chan-ch64-09.png", (245, 1380, 1545, 2075), []),
    ("f473.png", "chan-ch64/chan-ch64-10.png", (245, 235, 1545, 935), []),
    ("f473.png", "chan-ch64/chan-ch64-11.png", (245, 1080, 1545, 1775), []),
    ("f474.png", "chan-ch64/chan-ch64-12.png", (245, 235, 1545, 935), []),
    ("f474.png", "chan-ch64/chan-ch64-13.png", (245, 1080, 1545, 1775), []),
    ("f475.png", "chan-ch64/chan-ch64-14.png", (245, 235, 1545, 935), []),
    ("f475.png", "chan-ch64/chan-ch64-15.png", (245, 1040, 1545, 1685), []),
    ("f476.png", "chan-ch64/chan-ch64-16.png", (245, 235, 1545, 935), []),
    ("f476.png", "chan-ch64/chan-ch64-17.png", (245, 1080, 1545, 1775), []),
    ("f477.png", "chan-ch64/chan-ch64-18.png", (245, 235, 1545, 935), []),
    ("f477.png", "chan-ch64/chan-ch64-19.png", (245, 1080, 1545, 1775), []),
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
