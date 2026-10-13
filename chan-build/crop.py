# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

WORK = r"E:\生活\股票操练大全全套\chan-build\work-fig-课1-16"
OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

def crop(page, box, outname, adbox=None):
    im = Image.open(os.path.join(WORK, f"page{page:03d}.png")).convert("RGB")
    c = im.crop(box)
    if adbox:
        d = ImageDraw.Draw(c)
        d.rectangle(adbox, fill=(255,255,255))
    outdir = os.path.join(OUT, outname.split("/")[0])
    os.makedirs(outdir, exist_ok=True)
    c.save(os.path.join(outdir, outname.split("/")[1]))
    print(outname, c.size)

# ---- 标题页顶部大盘图（标准区域）----
# ch01 已裁(13)
crop(15, (255,360,1565,1000), "chan-ch02/chan-ch02-01.png")
crop(16, (255,360,1565,1000), "chan-ch03/chan-ch03-01.png")
crop(17, (255,360,1565,1000), "chan-ch04/chan-ch04-01.png")
crop(20, (255,360,1565,1000), "chan-ch05/chan-ch05-01.png")
crop(21, (255,360,1565,1000), "chan-ch06/chan-ch06-01.png")
crop(23, (255,360,1565,1000), "chan-ch07/chan-ch07-01.png")
crop(27, (255,360,1565,1000), "chan-ch08/chan-ch08-01.png")
crop(29, (255,360,1565,1000), "chan-ch09/chan-ch09-01.png")
crop(31, (255,360,1565,1000), "chan-ch10/chan-ch10-01.png")
crop(34, (255,360,1565,1000), "chan-ch11/chan-ch11-01.png")
crop(37, (255,360,1565,1000), "chan-ch12/chan-ch12-01.png")
crop(47, (255,360,1565,1000), "chan-ch15/chan-ch15-01.png")
crop(53, (255,360,1565,1000), "chan-ch16/chan-ch16-01.png", adbox=(0,45,470,235))
print("done title charts")
