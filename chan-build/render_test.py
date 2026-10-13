import pymupdf
pdf = r"E:\生活\股票操练大全全套\超高清无水印《市场哲学的数学原理完全配图手册》2017(1).pdf"
doc = pymupdf.open(pdf)
print("total pages:", doc.page_count)
for pno, zoom in [(12, 2.0), (12, 2.5), (12, 3.0)]:
    page = doc[pno]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    out = rf"E:\生活\股票操练大全全套\chan-build\test-render\p{pno+1:03d}_z{zoom}.png"
    pix.save(out)
    print("saved", out, pix.width, "x", pix.height)
