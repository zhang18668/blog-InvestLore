import pymupdf
pdf = r"E:\生活\股票操练大全全套\超高清无水印《市场哲学的数学原理完全配图手册》2017(1).pdf"
doc = pymupdf.open(pdf)
outdir = r"E:\生活\股票操练大全全套\chan-build\verify-tail"
import os
os.makedirs(outdir, exist_ok=True)
for pno in [352, 356, 687, 689, 692, 702, 706, 712]:
    page = doc[pno]  # 0-based: PDF 353, 357, 688, 690, 693, 703, 707, 713
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2.0, 2.0))
    pix.save(os.path.join(outdir, f"pdf{pno+1:03d}.png"))
    print("saved pdf", pno+1)
