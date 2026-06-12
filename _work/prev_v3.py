# -*- coding: utf-8 -*-
import fitz, os
PDF = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\preview_v3.pdf"
OUT = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work"
doc = fitz.open(PDF)
print("PAGES:", doc.page_count)
for p in [1, 2]:
    pix = doc[p].get_pixmap(matrix=fitz.Matrix(1.95,1.95))
    fn = os.path.join(OUT, f"v3_p{p+1}.png"); pix.save(fn); print("saved", fn)
doc.close()
