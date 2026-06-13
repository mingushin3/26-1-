export const meta = {
  name: 'studyguide-v2-content',
  description: '14개 강의를 일타강사 레이어드 정리본 v2 콘텐츠(JSON)로 재생성 + 적대적 검증',
  phases: [
    { title: 'Generate', detail: '강의별 1 에이전트: 스크립트+슬라이드+JSON 교차대조 → 섹션 JSON' },
    { title: 'Verify', detail: '강의별 1 적대적 검증: 스코프 인용 실재·사실 일치·exam50 커버·약어풀이' },
  ],
}

const BASE = '/Users/min9/Documents/GitHub/26-1-'
const SG = `${BASE}/_work/studyguide`

// code, 라벨, 교수, 스크립트 txt(절대경로 or null), exam50 qrefs(반드시 커버)
const LECTURES = [
  { code:'wonjaelee', label:'03-03 암생물학 패러다임 (이원재)', prof:'이원재', txt:null,
    slide:'3월 3일 합동강의 (1).pdf', exam50:['wonjaelee-g1','wonjaelee-g2'] },
  { code:'golgi', label:'03-10 골지체 (김지윤)', prof:'김지윤',
    txt:`${BASE}/03-10 강의 골지체의 비정형 기능, 소기관 위치 기반 질병.txt`,
    slide:'2026_합동강의_약리학교실 김지윤_강의원고.pdf', exam50:['golgi-1','golgi-2','golgi-3','golgi-g1','golgi-4'] },
  { code:'bloodomics', label:'03-17 혈액암 오믹스 (정승현)', prof:'정승현',
    txt:`${BASE}/03-17 강의 유전체 분석 기반 혈액암 오믹스 데이터 분석.txt`,
    slide:'260317_생명의과학세미나2_필수슬라이드.pdf', exam50:['bloodomics-1','bloodomics-g1','bloodomics-2'] },
  { code:'scrna', label:'03-24 단일세포 전사체 scRNA-seq (이혜옥)', prof:'이혜옥',
    txt:`${BASE}/03-24 강의 단일세포 전사체 분석 입문.txt`,
    slide:'20260324_대학원합동강의_필수슬라이드_.pdf', exam50:['scrna-1','scrna-2','scrna-3','scrna-4','scrna-g1'] },
  { code:'llmngs', label:'03-31 LLM·NGS·정밀의료·바이오인포', prof:'(의료정보학)',
    txt:`${BASE}/03-31 강의 LLM, NGS, 정밀의료와 바이오인포매틱스 해.txt`,
    slide:'3월 31일_대학원공개강의_summary.pdf', exam50:['llmngs-1','llmngs-2'] },
  { code:'genetherapy', label:'04-07 유전자치료 (김영광)', prof:'김영광',
    txt:`${BASE}/04-07 강의 유전자 치료 기술과 최신 동향.txt`,
    slide:'2026_대학원합동강의_김영광_시험_필수슬라이드.pdf', exam50:['genetherapy-1','genetherapy-2','genetherapy-3'] },
  { code:'ev', label:'04-14 세포외소포 EV (김일진)', prof:'김일진',
    txt:`${BASE}/04-14 강의 세포외 소포(EV) 전주기—정의·분류·기능, 액.txt`,
    slide:'2026학년도 1학기 합동강의 강의원고_김일진.pdf', exam50:['ev-1','ev-2','ev-3'] },
  { code:'nanomrna', label:'04-21 나노메디슨·mRNA-LNP (구희범)', prof:'구희범',
    txt:`${BASE}/04-21 강의 나노메디슨과 mRNA-LNP 유전자 전달의 임상.txt`,
    slide:'20260421_합동강의_koo.pdf', exam50:['nanomrna-1'] },
  { code:'dpath', label:'04-28 디지털병리 WSI·AI (이성학)', prof:'이성학',
    txt:`${BASE}/04-28 강의 디지털 병리 WSI와 딥러닝 기반 AI 병리 —.txt`,
    slide:'DL_Pathology_2026-대학원-ver1.3 (1).pdf', exam50:['dpath-1','dpath-2','dpath-g1','dpath-g2'] },
  { code:'thyroid', label:'05-12 갑상선암 바이오마커 CYFRA (임동석)', prof:'임동석',
    txt:`${BASE}/05-12 강의 갑상선암 진단과 새로운 바이오마커 CYFRA 2.txt`,
    slide:'대학원발표_2026_갑상선암_biomarker (2).pdf', exam50:['thyroid-1','thyroid-2','thyroid-3','thyroid-g1'] },
  { code:'tert', label:'05-19 TERT·B형간염·간암 (장정원)', prof:'장정원',
    txt:`${BASE}/05-19 강의 B형 간염, TERT, 그리고 간암 발생 메커니.txt`,
    slide:'대학원합동강의-JJW-P20236 (1).pdf', exam50:['tert-1','tert-2','tert-g1','tert-3','tert-g2','tert-g3'] },
  { code:'brain', label:'05-26 신경외과·뇌종양 (Stephen Ahn)', prof:'안스데반(Stephen Ahn)',
    txt:`${BASE}/05-26 강의 신경외과 및 뇌종양 치료의 최신 지견.txt`,
    slide:'260526_대학원강의자료.pdf', exam50:['brain-1','brain-2','brain-3','brain-4'] },
  { code:'immuno', label:'06-02 면역항암·간암저항성 (성필수)', prof:'성필수',
    txt:`${BASE}/06-02 강의 면역항암치료 원리와 간암 저항성 극복 전략.txt`,
    slide:'202606 대학원 통합강의_ 종양면역학 (1).pdf', exam50:['immuno-1','immuno-2','immuno-g1','immuno-g2'] },
  { code:'gastric', label:'06-09 위암 맞춤치료 (박재명)', prof:'박재명',
    txt:`${BASE}/06-09 강의 위암의 진단, 분류 및 최신 맞춤형 치료 전략.txt`,
    slide:'합동강의_강의록__박재명_1.pdf', exam50:['gastric-1','gastric-2','gastric-3','gastric-g1'] },
]

