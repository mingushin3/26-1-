# -*- coding: utf-8 -*-
"""일타강사 시험 정리본 v2 빌더 (레이어드 구조).
입력: _work/studyguide_v2/{code}.json (14) + _work/studyguide/exam50.json + all87.json
구조(강의당): 🎯한 줄 핵심 → 📋시험범위 배너 → 🍱비유 → ⭐출제1순위 TOP 2-3 카드(쉬운설명+출제포인트)
            → ➕추가 함정 체크(압축) → 그림 → ✅한 줄 암기
표지: 3회독 학습법 + 교수님 시험범위 한눈에 표 + 연대순 TOC. 부록: v3 50문항 커버리지 검증표.
출력: 생명의과학세미나_기말_정리본_v2(일타강사).html (도식 base64 임베드, A4 인쇄용)."""
import fitz, os, json, base64, html, re, io
from collections import Counter
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SGV2 = os.path.join(BASE, "_work", "studyguide_v2")
SG   = os.path.join(BASE, "_work", "studyguide")
OUT  = os.path.join(BASE, "생명의과학세미나_기말_정리본_v2(일타강사).html")

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
    if not os.path.exists(p):
        import glob as _g
        stem = re.sub(r"[^0-9A-Za-z가-힣]","",os.path.basename(pdf_name))[:8]
        cand = [f for f in _g.glob(os.path.join(BASE,"*.pdf")) if stem and stem in re.sub(r"[^0-9A-Za-z가-힣]","",os.path.basename(f))]
        p = cand[0] if cand else None
    if not p or not os.path.exists(p):
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
        _figcache[key] = (base64.b64encode(jpg).decode("ascii"),"ok"); return _figcache[key]
    except Exception as e:
        _figcache[key] = (None,f"err {e}"); return _figcache[key]

def esc(s): return html.escape(str(s if s is not None else ""))
def clean(s):
    """선행 ✅/❌/✔/✗ 및 공백 제거 (열 헤더에서 부호를 제공하므로)."""
    return re.sub(r"^\s*[✅❌✔✗☑️·\-—\s]+","", str(s or "")).strip()

# ── load ──
sections = {}
for code in ORDER:
    sections[code] = json.load(open(os.path.join(SGV2, f"{code}.json"), encoding="utf-8"))
exam50 = json.load(open(os.path.join(SG,"exam50.json"), encoding="utf-8"))
all87  = json.load(open(os.path.join(SG,"all87.json"), encoding="utf-8"))
top50_ids = {q["id"] for q in exam50}

# coverage: v2 어디에 그 qref가 있나
covered = set()
for code in ORDER:
    s = sections[code]
    for t in s.get("top_topics",[]): covered.add(t.get("qref"))
    for c in s.get("checklist",[]):  covered.add(c.get("qref"))
miss50 = [q["id"] for q in exam50 if q["id"] not in covered]
miss87 = [q["id"] for q in all87  if q["id"] not in covered]

