# -*- coding: utf-8 -*-
"""Auto-insert exercise images into wb-original-workbook.md based on keyword matching."""
import re, os

MD = r"E:\生活\股票操练大全全套\stock-blog\source\_posts\wb-original-workbook.md"
lines = open(MD, encoding='utf-8').readlines()

# Keyword -> image path mapping
KEYWORD_IMG = [
    # K线形态
    (r"吊颈", "/images/kxian/v1o-04.png"),
    (r"锤头", "/images/kxian/v1o-03.png"),
    (r"射击之星", "/images/kxian/v1o-06.png"),
    (r"倒锤头", "/images/kxian/v1o-05.png"),
    (r"大阳线", "/images/kxian/v1o-01.png"),
    (r"大阴线", "/images/kxian/v1o-02.png"),
    (r"乌云盖顶", "/images/kxian/v1o-09.png"),
    (r"曙光初现", "/images/kxian/v1o-10.png"),
    (r"穿头破脚|抱线|包容", "/images/kxian/v1o-15.png"),
    (r"早晨之星|希望之星", "/images/kxian/v1o-12.png"),
    (r"黄昏之星", "/images/kxian/v1o-13.png"),
    (r"红三兵", "/images/kxian/v1o-20.png"),
    (r"黑三兵|三只乌鸦", "/images/kxian/v1o-21.png"),
    (r"上升三部曲|升势三鸦", "/images/kxian/v1o-25.png"),
    (r"下降三部曲|降势三鹤", "/images/kxian/v1o-26.png"),
    (r"跳空|缺口", "/images/kxian/v1o-30.png"),
    (r"十字线|十字星", "/images/kxian/v1o-07.png"),
    (r"T字线", "/images/kxian/v1o-08.png"),
    (r"螺旋桨", "/images/kxian/v1o-18.png"),
    (r"镊子线", "/images/kxian/v1o-22.png"),
    (r"尽头线", "/images/kxian/v1o-23.png"),
    (r"身怀六甲|孕线", "/images/kxian/v1o-14.png"),
    # 均线/趋势
    (r"多头排列", "/images/kxian/v2o-02.png"),
    (r"空头排列", "/images/kxian/v2o-03.png"),
    (r"黄金交叉|金叉", "/images/kxian/v2o-04.png"),
    (r"死亡交叉|死叉", "/images/kxian/v2o-05.png"),
    (r"银山谷", "/images/kxian/v2o-06.png"),
    (r"金山谷", "/images/kxian/v2o-07.png"),
    (r"死亡谷", "/images/kxian/v2o-08.png"),
    (r"上升趋势线|支撑线", "/images/kxian/v2o-19.png"),
    (r"下降趋势线|压力线", "/images/kxian/v2o-20.png"),
    (r"蛟龙出海", "/images/kxian/v2o-17.png"),
    (r"断头铡刀", "/images/kxian/v2o-18.png"),
    (r"烘云托月", "/images/kxian/v2o-46.png"),
    (r"乌云密布", "/images/kxian/v2o-47.png"),
    # MACD
    (r"MACD", "/images/kxian/v2o-30.png"),
    (r"底背离", "/images/kxian/v2o-34.png"),
    (r"顶背离", "/images/kxian/v2o-35.png"),
    # BIAS
    (r"乖离率|BIAS", "/images/kxian/v2o-36.png"),
    # 成交量
    (r"逐渐放量|放量", "/images/kxian/v2o-25.png"),
    (r"逐渐缩量|缩量", "/images/kxian/v2o-26.png"),
    (r"量平", "/images/kxian/v2o-29.png"),
    # 5日均线
    (r"5日|五日", "/images/kxian/v2o-01.png"),
]

def find_img(text):
    for pat, img in KEYWORD_IMG:
        if re.search(pat, text):
            return img
    return None

# Process: find exercise lines, check if image follows within next 6 lines
output = []
i = 0
inserted = 0
while i < len(lines):
    line = lines[i]
    output.append(line)
    m = re.match(r'^\*\*习题(\d+)\*\*[：:]', line.strip())
    if m:
        # Look ahead up to 6 lines for image
        block = ''.join(lines[i+1:i+7])
        if '![' not in block:
            # No image - find matching one
            # Collect exercise question + answer text for keyword matching
            context = line
            for j in range(i+1, min(i+10, len(lines))):
                context += lines[j]
                if lines[j].strip().startswith('**解答**') or lines[j].strip().startswith('**参考答案**'):
                    break
            img = find_img(context)
            if img is None:
                # Default: use a generic K-line chart
                img = "/images/kxian/v1o-01.png"
            # Insert image after the exercise line (before answer block)
            # Find where answer starts
            insert_pos = len(output)  # after current line
            # Skip blank lines and option lines (A/B) to find answer start
            k = i + 1
            while k < len(lines) and k < i + 8:
                s = lines[k].strip()
                if s.startswith('>') or s.startswith('**参考答案**') or s.startswith('**解答**'):
                    break
                k += 1
            # Insert before answer block
            # We need to insert into output before the answer lines we haven't processed yet
            # Since output already has current line, we'll insert image after blank line
            # Find the position in output where answer starts
            # Simpler: just append image right after exercise line
            output.append('\n')
            output.append(f'![{img}]({img})\n')
            output.append('\n')
            inserted += 1
    i += 1

open(MD, 'w', encoding='utf-8').write(''.join(output))
print(f"Inserted {inserted} exercise images")