// ── 섹션 JSON 스키마 (generate 산출 = verify의 section 필드) ──
const SECTION = {
  type:'object', additionalProperties:true,
  properties:{
    code:{type:'string'},
    lecture_label:{type:'string'},
    professor:{type:'string'},
    essence:{type:'string', description:'🎯 한 줄 핵심. 비전공 20세가 한 번에 그림 잡는 평이한 1문장.'},
    analogy:{type:'string', description:'🍱 일상 비유 1~2문장.'},
    scope:{type:'object', additionalProperties:false, properties:{
      declared:{type:'boolean', description:'교수가 시험범위를 명시적으로 못박았으면 true'},
      quote:{type:'string', description:'명시했다면 txt에 실제 존재하는 verbatim 인용(없으면 빈 문자열)'},
      summary:{type:'string', description:'"시험범위 = …" 형태 1줄. 미선언이면 "명시 없음 — 강조신호 기반 선정".'}
    }, required:['declared','quote','summary']},
    top_topics:{type:'array', minItems:2, maxItems:3, items:{
      type:'object', additionalProperties:false, properties:{
        title:{type:'string'},
        plain_explanation:{type:'string', description:'2~4문장. 비전공 20세 눈높이. 모든 영어/약어는 첫 등장 시 한글 풀이 병기.'},
        why_how:{type:'string', description:'왜 중요/어떻게 작동하는지 기전을 일상어로 1~2문장.'},
        exam_point:{type:'object', additionalProperties:false, properties:{
          correct:{type:'string', description:'✅ 슬라이드 기반 옳은 방향'},
          trap:{type:'string', description:'❌ 시험에서 거꾸로 뒤집어 내는 함정 진술'}
        }, required:['correct','trap']},
        qref:{type:'string'},
        exam_probability:{type:'integer'}
      }, required:['title','plain_explanation','why_how','exam_point','qref','exam_probability']
    }},
    checklist:{type:'array', description:'top_topics에 안 들어간 나머지 지식점(선언범위 내). exam50 qref는 무조건 포함.', items:{
      type:'object', additionalProperties:false, properties:{
        topic:{type:'string'},
        correct:{type:'string', description:'✅ 1줄'},
        trap:{type:'string', description:'❌ 1줄'},
        qref:{type:'string'},
        is_exam50:{type:'boolean'}
      }, required:['topic','correct','trap','qref','is_exam50']
    }},
    memorize:{type:'array', items:{type:'string'}, description:'시험장 직전 한 줄 암기 3~5개'},
    figure:{type:'object', additionalProperties:false, properties:{
      pdf:{type:'string'}, page:{type:'integer'}, caption:{type:'string'}
    }, required:['pdf','page','caption']}
  },
  required:['code','lecture_label','professor','essence','analogy','scope','top_topics','checklist','memorize','figure']
}

