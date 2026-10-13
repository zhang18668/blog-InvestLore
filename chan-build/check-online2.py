import urllib.request, io, re
from PIL import Image

# 1) 线上页面广告残留检查
pages = ["chan-index", "chan-ch01", "chan-ch54", "chan-ch94", "chan-ch108"]
kws = ["chanlun.taobao", "铜版纸", "273237639", "gqoqqq", "购买网址", "作者主页", "QQ群"]
for p in pages:
    url = "https://blog.zhangzhh13.xyz/2026/10/12/%s/" % p
    html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "ignore")
    hits = [k for k in kws if k in html]
    print(p, "广告命中:", hits if hits else "无", "| 图引用数:", html.count("images/chan/"))

# 2) 线上图片 PNG 完整性（下载解码）
for i in ["chan-ch01/chan-ch01-01.png", "chan-ch54/chan-ch54-55.png", "chan-ch108/chan-ch108-08.png"]:
    url = "https://blog.zhangzhh13.xyz/images/chan/" + i
    data = urllib.request.urlopen(url, timeout=60).read()
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        print(i, "PNG完整:", im.size, im.format)
    except Exception as e:
        print(i, "PNG损坏:", e)
