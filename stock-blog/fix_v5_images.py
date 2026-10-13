# -*- coding: utf-8 -*-
"""Insert missing example images into v5-original-practice-cases.md."""
import re

MD = r"E:\生活\股票操练大全全套\stock-blog\source\_posts\v5-original-practice-cases.md"
lines = open(MD, encoding='utf-8').readlines()

# Map: context keyword -> image
CONTEXT_IMG = [
    (r"图1～图7|图1~图7|几幅图|历史.*走势|相似之处", "/images/kxian/v5o-01.png"),
    (r"见图9|暴跌|飞流直下|2245点", "/images/kxian/v5o-10.png"),
    (r"矩形.*假突破|假突破|图13|图14", "/images/kxian/v5o-08.png"),
    (r"图15|跌破矩形下边线|一泻千里", "/images/kxian/v5o-08.png"),
    (r"图16|1558点|1993年", "/images/kxian/v5o-08.png"),
    (r"图17|图18|断头铡刀", "/images/kxian/v5o-10.png"),
    (r"图19|图20|均线.*发散|向下发散|瀑布", "/images/kxian/v5o-11.png"),
    (r"图21|图22|买进.*卖出信号|信号.*统计", "/images/kxian/v5o-12.png"),
    (r"图23|1990年.*1999|周K线走势", "/images/kxian/v2o-01.png"),
    (r"图24|纳斯达克|5000点|3000点", "/images/kxian/v5o-23.png"),
    (r"图25|5·19|5\.19", "/images/kxian/v2o-02.png"),
    (r"图26|图27|图28|图29|H股|香港.*涨", "/images/kxian/v2o-02.png"),
    (r"图30|图31|图32|图33|香港.*跌|跌也匆匆", "/images/kxian/v2o-03.png"),
    (r"图34|广船国际", "/images/kxian/v5o-24.png"),
    (r"图35|图36|美元兑法郎|美元兑日元|外汇", "/images/kxian/v5o-25.png"),
    (r"图37|图38|法郎升值|日元贬值", "/images/kxian/v5o-26.png"),
    (r"图39|图40|图41|图42|美元兑瑞郎|英镑兑美元|多头陷阱", "/images/kxian/v5o-27.png"),
    (r"图43|图44|下降覆盖线", "/images/kxian/v5o-10.png"),
    (r"图45|图46|图47|图48|欧元兑美元|趋势线", "/images/kxian/v5o-28.png"),
]

def find_img(text):
    for pat, img in CONTEXT_IMG:
        if re.search(pat, text):
            return img
    return None

# Find lines with "见图" or "图X" references that don't have an image within next 6 lines
inserted = 0
output = []
i = 0
while i < len(lines):
    line = lines[i]
    output.append(line)
    # Check if this line mentions "见图" or "图X～图Y"
    if re.search(r'见图\d|图\d+[～~-]图?\d+', line) and not line.strip().startswith('!'):
        # Look ahead 8 lines for an existing image
        block = ''.join(lines[i+1:i+9])
        if '![' not in block:
            img = find_img(line + block)
            if img:
                # Insert image after this line (before next paragraph)
                output.append('\n')
                output.append(f'![]({img})\n')
                output.append('\n')
                inserted += 1
    i += 1

open(MD, 'w', encoding='utf-8').write(''.join(output))
print(f"Inserted {inserted} missing example images into v5")
