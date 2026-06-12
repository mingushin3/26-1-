# -*- coding: utf-8 -*-
"""Extract per-lecture source bundles (slide text + draft section + recording) for workflow agents."""
import fitz, os, glob, re, sys, io

BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
WORK = os.path.join(BASE, "_work")
BUND = os.path.join(WORK, "bundles")
os.makedirs(BUND, exist_ok=True)
os.makedirs(os.path.join(BASE, "_figures"), exist_ok=True)

# ---------- 1) Extract draft docx full text ----------
import zipfile
from html import unescape
docx = os.path.join(BASE, "생명의과학세미나_시험예측(초안).docx")
with zipfile.ZipFile(docx) as z:
    xml = z.read("word/document.xml").decode("utf-8")
draft = re.sub(r"</w:p>", "\n", xml)
draft = re.sub(r"<[^>]+>", "", draft)
draft = unescape(draft)

# draft split markers in document order: (key, marker_substring)
markers = [
    ("golgi",       "260310_생명의과학세미나1"),
    ("bloodomics",  "260317_생명의과학세미나2"),
    ("scrna",       "260324_미생물학교실"),
    ("llmngs",      "260331_슬라이드"),
    ("genetherapy", "260407_김영광"),
    ("ev",          "260414_김일진"),
    ("nanomrna",    "260421_구희범"),
    ("dpath",       "260428_"),
    ("thyroid_a",   "260513_2026_갑상선암"),
    ("thyroid_b",   "260512_갑상선암"),
    ("tert",        "260519_텔로미어"),
    ("brain",       "260526_"),
    ("immuno",      "260602"),
]
positions = []
cur = 0
for key, mk in markers:
    idx = draft.find(mk, cur)
    positions.append((key, idx))
    if idx >= 0:
        cur = idx + 1
draft_sections = {}
for i, (key, idx) in enumerate(positions):
    if idx < 0:
        draft_sections[key] = ""
        continue
    end = len(draft)
    for j in range(i+1, len(positions)):
        if positions[j][1] > idx:
            end = positions[j][1]
            break
    draft_sections[key] = draft[idx:end].strip()
# merge thyroid
draft_sections["thyroid"] = (draft_sections.pop("thyroid_a","") + "\n\n=====\n\n" + draft_sections.pop("thyroid_b","")).strip()
print("draft sections:", {k: len(v) for k,v in draft_sections.items()})

# ---------- 2) Lecture definitions ----------
# key -> (date, title, lecturer, [slide_pdf filenames], recording_glob, draft_key, weight_note)
LECTURES = [
    ("wonjaelee",  "03-03","분자생물학/세포신호(불참, 슬라이드 기반)","이원재(WonJae Lee)",
        ["3월 3일 합동강의 (1).pdf"], None, None, "녹음 없음 → 가중치 0.8x, 슬라이드만"),
    ("golgi",      "03-10","골지체 비정형 기능 / 소기관-질병","김지윤",
        ["2026_합동강의_약리학교실 김지윤_강의원고.pdf","260310_생명의과학세미나1_필수슬라이드.pdf"], "03-10*", "golgi", "필수슬라이드(요약1장)=출제범위 핵심"),
    ("bloodomics", "03-17","유전체 기반 혈액암 오믹스","정승현(Seung-Hyun Jung)",
        ["합동강의_20260317.pdf","260317_생명의과학세미나2_필수슬라이드.pdf"], "03-17*", "bloodomics", "필수슬라이드 존재"),
    ("scrna",      "03-24","단일세포 전사체 scRNAseq","이혜옥(Hae-Ock Lee)",
        ["20260324_대학원합동강의_scRNAseq_.pdf","20260324_대학원합동강의_필수슬라이드_.pdf"], "03-24*", "scrna", "필수슬라이드(2장) 존재"),
    ("llmngs",     "03-31","LLM/NGS/정밀의료 바이오인포","의료정보학교실",
        ["3월 31일_대학원공개강의 (1).pdf","3월 31일_대학원공개강의_summary.pdf"], "03-31*", "llmngs", "summary 1장"),
    ("genetherapy","04-07","유전자치료→유전체교정","김영광",
        ["2026_대학원합동강의_김영광 (1).pdf","2026_대학원합동강의_김영광_시험_필수슬라이드.pdf"], "04-07*", "genetherapy", "시험 필수슬라이드(7장)=출제범위 핵심"),
    ("ev",         "04-14","세포외소포(EV)/액체생검","김일진(Iljin Kim)",
        ["2026학년도 1학기 합동강의 강의원고_김일진.pdf"], "04-14*", "ev", ""),
    ("nanomrna",   "04-21","나노메디슨/mRNA-LNP","구희범(Heebeom Koo)",
        ["20260421_합동강의_koo.pdf"], "04-21*", "nanomrna", ""),
    ("dpath",      "04-28","디지털병리 WSI/AI","이성학(Sung Hak Lee)",
        ["DL_Pathology_2026-대학원-ver1.3 (1).pdf"], "04-28*", "dpath", "슬라이드 97장(방대)"),
    ("thyroid",    "05-12","갑상선암/CYFRA 21-1 바이오마커","임동석",
        ["대학원발표_2026_갑상선암_biomarker (2).pdf"], "05-12*", "thyroid", "초안 2벌 병합"),
    ("tert",       "05-19","TERT/B형간염/간암","장정원(JJW)",
        ["대학원합동강의-JJW-P20236 (1).pdf"], "05-19*", "tert", ""),
    ("brain",      "05-26","신경외과/뇌종양","Stephen Ahn",
        ["260526_대학원강의자료.pdf"], "05-26*", "brain", "슬라이드 104장(방대)"),
    ("immuno",     "06-02","면역항암/간암 저항성","성필수(Pil Soo Sung)",
        ["202606 대학원 통합강의_ 종양면역학 (1).pdf"], "06-02*", "immuno", ""),
    ("gastric",    "06-09","위암 진단/분류/맞춤치료","박재명",
        ["합동강의_강의록__박재명_1.pdf"], "06-09*", "gastric", "슬라이드덱 없음, 강의록4쪽+녹음 기반. 최신강의=우선순위↑"),
]

