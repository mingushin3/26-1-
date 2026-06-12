# -*- coding: utf-8 -*-
"""일타강사 시험 정리본 빌더.
입력: _work/studyguide/{code}.json (14개 섹션) + exam50.json + all87.json
출력: 생명의과학세미나_기말_정리본(일타강사).html  (단일 인쇄용 A4, 도식 base64 임베드)
함정표(traps)가 본문의 중심. 부록에 v3 50문항 커버리지 검증표."""
import fitz, os, json, base64, html, re, io
from collections import Counter
from PIL import Image

BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
WORK = os.path.join(BASE, "_work")
SG = os.path.join(WORK, "studyguide")
FIGDIR = os.path.join(BASE, "_figures"); os.makedirs(FIGDIR, exist_ok=True)
OUT = os.path.join(BASE, "생명의과학세미나_기말_정리본(일타강사).html")

ORDER = ["wonjaelee","golgi","bloodomics","scrna","llmngs","genetherapy","ev",
         "nanomrna","dpath","thyroid","tert","brain","immuno","gastric"]
SHORT = {
 "wonjaelee":"암생물학 패러다임","golgi":"골지체","bloodomics":"혈액암 오믹스","scrna":"scRNAseq",
 "llmngs":"LLM·NGS·정밀의료","genetherapy":"유전자치료","ev":"세포외소포(EV)","nanomrna":"나노·mRNA-LNP",
 "dpath":"디지털병리","thyroid":"갑상선암 CYFRA","tert":"TERT·B형간염·간암","brain":"신경외과·뇌종양",
 "immuno":"면역항암·간암저항성","gastric":"위암 맞춤치료"}

_figcache = {}
def render_fig(pdf_name, page):
    key = (pdf_name, int(page))
    if key in _figcache: return _figcache[key]
    p = os.path.join(BASE, pdf_name)
    if not os.path.exists(pdf_name) and not os.path.exists(p):
        # fuzzy
        import glob as _g
        stem = re.sub(r"[^0-9A-Za-z가-힣]","",os.path.basename(pdf_name))[:8]
        cand = [f for f in _g.glob(os.path.join(BASE,"*.pdf")) if stem and stem in re.sub(r"[^0-9A-Za-z가-힣]","",os.path.basename(f))]
        p = cand[0] if cand else None
    elif os.path.exists(pdf_name): p = pdf_name
    if not p:
        _figcache[key] = (None,"missing"); return _figcache[key]
    try:
        doc = fitz.open(p); pno = max(1,min(int(page),doc.page_count))-1; pg = doc[pno]; rect = pg.rect
        dirs = Counter()
        for bl in pg.get_text("dict").get("blocks",[]):
            for ln in bl.get("lines",[]): dirs[tuple(round(x) for x in ln.get("dir",(1,0)))] += len(ln.get("spans",[]) or [1])
        dom = dirs.most_common(1)[0][0] if dirs else (1,0)
        zoom = max(min(2.2,1500.0/max(1.0,rect.width)),1.4)
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom,zoom),alpha=False)
        img = Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
        if dom==(0,1): img = img.transpose(Image.ROTATE_90)
        elif dom==(0,-1): img = img.transpose(Image.ROTATE_270)
        elif dom==(-1,0): img = img.transpose(Image.ROTATE_180)
        if img.width>1500: img = img.resize((1500,round(img.height*1500/img.width)),Image.LANCZOS)
        buf = io.BytesIO(); img.save(buf,format="JPEG",quality=82); jpg = buf.getvalue()
        doc.close()
        b64 = base64.b64encode(jpg).decode("ascii")
        _figcache[key] = (b64,"ok"); return _figcache[key]
    except Exception as e:
        _figcache[key] = (None,f"err {e}"); return _figcache[key]

def esc(s): return html.escape(str(s if s is not None else ""))

# load
sections = {}
for code in ORDER:
    p = os.path.join(SG, f"{code}.json")
    sections[code] = json.load(open(p, encoding="utf-8"))
exam50 = json.load(open(os.path.join(SG,"exam50.json"), encoding="utf-8"))
all87 = json.load(open(os.path.join(SG,"all87.json"), encoding="utf-8"))
top50_ids = {q["id"] for q in exam50}

# coverage cross-check
covered = set()
for code in ORDER:
    for t in sections[code].get("traps",[]): covered.add(t.get("qref"))
