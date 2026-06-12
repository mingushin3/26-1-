# -*- coding: utf-8 -*-
"""v3 builder: merge v2 (core+gap), rank by exam_probability, take TOP 50,
render as a single-column integrated 문제-해설 통합본 (each Q immediately followed by
red 정답 + 일타강사 해설 + figure). Printable A4."""
import fitz, os, glob, json, base64, html, re, io
from PIL import Image
from collections import Counter

BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
WORK = os.path.join(BASE, "_work")
VDIR = os.path.join(WORK, "verified"); GDIR = os.path.join(WORK, "v2verified")
FIGDIR = os.path.join(BASE, "_figures"); os.makedirs(FIGDIR, exist_ok=True)
OUT = os.path.join(BASE, "생명의과학세미나_기말_예상모의고사_v3(50문항 통합본).html")
TOPN = 50

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
    txt = open(path,encoding="utf-8").read().strip()
    txt = re.sub(r"^```(json)?","",txt).strip(); txt = re.sub(r"```$","",txt).strip()
    a,b = txt.find("["), txt.rfind("]")
    if a!=-1 and b!=-1 and b>a: txt = txt[a:b+1]
    return json.loads(txt)

def norm_q(q, key, gap):
    q.setdefault("lecture_key",key); q.setdefault("lecture_label",LABELS.get(key,key)); q["_gap"]=gap
    try: q["exam_probability"]=int(round(float(q.get("exam_probability",50))))
    except Exception: q["exam_probability"]=50
    q.setdefault("study_strength","★★"); q.setdefault("tier",1)
    for f in ("explanation","correct_fact","selection_reason","topic"): q.setdefault(f,"")
    q.setdefault("scope_confidence","high")
    sr = re.sub(r"\[검증[^\]]*\]","",q.get("selection_reason","") or "")
    sr = re.sub(r"^\s*선정\s*사유\s*[:：]\s*","",sr).strip(); q["selection_reason"]=sr
    ai = q.get("answer_index")
    if not isinstance(ai,int) or not (0<=ai<len(q.get("options",[]))): q["answer_index"]=0
    return q

def resolve_pdf(name):
    if not name: return None
    p=os.path.join(BASE,name)
    if os.path.exists(p): return p
    h=glob.glob(os.path.join(BASE,os.path.basename(name)))
    if h: return h[0]
    stem=re.sub(r"[^0-9A-Za-z가-힣]","",os.path.basename(name))[:8]
    for f in glob.glob(os.path.join(BASE,"*.pdf")):
        if stem and stem in re.sub(r"[^0-9A-Za-z가-힣]","",os.path.basename(f)): return f
    return None

def render_fig(pdf_name, page, fid):
    pdf=resolve_pdf(pdf_name)
    if not pdf: return None,"missing"
    try:
        doc=fitz.open(pdf); pno=max(1,min(int(page),doc.page_count))-1; pg=doc[pno]; rect=pg.rect
        landscape=rect.width>rect.height*1.05; nimg=len(pg.get_images())
        if (not landscape) and nimg==0: doc.close(); return None,"skip"
        dirs=Counter()
        for bl in pg.get_text("dict").get("blocks",[]):
            for ln in bl.get("lines",[]): dirs[tuple(round(x) for x in ln.get("dir",(1,0)))]+=len(ln.get("spans",[]) or [1])
        dom=dirs.most_common(1)[0][0] if dirs else (1,0)
        zoom=max(min(2.2,1400.0/max(1.0,rect.width)),1.4)
        pix=pg.get_pixmap(matrix=fitz.Matrix(zoom,zoom),alpha=False)
        img=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
        if dom==(0,1): img=img.transpose(Image.ROTATE_90)
        elif dom==(0,-1): img=img.transpose(Image.ROTATE_270)
        elif dom==(-1,0): img=img.transpose(Image.ROTATE_180)
        if img.width>1400: img=img.resize((1400,round(img.height*1400/img.width)),Image.LANCZOS)
        buf=io.BytesIO(); img.save(buf,format="JPEG",quality=82); jpg=buf.getvalue()
        open(os.path.join(FIGDIR,f"{fid}.jpg"),"wb").write(jpg); doc.close()
        return base64.b64encode(jpg).decode("ascii"),"ok"
    except Exception as e:
        return None,f"err {e}"

# load & merge
allq=[]
for key in ORDER:
    for d,gap in ((VDIR,False),(GDIR,True)):
        p=os.path.join(d,f"{key}.json")
        if not os.path.exists(p): continue
        for q in load_json_loose(p): allq.append(norm_q(q,key,gap))
allq.sort(key=lambda q:-q.get("exam_probability",0))
# selection with per-lecture floor: guarantee >=1 question per lecture, then fill by global probability
by_lec={}
for q in allq: by_lec.setdefault(q["lecture_key"],[]).append(q)  # each list already prob-desc
floor=[by_lec[k][0] for k in ORDER if by_lec.get(k)]
floor_ids={q["id"] for q in floor}
rest=[q for q in allq if q["id"] not in floor_ids]
fill=rest[:max(0,TOPN-len(floor))]
top=floor+fill
top.sort(key=lambda q:-q.get("exam_probability",0))
top=top[:TOPN]
for i,q in enumerate(top,1): q["_num"]=i
floor_only=[q for q in floor if q in top and q["exam_probability"] < (fill[-1]["exam_probability"] if fill else 0)]

