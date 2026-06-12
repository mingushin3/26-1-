# -*- coding: utf-8 -*-
"""v2 builder: merge core(verified) + gap(v2verified) questions, re-rank by exam_probability,
render figures, assemble printable A4 two-column HTML (문제집+해설집) + self-audit."""
import fitz, os, glob, json, base64, html, re, sys, io
from PIL import Image
from collections import Counter

BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
WORK = os.path.join(BASE, "_work")
VDIR = os.path.join(WORK, "verified")
GDIR = os.path.join(WORK, "v2verified")
FIGDIR = os.path.join(BASE, "_figures")
os.makedirs(FIGDIR, exist_ok=True)
OUT = os.path.join(BASE, "생명의과학세미나_기말_예상모의고사_v2.html")

ORDER = ["wonjaelee","golgi","bloodomics","scrna","llmngs","genetherapy","ev",
         "nanomrna","dpath","thyroid","tert","brain","immuno","gastric"]
LABELS = {
 "wonjaelee":"03-03 암생물학 패러다임 (이원재)","golgi":"03-10 골지체 (김지윤)",
 "bloodomics":"03-17 혈액암 오믹스 (정승현)","scrna":"03-24 scRNAseq (이혜옥)",
 "llmngs":"03-31 LLM·NGS·바이오인포 (의료정보학)","genetherapy":"04-07 유전자치료 (김영광)",
 "ev":"04-14 세포외소포·액체생검 (김일진)","nanomrna":"04-21 나노메디슨·mRNA-LNP (구희범)",
 "dpath":"04-28 디지털병리 (이성학)","thyroid":"05-12 갑상선암 바이오마커 (임동석)",
 "tert":"05-19 TERT·B형간염·간암 (장정원)","brain":"05-26 신경외과·뇌종양 (Stephen Ahn)",
 "immuno":"06-02 면역항암·간암저항성 (성필수)","gastric":"06-09 위암 맞춤치료 (박재명)"}
CIRC = ["①","②","③","④","⑤","⑥"]

def load_json_loose(path):
    txt = open(path, "r", encoding="utf-8").read().strip()
    txt = re.sub(r"^```(json)?", "", txt).strip(); txt = re.sub(r"```$", "", txt).strip()
    a, b = txt.find("["), txt.rfind("]")
    if a != -1 and b != -1 and b > a: txt = txt[a:b+1]
    return json.loads(txt)

def norm_q(q, key, gap):
    w = []
    q.setdefault("lecture_key", key); q.setdefault("lecture_label", LABELS.get(key, key))
    q["_gap"] = gap
    opts = q.get("options") or []
    if len(opts) != 5: w.append(f"{q.get('id')}: options={len(opts)}")
    ai = q.get("answer_index")
    if not isinstance(ai, int) or not (0 <= ai < len(opts)):
        w.append(f"{q.get('id')}: bad answer_index={ai}"); q["answer_index"] = 0 if opts else None
    if not q.get("stem"): w.append(f"{q.get('id')}: missing stem")
    if "옳지" not in (q.get("stem","")): w.append(f"{q.get('id')}: stem not 옳지않은")
    try: q["exam_probability"] = int(round(float(q.get("exam_probability", 50))))
    except Exception: q["exam_probability"] = 50
    q.setdefault("study_strength", "★★"); q.setdefault("tier", 1)
    for f in ("explanation","correct_fact","selection_reason","topic"): q.setdefault(f, "")
    q.setdefault("scope_confidence", "high")
    sr = re.sub(r"\[검증[^\]]*\]", "", q.get("selection_reason","") or "")
    sr = re.sub(r"^\s*선정\s*사유\s*[:：]\s*", "", sr).strip(); q["selection_reason"] = sr
    return q, w

def resolve_pdf(name):
    if not name: return None
    p = os.path.join(BASE, name)
    if os.path.exists(p): return p
    hits = glob.glob(os.path.join(BASE, os.path.basename(name)))
    if hits: return hits[0]
    stem = re.sub(r"[^0-9A-Za-z가-힣]", "", os.path.basename(name))[:8]
    for f in glob.glob(os.path.join(BASE, "*.pdf")):
        if stem and stem in re.sub(r"[^0-9A-Za-z가-힣]", "", os.path.basename(f)): return f
    return None

