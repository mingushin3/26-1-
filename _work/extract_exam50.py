# -*- coding: utf-8 -*-
"""Replicate build_html_v3.py selection EXACTLY to get the authoritative top-50,
and dump compact specs for the study-guide coverage target + appendix."""
import os, glob, json, re

BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
WORK = os.path.join(BASE, "_work")
VDIR = os.path.join(WORK, "verified"); GDIR = os.path.join(WORK, "v2verified")
OUTDIR = os.path.join(WORK, "studyguide"); os.makedirs(OUTDIR, exist_ok=True)
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

def load_json_loose(path):
    txt = open(path, encoding="utf-8").read().strip()
    txt = re.sub(r"^```(json)?", "", txt).strip(); txt = re.sub(r"```$", "", txt).strip()
    a, b = txt.find("["), txt.rfind("]")
    if a != -1 and b != -1 and b > a: txt = txt[a:b+1]
    return json.loads(txt)

def norm(q, key, gap):
    q.setdefault("lecture_key", key); q.setdefault("lecture_label", LABELS.get(key, key)); q["_gap"] = gap
    try: q["exam_probability"] = int(round(float(q.get("exam_probability", 50))))
    except Exception: q["exam_probability"] = 50
    q.setdefault("study_strength", "★★"); q.setdefault("tier", 1)
    for f in ("explanation","correct_fact","selection_reason","topic","stem"): q.setdefault(f, "")
    ai = q.get("answer_index")
    if not isinstance(ai, int) or not (0 <= ai < len(q.get("options", []))): q["answer_index"] = 0
    return q

allq = []
for key in ORDER:
    for d, gap in ((VDIR, False), (GDIR, True)):
        p = os.path.join(d, f"{key}.json")
        if not os.path.exists(p): continue
        for q in load_json_loose(p): allq.append(norm(q, key, gap))
allq.sort(key=lambda q: -q.get("exam_probability", 0))

# v3 selection: per-lecture floor (>=1) then fill by prob to 50
by_lec = {}
for q in allq: by_lec.setdefault(q["lecture_key"], []).append(q)
floor = [by_lec[k][0] for k in ORDER if by_lec.get(k)]
floor_ids = {q["id"] for q in floor}
rest = [q for q in allq if q["id"] not in floor_ids]
fill = rest[:max(0, TOPN - len(floor))]
top = floor + fill
top.sort(key=lambda q: -q.get("exam_probability", 0))
top = top[:TOPN]
for i, q in enumerate(top, 1): q["_num"] = i
top_ids = {q["id"] for q in top}

def slim(q):
    ai = q["answer_index"]; opts = q.get("options", [])
    return {
        "id": q["id"], "num": q.get("_num"), "lecture_key": q["lecture_key"],
        "lecture_label": q["lecture_label"], "topic": q.get("topic",""),
        "exam_probability": q["exam_probability"], "gap": q["_gap"],
        "stem": q.get("stem",""),
        "answer_index": ai, "answer_option": opts[ai] if 0 <= ai < len(opts) else "",
        "correct_fact": q.get("correct_fact",""),
    }

exam50 = [slim(q) for q in top]
all87 = [{"id":q["id"],"lecture_key":q["lecture_key"],"in_top50":q["id"] in top_ids,
          "exam_probability":q["exam_probability"],"topic":q.get("topic",""),
          "correct_fact":q.get("correct_fact",""),"gap":q["_gap"]} for q in allq]

json.dump(exam50, open(os.path.join(OUTDIR,"exam50.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(all87, open(os.path.join(OUTDIR,"all87.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

per_top = {k: sum(1 for q in top if q["lecture_key"]==k) for k in ORDER}
per_all = {k: len(by_lec.get(k,[])) for k in ORDER}
print("TOTAL allq:", len(allq), " top50:", len(top))
print("per-lecture TOP50:", per_top)
print("per-lecture ALL(87):", per_all)
print("cutoff prob:", top[-1]["exam_probability"])
print("ids per lecture (top50):")
for k in ORDER:
    ids = [q["id"] for q in top if q["lecture_key"]==k]
    print(f"  {k:12s} ({per_top[k]}): {ids}")
print("WROTE:", os.path.join(OUTDIR,"exam50.json"), "and all87.json")