miss50 = [q["id"] for q in exam50 if q["id"] not in covered]
miss87 = [q["id"] for q in all87 if q["id"] not in covered]

CIRC = ["①","②","③","④","⑤","⑥"]
P = []
P.append("""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>생명의과학세미나 기말 — 일타강사 시험 정리본</title>
<style>
:root{--ink:#1a1a1a;--mut:#555;--line:#c4c4c4;--red:#c62828;--grn:#1b7a3d;--acc:#0d47a1;--box:#f5f7fa;--ylw:#fff8e1;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;color:var(--ink);font-family:"Malgun Gothic","맑은 고딕",AppleGothic,sans-serif;font-size:9.6pt;line-height:1.38;}
@page{size:A4;margin:11mm 10mm 12mm 10mm;}
.page{page-break-after:always;}
.apxpage{page-break-before:always;}
.lec{margin-top:3mm;}
.lec h2{break-after:avoid;page-break-after:avoid;}
h1{font-size:18pt;margin:0 0 2mm;}
h2{font-size:13pt;margin:0 0 2mm;color:#fff;background:var(--acc);padding:2mm 3mm;border-radius:4px;}
.sec{break-inside:avoid;}
.lead{color:var(--mut);font-size:9.2pt;margin:0 0 3mm;}
.essence{background:var(--box);border-left:4px solid var(--acc);border-radius:4px;padding:2mm 3mm;margin:1.6mm 0;break-inside:avoid;}
.essence .e{font-weight:700;} .essence .a{color:#7a3b00;margin-top:0.8mm;}
.ana{font-style:italic;}
.cpt{margin:2mm 0 1mm;break-inside:avoid;}
.cpt h3{font-size:10.3pt;margin:1.6mm 0 1mm;color:var(--acc);border-bottom:1px dashed var(--line);padding-bottom:0.5mm;}
ul.pts{margin:0.8mm 0 1mm;padding-left:5mm;} ul.pts li{margin:0.5mm 0;}
table{border-collapse:collapse;width:100%;font-size:8.5pt;margin:1.2mm 0;}
thead{display:table-header-group;}
tr{break-inside:avoid;page-break-inside:avoid;}
th,td{border:1px solid var(--line);padding:1.3mm 1.8mm;vertical-align:top;text-align:left;}
th{background:var(--box);font-weight:700;}
.ctab{break-inside:avoid;} .ctab caption{font-weight:700;font-size:8.8pt;text-align:left;margin-bottom:0.8mm;color:#333;}
.traphead{margin:2.4mm 0 1mm;font-weight:800;font-size:10.2pt;color:var(--red);break-after:avoid;page-break-after:avoid;}
.traptab th.ttopic{width:20%;} .traptab th.tok{width:42%;} .traptab th.tno{width:38%;}
.traptab td.ok{background:#eafaf0;} .traptab td.no{background:#fdecec;}
.traptab .qb{display:inline-block;font-size:7.4pt;color:#444;background:#eef;border:1px solid #ccd;border-radius:3px;padding:0 3px;margin-right:3px;}
.traptab .q50{background:#fff3cd;border-color:#e0c200;color:#7a5b00;font-weight:700;}
.memo{background:var(--ylw);border:1px solid #ffe082;border-radius:4px;padding:2mm 3mm;margin:2.5mm 0 1mm;}
.memo b{color:#7a5b00;}
.memo ul{margin:1mm 0 0;padding-left:5mm;} .memo li{margin:0.5mm 0;font-weight:600;}
figure{margin:1.6mm 0;text-align:center;break-inside:avoid;} figure img{max-width:68%;max-height:72mm;border:1px solid var(--line);border-radius:3px;}
figcaption{font-size:7.8pt;color:var(--mut);margin-top:0.6mm;}
.badge{display:inline-block;font-size:8pt;background:#fff;border:1px solid var(--line);border-radius:3px;padding:0 5px;margin-left:5px;color:#333;vertical-align:middle;}
.toc{column-count:2;column-gap:7mm;font-size:9pt;}
.toc div{margin:0.8mm 0;break-inside:avoid;}
.toc .n{display:inline-block;width:6mm;color:var(--acc);font-weight:700;}
.note{font-size:8.6pt;color:var(--mut);}
.apx td,.apx th{font-size:8.3pt;padding:1.2mm 1.6mm;}
.apx .c{text-align:center;} .ok2{color:var(--grn);font-weight:700;} .x2{color:var(--red);font-weight:700;}
hr.s{border:none;border-top:1px solid var(--line);margin:3mm 0;}
</style></head><body>""")

