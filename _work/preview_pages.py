# -*- coding: utf-8 -*-
import fitz, os
PDF = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\preview.pdf"
OUT = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work"
doc = fitz.open(PDF)
# find first explanation page by scanning text for '제2부'
exp_start = None
for p in range(doc.page_count):
    if "제2부" in doc[p].get_text():
        exp_start = p; break
print("explanation section starts at page", (exp_start+1) if exp_start is not None else "?")
# find last page (audit)
audit = None
for p in range(doc.page_count-1, -1, -1):
    if "제3부" in doc[p].get_text():
        audit = p; break
print("audit page", (audit+1) if audit is not None else "?")
targets = [exp_start, exp_start+1] if exp_start is not None else []
if audit is not None: targets.append(audit)
for p in targets:
    pix = doc[p].get_pixmap(matrix=fitz.Matrix(2.0,2.0))
    fn = os.path.join(OUT, f"exp_p{p+1}.png")
    pix.save(fn); print("saved", fn)
doc.close()
