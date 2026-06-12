# -*- coding: utf-8 -*-
"""Phase D+E: read verified question JSONs, render high-yield slide figures (PNG/base64),
assemble a single printable A4 two-column HTML mock-exam (문제집 + 해설집) + self-audit table."""
import fitz, os, glob, json, base64, html, re, sys, io
from PIL import Image
from collections import Counter

BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
WORK = os.path.join(BASE, "_work")
VDIR = os.path.join(WORK, "verified")
FIGDIR = os.path.join(BASE, "_figures")
os.makedirs(FIGDIR, exist_ok=True)
OUT = os.path.join(BASE, "생명의과학세미나_기말_예상모의고사.html")

# lecture display order (by date) + expected counts for audit
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

def load_json_loose(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    txt = txt.strip()
    # strip code fences if any
    txt = re.sub(r"^```(json)?", "", txt).strip()
    txt = re.sub(r"```$", "", txt).strip()
    # find first [ ... last ]
    a, b = txt.find("["), txt.rfind("]")
    if a != -1 and b != -1 and b > a:
        txt = txt[a:b+1]
    return json.loads(txt)

CIRC = ["①","②","③","④","⑤","⑥"]

def norm_q(q, key):
    """Validate/normalize a question dict; return (q, warnings)."""
    w = []
    q.setdefault("lecture_key", key)
    q.setdefault("lecture_label", LABELS.get(key, key))
    opts = q.get("options") or []
    if len(opts) != 5:
        w.append(f"{q.get('id')}: options={len(opts)} (expected 5)")
    ai = q.get("answer_index")
    if not isinstance(ai, int) or not (0 <= ai < len(opts)):
        w.append(f"{q.get('id')}: bad answer_index={ai}")
        q["answer_index"] = 0 if opts else None
    if not q.get("stem"):
        w.append(f"{q.get('id')}: missing stem")
    try:
        q["exam_probability"] = int(round(float(q.get("exam_probability", 50))))
    except Exception:
        q["exam_probability"] = 50
    q.setdefault("study_strength", "★★")
    q.setdefault("tier", 1)
    q.setdefault("explanation", "")
    q.setdefault("correct_fact", "")
    q.setdefault("selection_reason", "")
    q.setdefault("topic", "")
    q.setdefault("scope_confidence", "high")
    # clean selection_reason: drop verifier meta-notes [검증:...] and leading label
    sr = q.get("selection_reason", "") or ""
    sr = re.sub(r"\[검증[^\]]*\]", "", sr)
    sr = re.sub(r"^\s*선정\s*사유\s*[:：]\s*", "", sr).strip()
    q["selection_reason"] = sr
    return q, w

def resolve_pdf(name):
    if not name: return None
    p = os.path.join(BASE, name)
    if os.path.exists(p): return p
    base = os.path.basename(name)
    hits = glob.glob(os.path.join(BASE, base))
    if hits: return hits[0]
    # fuzzy: match by a distinctive token
    stem = re.sub(r"[^0-9A-Za-z가-힣]", "", base)[:8]
    for f in glob.glob(os.path.join(BASE, "*.pdf")):
        if stem and stem in re.sub(r"[^0-9A-Za-z가-힣]", "", os.path.basename(f)):
            return f
    return None

def render_fig(pdf_name, page, fid):
    """Render a slide page to JPEG base64. Skip portrait/text-manuscript pages (not real figures)."""
    pdf = resolve_pdf(pdf_name)
    if not pdf:
        return None, f"PDF not found: {pdf_name}", "missing"
    try:
        doc = fitz.open(pdf)
        pno = max(1, min(int(page), doc.page_count)) - 1
        pg = doc[pno]
        rect = pg.rect
        landscape = rect.width > rect.height * 1.05
        nimg = len(pg.get_images())
        # text-manuscript page (portrait & no embedded images) => not a figure, skip
        if (not landscape) and nimg == 0:
            doc.close()
            return None, f"skip(text page, portrait, no images): {os.path.basename(pdf)} p{page}", "skip"
        # dominant text direction -> detect rotated slide content
        dirs = Counter()
        for bl in pg.get_text("dict").get("blocks", []):
            for ln in bl.get("lines", []):
                dirs[tuple(round(x) for x in ln.get("dir", (1, 0)))] += len(ln.get("spans", []) or [1])
        dom = dirs.most_common(1)[0][0] if dirs else (1, 0)
        zoom = min(2.2, 1400.0 / max(1.0, rect.width))
        zoom = max(zoom, 1.4)
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # rotate to make text upright (y-down screen coords)
        if dom == (0, 1):   img = img.transpose(Image.ROTATE_90)
        elif dom == (0, -1): img = img.transpose(Image.ROTATE_270)
        elif dom == (-1, 0): img = img.transpose(Image.ROTATE_180)
        if img.width > 1500:
            img = img.resize((1500, round(img.height * 1500 / img.width)), Image.LANCZOS)
        buf = io.BytesIO(); img.save(buf, format="JPEG", quality=82)
        jpg = buf.getvalue()
        with open(os.path.join(FIGDIR, f"{fid}.jpg"), "wb") as f:
            f.write(jpg)
        doc.close()
        b64 = base64.b64encode(jpg).decode("ascii")
        return b64, None, "ok"
    except Exception as e:
        return None, f"render error {pdf_name} p{page}: {e}", "error"

# ---- load all verified questions ----
all_q = []
warnings = []
per_lec = {k: 0 for k in ORDER}
for key in ORDER:
    path = os.path.join(VDIR, f"{key}.json")
    if not os.path.exists(path):
        warnings.append(f"MISSING verified file: {key}.json")
        continue
    try:
        arr = load_json_loose(path)
    except Exception as e:
        warnings.append(f"PARSE FAIL {key}.json: {e}")
        continue
    for q in arr:
        q, w = norm_q(q, key)
        warnings.extend(w)
        all_q.append(q)
        per_lec[key] += 1

# ---- order by exam_probability desc (stable by lecture order then prob) ----
all_q.sort(key=lambda q: (-q.get("exam_probability", 0)))
for i, q in enumerate(all_q, 1):
    q["_num"] = i

# ---- render figures (only needed) ----
fig_report = []
for q in all_q:
    fg = q.get("figure") or {}
    if fg.get("needed") and fg.get("pdf"):
        b64, err, status = render_fig(fg.get("pdf"), fg.get("page", 1), f"fig_{q['_num']}_{q['lecture_key']}")
        if b64:
            q["_fig_b64"] = b64
            fig_report.append(f"Q{q['_num']} {q['lecture_key']} fig OK ({fg.get('pdf')} p{fg.get('page')})")
        else:
            q["_fig_b64"] = None
            fig_report.append(f"Q{q['_num']} {q['lecture_key']} fig {status}: {err}")

def esc(s): return html.escape(str(s if s is not None else ""))

# ---- build HTML ----
total = len(all_q)
parts = []
parts.append("""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>생명의과학세미나 기말 예상 모의고사</title>
<style>
:root{ --ink:#1a1a1a; --mut:#555; --line:#bbb; --hl:#c62828; --box:#f6f7f9; --acc:#0d47a1; }
*{box-sizing:border-box;}
html,body{margin:0;padding:0;color:var(--ink);
 font-family:"Malgun Gothic","맑은 고딕",AppleGothic,sans-serif; font-size:10.3pt; line-height:1.45;}
@page{ size:A4; margin:12mm 11mm 14mm 11mm; }
.page{ page-break-after:always; }
h1{font-size:18pt;margin:0 0 2mm;} h2{font-size:13pt;margin:6mm 0 3mm;border-bottom:2px solid var(--acc);padding-bottom:1mm;color:var(--acc);}
.lead{color:var(--mut);font-size:9.3pt;margin:0 0 4mm;}
.meta-tbl{border-collapse:collapse;width:100%;font-size:9pt;margin:3mm 0;}
.meta-tbl th,.meta-tbl td{border:1px solid var(--line);padding:2px 5px;text-align:left;}
.meta-tbl th{background:var(--box);}
/* problem booklet : two columns */
.qcols{ column-count:2; column-gap:7mm; }
.q{ break-inside:avoid; -webkit-column-break-inside:avoid; page-break-inside:avoid;
 border:1px solid var(--line); border-radius:4px; padding:3mm 3.2mm; margin:0 0 3mm; background:#fff; }
.qhead{ display:flex; justify-content:space-between; align-items:baseline; gap:4px; margin-bottom:1.5mm;}
.qno{ font-weight:700; color:var(--acc); font-size:10.6pt;}
.qtag{ font-size:7.6pt; color:#fff; background:#607d8b; border-radius:3px; padding:1px 5px; white-space:nowrap;}
.stem{ font-weight:600; margin:0 0 2mm;}
.opt{ margin:0.7mm 0; padding-left:1mm; text-indent:0; }
.opt .c{ color:var(--acc); font-weight:700; margin-right:2px;}
/* explanation booklet */
.exp{ border:1px solid var(--line); border-left:4px solid var(--acc);
 border-radius:4px; padding:3.5mm 4mm; margin:0 0 4mm; background:#fff;}
.exp .top{ break-inside:avoid; page-break-inside:avoid; }
.exp .top{ display:flex; flex-wrap:wrap; gap:6px 10px; align-items:baseline; margin-bottom:1.5mm;}
.exp .eno{ font-weight:700; color:var(--acc); font-size:11pt;}
.ans{ font-weight:700; color:var(--hl); }
.badge{ font-size:8pt; background:var(--box); border:1px solid var(--line); border-radius:3px; padding:1px 6px; color:#333;}
.exp .label{ font-weight:700; color:#333; }
.block{ margin:1.6mm 0; }
.fact{ background:#fff8e1; border:1px solid #ffe082; border-radius:3px; padding:2mm 3mm; }
.reason{ color:var(--mut); font-size:9pt;}
figure{margin:2mm 0;text-align:center;break-inside:avoid;page-break-inside:avoid;} figure img{max-width:100%;border:1px solid var(--line);}
figcaption{font-size:8.3pt;color:var(--mut);margin-top:1mm;}
.optlist{margin:1.5mm 0;} .optline{margin:0.5mm 0;} .optwrong{color:var(--hl);font-weight:600;}
.note{font-size:8.6pt;color:var(--mut);}
.audit td,.audit th{font-size:8.8pt;}
.star{color:#e6a700;font-weight:700;}
.hr{height:0;border-top:1px dashed var(--line);margin:2mm 0;}
</style></head><body>""")

# ---- cover / instructions ----
parts.append('<div class="page">')
parts.append('<h1>26년 1학기 「생명의과학세미나」 기말 — 출제확률 기반 예상 모의고사</h1>')
parts.append(f'<p class="lead">대학원(석·박사) 수준 · 전 문항 「옳지 않은 것은?」 5지선다 · 총 <b>{total}문항</b> '
             '(일반 합동 기말 추정 ~17문항 × 3배수) · 출제확률 높은 순 정렬. '
             '범위(C1): 각 강의 <b>슬라이드(닫힌 우주)</b>에 등장하는 내용으로 한정, 녹음본은 강조·해설 근거로만 사용.</p>')
parts.append('<p class="note">활용법: ①~⑤ 중 <b>틀린 1개</b>를 고르되, 나머지 옳은 4지를 정독하면 그 토픽의 핵심이 정리됩니다. '
             '해설집에서 정답·일타강사 해설·그림·선정사유·학습강도(★★★ 필수/★★ 권장/★ 참고)를 확인하세요.</p>')
parts.append('</div>')

# ---- 문제집 ----
parts.append('<div class="page">')
parts.append('<h2>제1부 · 문제집 (Mock Exam)</h2>')
parts.append('<div class="qcols">')
for q in all_q:
    parts.append('<div class="q">')
    parts.append(f'<div class="qhead"><span class="qno">문 {q["_num"]}.</span>'
                 f'<span class="qtag">{esc(q["lecture_label"])}</span></div>')
    parts.append(f'<div class="stem">{esc(q["stem"])}</div>')
    for i, o in enumerate(q.get("options", [])):
        parts.append(f'<div class="opt"><span class="c">{CIRC[i]}</span>{esc(o)}</div>')
    parts.append('</div>')
parts.append('</div></div>')

# ---- 해설집 ----
parts.append('<div class="page">')
parts.append('<h2>제2부 · 정답 및 일타강사 해설집</h2>')
for q in all_q:
    ai = q.get("answer_index", 0)
    ai = ai if isinstance(ai, int) and 0 <= ai < len(q.get("options", [])) else 0
    parts.append('<div class="exp">')
    parts.append('<div class="top">'
                 f'<span class="eno">문 {q["_num"]}.</span>'
                 f'<span class="badge">{esc(q["lecture_label"])}</span>'
                 f'<span class="ans">정답 {CIRC[ai]}</span>'
                 f'<span class="badge">출제확률 {q.get("exam_probability","?")}%</span>'
                 f'<span class="badge">TIER {q.get("tier","?")}</span>'
                 f'<span class="badge">학습강도 <span class="star">{esc(q.get("study_strength","★★"))}</span></span>'
                 f'<span class="badge">토픽: {esc(q.get("topic",""))}</span>'
                 '</div>')
    # options recap with wrong one marked
    parts.append('<div class="optlist note">')
    for i, o in enumerate(q.get("options", [])):
        cls = "optline optwrong" if i == ai else "optline"
        mark = " ✗(옳지 않음)" if i == ai else ""
        parts.append(f'<div class="{cls}">{CIRC[i]} {esc(o)}{mark}</div>')
    parts.append('</div>')
    # figure
    if q.get("_fig_b64"):
        cap = (q.get("figure") or {}).get("caption", "")
        parts.append(f'<figure><img src="data:image/jpeg;base64,{q["_fig_b64"]}" alt="figure">'
                     f'<figcaption>[그림] {esc(cap)} · 출처 슬라이드</figcaption></figure>')
    parts.append(f'<div class="block"><span class="label">📝 일타강사 해설</span><br>{esc(q.get("explanation",""))}</div>')
    if q.get("correct_fact"):
        parts.append(f'<div class="block fact"><span class="label">✔ 바로잡기</span> {esc(q.get("correct_fact",""))}</div>')
    if q.get("selection_reason"):
        parts.append(f'<div class="block reason"><span class="label">🎯 선정 사유</span> {esc(q.get("selection_reason",""))}'
                     + (f' · <i>범위신뢰도 {esc(q.get("scope_confidence"))}</i>' if q.get("scope_confidence") else "")
                     + '</div>')
    parts.append('</div>')
parts.append('</div>')

# ---- self-audit ----
parts.append('<div class="page">')
parts.append('<h2>제3부 · 자가검수 & 출제 커버리지</h2>')
parts.append('<table class="meta-tbl audit"><tr><th>강의</th><th>문항수</th><th>대표 토픽(상위)</th></tr>')
for key in ORDER:
    qs = [q for q in all_q if q["lecture_key"] == key]
    tops = " / ".join(dict.fromkeys([q.get("topic","") for q in qs[:3] if q.get("topic")]))
    parts.append(f'<tr><td>{esc(LABELS.get(key,key))}</td><td style="text-align:center">{len(qs)}</td><td>{esc(tops)}</td></tr>')
parts.append(f'<tr><th>합계</th><th style="text-align:center">{total}</th><th></th></tr>')
parts.append('</table>')
parts.append('<p class="note">검수 원칙: 전 문항 슬라이드(닫힌 우주) 기준 적대적 검증 — 틀린 선지 정확히 1개, 옳은 4지 슬라이드 근거, '
             '해설은 교수 발화 기반. 출제확률 순 배치. 본 세트는 강의별 TIER 1(고강조) 토픽을 3배수로 커버하도록 설계됨.</p>')
parts.append('</div>')

parts.append("</body></html>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(parts))

# ---- stdout report ----
print("="*60)
print(f"TOTAL questions: {total}")
print("per-lecture:", {k: per_lec[k] for k in ORDER})
print("OUTPUT:", OUT)
print("-- figures --")
for r in fig_report: print("  ", r)
print("-- warnings --")
for w in warnings: print("  ", w)
if not warnings: print("   (none)")
