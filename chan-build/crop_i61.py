# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课60-66"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

SPECS = [
    ("f451.png", "chan-ch61/chan-ch61-01.png", (250, 500, 1545, 1125), []),
    ("f452.png", "chan-ch61/chan-ch61-02.png", (245, 190, 1545, 875), []),
    ("f452.png", "chan-ch61/chan-ch61-03.png", (245, 1080, 1545, 1560), [(380, 220, 1120, 430)]),
    ("f453.png", "chan-ch61/chan-ch61-04.png", (245, 240, 1545, 925), []),
    ("f453.png", "chan-ch61/chan-ch61-05.png", (245, 950, 1545, 1625), []),
    ("f453.png", "chan-ch61/chan-ch61-06.png", (245, 1690, 1545, 2375), [(330, 195, 1160, 500)]),
    ("f454.png", "chan-ch61/chan-ch61-07.png", (245, 240, 1545, 925), []),
    ("f454.png", "chan-ch61/chan-ch61-08.png", (245, 1290, 1545, 1975), []),
    ("f455.png", "chan-ch61/chan-ch61-09.png", (245, 240, 1545, 925), []),
    ("f455.png", "chan-ch61/chan-ch61-10.png", (245, 1100, 1545, 1785), []),
    ("f456.png", "chan-ch61/chan-ch61-11.png", (245, 240, 1545, 925), []),
    ("f456.png", "chan-ch61/chan-ch61-12.png", (245, 1290, 1545, 1975), []),
    ("f457.png", "chan-ch61/chan-ch61-13.png", (245, 240, 1545, 925), []),
    ("f457.png", "chan-ch61/chan-ch61-14.png", (245, 990, 1545, 1675), []),
    ("f458.png", "chan-ch61/chan-ch61-15.png", (245, 240, 1545, 925), []),
    ("f458.png", "chan-ch61/chan-ch61-16.png", (245, 1290, 1545, 1975), [(330, 230, 1160, 440)]),
    ("f459.png", "chan-ch61/chan-ch61-17.png", (245, 240, 1545, 925), []),
    ("f459.png", "chan-ch61/chan-ch61-18.png", (245, 1100, 1545, 1785), [(330, 230, 1160, 440)]),
    ("f460.png", "chan-ch61/chan-ch61-19.png", (245, 240, 1545, 925), []),
    ("f460.png", "chan-ch61/chan-ch61-20.png", (245, 990, 1545, 1675), []),
    ("f461.png", "chan-ch61/chan-ch61-21.png", (245, 235, 1545, 935), []),
    ("f461.png", "chan-ch61/chan-ch61-22.png", (245, 965, 1545, 1635), []),
    ("f461.png", "chan-ch61/chan-ch61-23.png", (245, 1660, 1545, 2335), []),
]

# whiten rects are in CROP coordinates
for src, rel, box, whites in SPECS:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    crop = im.crop(box)
    d = ImageDraw.Draw(crop)
    for (wl, wt, wr, wb) in whites:
        d.rectangle((wl, wt, wr, wb), fill=(255, 255, 255))
    outp = os.path.join(DST, rel)
    crop.save(outp)
    print("saved", rel, crop.size)
