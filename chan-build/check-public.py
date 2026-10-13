import io, re, os
names = ["chan-ch94", "chan-ch01", "chan-ch54", "chan-ch108", "chan-ch09", "chan-ch61"]
base = r"E:\生活\股票操练大全全套\stock-blog\public"
for name in names:
    p = os.path.join(base, "2026", "10", "12", name, "index.html")
    t = io.open(p, encoding="utf-8").read()
    refs = re.findall(r"/images/chan/(chan-ch\d+)/chan-ch\d+-\d+\.png", t)
    missing = []
    for m in re.findall(r"/images/(chan/chan-ch\d+/chan-ch\d+-\d+\.png)", t):
        fp = os.path.join(base, "images", m.replace("/", "\\"))
        if not os.path.isfile(fp):
            missing.append(m)
    print(name, "refs=", len(refs), "missing=", len(missing), "样例:", refs[:2])
