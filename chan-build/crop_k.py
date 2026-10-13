import os
from PIL import Image

WORK = r"E:\生活\股票操练大全全套\chan-build\work-fig-课74-80"
IMGROOT = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

def load(pno):
    return Image.open(os.path.join(WORK, f"f{pno:03d}.png")).convert("RGB")

def save(img, ch, idx):
    d = os.path.join(IMGROOT, f"chan-ch{ch:02d}")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"chan-ch{ch:02d}-{idx:02d}.png")
    img.save(p)
    print("saved", p, img.size)

def crop(pno, box):
    return load(pno).crop(box)

def whiten(img, box):
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=(255,255,255))

# ---- ch74 ----
# 01: f538 top dashboard 上证指数 2007-08-28
im = crop(538, (232, 358, 1555, 1020))
whiten(im, (10, 70, 560, 250))   # ad white bar inside chart (relative to crop)
save(im, 74, 1)
# 02: f539 上证指数 1994 daily (325点缺口)
im = crop(539, (250, 232, 1550, 888))
save(im, 74, 2)
print("ch74 done")

# ---- ch75 ----
im = crop(541, (250, 359, 1550, 1043))
whiten(im, (5, 55, 490, 218))
save(im, 75, 1)
im = crop(542, (265, 1232, 1564, 1918))
save(im, 75, 2)
im = crop(543, (250, 225, 1557, 925))
save(im, 75, 3)
print("ch75 done")

# ---- ch76 ----
im = crop(544, (250, 381, 1550, 1050))
whiten(im, (5, 60, 490, 225))
save(im, 76, 1)
im = crop(545, (265, 1600, 1557, 2268))
save(im, 76, 2)
print("ch76 done")

# ---- ch77 ----
im = crop(546, (265, 410, 1557, 1100))
whiten(im, (10, 65, 520, 230))
save(im, 77, 1)
# f547 三张并排实盘
im = crop(547, (265, 232, 1557, 882)); save(im, 77, 2)
im = crop(547, (265, 988, 1557, 1635)); save(im, 77, 3)
im = crop(547, (265, 1741, 1557, 2285)); save(im, 77, 4)
# f548
im = crop(548, (260, 455, 1580, 860)); save(im, 77, 5)
im = crop(548, (480, 1500, 1330, 1960)); save(im, 77, 6)
# f549
im = crop(549, (420, 380, 1580, 900)); save(im, 77, 7)
im = crop(549, (230, 1500, 1490, 1810)); save(im, 77, 8)
# f550
im = crop(550, (260, 310, 1440, 1180)); save(im, 77, 9)
im = crop(550, (220, 1630, 1560, 2210)); save(im, 77, 10)
# f551
im = crop(551, (220, 620, 1490, 1110)); save(im, 77, 11)
im = crop(551, (250, 1450, 1560, 2040)); save(im, 77, 12)
# f552
im = crop(552, (360, 340, 1450, 800)); save(im, 77, 13)
im = crop(552, (390, 1440, 1410, 1940)); save(im, 77, 14)
# f553
im = crop(553, (440, 490, 1510, 1060)); save(im, 77, 15)
im = crop(553, (300, 1250, 1460, 1680)); save(im, 77, 16)
# f554
im = crop(554, (320, 270, 1550, 760)); save(im, 77, 17)
im = crop(554, (280, 860, 1580, 1420)); save(im, 77, 18)
im = crop(554, (360, 1790, 1420, 2210)); save(im, 77, 19)
# f555
im = crop(555, (300, 640, 1420, 1320)); save(im, 77, 20)
im = crop(555, (250, 1610, 1570, 2300)); save(im, 77, 21)
# f556
im = crop(556, (250, 230, 1570, 930)); save(im, 77, 22)
im = crop(556, (250, 1410, 1570, 2100)); save(im, 77, 23)
print("ch77 done")

