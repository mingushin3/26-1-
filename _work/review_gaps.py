# -*- coding: utf-8 -*-
import json, os, re
G = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\v2verified"
OUT = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\review_gaps.txt"
order=["golgi","bloodomics","scrna","llmngs","genetherapy","ev","nanomrna","dpath","thyroid","tert","brain","immuno","gastric","wonjaelee"]
def loadloose(p):
    t=open(p,encoding="utf-8").read().strip()
    t=re.sub(r"^```(json)?","",t).strip(); t=re.sub(r"```$","",t).strip()
    a,b=t.find("["),t.rfind("]")
    return json.loads(t[a:b+1])
lines=[]; total=0; issues=[]; figs=0; C="①②③④⑤"
counts={}
for k in order:
    p=os.path.join(G,k+".json")
    if not os.path.exists(p): issues.append(f"{k}: MISSING"); counts[k]=0; continue
    try: arr=loadloose(p)
    except Exception as e: issues.append(f"{k}: PARSE FAIL {e}"); counts[k]=0; continue
    counts[k]=len(arr); total+=len(arr)
    for q in arr:
        ai=q.get("answer_index",0); opts=q.get("options",[])
        if len(opts)!=5: issues.append(f"{q.get('id')}: {len(opts)} opts")
        if not isinstance(ai,int) or not(0<=ai<len(opts)): issues.append(f"{q.get('id')}: ai={ai}")
        if "옳지" not in q.get("stem",""): issues.append(f"{q.get('id')}: stem form")
        if (q.get('figure') or {}).get('needed'): figs+=1
        lines.append(f"\n{'='*76}\n[{k}] {q.get('id')} | prob {q.get('exam_probability')} | {q.get('study_strength')}")
        lines.append(f"TOPIC: {q.get('topic')}")
        lines.append(f"STEM : {q.get('stem')}")
        for i,o in enumerate(opts):
            lines.append(f"  {C[i]} {o}{'  ★틀림(정답)' if i==ai else ''}")
        lines.append(f"바로잡기: {q.get('correct_fact')}")
        lines.append(f"선정 : {q.get('selection_reason')}")
open(OUT,"w",encoding="utf-8").write("\n".join(lines))
print("TOTAL gap questions:", total)
print("counts:", {k:counts[k] for k in order})
print("figures requested:", figs)
print("ISSUES:", len(issues))
for i in issues: print("  -", i)
print("dump ->", OUT)
