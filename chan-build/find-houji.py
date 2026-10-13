import re
h = open(r"E:\生活\股票操练大全全套\chan-build\dl-chan-ch54.html", encoding="utf-8").read()
i = h.find("后记")
while i != -1:
    seg = h[max(0,i-150):i+60].replace("\n"," ")
    print("--- idx", i, "---")
    print(seg[:220])
    i = h.find("后记", i+1)
    if i > 100000: break