CIRC = ["①","②","③","④","⑤","⑥","⑦","⑧"]
P = []
P.append("""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>생명의과학세미나 기말 — 일타강사 시험 정리본 v2</title>
<style>
:root{--ink:#1c1c1c;--mut:#5a5a5a;--line:#cfcfcf;--red:#c62828;--grn:#1b7a3d;--acc:#0d47a1;--acc2:#1565c0;
--box:#f3f6fb;--ylw:#fff8e1;--grnbg:#e9f7ee;--cardbg:#fbfcfe;--okbg:#eafaf0;--nobg:#fdecec;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;color:var(--ink);font-family:"Malgun Gothic","맑은 고딕",AppleGothic,"Apple SD Gothic Neo",sans-serif;font-size:10pt;line-height:1.5;}
@page{size:A4;margin:12mm 11mm 13mm 11mm;}
.page{page-break-after:always;}
.lec{margin-top:4mm;page-break-inside:auto;}
.lec h2{break-after:avoid;page-break-after:avoid;}
h1{font-size:19pt;margin:0 0 3mm;line-height:1.25;}
h2{font-size:13.5pt;margin:0 0 2.5mm;color:#fff;background:linear-gradient(90deg,var(--acc),var(--acc2));padding:2.4mm 3.2mm;border-radius:5px;}
.lead{color:var(--mut);font-size:9.6pt;margin:0 0 3mm;}
/* 🎯 essence */
.essence{background:var(--box);border-left:5px solid var(--acc);border-radius:5px;padding:2.4mm 3.2mm;margin:2mm 0;break-inside:avoid;font-size:10.5pt;}
.essence b{color:var(--acc);}
/* 📋 scope banner */
.scope{border-radius:5px;padding:2.2mm 3.2mm;margin:2mm 0;break-inside:avoid;font-size:9.6pt;}
.scope.decl{background:var(--grnbg);border:1px solid #9ad6b0;border-left:5px solid var(--grn);}
.scope.nodecl{background:#f6f6f6;border:1px solid #ddd;border-left:5px solid #bbb;color:#555;}
.scope .lbl{font-weight:800;color:var(--grn);} .scope.nodecl .lbl{color:#777;}
.scope .q{font-style:italic;color:#33691e;background:#fff;border:1px dashed #9ad6b0;border-radius:4px;padding:1mm 2mm;margin:1mm 0 0;display:block;}
.scope .sm{margin-top:1mm;font-weight:700;}
/* 🍱 analogy */
.analogy{background:#fffdf5;border:1px solid #ffe9a8;border-radius:5px;padding:2mm 3.2mm;margin:2mm 0;break-inside:avoid;}
.analogy b{color:#8a6d00;}
/* TOP topic cards */
.toptitle{margin:3mm 0 1.5mm;font-weight:800;font-size:11pt;color:var(--red);border-bottom:2px solid var(--red);padding-bottom:1mm;break-after:avoid;}
.card{border:1px solid #d6e0f0;border-radius:6px;padding:2.4mm 3mm 2.6mm;margin:2mm 0;background:var(--cardbg);break-inside:avoid;}
.card .ch{font-weight:800;font-size:10.6pt;color:var(--acc);margin-bottom:1mm;}
.card .ch .num{display:inline-block;background:var(--acc);color:#fff;border-radius:50%;width:6.2mm;height:6.2mm;line-height:6.2mm;text-align:center;font-size:9.5pt;margin-right:1.5mm;}
.card .ch .pb{float:right;font-size:8pt;font-weight:700;color:#7a5b00;background:#fff3cd;border:1px solid #e0c200;border-radius:3px;padding:0 5px;}
.card .exp{margin:0.6mm 0;} .card .exp .t{font-weight:700;color:#444;}
.card .how{margin:0.6mm 0;color:#333;}
.card .ep{margin-top:1.4mm;border-top:1px dashed #d0d0d0;padding-top:1.2mm;}
.card .ep .ok{display:block;color:#10632f;} .card .ep .no{display:block;color:#b3261e;margin-top:0.6mm;}
.card .ep b{font-weight:800;}
/* checklist */
.cklhead{margin:2.6mm 0 1mm;font-weight:800;font-size:9.8pt;color:#333;break-after:avoid;}
table{border-collapse:collapse;width:100%;font-size:8.7pt;margin:1mm 0;}
thead{display:table-header-group;}
tr{break-inside:avoid;page-break-inside:avoid;}
th,td{border:1px solid var(--line);padding:1.3mm 1.8mm;vertical-align:top;text-align:left;}
th{background:var(--box);font-weight:700;}
.ckl th.t1{width:24%;} .ckl th.t2{width:40%;} .ckl th.t3{width:36%;}
.ckl td.ok{background:var(--okbg);} .ckl td.no{background:var(--nobg);}
.ckl .qb{display:inline-block;font-size:7.2pt;color:#444;background:#eef;border:1px solid #ccd;border-radius:3px;padding:0 3px;margin-bottom:1px;}
.ckl .q50{background:#fff3cd;border-color:#e0c200;color:#7a5b00;font-weight:700;}
/* memorize */
.memo{background:var(--ylw);border:1px solid #ffe082;border-radius:5px;padding:2.2mm 3.2mm;margin:2.6mm 0 1mm;break-inside:avoid;}
.memo b{color:#7a5b00;} .memo ul{margin:1mm 0 0;padding-left:5mm;} .memo li{margin:0.6mm 0;font-weight:600;}
/* figure */
figure{margin:2mm 0;text-align:center;break-inside:avoid;} figure img{max-width:72%;max-height:74mm;border:1px solid var(--line);border-radius:4px;}
figcaption{font-size:7.8pt;color:var(--mut);margin-top:0.6mm;}
/* cover */
.badge{display:inline-block;font-size:8pt;background:#fff;border:1px solid var(--line);border-radius:3px;padding:0 5px;margin-left:5px;color:#333;vertical-align:middle;}
.toc{column-count:2;column-gap:7mm;font-size:9pt;}
.toc div{margin:0.9mm 0;break-inside:avoid;} .toc .n{display:inline-block;width:6mm;color:var(--acc);font-weight:700;}
.scopetab{font-size:8.6pt;} .scopetab th.s1{width:21%;} .scopetab th.s2{width:13%;} .scopetab th.s3{width:66%;}
.scopetab td.y{color:var(--grn);font-weight:800;text-align:center;} .scopetab td.n{color:#999;text-align:center;}
.note{font-size:8.6pt;color:var(--mut);}
.apxpage{page-break-before:always;}
.apx td,.apx th{font-size:8.3pt;padding:1.2mm 1.6mm;}
.apx .c{text-align:center;} .ok2{color:var(--grn);font-weight:700;} .x2{color:var(--red);font-weight:700;}
hr.s{border:none;border-top:1px solid var(--line);margin:3mm 0;}
</style></head><body>""")