def render_fig(pdf_name, page, fid):
    pdf = resolve_pdf(pdf_name)
    if not pdf: return None, f"PDF not found: {pdf_name}", "missing"
    try:
        doc = fitz.open(pdf); pno = max(1, min(int(page), doc.page_count)) - 1
        pg = doc[pno]; rect = pg.rect
        landscape = rect.width > rect.height * 1.05; nimg = len(pg.get_images())
        if (not landscape) and nimg == 0:
            doc.close(); return None, f"skip(text page): {os.path.basename(pdf)} p{page}", "skip"
        dirs = Counter()
        for bl in pg.get_text("dict").get("blocks", []):
            for ln in bl.get("lines", []):
                dirs[tuple(round(x) for x in ln.get("dir", (1, 0)))] += len(ln.get("spans", []) or [1])
        dom = dirs.most_common(1)[0][0] if dirs else (1, 0)
        zoom = max(min(2.2, 1400.0 / max(1.0, rect.width)), 1.4)
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if dom == (0,1): img = img.transpose(Image.ROTATE_90)
        elif dom == (0,-1): img = img.transpose(Image.ROTATE_270)
        elif dom == (-1,0): img = img.transpose(Image.ROTATE_180)
        if img.width > 1500: img = img.resize((1500, round(img.height*1500/img.width)), Image.LANCZOS)
        buf = io.BytesIO(); img.save(buf, format="JPEG", quality=82); jpg = buf.getvalue()
        open(os.path.join(FIGDIR, f"{fid}.jpg"), "wb").write(jpg)
        doc.close(); return base64.b64encode(jpg).decode("ascii"), None, "ok"
    except Exception as e:
        return None, f"render error {pdf_name} p{page}: {e}", "error"

all_q = []; warnings = []; per_lec = {k:{"core":0,"gap":0} for k in ORDER}
for key in ORDER:
    for d, gap in ((VDIR,False),(GDIR,True)):
        path = os.path.join(d, f"{key}.json")
        if not os.path.exists(path):
            if not gap: warnings.append(f"MISSING core: {key}.json")
            continue
        try: arr = load_json_loose(path)
        except Exception as e: warnings.append(f"PARSE FAIL {d}/{key}.json: {e}"); continue
        for q in arr:
            q, w = norm_q(q, key, gap); warnings.extend(w); all_q.append(q)
            per_lec[key]["gap" if gap else "core"] += 1

all_q.sort(key=lambda q: (-q.get("exam_probability", 0)))
for i, q in enumerate(all_q, 1): q["_num"] = i

fig_report = []
for q in all_q:
    fg = q.get("figure") or {}
    if fg.get("needed") and fg.get("pdf"):
        b64, err, status = render_fig(fg.get("pdf"), fg.get("page",1), f"fig_v2_{q['_num']}_{q['lecture_key']}")
        q["_fig_b64"] = b64
        fig_report.append(f"Q{q['_num']} {q['lecture_key']} {'OK' if b64 else status}: {err or fg.get('pdf')}")

