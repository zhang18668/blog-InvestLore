import urllib.request, re
for p in ["chan-index", "chan-ch54"]:
    url = "https://blog.zhangzhh13.xyz/2026/10/12/%s/" % p
    html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "ignore")
    out = []
    for kw in ["chanlun.taobao", "QQ群", "铜版纸", "购买网址", "273237639"]:
        for m in re.finditer(re.escape(kw), html):
            s = max(0, m.start()-80)
            ctx = html[s:m.end()+80].replace("\n", " ")
            out.append("[%s] ...%s..." % (kw, ctx))
    open(r"E:\生活\股票操练大全全套\chan-build\ctx-%s.txt" % p, "w", encoding="utf-8").write("\n".join(out) if out else "NO_HITS")
print("done")
