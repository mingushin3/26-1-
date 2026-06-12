# -*- coding: utf-8 -*-
import json, os, re
V = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\verified"
OUT = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\review_dump.txt"
order=["wonjaelee","golgi","bloodomics","scrna","llmngs","genetherapy","ev","nanomrna","dpath","thyroid","tert","brain","immuno","gastric"]
def loadloose(p):
    t=open(p,encoding="utf-8").read().strip()
    a,b=t.find("["),t.rfind("]")
    return json.loads(t[a:b+1])
allq=[]
for k in order:
    for q in loadloose(os.path.join(V,k+".json")):
        allq.append(q)
allq.sort(key=lambda q:-q.get("exam_probability",0))
C="①②③④⑤"
lines=[]
for n,q in enumerate(allq,1):
    ai=q.get("answer_index",0)
    lines.append(f"\n{'='*78}")
    lines.append(f"[문{n}] {q.get('lecture_key')} | prob {q.get('exam_probability')} | {q.get('study_strength')} | id={q.get('id')}")
    lines.append(f"TOPIC: {q.get('topic')}")
    lines.append(f"STEM : {q.get('stem')}")
    for i,o in enumerate(q.get("options",[])):
        mk = "  ★틀림(정답)" if i==ai else ""
        lines.append(f"  {C[i]} {o}{mk}")
    lines.append(f"바로잡기: {q.get('correct_fact')}")
open(OUT,"w",encoding="utf-8").write("\n".join(lines))
print("wrote", OUT, "questions", len(allq))
