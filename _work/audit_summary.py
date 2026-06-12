# -*- coding: utf-8 -*-
import json, os, re
A = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사\_work\audit"
order=["golgi","bloodomics","scrna","llmngs","genetherapy","ev","nanomrna","dpath","thyroid","tert","brain","immuno","gastric","wonjaelee"]
def loadloose(p):
    t=open(p,encoding="utf-8").read().strip()
    t=re.sub(r"^```(json)?","",t).strip(); t=re.sub(r"```$","",t).strip()
    a,b=t.find("{"),t.rfind("}")
    return json.loads(t[a:b+1])
tot_add=0; tot_drop=0
for k in order:
    p=os.path.join(A,k+".json")
    if not os.path.exists(p):
        print(f"\n##### {k}: MISSING audit"); continue
    try: d=loadloose(p)
    except Exception as e:
        print(f"\n##### {k}: PARSE FAIL {e}"); continue
    gaps=[g for g in d.get("gaps",[]) if g.get("recommend_add")]
    weak=d.get("weak_to_replace",[])
    addc=d.get("recommended_add_count",0)
    drops=d.get("recommended_drop_ids",[])
    tot_add+=addc; tot_drop+=len(drops)
    print(f"\n##### {k} | verdict={d.get('verdict')} | 권장추가={addc} | 약문항={len(weak)} | drop={drops}")
    # current topics reassessed prob (flag low)
    low=[c for c in d.get("current_topics",[]) if (c.get("exam_prob_reassessed") or 100)<70 or not c.get("keep",True)]
    for c in low:
        print(f"   [현문항 약함] {c.get('id')} p={c.get('exam_prob_reassessed')} keep={c.get('keep')} : {c.get('note','')[:80]}")
    for g in gaps:
        print(f"   [GAP +{g.get('exam_prob')}] {g.get('topic')}  <{g.get('source_slide')}> :: {g.get('why_high_yield','')[:90]}")
    for w in weak:
        print(f"   [WEAK] {w.get('id')} : {w.get('reason','')[:90]}")
    if d.get("notes"): print(f"   note: {d.get('notes')[:160]}")
print(f"\n===== TOTAL recommended_add={tot_add}, recommended_drop={tot_drop} =====")
