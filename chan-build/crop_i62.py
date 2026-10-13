# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课60-66"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

SPECS = [
    ("f462.png", "chan-ch62/chan-ch62-01.png", (250, 380, 1540, 1060), [(540, 290, 1330, 490)]),
    ("f462.png", "chan-ch62/chan-ch62-02.png", (380, 1480, 1450, 1970), []),
    ("f463.png", "chan-ch62/chan-ch62-03.png", (500, 290, 1450, 520), []),
    ("f463.png", "chan-ch62/chan-ch62-04.png", (500, 620, 1450, 870), []),
    ("f463.png", "chan-ch62/chan-ch62-05.png", (380, 1500, 1380, 1760), []),
    ("f463.png", "chan-ch62/chan-ch62-06.png", (480, 1840, 1380, 2110), []),
    ("f464.png", "chan-ch62/chan-ch62-07.png", (350, 470, 1450, 830), []),
    ("f464.png", "chan-ch62/chan-ch62-08.png", (350, 1380, 1450, 1760), []),
    ("f465.png", "chan-ch62/chan-ch62-09.png", (250, 290, 1380, 720), []),
    ("f465.png", "chan-ch62/chan-ch62-10.png", (300, 880, 1380, 1230), []),
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