# ===== COVER =====
P.append('<div class="page">')
P.append('<h1>26년 1학기 「생명의과학세미나」 기말 — <span style="color:#0d47a1">일타강사 정리본 v2</span></h1>')
P.append('<p class="lead">14개 강의를 <b>"한 번 읽고 이해되게"</b> 재구성했습니다. 강의마다 ① 🎯한 줄 핵심 → ② 📋교수님이 찍어준 시험범위 → '
         '③ 🍱비유 → ④ <b style="color:#c62828">⭐출제 1순위 TOP 2~3</b>(쉬운 설명+출제 포인트) → ⑤ ➕나머지 함정 압축 체크 → ⑥ ✅한 줄 암기 순서입니다. '
         '예상 모의고사 v3(50문항)는 전부 <b>「옳지 않은 것은?」 5지선다</b>라, 각 카드의 <b style="color:#10632f">✅(맞는 방향)</b>만 머리에 넣으면 '
         '<b style="color:#b3261e">❌(거꾸로 뒤집은 선지)</b>가 곧 정답입니다.</p>')
P.append('<div class="essence"><b>📌 3회독 학습법</b>'
         '<ul style="margin:1mm 0 0;padding-left:5mm;">'
         '<li><b>1회독(이해)</b> — 각 강의 🎯핵심·🍱비유 + ⭐TOP 토픽의 [쉬운 설명]만 읽어 "그림"을 잡는다.</li>'
         '<li><b>2회독(출제 포인트)</b> — TOP 토픽의 🎯출제포인트 ✅/❌ + ➕체크리스트의 ✅만 집중. ❌는 "이렇게 나오면 그게 답".</li>'
         '<li><b>3회독(셀프테스트)</b> — ✅한 줄 암기로 빠르게 훑고, 부록 50문항 표로 자가점검. 막히면 해당 강의로 복귀.</li>'
         '</ul></div>')

# 교수님 시험범위 한눈에
P.append('<h2 style="margin-top:4mm">🎯 교수님이 찍어준 시험범위 한눈에</h2>')
P.append('<table class="scopetab"><thead><tr><th class="s1">강의</th><th class="s2">범위 명시</th><th class="s3">시험범위 / 핵심 포인트</th></tr></thead><tbody>')
for i,code in enumerate(ORDER,1):
    s = sections[code]; sc = s.get("scope",{})
    decl = sc.get("declared")
    ycell = '<td class="y">✔ 명시</td>' if decl else '<td class="n">강조신호</td>'
    P.append(f'<tr><td><b>{i:02d}.</b> {esc(SHORT.get(code,code))}</td>{ycell}<td>{esc(clean(sc.get("summary","")))}</td></tr>')
P.append('</tbody></table>')

# 미니 TOC
P.append('<h2 style="margin-top:4mm">강의 한눈에 (연대순)</h2><div class="toc">')
for i,code in enumerate(ORDER,1):
    s = sections[code]; nt = len(s.get("top_topics",[])); nc = len(s.get("checklist",[]))
    n50 = sum(1 for q in (s.get("top_topics",[])+s.get("checklist",[])) if q.get("qref") in top50_ids)
    P.append(f'<div><span class="n">{i:02d}</span><b>{esc(s.get("lecture_label",code))}</b> '
             f'<span class="badge">TOP {nt} · 체크 {nc} · 출제50 {n50}</span></div>')
P.append('</div>')
P.append(f'<hr class="s"><p class="note">커버리지: 본 정리본은 검증 풀 <b>{len(all87)}개 지식점</b> 중 v3 실제 출제 <b>50문항</b>을 '
         f'<b class="ok2">{50-len(miss50)}/50</b> 수록(부록 검증표). '
         f'범위(C1): 각 강의 슬라이드(닫힌 우주) 한정 · 근거: 슬라이드+녹음. 도식은 원본 슬라이드 캡처.</p>')
P.append('</div>')

