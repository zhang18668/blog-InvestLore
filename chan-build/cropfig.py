import sys, os
from PIL import Image

SRC = r"E:\生活\股票操练大全全套\chan-build\work-fig-课30-36"
DST = r"E:\生活\股票操练大全全套\stock-blog\source\images\chan"

def crop_page(pdf_page, out_name, box, ads=None):
    """box/ads 用千分比 (l,t,r,b)。ads: list of (l,t,r,b) 涂白区域。"""
    p = os.path.join(SRC, f"p{pdf_page:03d}.png")
    im = Image.open(p).convert("RGB")
    W, H = im.size
    l, t, r, b = box
    crop = im.crop((int(l/1000*W), int(t/1000*H), int(r/1000*W), int(b/1000*H)))
    cw, ch = crop.size
    if ads:
        for (al, at, ar, ab) in ads:
            cl = int((al-l)/(r-l)*cw)
            cr = int((ar-l)/(r-l)*cw)
            ct = int((at-t)/(b-t)*ch)
            cb = int((ab-t)/(b-t)*ch)
            crop.paste((255,255,255), (cl, ct, cr, cb))
    outdir = os.path.join(DST, out_name.rsplit("-", 1)[0])
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, out_name)
    crop.save(out)
    print("saved", out, crop.size)

if __name__ == "__main__":
    # 用法: python cropfig.py <pdf_page> <out_name> <l,t,r,b> [al,at,ar,ab ...]
    pdf_page = int(sys.argv[1])
    out_name = sys.argv[2]
    nums = [float(x) for x in ",".join(sys.argv[3:]).split(",") if x.strip()]
    box = tuple(nums[:4])
    ads = []
    rest = nums[4:]
    for i in range(0, len(rest), 4):
        ads.append(tuple(rest[i:i+4]))
    crop_page(pdf_page, out_name, box, ads)
