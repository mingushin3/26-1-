# -*- coding: utf-8 -*-
import fitz, os, glob, json, re
from PIL import Image
from collections import Counter
BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
FIG = os.path.join(BASE, "_figures")
print("=== rendered figure dimensions ===")
for f in sorted(glob.glob(os.path.join(FIG, "*.jpg"))):
    im = Image.open(f); w,h = im.size
    print(f"  {os.path.basename(f):28s} {w}x{h}  {'PORTRAIT(의심)' if h>w else 'landscape'}")

# For each figure's source page, report page.rotation and dominant text direction
V = os.path.join(BASE, "_work", "verified")
def loadloose(p):
    t=open(p,encoding='utf-8').read().strip()
    a,b=t.find('['),t.rfind(']')
    return json.loads(t[a:b+1])
def resolve(name):
    p=os.path.join(BASE,name)
    if os.path.exists(p): return p
    h=glob.glob(os.path.join(BASE, os.path.basename(name)))
    return h[0] if h else None
print("\n=== source page orientation/rotation/text-dir ===")
seen=set()
for k in ["wonjaelee","golgi","bloodomics","scrna","llmngs","genetherapy","ev","nanomrna","dpath","thyroid","tert","brain","immuno","gastric"]:
    fp=os.path.join(V,k+".json")
    if not os.path.exists(fp): continue
    for q in loadloose(fp):
        fg=q.get("figure") or {}
        if not (fg.get("needed") and fg.get("pdf")): continue
        pdf=resolve(fg["pdf"]);
        if not pdf: continue
        key=(fg["pdf"],fg.get("page"))
        if key in seen: continue
        seen.add(key)
        doc=fitz.open(pdf); pno=max(1,min(int(fg.get("page",1)),doc.page_count))-1
        pg=doc[pno]; r=pg.rect
        dirs=Counter()
        d=pg.get_text("dict")
        for bl in d.get("blocks",[]):
            for ln in bl.get("lines",[]):
                dr=tuple(round(x) for x in ln.get("dir",(1,0)))
                dirs[dr]+=1
        dom=dirs.most_common(1)[0][0] if dirs else (1,0)
        try: rot=pg.rotation
        except Exception: rot='NA'
        doc.close()
        ori = 'portrait' if r.height>r.width else 'landscape'
        print(f"  {k:11s} {os.path.basename(pdf)[:30]:30s} p{fg.get('page'):>3} {ori:9s} rot={rot} domdir={dom}")
