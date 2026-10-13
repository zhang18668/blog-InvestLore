import urllib.request
pages = ["chan-index", "chan-ch01", "chan-ch54", "chan-ch94", "chan-ch108"]
kws = ["chanlun.taobao", "铜版纸", "273237639", "gqoqqq", "购买网址", "作者主页", "QQ群"]
lines = []
for p in pages:
    url = "https://blog.zhangzhh13.xyz/2026/10/12/%s/" % p
    html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "ignore")
    hits = [k for k in kws if k in html]
    lines.append("%s 广告=%s 图引用=%d" % (p, hits if hits else "无", html.count("images/chan/")))
open(r"E:\生活\股票操练大全全套\chan-build\online-check.txt", "w", encoding="utf-8").write("\n".join(lines))
print("written")