const VERIFY = {
  type:'object', additionalProperties:false,
  properties:{
    section: SECTION,
    scope_quote_verified:{type:'boolean'},
    coverage_ok:{type:'boolean'},
    missing_exam50:{type:'array', items:{type:'string'}},
    issues_found:{type:'array', items:{type:'string'}}
  },
  required:['section','scope_quote_verified','coverage_ok','missing_exam50','issues_found']
}

function genPrompt(L){
  return `너는 대한민국 대학 "일타강사"다. 의학·생명과학 대학원 합동강의를 듣는 **비전공 대학교 1학년(20세)**이 한 번 읽고 바로 이해하고, 시험에서 맞히도록 강의 1개의 정리본 섹션을 만든다.

# 대상 강의
- code: ${L.code}
- 라벨: ${L.label}
- 교수: ${L.prof}
- 스크립트(txt): ${L.txt ? L.txt : '(이 강의는 전사 txt 없음 — JSON 데이터만 사용)'}
- 슬라이드 PDF 파일명: ${L.slide}
- 이 강의의 exam50 qref(예측 출제 — 반드시 어딘가에 커버): ${JSON.stringify(L.exam50)}

# 반드시 읽을 입력 파일 (python json.load 또는 Read 사용; 파일명에 특수문자 있으니 Read 툴 또는 python open() 권장)
1. ${SG}/${L.code}.json — **1차 사실 출처**. keys: essence, analogy, concepts(heading+points; 슬라이드 기반), traps(지식점: qref/topic/correct(✅)/trap(❌)), memorize, figures(pdf/page/caption). 이 강의의 traps가 전체 지식점 풀(=all87 해당분).
2. ${BASE}/_work/verified/${L.code}.json — 문항들: topic, tier, exam_probability, correct_fact, explanation, selection_reason. 출제확률·중요도 근거.
3. ${BASE}/_work/v2add/${L.code}.json — 보강 토픽(있으면 참고).
${L.txt ? `4. 스크립트 txt — **스코프/강조 판단 전용**. python으로 파일을 읽고 정규식으로 다음 키워드 주변(±5줄)을 확인: 시험|기말|출제|낼|나올|나옵|안 나|써머리|summary|슬라이드|필수|외우|암기|중요|핵심|반드시|꼭|이것만|이거는|포인트|쉽|다 나. 교수가 시험범위/난이도/꼭 볼 것을 직접 말한 문장을 찾아라.` : ''}

# 산출(StructuredOutput JSON) 작성 규칙
- **C1(절대): 사실은 슬라이드(닫힌 우주)에 등장한 것만.** studyguide concepts/traps와 verified가 이미 슬라이드 기반이니 그것을 사실 근거로 삼고, 새 사실을 지어내지 마라. 스크립트는 강조·범위 판단에만.
- essence: studyguide essence를 **더 쉬운 1문장**으로 압축(전공 약어 최소화).
- analogy: studyguide analogy를 살리되 어색하면 다듬기.
- scope:
  - txt에서 교수가 시험범위를 명시했으면 declared=true, quote=**txt에 실제 그대로 존재하는 문장 일부(verbatim, 너가 지어내면 안 됨)**, summary="시험범위 = …".
  - 명시 없으면 declared=false, quote="", summary="명시적 범위 선언 없음 — 강조신호(반복·경고·비교) 기반 선정".
- top_topics(2~3개): 출제확률 최상위 + 교수 최강조 토픽을 골라라(대개 ${L.code}-1/-2/-3 또는 exam50 상위). 각 토픽:
  - title: 개념명(한글, 핵심 영어 병기 가능).
  - plain_explanation: **2~4문장, 20세 눈높이.** 모든 영어/약어는 첫 등장 시 한글 뜻 병기(예: "TGN(트랜스골지망 = 골지의 출구쪽 끝)"). 그림 그리듯 직관적으로.
  - why_how: 왜 중요한지/어떻게 작동하는지 일상어 1~2문장.
  - exam_point.correct: ✅ 옳은 방향(슬라이드 근거). exam_point.trap: ❌ 시험이 거꾸로 뒤집어 낼 함정 문장.
  - qref: 해당 studyguide trap qref. exam_probability: verified/추정 정수(%).
- checklist: top_topics에 안 든 **나머지 지식점**을 ✅/❌ 1줄씩 압축 수록. 단:
  - scope.declared=true(교수가 범위를 좁게 못박음)면 **선언 범위 밖 지엽 항목은 과감히 제외**.
  - 그러나 **exam50 qref(${JSON.stringify(L.exam50)})는 top_topics나 checklist 중 어딘가에 무조건 포함**(is_exam50=true). 범위 밖이어도 유지.
- memorize: studyguide memorize를 시험장 직전용 한 줄 암기 3~5개로 다듬기.
- figure: studyguide figures[0]의 pdf/page/caption 그대로(가장 결정적 슬라이드 1장).

출력은 JSON만. 한국어. 군더더기 없이.`
}

