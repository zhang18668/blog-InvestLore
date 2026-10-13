# -*- coding: utf-8 -*-
import re, os
posts = r'E:\生活\股票操练大全全套\stock-blog\source\_posts'
imgroot = r'E:\生活\股票操练大全全套\stock-blog\source'
missing = []
total = 0
per = {}
for n in range(95, 109):
    f = os.path.join(posts, f'chan-ch{n}.md')
    c = open(f, encoding='utf-8').read()
    refs = re.findall(r'!\[\]\((/images/chan/[^)]+)\)', c)
    per[n] = len(refs)
    for r in refs:
        total += 1
        p = os.path.join(imgroot, r.lstrip('/'))
        if not os.path.exists(p):
            missing.append((n, r))
print('total refs:', total)
print('per chapter:', per)
print('missing:', missing)
# check numbering continuity per chapter
for n in range(95, 109):
    f = os.path.join(posts, f'chan-ch{n}.md')
    c = open(f, encoding='utf-8').read()
    nums = [int(x) for x in re.findall(rf'chan-ch{n}-(\d+)\.png', c)]
    expected = list(range(1, len(nums)+1))
    if nums != expected:
        print('NUMBERING GAP ch', n, nums)
print('numbering check done')
# check front matter integrity: count fields
for n in range(95, 109):
    c = open(os.path.join(posts, f'chan-ch{n}.md'), encoding='utf-8').read()
    fm = c.split('---')[1]
    for k in ['title:', 'date:', 'tags:', 'categories:', 'series:', 'description:', 'top_img:']:
        if k not in fm:
            print('FM MISSING ch', n, k)
    if 'class="summary-card"' not in c:
        print('summary-card missing ch', n)
    if 'class="post-nav"' not in c:
        print('post-nav missing ch', n)
print('fm/nav check done')