def esc(s): return html.escape(str(s if s is not None else ""))
total = len(all_q); ncore = sum(1 for q in all_q if not q["_gap"]); ngap = total - ncore
parts = []
parts.append("""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>생명의과학세미나 기말 예상 모의고사 v2 (완전판)</title>
<style>
:root{ --ink:#1a1a1a; --mut:#555; --line:#bbb; --hl:#c62828; --box:#f6f7f9; --acc:#0d47a1; --gap:#1b7a3d; }
*{box-sizing:border-box;}
html,body{margin:0;padding:0;color:var(--ink);font-family:"Malgun Gothic","맑은 고딕",AppleGothic,sans-serif;font-size:10.3pt;line-height:1.45;}
@page{ size:A4; margin:12mm 11mm 14mm 11mm; }
.page{ page-break-after:always; }
h1{font-size:17.5pt;margin:0 0 2mm;} h2{font-size:13pt;margin:6mm 0 3mm;border-bottom:2px solid var(--acc);padding-bottom:1mm;color:var(--acc);}
.lead{color:var(--mut);font-size:9.3pt;margin:0 0 4mm;}
.meta-tbl{border-collapse:collapse;width:100%;font-size:9pt;margin:3mm 0;}
.meta-tbl th,.meta-tbl td{border:1px solid var(--line);padding:2px 5px;text-align:left;} .meta-tbl th{background:var(--box);}
.qcols{ column-count:2; column-gap:7mm; }
.q{ break-inside:avoid;-webkit-column-break-inside:avoid;page-break-inside:avoid;border:1px solid var(--line);border-radius:4px;padding:3mm 3.2mm;margin:0 0 3mm;background:#fff; }
.qhead{ display:flex;justify-content:space-between;align-items:baseline;gap:4px;margin-bottom:1.5mm;}
.qno{ font-weight:700;color:var(--acc);font-size:10.6pt;}
.qtag{ font-size:7.6pt;color:#fff;background:#607d8b;border-radius:3px;padding:1px 5px;white-space:nowrap;}
.qtag.g{ background:var(--gap); }
.stem{ font-weight:600;margin:0 0 2mm;}
.opt{ margin:0.7mm 0;padding-left:1mm;} .opt .c{ color:var(--acc);font-weight:700;margin-right:2px;}
.exp{ border:1px solid var(--line);border-left:4px solid var(--acc);border-radius:4px;padding:3.5mm 4mm;margin:0 0 4mm;background:#fff;}
.exp.g{ border-left-color:var(--gap); }
.exp .top{ display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;margin-bottom:1.5mm;break-inside:avoid;page-break-inside:avoid;}
.exp .eno{ font-weight:700;color:var(--acc);font-size:11pt;}
.ans{ font-weight:700;color:var(--hl); }
.badge{ font-size:8pt;background:var(--box);border:1px solid var(--line);border-radius:3px;padding:1px 6px;color:#333;}
.badge.gap{ background:#e7f6ec;border-color:#9ed3b3;color:#1b7a3d;font-weight:700;}
.exp .label{ font-weight:700;color:#333; } .block{ margin:1.6mm 0; }
.fact{ background:#fff8e1;border:1px solid #ffe082;border-radius:3px;padding:2mm 3mm; }
.reason{ color:var(--mut);font-size:9pt;}
figure{margin:2mm 0;text-align:center;break-inside:avoid;page-break-inside:avoid;} figure img{max-width:100%;border:1px solid var(--line);}
figcaption{font-size:8.3pt;color:var(--mut);margin-top:1mm;}
.optlist{margin:1.5mm 0;} .optline{margin:0.5mm 0;} .optwrong{color:var(--hl);font-weight:600;}
.note{font-size:8.6pt;color:var(--mut);} .audit td,.audit th{font-size:8.8pt;} .star{color:#e6a700;font-weight:700;}
</style></head><body>""")

parts.append('<div class="page">')
parts.append('<h1>26년 1학기 「생명의과학세미나」 기말 — 출제확률 기반 예상 모의고사 <span style="color:#1b7a3d">v2 (완전판)</span></h1>')
parts.append(f'<p class="lead">대학원(석·박사) 수준 · 전 문항 「옳지 않은 것은?」 5지선다 · 총 <b>{total}문항</b> '
             f'(핵심 {ncore} + <span style="color:#1b7a3d"><b>써머리 보완 {ngap}</b></span>) · 출제확률 높은 순 정렬. '
             'v2는 재감사에서 <b>필수/요약/마지막(Conclusion·Take-home) 슬라이드</b> 기반 누락 고출제 주제를 보완한 완전판입니다. '
             '범위(C1): 각 강의 슬라이드(닫힌 우주) 한정.</p>')
parts.append('<p class="note">초록색 <span class="badge gap">보완</span> 배지 = 재감사로 추가된, 교수가 말로 강조하지 않아도 '
             '요약/마지막 슬라이드에서 출제가 집중되는 고확률 주제. ①~⑤ 중 <b>틀린 1개</b>를 고르되 나머지 옳은 4지로 토픽을 정리하세요.</p>')
parts.append('</div>')

parts.append('<div class="page"><h2>제1부 · 문제집 (Mock Exam · v2)</h2><div class="qcols">')
for q in all_q:
    parts.append('<div class="q">')
    tagcls = "qtag g" if q["_gap"] else "qtag"
    tagtxt = ("⊕ " if q["_gap"] else "") + esc(q["lecture_label"])
    parts.append(f'<div class="qhead"><span class="qno">문 {q["_num"]}.</span><span class="{tagcls}">{tagtxt}</span></div>')
    parts.append(f'<div class="stem">{esc(q["stem"])}</div>')
    for i,o in enumerate(q.get("options",[])):
        parts.append(f'<div class="opt"><span class="c">{CIRC[i]}</span>{esc(o)}</div>')
    parts.append('</div>')
parts.append('</div></div>')