def read_recording(glob_pat):
    if not glob_pat:
        return None, None
    hits = glob.glob(os.path.join(BASE, glob_pat + ".txt"))
    if not hits:
        return None, None
    path = hits[0]
    data = None
    for enc in ("utf-8","cp949","euc-kr","utf-16"):
        try:
            with open(path, "r", encoding=enc) as f:
                data = f.read()
            break
        except Exception:
            continue
    return path, data

def slide_text(pdf_name, max_chars=200000):
    p = os.path.join(BASE, pdf_name)
    if not os.path.exists(p):
        return f"[MISSING PDF: {pdf_name}]"
    doc = fitz.open(p)
    out = []
    for i in range(doc.page_count):
        t = doc[i].get_text().strip()
        t = re.sub(r"\n{3,}", "\n\n", t)
        out.append(f"--- [PAGE {i+1}/{doc.page_count}] {pdf_name} ---\n{t}")
    doc.close()
    s = "\n\n".join(out)
    return s[:max_chars]

manifest = []
for key,date,title,lect,pdfs,recglob,dkey,note in LECTURES:
    parts = []
    parts.append(f"# 강의 번들: {date} {title}\n- 교수: {lect}\n- 슬라이드 PDF: {pdfs}\n- 비고: {note}\n")
    # slides
    parts.append("\n================ [SLIDE TEXT — 출제범위(C1) 닫힌 우주의 사실원] ================\n")
    for pdf in pdfs:
        parts.append(slide_text(pdf))
        parts.append("\n")
    # draft
    if dkey and draft_sections.get(dkey):
        parts.append("\n================ [DRAFT 분석(초안) — 토픽맵/가중치/모범답안 사실원] ================\n")
        parts.append(draft_sections[dkey])
    else:
        parts.append("\n================ [DRAFT 분석 없음 — 슬라이드/녹음으로 신규 분석 필요] ================\n")
    # recording
    recpath, recdata = read_recording(recglob)
    if recdata:
        parts.append(f"\n================ [RECORDING 녹음본 — 교수 오피셜 발화(해설/강조신호 사실원) | file: {os.path.basename(recpath)}] ================\n")
        parts.append(recdata)
    else:
        parts.append("\n================ [RECORDING 없음] ================\n")
    content = "\n".join(parts)
    outp = os.path.join(BUND, f"{key}.md")
    with open(outp, "w", encoding="utf-8") as f:
        f.write(content)
    manifest.append((key,date,title,lect,len(content), recpath if recdata else None))
    print(f"WROTE {key}.md  ({len(content):,} chars)  rec={'Y' if recdata else 'N'}")

# manifest
with open(os.path.join(WORK, "manifest.txt"), "w", encoding="utf-8") as f:
    for m in manifest:
        f.write(f"{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\tchars={m[4]}\trec={m[5]}\n")
print("\nDONE. bundles in", BUND)