top_ids={q["id"] for q in top}
cut=[q for q in allq if q["id"] not in top_ids]
# figures for top
figrep=[]
for q in top:
    fg=q.get("figure") or {}
    if fg.get("needed") and fg.get("pdf"):
        b64,st=render_fig(fg.get("pdf"),fg.get("page",1),f"v3_{q['_num']}_{q['lecture_key']}")
        q["_fig_b64"]=b64; figrep.append(f"Q{q['_num']} {q['lecture_key']}: {st}")

def esc(s): return html.escape(str(s if s is not None else ""))
ngap=sum(1 for q in top if q["_gap"]); ncore=TOPN-ngap
parts=[]
parts.append("""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>생명의과학세미나 기말 예상 모의고사 v3 (50문항 문제·해설 통합본)</title>
<style>
:root{ --ink:#1a1a1a; --mut:#555; --line:#bbb; --red:#d50000; --box:#f6f7f9; --acc:#0d47a1; --gap:#1b7a3d; }
*{box-sizing:border-box;}
html,body{margin:0;padding:0;color:var(--ink);font-family:"Malgun Gothic","맑은 고딕",AppleGothic,sans-serif;font-size:10.5pt;line-height:1.5;}
@page{ size:A4; margin:13mm 12mm 14mm 12mm; }
.page{ page-break-after:always; }
h1{font-size:17pt;margin:0 0 2mm;} h2{font-size:12.5pt;margin:5mm 0 3mm;border-bottom:2px solid var(--acc);padding-bottom:1mm;color:var(--acc);}
.lead{color:var(--mut);font-size:9.4pt;margin:0 0 3mm;}
.meta-tbl{border-collapse:collapse;width:100%;font-size:8.8pt;margin:2mm 0;}
.meta-tbl th,.meta-tbl td{border:1px solid var(--line);padding:2px 5px;text-align:left;} .meta-tbl th{background:var(--box);}
.item{ border:1px solid var(--line); border-left:4px solid var(--acc); border-radius:5px; padding:3.5mm 4mm; margin:0 0 4.5mm; background:#fff; }
.item.g{ border-left-color:var(--gap); }
.qhead{ break-inside:avoid; page-break-inside:avoid; }
.htop{ display:flex; flex-wrap:wrap; gap:5px 9px; align-items:baseline; margin-bottom:1.5mm; }
.qno{ font-weight:700; color:var(--acc); font-size:11.5pt; }
.badge{ font-size:8pt; background:var(--box); border:1px solid var(--line); border-radius:3px; padding:1px 6px; color:#333; }
.badge.gap{ background:#e7f6ec; border-color:#9ed3b3; color:#1b7a3d; font-weight:700; }
.star{ color:#e6a700; font-weight:700; }
.stem{ font-weight:700; margin:0 0 2mm; }
.opt{ margin:0.9mm 0; padding-left:2mm; } .opt .c{ font-weight:700; margin-right:3px; color:var(--acc); }
.opt.ans{ color:var(--red); font-weight:700; } .opt.ans .c{ color:var(--red); }
.answerline{ margin:2mm 0 1mm; font-weight:700; color:var(--red); font-size:10.6pt; }
.exp{ margin:1.5mm 0; } .label{ font-weight:700; color:#333; }
.fact{ background:#fff8e1; border:1px solid #ffe082; border-radius:3px; padding:2mm 3mm; margin:1.5mm 0; }
.reason{ color:var(--mut); font-size:9pt; margin-top:1mm; }
figure{ margin:2mm 0; text-align:center; break-inside:avoid; page-break-inside:avoid; } figure img{ max-width:100%; border:1px solid var(--line); }
figcaption{ font-size:8.3pt; color:var(--mut); margin-top:1mm; }
.note{ font-size:8.7pt; color:var(--mut); }
</style></head><body>""")

# cover
parts.append('<div class="page">')
parts.append('<h1>26년 1학기 「생명의과학세미나」 기말 예상 모의고사 <span style="color:#1b7a3d">v3</span> · 50문항 <span style="color:#d50000">문제·해설 통합본</span></h1>')
parts.append(f'<p class="lead">대학원(석·박사) 수준 · 전 문항 「옳지 않은 것은?」 5지선다 · v2(87문항)에서 <b>{TOPN}문항 선별</b> '
             f'(<b>14개 강의 각 최소 1문항 보장</b> 후 나머지는 출제확률 순) · 출제확률 높은 순 정렬(핵심 {ncore} + <span style="color:#1b7a3d">써머리 보완 {ngap}</span>). '
             '각 문항 바로 아래에 <span style="color:#d50000;font-weight:700">정답(빨간색)</span>과 일타강사 해설을 통합 기재. 범위(C1): 각 강의 슬라이드(닫힌 우주) 한정.</p>')