# ===== LECTURE SECTIONS =====
for i,code in enumerate(ORDER,1):
    s = sections[code]
    P.append('<div class="lec">')
    tops = s.get("top_topics",[]); ckl = s.get("checklist",[])
    P.append(f'<h2>강의 {i:02d}. {esc(s.get("lecture_label",code))} '
             f'<span style="float:right;font-size:9pt;font-weight:400">출제 1순위 {len(tops)}개</span></h2>')
    # 🎯 essence
    P.append(f'<div class="essence">🎯 <b>한 줄 핵심</b> — {esc(s.get("essence",""))}</div>')
    # 📋 scope
    sc = s.get("scope",{})
    if sc.get("declared"):
        q = clean(sc.get("quote",""))
        P.append('<div class="scope decl"><span class="lbl">📋 교수님이 못박은 시험범위</span>'
                 + (f'<span class="q">“{esc(q)}”</span>' if q else '')
                 + f'<div class="sm">→ {esc(clean(sc.get("summary","")))}</div></div>')
    else:
        P.append('<div class="scope nodecl"><span class="lbl">📋 시험범위</span> '
                 + esc(clean(sc.get("summary","명시적 범위 선언 없음 — 강조신호 기반 선정")))+'</div>')
    # 🍱 analogy
    if s.get("analogy"):
        P.append(f'<div class="analogy">🍱 <b>한 입 비유</b> — {esc(s.get("analogy",""))}</div>')
    # ⭐ TOP topics
    P.append('<div class="toptitle">⭐ 출제 1순위 TOP — 이것만은 "이해"하고 가자</div>')
    for j,t in enumerate(tops):
        prob = t.get("exam_probability")
        pb = f'<span class="pb">출제 {prob}%</span>' if prob else ''
        P.append('<div class="card">')
        P.append(f'<div class="ch"><span class="num">{CIRC[j] if j<len(CIRC) else j+1}</span>{esc(t.get("title",""))}{pb}</div>')
        P.append(f'<div class="exp"><span class="t">쉬운 설명 ·</span> {esc(t.get("plain_explanation",""))}</div>')
        if t.get("why_how"):
            P.append(f'<div class="how"><span class="t" style="color:#444;font-weight:700">왜/어떻게 ·</span> {esc(t.get("why_how"))}</div>')
        ep = t.get("exam_point",{})
        P.append('<div class="ep">'
                 f'<span class="ok"><b>✅ 이게 맞다</b> · {esc(clean(ep.get("correct","")))}</span>'
                 f'<span class="no"><b>❌ 이렇게 뒤집어 낸다</b> · {esc(clean(ep.get("trap","")))}</span>'
                 '</div>')
        P.append('</div>')
    # ➕ checklist
    if ckl:
        P.append('<div class="cklhead">➕ 추가 함정 체크 (압축) — ✅만 외우면 ❌가 보인다</div>')
        P.append('<table class="ckl"><thead><tr><th class="t1">지식점</th>'
                 '<th class="t2">✅ 이게 맞다</th><th class="t3">❌ 이렇게 나오면 그게 답</th></tr></thead><tbody>')
        for c in ckl:
            qref = c.get("qref",""); q50 = "q50" if qref in top50_ids else ""
            badge = f'<span class="qb {q50}">{esc(qref)}{" ★출제" if qref in top50_ids else ""}</span>'
            P.append('<tr>'
                     f'<td>{badge}<br>{esc(c.get("topic",""))}</td>'
                     f'<td class="ok">{esc(clean(c.get("correct","")))}</td>'
                     f'<td class="no">{esc(clean(c.get("trap","")))}</td></tr>')
        P.append('</tbody></table>')
    # figure
    fg = s.get("figure",{})
    if fg.get("pdf") and fg.get("page"):
        b64,st = render_fig(fg["pdf"], fg["page"])
        if b64:
            P.append(f'<figure><img src="data:image/jpeg;base64,{b64}" alt="fig">'
                     f'<figcaption>[그림] {esc(fg.get("caption",""))} · 출처 원본 슬라이드</figcaption></figure>')
    # ✅ memorize
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
         + (f' · <b class="x2">미커버 {miss50}</b>' if miss50 else ' (전 문항 수록 ✓)')
         + '. 각 행의 「정리본 위치」 = 해당 강의의 그 qref(TOP 카드 또는 ➕체크리스트). ✅ 방향을 그대로, 시험은 거꾸로.</p>')
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
P.append(f'<p class="note">전 {len(all87)}개 지식점 커버: {87-len(miss87)}/87' + (f' · 미커버 {miss87}' if miss87 else ' (전부 수록)') + '.</p>')
P.append('</div></body></html>')

open(OUT,"w",encoding="utf-8").write("\n".join(P))
print("OUTPUT:", OUT)
print("size:", os.path.getsize(OUT), "bytes")
print("covered top50:", 50-len(miss50), "/50  miss:", miss50)
print("covered all87:", 87-len(miss87), "/87  miss:", miss87)
print("figures:", {f"{k[0][:18]}..p{k[1]}": v[1] for k,v in _figcache.items()})
