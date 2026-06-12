# -*- coding: utf-8 -*-
import json, os, re
V = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\verified"
def loadloose(p):
    t=open(p,encoding="utf-8").read().strip()
    t=re.sub(r"^```(json)?","",t).strip(); t=re.sub(r"```$","",t).strip()
    a,b=t.find("["),t.rfind("]")
    if a!=-1 and b!=-1: t=t[a:b+1]
    return json.loads(t)
order=["wonjaelee","golgi","bloodomics","scrna","llmngs","genetherapy","ev","nanomrna","dpath","thyroid","tert","brain","immuno","gastric"]
total=0; issues=[]; counts={}; figs=[]
data={}
for k in order:
    p=os.path.join(V,k+".json")
    try: arr=loadloose(p)
    except Exception as e: issues.append(f"{k}: PARSE FAIL {e}"); counts[k]=0; continue
    data[k]=arr; counts[k]=len(arr); total+=len(arr)
    for q in arr:
        qid=q.get("id","?"); opts=q.get("options",[]); ai=q.get("answer_index")
        if len(opts)!=5: issues.append(f"{qid}: {len(opts)} options")
        if not isinstance(ai,int) or not(0<=ai<len(opts)): issues.append(f"{qid}: ai={ai}")
        if "옳지" not in q.get("stem",""): issues.append(f"{qid}: stem form? {q.get('stem','')[:50]}")
        fg=q.get("figure") or {}
        if fg.get("needed"): figs.append(f"{qid} -> {fg.get('pdf')} p{fg.get('page')}: {fg.get('caption','')}")
print("TOTAL:",total); print("counts:",{k:counts[k] for k in order})
print("figures requested:",len(figs))
for f in figs: print("   FIG",f)
print("ISSUES:",len(issues))
for i in issues: print("   -",i)
print("\n"+"="*70+"\nSAMPLES\n"+"="*70)
def dump(k, idx=0):
    q=data[k][idx]
    print(f"\n### [{k}] {q.get('id')} | prob={q.get('exam_probability')} tier={q.get('tier')} {q.get('study_strength')}")
    print("TOPIC:",q.get("topic"))
    print("STEM :",q.get("stem"))
    for i,o in enumerate(q.get("options",[])):
        mk=" <== 옳지않음(정답)" if i==q.get("answer_index") else ""
        print(f"   {'①②③④⑤'[i]} {o}{mk}")
    print("해설 :",q.get("explanation"))
    print("바로잡기:",q.get("correct_fact"))
    print("선정 :",q.get("selection_reason"))
for k in ["golgi","gastric","wonjaelee","immuno","scrna"]:
    if k in data and data[k]: dump(k,0)