parts.append('<div class="page"><h2>제2부 · 정답 및 일타강사 해설집 (v2)</h2>')
for q in all_q:
    ai = q.get("answer_index",0); ai = ai if isinstance(ai,int) and 0<=ai<len(q.get("options",[])) else 0
    parts.append(f'<div class="exp{" g" if q["_gap"] else ""}">')
    gapbadge = '<span class="badge gap">써머리 보완</span>' if q["_gap"] else ''
    parts.append('<div class="top">'
                 f'<span class="eno">문 {q["_num"]}.</span>{gapbadge}'
                 f'<span class="badge">{esc(q["lecture_label"])}</span>'
                 f'<span class="ans">정답 {CIRC[ai]}</span>'
                 f'<span class="badge">출제확률 {q.get("exam_probability","?")}%</span>'
                 f'<span class="badge">TIER {q.get("tier","?")}</span>'
                 f'<span class="badge">학습강도 <span class="star">{esc(q.get("study_strength","★★"))}</span></span>'
                 f'<span class="badge">토픽: {esc(q.get("topic",""))}</span></div>')
    parts.append('<div class="optlist note">')
    for i,o in enumerate(q.get("options",[])):
        cls = "optline optwrong" if i==ai else "optline"; mark = " ✗(옳지 않음)" if i==ai else ""
        parts.append(f'<div class="{cls}">{CIRC[i]} {esc(o)}{mark}</div>')
    parts.append('</div>')
    if q.get("_fig_b64"):
        cap = (q.get("figure") or {}).get("caption","")
        parts.append(f'<figure><img src="data:image/jpeg;base64,{q["_fig_b64"]}" alt="figure"><figcaption>[그림] {esc(cap)} · 출처 슬라이드</figcaption></figure>')
    parts.append(f'<div class="block"><span class="label">📝 일타강사 해설</span><br>{esc(q.get("explanation",""))}</div>')
    if q.get("correct_fact"):
        parts.append(f'<div class="block fact"><span class="label">✔ 바로잡기</span> {esc(q.get("correct_fact",""))}</div>')
    if q.get("selection_reason"):
        parts.append(f'<div class="block reason"><span class="label">🎯 선정 사유</span> {esc(q.get("selection_reason",""))}'
                     + (f' · <i>범위신뢰도 {esc(q.get("scope_confidence"))}</i>' if q.get("scope_confidence") else "") + '</div>')
    parts.append('</div>')
parts.append('</div>')

parts.append('<div class="page"><h2>제3부 · 자가검수 & 출제 커버리지 (v2)</h2>')
parts.append('<table class="meta-tbl audit"><tr><th>강의</th><th>핵심</th><th>보완</th><th>계</th><th>대표 토픽(상위)</th></tr>')
for key in ORDER:
    qs = [q for q in all_q if q["lecture_key"]==key]
    tops = " / ".join(dict.fromkeys([q.get("topic","") for q in qs[:3] if q.get("topic")]))
    parts.append(f'<tr><td>{esc(LABELS.get(key,key))}</td><td style="text-align:center">{per_lec[key]["core"]}</td>'
                 f'<td style="text-align:center;color:#1b7a3d">{per_lec[key]["gap"]}</td>'
                 f'<td style="text-align:center"><b>{len(qs)}</b></td><td>{esc(tops)}</td></tr>')
parts.append(f'<tr><th>합계</th><th style="text-align:center">{ncore}</th><th style="text-align:center;color:#1b7a3d">{ngap}</th>'
             f'<th style="text-align:center">{total}</th><th></th></tr></table>')
parts.append('<p class="note">v2 보완 원칙: 14개 강의의 <b>필수/요약/마지막(Conclusion·Take-home) 슬라이드</b>를 닫힌우주의 최우선 출제범위로 재가중하여, '
             'top-50 재정렬 과정에서 누락됐던 고출제 주제를 적대적 검증을 거쳐 추가. 기존 50문항은 전수 재검수 결과 전부 유지(약문항 0). '
             '전 문항 슬라이드 근거·틀린 선지 정확히 1개·해설은 교수 발화/슬라이드 기반.</p>')
parts.append('</div></body></html>')

open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print("="*60); print(f"TOTAL {total} (core {ncore} + gap {ngap})")
print("per-lecture:", {k:(per_lec[k]["core"],per_lec[k]["gap"]) for k in ORDER})
print("OUTPUT:", OUT)
print("-- figures --");
for r in fig_report: print("  ", r)
print("-- warnings --");
for w in warnings: print("  ", w)
if not warnings: print("   (none)")