function verPrompt(L){
  return `너는 적대적 사실검증자다. 아래 강의 정리본 섹션(JSON)을 원본 데이터와 대조해 오류를 잡고 **수정된 섹션**을 돌려준다.

# 강의: ${L.code} / ${L.label}
# 이 강의 exam50 qref(반드시 커버): ${JSON.stringify(L.exam50)}
# 대조용 파일: ${SG}/${L.code}.json (traps=정답풀), ${BASE}/_work/verified/${L.code}.json (correct_fact), ${L.txt ? `스크립트 ${L.txt}` : '(txt 없음)'}

# 검증 항목 (각각 수행 후 수정)
1) **스코프 인용 실재성**: section.scope.declared=true이면 scope.quote가 txt 파일에 **실제로 존재**하는지 python으로 확인(핵심 어절로 substring 검색, 공백차이 허용). 존재하지 않으면 → declared=false로 강등, quote="", summary 수정. 결과를 scope_quote_verified로 보고.
2) **사실 일치**: 각 top_topic의 plain_explanation·exam_point.correct가 studyguide traps의 correct(✅)/verified correct_fact와 **모순되지 않는지**. 방향이 거꾸로거나 슬라이드에 없는 주장(환각)이면 데이터에 맞게 수정. checklist의 correct/trap도 점검.
3) **커버리지**: exam50 qref(${JSON.stringify(L.exam50)})가 top_topics[].qref ∪ checklist[].qref에 **전부** 있는지 확인. 빠진 게 있으면 studyguide trap에서 해당 항목을 가져와 checklist에 추가(is_exam50=true). 최종 누락을 missing_exam50로, 빈 배열이면 coverage_ok=true.
4) **약어 풀이**: plain_explanation/why_how/exam_point에 한글 풀이 없이 등장하는 영어 약어(예: TGN, YAP, ctDNA, UMI, BWA, PRS, AAV, ASO, siRNA, LNP, WSI, CNN, TPS, FNAC, Tg, TERT, HBV, BBB, GBM, CAR-T, CAF, TAM, TCGA, HER2, MSI, PD-L1, CLDN18.2 등)가 있으면 **첫 등장 위치에 한글 뜻을 병기**.
5) 발견·수정한 문제를 issues_found에 간단히 나열.

출력: VERIFY 스키마(section=수정된 섹션 전체, scope_quote_verified, coverage_ok, missing_exam50, issues_found). 섹션의 모든 필드를 보존하며 수정분만 반영. 한국어.`
}

phase('Generate')
log(`14개 강의 콘텐츠 생성 시작 (generate→verify 파이프라인)`)

const results = await pipeline(
  LECTURES,
  (L) => agent(genPrompt(L), { label:`gen:${L.code}`, phase:'Generate', schema: SECTION }),
  (section, L) => {
    if (!section) return null
    return agent(verPrompt(L), { label:`verify:${L.code}`, phase:'Verify', schema: VERIFY })
      .then(v => v ? { code:L.code, ...v } : { code:L.code, section, scope_quote_verified:null, coverage_ok:null, missing_exam50:[], issues_found:['verify 실패 — 생성본 그대로 사용'] })
  }
)

const ok = results.filter(Boolean)
log(`완료: ${ok.length}/14. 커버리지 OK: ${ok.filter(r=>r.coverage_ok).length}, 미커버 강의: ${ok.filter(r=>r.missing_exam50&&r.missing_exam50.length).map(r=>r.code).join(',')||'없음'}`)
return ok
