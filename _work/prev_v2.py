# -*- coding: utf-8 -*-
import fitz, os
PDF = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\preview_v2.pdf"
OUT = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work"
doc = fitz.open(PDF)
print("PAGES:", doc.page_count)
exp = next((p for p in range(doc.page_count) if "제2부" in doc[p].get_text()), None)
aud = next((p for p in range(doc.page_count-1,-1,-1) if "제3부" in doc[p].get_text()), None)
print("문제집 p2~", (exp), " 해설집 시작", (exp+1) if exp is not None else "?", " 자가검수", (aud+1) if aud is not None else "?")
for p in [2, exp+1 if exp else 18, aud]:
    if p is None: continue
    pix = doc[p].get_pixmap(matrix=fitz.Matrix(1.9,1.9))
    fn = os.path.join(OUT, f"v2_p{p+1}.png"); pix.save(fn); print("saved", fn)
doc.close()