parts.append('<p class="note">학습법: ①~⑤ 중 <b style="color:#d50000">빨간색으로 표시된 선지가 「옳지 않은」 정답</b>입니다. '
             '나머지 4개 옳은 선지로 그 토픽의 핵심을 정리하고, 해설·바로잡기로 함정을 확인하세요. '
             '🟢 <span class="badge gap">보완</span> = 교수가 말로 강조 안 해도 요약/마지막 슬라이드에서 출제 집중되는 항목.</p>')
parts.append('</div>')

# integrated items (single column flow)
parts.append('<div class="page"><h2>문제 · 정답 · 해설 통합 (출제확률 순 1~50)</h2>')
for q in top:
    ai=q.get("answer_index",0); opts=q.get("options",[])
    ai=ai if isinstance(ai,int) and 0<=ai<len(opts) else 0
    parts.append(f'<div class="item{" g" if q["_gap"] else ""}">')
    parts.append('<div class="qhead">')
    gapbadge='<span class="badge gap">보완</span>' if q["_gap"] else ''
    parts.append('<div class="htop">'
                 f'<span class="qno">문 {q["_num"]}.</span>{gapbadge}'
                 f'<span class="badge">{esc(q["lecture_label"])}</span>'
                 f'<span class="badge">출제확률 {q.get("exam_probability","?")}%</span>'
                 f'<span class="badge">TIER {q.get("tier","?")}</span>'
                 f'<span class="badge">학습강도 <span class="star">{esc(q.get("study_strength","★★"))}</span></span></div>')
    parts.append(f'<div class="stem">{esc(q.get("stem",""))}</div>')
    for i,o in enumerate(opts):
        cls="opt ans" if i==ai else "opt"
        parts.append(f'<div class="{cls}"><span class="c">{CIRC[i]}</span>{esc(o)}</div>')
    parts.append(f'<div class="answerline">▶ 정답 {CIRC[ai]} (위 빨간색 선지가 「옳지 않은」 진술)</div>')
    parts.append('</div>')  # end qhead
    parts.append(f'<div class="exp"><span class="label">📝 일타강사 해설</span><br>{esc(q.get("explanation",""))}</div>')
    if q.get("correct_fact"):
        parts.append(f'<div class="fact"><span class="label">✔ 바로잡기</span> {esc(q.get("correct_fact",""))}</div>')
    if q.get("_fig_b64"):
        cap=(q.get("figure") or {}).get("caption","")
        parts.append(f'<figure><img src="data:image/jpeg;base64,{q["_fig_b64"]}" alt="figure"><figcaption>[그림] {esc(cap)} · 출처 슬라이드</figcaption></figure>')
    if q.get("selection_reason"):
        parts.append(f'<div class="reason"><span class="label">🎯 선정 사유</span> {esc(q.get("selection_reason",""))}</div>')
    parts.append('</div>')
parts.append('</div>')

# coverage + cut note
parts.append('<div class="page"><h2>출제 커버리지 & 상위 50 컷오프</h2>')
parts.append('<table class="meta-tbl"><tr><th>강의</th><th>상위50 채택</th><th>최저 채택확률</th></tr>')
for key in ORDER:
    qs=[q for q in top if q["lecture_key"]==key]
    mn=min([q["exam_probability"] for q in qs]) if qs else "-"
    parts.append(f'<tr><td>{esc(LABELS.get(key,key))}</td><td style="text-align:center">{len(qs)}</td><td style="text-align:center">{mn}</td></tr>')
parts.append(f'<tr><th>합계</th><th style="text-align:center">{TOPN}</th><th></th></tr></table>')
cutprob = top[-1]["exam_probability"] if top else 0
floor_txt = ", ".join(f"{LABELS.get(q['lecture_key'],q['lecture_key']).split(' ')[0]}({q['exam_probability']}%)" for q in floor_only)
parts.append(f'<p class="note">선별 방식: <b>14개 강의 각 최소 1문항 보장</b>(전 강의 커버) 후 나머지를 출제확률 순으로 채워 총 {TOPN}문항. '
             f'이 보장 규칙으로 들어온 낮은 확률 문항: {floor_txt if floor_txt else "없음"}. '
             f'v2(87문항) 중 미채택 {len(cut)}문항(전체판은 v2 참조). 핵심 {ncore} + 써머리 보완 {ngap}. '
             '전 문항 슬라이드 닫힌우주 기준 적대적 검증 완료, 정답은 빨간색 표기.</p>')
parts.append('</div></body></html>')

open(OUT,"w",encoding="utf-8").write("\n".join(parts))
print("="*60)
print(f"TOP {TOPN} (core {ncore} + gap {ngap}); cutoff prob = {cutprob}%")
print("per-lecture(top50):", {k:sum(1 for q in top if q['lecture_key']==k) for k in ORDER})
print("CUT (below top50):", [(q['id'],q['exam_probability']) for q in cut])
print("OUTPUT:", OUT)
print("figures:", [r for r in figrep])
