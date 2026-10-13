import urllib.request
imgs = [
    "chan-ch01/chan-ch01-01.png", "chan-ch01/chan-ch01-03.png",
    "chan-ch33/chan-ch33-01.png", "chan-ch54/chan-ch54-55.png",
    "chan-ch94/chan-ch94-01.png", "chan-ch94/chan-ch94-02.png",
    "chan-ch108/chan-ch108-08.png", "chan-ch60/chan-ch60-03.png",
    "chan-ch84/.keep",  # 不存在，预期404
]
for i in imgs:
    url = "https://blog.zhangzhh13.xyz/images/chan/" + i
    try:
        req = urllib.request.Request(url, method="HEAD")
        r = urllib.request.urlopen(req, timeout=30)
        size = r.headers.get("Content-Length", "?")
        print(i, "->", r.status, "size=", size)
    except Exception as e:
        code = getattr(e, "code", None)
        print(i, "-> ERR", code, str(e)[:80])