# ===== COVER =====
P.append('<div class="page">')
P.append('<h1>26년 1학기 「생명의과학세미나」 기말 — <span style="color:#0d47a1">일타강사 시험 정리본</span></h1>')
P.append('<p class="lead">14개 강의 핵심을 "먹기 좋게" 압축. 본문의 중심은 <b style="color:#c62828">⚠️ 함정 방향표</b> — '
         '예상 모의고사 v3(50문항)는 <b>전 문항 「옳지 않은 것은?」 5지선다</b>이고, 정답(틀린 선지)은 항상 '
         '<b>옳은 방향을 거꾸로 뒤집은 진술</b>이다. 그 "올바른 방향(✅)"을 모두 박아두었으니, 표를 거꾸로 한 선지만 고르면 된다.</p>')
P.append('<div class="essence"><div class="e">📌 3회독 학습법</div>'
         '<ul class="pts">'
         '<li><b>1회독</b> — 각 강의 🎯본질·비유 + 핵심개념으로 "그림"을 잡는다(이해).</li>'
         '<li><b>2회독</b> — <b style="color:#c62828">함정 방향표</b>의 ✅(올바름)만 집중 암기. ❌(함정)은 "이렇게 나오면 그게 답"이라고 본다.</li>'
         '<li><b>3회독</b> — ✅ 한 줄 암기 + 부록 50문항 표로 self-test. 막히면 해당 강의로 복귀.</li>'
         '</ul></div>')
# mini TOC
P.append('<h2 style="margin-top:3mm">강의 한눈에 (연대순)</h2><div class="toc">')
for i,code in enumerate(ORDER,1):
    s = sections[code]; nt = len(s.get("traps",[]))
    n50 = sum(1 for t in s.get("traps",[]) if t.get("qref") in top50_ids)
    P.append(f'<div><span class="n">{i:02d}</span><b>{esc(s.get("lecture_label",code))}</b> '
             f'<span class="badge">함정 {nt} · 출제50 {n50}</span></div>')
P.append('</div>')
P.append(f'<hr class="s"><p class="note">커버리지: 본 정리본은 검증 풀 전체 <b>{len(all87)}개 지식점</b>을 함정표로 수록했고, '
         f'그중 v3 실제 출제 <b>50문항</b>을 모두 포함한다(부록 검증표 참조). '
         f'범위(C1): 각 강의 슬라이드(닫힌 우주) 한정 · 근거: 슬라이드+녹음. 도식은 원본 슬라이드 캡처.</p>')
P.append('</div>')

