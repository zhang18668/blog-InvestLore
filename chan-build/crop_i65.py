# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课60-66"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

SPECS = [
    ("f478.png", "chan-ch65/chan-ch65-01.png", (250, 385, 1540, 1110), [(0, 0, 520, 100)]),
    ("f478.png", "chan-ch65/chan-ch65-02.png", (550, 1530, 1100, 1840), []),
    ("f478.png", "chan-ch65/chan-ch65-03.png", (550, 1950, 1100, 2290), []),
    ("f479.png", "chan-ch65/chan-ch65-04.png", (450, 660, 1050, 980), []),
    ("f479.png", "chan-ch65/chan-ch65-05.png", (450, 1300, 1150, 1620), []),
    ("f480.png", "chan-ch65/chan-ch65-06.png", (350, 280, 1260, 800), []),
    ("f480.png", "chan-ch65/chan-ch65-07.png", (400, 1050, 1100, 1400), []),
    ("f480.png", "chan-ch65/chan-ch65-08.png", (350, 1550, 1100, 1900), []),
    ("f481.png", "chan-ch65/chan-ch65-09.png", (245, 540, 1545, 1225), []),
    ("f481.png", "chan-ch65/chan-ch65-10.png", (245, 1260, 1545, 1955), []),
    ("f482.png", "chan-ch65/chan-ch65-11.png", (245, 235, 1545, 935), []),
    ("f482.png", "chan-ch65/chan-ch65-12.png", (300, 1500, 1050, 1835), []),
    ("f483.png", "chan-ch65/chan-ch65-13.png", (250, 280, 1250, 820), []),
    ("f483.png", "chan-ch65/chan-ch65-14.png", (250, 1050, 1350, 1500), []),
    ("f484.png", "chan-ch65/chan-ch65-15.png", (250, 280, 1350, 880), []),
    ("f484.png", "chan-ch65/chan-ch65-16.png", (250, 1150, 1350, 1680), []),
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
