import os, re, sys
base = r"E:\生活\股票操练大全全套\stock-blog\source"
img_root = os.path.join(base, "images", "chan")
posts = os.path.join(base, "_posts")
problems = []
total_files = 0
total_refs = 0
noimg_lessons = []
for n in range(1, 109):
    d = os.path.join(img_root, f"chan-ch{n:02d}")
    md = os.path.join(posts, f"chan-ch{n:02d}.md")
    if not os.path.isfile(md):
        problems.append(f"ch{n:02d}: md 缺失"); continue
    files = sorted([f for f in os.listdir(d) if f.endswith(".png")]) if os.path.isdir(d) else []
    total_files += len(files)
    with open(md, encoding="utf-8") as fh:
        text = fh.read()
    refs = re.findall(r"!\[\]\(/images/chan/chan-ch%02d/chan-ch%02d-(\d+)\.png\)" % (n, n), text)
    total_refs += len(refs)
    # 检查引用路径与文件匹配
    for r in refs:
        if f"chan-ch{n:02d}-{r}.png" not in files:
            problems.append(f"ch{n:02d}: 引用 chan-ch{n:02d}-{r}.png 但文件缺失")
    # 编号连续性
    nums = sorted(int(x) for x in refs)
    if nums != list(range(1, len(nums)+1)):
        problems.append(f"ch{n:02d}: 引用编号不连续 {nums}")
    # front matter 结构
    for key in ["title:", "date:", "tags:", "categories:", "series:", "description:", "top_img:", 'class="summary-card"', 'class="post-nav"']:
        if key not in text:
            problems.append(f"ch{n:02d}: 缺 {key}")
    # 广告残留
    for kw in ["chanlun.taobao", "铜版纸", "273237639", "gqoqqq", "购买网址", "作者主页"]:
        if kw in text:
            problems.append(f"ch{n:02d}: md 广告关键词 {kw}")
    if not refs:
        noimg_lessons.append(n)
print(f"图片文件总数: {total_files}")
print(f"md 引用总数: {total_refs}")
print(f"无图课程: {noimg_lessons}")
print(f"问题数: {len(problems)}")
for p in problems[:40]:
    print(" -", p)
sys.exit(0)