# ---- ch78 ----
im = crop(557, (250, 380, 1570, 1040)); save(im, 78, 1)
im = crop(557, (250, 1280, 1570, 1960)); save(im, 78, 2)
im = crop(558, (260, 190, 1460, 860)); save(im, 78, 3)
im = crop(558, (250, 1390, 1570, 2060)); save(im, 78, 4)
im = crop(559, (250, 350, 1570, 1030)); save(im, 78, 5)
im = crop(559, (250, 1100, 1570, 1820)); save(im, 78, 6)
im = crop(559, (150, 1850, 1480, 2150)); save(im, 78, 7)
im = crop(560, (290, 520, 1460, 830)); save(im, 78, 8)
im = crop(560, (210, 1190, 1430, 1580)); save(im, 78, 9)
im = crop(560, (180, 1950, 1440, 2350)); save(im, 78, 10)
im = crop(561, (250, 225, 1570, 920)); save(im, 78, 11)
im = crop(561, (250, 1020, 1570, 1720)); save(im, 78, 12)
im = crop(562, (250, 225, 1570, 910)); save(im, 78, 13)
im = crop(562, (200, 1280, 1460, 1640)); save(im, 78, 14)
im = crop(562, (190, 1880, 1460, 2300)); save(im, 78, 15)
im = crop(563, (160, 290, 1590, 860)); save(im, 78, 16)
im = crop(563, (160, 1090, 1590, 1850)); save(im, 78, 17)
print("ch78 done")

# ---- ch79 ----
im = crop(564, (251, 508, 1557, 1120))
whiten(im, (470, 210, 1090, 400))
save(im, 79, 1)
im = crop(565, (190, 750, 1530, 1170)); save(im, 79, 2)
im = crop(565, (180, 1510, 1410, 2210)); save(im, 79, 3)
im = crop(566, (180, 230, 1440, 1030)); save(im, 79, 4)
im = crop(567, (220, 610, 1530, 990)); save(im, 79, 5)
im = crop(567, (230, 1020, 1550, 1440)); save(im, 79, 6)
im = crop(568, (270, 300, 1500, 830)); save(im, 79, 7)
im = crop(568, (220, 1220, 1550, 1590)); save(im, 79, 8)
im = crop(569, (250, 225, 1570, 920)); save(im, 79, 9)
im = crop(569, (250, 1020, 1570, 1720)); save(im, 79, 10)
im = crop(570, (250, 210, 1570, 930)); save(im, 79, 11)
im = crop(570, (250, 1030, 1570, 1730)); save(im, 79, 12)
im = crop(571, (250, 205, 1570, 910)); save(im, 79, 13)
im = crop(571, (250, 1190, 1570, 1890)); save(im, 79, 14)
im = crop(572, (250, 175, 1570, 860)); save(im, 79, 15)
im = crop(572, (250, 920, 1570, 1610)); save(im, 79, 16)
im = crop(572, (250, 1670, 1570, 2350)); save(im, 79, 17)
im = crop(573, (250, 490, 1570, 1260)); save(im, 79, 18)
im = crop(573, (250, 1290, 1570, 1970)); save(im, 79, 19)
im = crop(574, (250, 175, 1570, 860)); save(im, 79, 20)
im = crop(574, (250, 920, 1570, 1610)); save(im, 79, 21)
im = crop(574, (250, 1670, 1570, 2350)); save(im, 79, 22)
im = crop(575, (250, 190, 1570, 860)); save(im, 79, 23)
im = crop(575, (250, 920, 1570, 1610)); save(im, 79, 24)
print("ch79 done")

# ---- ch80 ----
im = crop(576, (251, 388, 1557, 1030))
whiten(im, (0, 20, 560, 265))
save(im, 80, 1)
im = crop(577, (250, 225, 1570, 920)); save(im, 80, 2)
im = crop(577, (250, 1050, 1570, 1750)); save(im, 80, 3)
im = crop(578, (250, 225, 1570, 920)); save(im, 80, 4)
im = crop(578, (250, 1150, 1570, 1820)); save(im, 80, 5)
im = crop(579, (250, 175, 1570, 860)); save(im, 80, 6)
im = crop(579, (250, 920, 1570, 1610)); save(im, 80, 7)
im = crop(579, (250, 1670, 1570, 2350)); save(im, 80, 8)
im = crop(580, (250, 225, 1570, 920)); save(im, 80, 9)
im = crop(580, (250, 990, 1570, 1680)); save(im, 80, 10)
im = crop(580, (250, 1720, 1570, 2390)); save(im, 80, 11)
im = crop(581, (250, 460, 1570, 1150)); save(im, 80, 12)
im = crop(581, (250, 1220, 1570, 1920)); save(im, 80, 13)
im = crop(582, (250, 190, 1570, 860)); save(im, 80, 14)
im = crop(582, (250, 920, 1570, 1610)); save(im, 80, 15)
im = crop(582, (250, 1670, 1570, 2350)); save(im, 80, 16)
print("ch80 done")
