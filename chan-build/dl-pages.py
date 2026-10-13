import urllib.request
for p in ["chan-ch54", "chan-index"]:
    url = "https://blog.zhangzhh13.xyz/2026/10/12/%s/" % p
    html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "ignore")
    open(r"E:\生活\股票操练大全全套\chan-build\dl-%s.html" % p, "w", encoding="utf-8").write(html)
    print(p, "len=", len(html), "has_title_教你炒股票54:", "教你炒股票54" in html, "has_航天机电:", "航天机电" in html, "has_houji:", "后记" in html)