# ===== LECTURE SECTIONS =====
for i,code in enumerate(ORDER,1):
    s = sections[code]
    P.append('<div class="lec">')
    nt = len(s.get("traps",[]))
    P.append(f'<h2>강의 {i:02d}. {esc(s.get("lecture_label",code))} '
             f'<span style="float:right;font-size:9pt;font-weight:400">함정 {nt}개</span></h2>')
    # essence + analogy
    P.append('<div class="essence">'
             f'<div class="e">🎯 {esc(s.get("essence",""))}</div>'
             f'<div class="a ana">🍱 {esc(s.get("analogy",""))}</div></div>')
    # concepts
    for c in s.get("concepts",[]):
        P.append('<div class="cpt">')
        P.append(f'<h3>{esc(c.get("heading",""))}</h3>')
        pts = c.get("points",[])
        if pts:
            P.append('<ul class="pts">')
            for pt in pts: P.append(f'<li>{esc(pt)}</li>')
            P.append('</ul>')
        tb = c.get("table")
        if tb and tb.get("rows"):
            P.append('<table class="ctab"><caption>'+esc(tb.get("title",""))+'</caption>')
            P.append('<tr>'+''.join(f'<th>{esc(h)}</th>' for h in tb.get("columns",[]))+'</tr>')
            for row in tb.get("rows",[]):
                P.append('<tr>'+''.join(f'<td>{esc(cell)}</td>' for cell in row)+'</tr>')
            P.append('</table>')
        P.append('</div>')
    # figures (압축: 강의당 가장 결정적 도식 1개)
    seen=set()
    for fg in s.get("figures",[])[:1]:
        pdf = fg.get("pdf"); pageno = fg.get("page")
        if not pdf or not pageno: continue
        if (pdf,pageno) in seen: continue
        seen.add((pdf,pageno))
        b64,st = render_fig(pdf, pageno)
        if b64:
            P.append(f'<figure><img src="data:image/jpeg;base64,{b64}" alt="fig">'
                     f'<figcaption>[그림] {esc(fg.get("caption",""))} · 출처 슬라이드</figcaption></figure>')
    # trap table (centerpiece)
    P.append('<div class="traphead">⚠️ 함정 방향표 — 「옳지 않은 것」은 ❌처럼 거꾸로 나온다</div>')
    P.append('<table class="traptab"><thead><tr><th class="ttopic">지식점</th>'
             '<th class="tok">✅ 이게 맞다 (옳은 선지/정설)</th>'
             '<th class="tno">❌ 이렇게 나오면 그게 답 (함정·틀린 선지)</th></tr></thead><tbody>')
    for t in s.get("traps",[]):
        qref = t.get("qref","")
        q50 = "q50" if qref in top50_ids else ""
        badge = f'<span class="qb {q50}">{esc(qref)}{" ★출제" if qref in top50_ids else ""}</span>'
        P.append('<tr>'
                 f'<td>{badge}<br>{esc(t.get("topic",""))}</td>'
                 f'<td class="ok">{esc(t.get("correct",""))}</td>'
                 f'<td class="no">{esc(t.get("trap",""))}</td></tr>')
    P.append('</tbody></table>')
    # memorize
    mem = s.get("memorize",[])
    if mem:
        P.append('<div class="memo"><b>✅ 시험장 직전 한 줄 암기</b><ul>')
        for m in mem: P.append(f'<li>{esc(m)}</li>')
        P.append('</ul></div>')
    P.append('</div>')

# ===== APPENDIX: 50-Q coverage =====
P.append('<div class="apxpage"><h2>부록. v3 예상 모의고사 50문항 커버리지 검증표</h2>')
P.append(f'<p class="note">아래 50문항(출제확률 순)이 본 정리본 어디서 풀리는지 매핑. '
         f'커버: <b class="ok2">{50-len(miss50)}/50</b>'
         + (f' · <b class="x2">미커버 {miss50}</b>' if miss50 else ' (전 문항 함정표 수록 ✓)')
         + '. 각 행의 「정리본 위치」 = 해당 강의 함정표의 그 qref 행(✅ 방향을 그대로, 시험은 거꾸로).</p>')
P.append('<table class="apx"><thead><tr><th class="c">문</th><th>강의</th><th>지식점</th>'
         '<th>✅ 정답 방향(요약)</th><th class="c">정리본 위치</th><th class="c">수록</th></tr></thead><tbody>')
for q in exam50:
    code = q["lecture_key"]; qref = q["id"]
    cf = q.get("correct_fact","") or q.get("topic","")
    cf = re.sub(r"\s+"," ",cf).strip()
    if len(cf)>150: cf = cf[:150]+"…"
    inc = qref in covered
    P.append('<tr>'
             f'<td class="c">{q["num"]}</td>'
             f'<td>{esc(SHORT.get(code,code))}</td>'
             f'<td>{esc(q.get("topic",""))}</td>'
             f'<td>{esc(cf)}</td>'
             f'<td class="c">{esc(SHORT.get(code,code))} ▸ <b>{esc(qref)}</b></td>'
             f'<td class="c">{"<span class=ok2>✓</span>" if inc else "<span class=x2>✗</span>"}</td></tr>')
P.append('</tbody></table>')
P.append(f'<p class="note">본 정리본은 v3 50문항 외에 검증 풀의 보완문항까지 합쳐 총 {len(all87)}개 지식점을 함정표로 포괄한다. '
         f'전 87개 지식점 커버: {87-len(miss87)}/87.</p>')
P.append('</div></body></html>')

open(OUT,"w",encoding="utf-8").write("\n".join(P))
print("OUTPUT:", OUT)
print("size:", os.path.getsize(OUT), "bytes")
print("covered top50:", 50-len(miss50), "/50  miss:", miss50)
print("covered all87:", 87-len(miss87), "/87  miss:", miss87)
print("figures rendered:", {k: v[1] for k,v in _figcache.items()})
