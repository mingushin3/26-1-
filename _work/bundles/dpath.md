# 강의 번들: 04-28 디지털병리 WSI/AI
- 교수: 이성학(Sung Hak Lee)
- 슬라이드 PDF: ['DL_Pathology_2026-대학원-ver1.3 (1).pdf']
- 비고: 슬라이드 97장(방대)


================ [SLIDE TEXT — 출제범위(C1) 닫힌 우주의 사실원] ================

--- [PAGE 1/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Sung Hak Lee
The Catholic University of Korea
Seoul St. Mary’s Hospital
1

--- [PAGE 2/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Impact of Digital Pathology
⚫Rapid referral of cases between organizations
✓Enhancing access to expert advice and opinion on diagnoses
⚫Improves laboratory workflow and analysis
✓Algorithms for analyzing slides are objective, accurate and quicker than 
microscopy
✓Rapid access to prior cases
⚫Sets the scene for the use of AI which will help bring advances to 
pathology services
What is Digital Pathology? 
⚫Acquisition, management, sharing and interpretation of pathology 
information in a digital environment
⚫Digital slides are created when glass slides are captured with a scanning 
device, that can be viewed on a computer screen or mobile device
2

--- [PAGE 3/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Whole Slide Image(WSI)
⚫전체슬라이드스캐너를이용해유리슬라이드한장을모두
스캔하여디지털변환된단일고해상도유리슬라이드영상
파일
⚫수십억개의픽셀을포함하고있는고해상도이미지, 파일크
기는1GB에서4GB정도
⚫일반적으로다중계층피라미드형식으로저장되어있으며, 
다양한해상도의이미지레벨에접근할수있음
3

--- [PAGE 4/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
WSI 전처리
패치추출(Patch Extraction)
⚫고해상도WSI의전체크기를다루는대신, 이미지를더작은, AI를통해처리가능한단위인정사각형패치
(Patch)로나누어분석
⚫패치크기는보통256x256 픽셀에서1024x1024 픽셀까지다양하게설정할수있음
4

--- [PAGE 5/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
WSI 전처리
조직/세포분할(Tissue/Cell Segmentation): 불필요한영역(배경또는흐릿한부분등)을식별하고제거
⚫배경제거(Background Removal): 의미있는조직/세포데이터가없는불필요한영역의처리를피하여계
산부담을줄임
색상정규화(Color Normalization): 이미지내색상값의분포를조정
⚫여러슬라이드간에색상차이를일관되게유지하여, 학습데이터불균형을줄이고결과의왜곡을최소화함
5

--- [PAGE 6/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
AI로WSI 분석
Patch Classifier + CNN(Convolutional Neural Network)
⚫Convolution (합성곱): 특정크기를가진필터를일정간격으로이동하면서입력데이터에각각의행과열
에필터값들을곱해주고그결과들을모두더하여새로운행렬에넣는연산작업을의미
⚫풀링(Pooling): 각각의개별패치에서예측된결과를집계하는기술
⚫컨볼루션필터에의해추출된피쳐맵의크기를축소하는데사용
⚫필요한주요특징들만학습을하여오버피팅이발생하는것을방지하기위함
⚫이런식으로컨볼루션과풀링과정을여러번반복하다보면최초이미지에서주요특이점들만남게됨
6

--- [PAGE 7/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
AI로WSI 분석
⚫완전연결계층(Fully Connected Layer, FC Layer): 추출된특징들을종합하여최종적인분류나예측을수
행하는역할을함
⚫주로합성곱신경망(CNN)의마지막부분에서평탄화(Flatten)된특징들을받아가중치를적용하고활성화함수를통해최종출력
을만들어내는데사용됨
⚫Softmax 함수: 활성화함수중하나로, 전체에대한각각의확률을구할때사용하는함수
⚫입력값에대한각각의편차를확대시켜큰값은상대적으로더크게, 작은값은더작게만듦
⚫이방식으로최종적으로입력이미지가어떤이미지인지확률을통하여분류가됨
7

--- [PAGE 8/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
AI Task
패치분류(Patch-level Classification)
⚫WSI의작은부분을분석하여해당패치가병변을포함하고있는지를판단
⚫패치간의상관관계나위치정보를사용하지않고개별패치만을분석함
⚫모델은원본WSI에서의위치관계를고려하지않기때문에공간정보가소
실될수있으나패치이미지의다양성을확보하고예측성능을향상시킬수
있음
슬라이드분류(Slide-level Classification)
⚫패치별로분류된예측결과를종합(Aggregation)하여전체슬라이드의예
측을결정하는방법
⚫각패치에대하여병변/암확률을나타내는히트맵을생성
⚫슬라이드자체를입력으로하여모델을학습하기보다는, 슬라이드에서추
출할수있는여러특징들을입력으로활용
8

--- [PAGE 9/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Strongly Supervised 
Models 
Weakly Supervised 
Models 
Multimodal Models 
Foundation Models 
Detect predefined 
structures
Count cells
Quantify IHC
One whole slide <-> One 
label
Diagnosis, Grading, 
Subtyping, Mutation, 
Response, Prognosis
Weakly supervision but 
additional data as input
Improve precisions
Train one model, fine 
tune on multiple 
downstream tasks
Facilitate & Improve 
precisions
https://jnkather.github.io/
9

--- [PAGE 10/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Strongly Supervised 
Models 
Weakly Supervised 
Models 
Multimodal Models 
Foundation Models 
Detect predefined 
structures
Count cells
Quantify IHC
One whole slide <-> One 
label
Diagnosis, Grading, 
Subtyping, Mutation, 
Response, Prognosis
Weakly supervision but 
additional data as input
Improve precisions
Train one model, fine 
tune on multiple 
downstream tasks
Facilitate & Improve 
precisions
https://jnkather.github.io/
10

--- [PAGE 11/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
AI–Powered Spatial Analysis of TIL
11

--- [PAGE 12/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Lunit SCOPE IO was developed with 
data from 3,166 WSI of 25 cancer types, 
including NSCLC
⚫For image-based validation of AI model 
to segment cancer epithelium (CE) and 
cancer stroma (CS), as well as to detect 
TIL in an independent cohort, LUAD (n = 
461) and LUSC (n = 462) images from 
TCGA, as well as NSCLC primary tumor 
tissues from SMC (n = 1,205) and 
SNUBH (n = 261) were included 
⚫In the SMC and SNUBH data sets, 
clinical outcomes including best OS and 
PFS of ICI were retrospectively reviewed
J Clin Oncol 40:1916-1928.12

--- [PAGE 13/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Immune Phenotype (IP) by Lunit SCOPE IO
⚫WSI were divided into 1 mm2-sized grids and the IP of 
each grid classified on the basis of the proportion of 
each component
⚫Inflamed: TIL density in CE area above the threshold 
(106/mm2)
⚫Immune-excluded: TIL density in CE area below the 
threshold and TIL density in CS area above the 
threshold (357/mm2)
⚫Immune-desert: both TIL density in CE area and that in 
CS area below the thresholds
⚫Inflamed score, immune-excluded score, and 
immune-desert score of WSI: the number of grids 
annotated to certain IP / total analyzed grids in WSI
⚫Representative IP of WSI: inflamed IP if the inflamed 
score was above 33.3%, or immune-excluded IP if 
immune-excluded score was above 33.3% and 
inflamed score was < 33.3%, and immune-desert IP 
otherwise
J Clin Oncol 40:1916-1928.13

--- [PAGE 14/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Improvement in OS and PFS after ICI treatment was observed in patients with inflamed IP
J Clin Oncol 40:1916-1928.14

--- [PAGE 15/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Median PFS for the inflamed and 
noninflamed IP was 4.0 vs 2.1 mo. 
(HR, 0.54; P = .001) for the PD-L1 
TPS 1%-49% subgroup
⚫In the PD-L1 TPS 1%-49% subgroup, 
the AUROC for prediction of tumor 
response to ICI by IP was 0.7609, 
and the AUROC by PD-L1 TPS status 
was 0.5561 (P < .05)
⚫IP classified by the AI-powered 
spatial TIL analyzer is potentially 
complementary to PD-L1 expression 
and may help to identify patient 
with PD-L1 TPS 1%-49% who may 
benefit from ICI monotherapy
J Clin Oncol 40:1916-1928.15

--- [PAGE 16/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
16

--- [PAGE 17/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Strongly Supervised 
Models 
Weakly Supervised 
Models 
Multimodal Models 
Foundation Models 
Detect predefined 
structures
Count cells
Quantify IHC
One whole slide <-> One 
label
Diagnosis, Grading, 
Subtyping, Mutation, 
Response, Prognosis
Weakly supervision but 
additional data as input
Improve precisions
Train one model, fine 
tune on multiple 
downstream tasks
Facilitate & Improve 
precisions
https://jnkather.github.io/
17

--- [PAGE 18/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Extraction of hidden information directly from routinely 
available data
⚫H&E slides: routinely available for almost every cancer patient
✓Easy-to-obtain, information-rich data source for the assessment 
by deep learning (DL) methods
⚫Much larger than radiological images in terms of pixels
⚫Images from histology slides carry much more information
✓Millions of different cells can be seen in a histology slide
✓Their morphology and spatial arrangement carry much more 
information than other medical images
⚫This high information density makes histological images an 
attractive source for DL-based biomarker extraction
Even the size of a whole chest CT dataset 
does not get close to the size of one 
histological WSIs derived from the tumor of 
the same patient when measured in pixels 
18

--- [PAGE 19/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Basic DL applications 
⚫Aim to simplify routine workflows that are 
currently entirely performed by pathologists 
⚫Detection of tumor tissue in biopsy samples or 
tumor subtyping based on morphology 
✓Gleason scoring of prostate cancer samples
⚫Potentially decrease cost and turnaround time 
in pathology departments
⚫No change the ultimate readout upon which 
clinicians base their Tx recommendations
Deep learning in cancer pathology: a new generation of clinical biomarkers.
Echle A, et al. Br J Cancer. 2021. 
19

--- [PAGE 20/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Advanced DL applications 
⚫Beyond the standard reporting that is currently 
performed by pathologists
⚫Prediction of genetic mutations and survival 
directly from H&E-stained tissue slides 
⚫Such advanced applications of DL can provide 
clinicians with additional information that is not 
being extracted from routine material in 
current clinical workflows
✓New class of biomarkers with potential 
prognostic and/or predictive information
Deep learning in cancer pathology: a new generation of clinical biomarkers.
Echle A, et al. Br J Cancer. 2021. 
20

--- [PAGE 21/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Description
Ext. 
validation
No of 
slides
No of 
patients
No of 
cohorts
AUROC
Tumor detection
Detection of breast cancer tissue on whole-slide images
Yes
605
N/A
4
0.9
Classification of breast cancer tissue into benign versus in situ versus invasive versus normal
No
1495
N/A
2
N/A
Detection of prostate carcinoma, basal cell carcinoma and breast cancer metastasis in axillary lymph nodes
No
44,715
15,187
3
0.99
Classification of breast cancer tissue into benign vs in situ vs invasive vs normal
No
2495
N/A
2
0.96–0.987
Identification of malignant tissue in nasopharyngeal biopsies
No
726
726
1
0.99
Tumor subtyping
Deep learning used for lymphoma subtyping
No
375
N/A
3
N/A
Classification of five types of colorectal polyps
No
697
N/A
1
N/A
Classification of lung cancer into adeno-, squamous cell- and small-cell lung carcinoma, normal
Yes
143
N/A
3
0.86
Real-time assistant on classification of hepatocellular carcinoma and cholangiocarcinoma
Yes
150
150
2
N/A
Classification of skin cancer WSIs in basaloid, squamous, melanocytic or other subtypes
Yes
18,607
N/A
4
0.88–0.96
Classification of gastric and colon cancer biopsies and specimens into adenocarcinoma, adenoma or normal
Yes
10,186
N/A
4
0.98
Tumor grading
Gleason grading of prostate cancer
No
312
N/A
1
0.93
Deep learning in cancer pathology: a new generation of clinical biomarkers.
Echle A, et al. Br J Cancer. 2021. 
21

--- [PAGE 22/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Ground-truth method and the DL system use the same image data as input for their prediction 
✓Presence of tumor tissue in prostate cancer samples is normally assessed from H&E-stained slides by a pathologist
✓Basic DL system recapitulates this task and is trained to predict the presence of cancer from the same H&E image
⚫Such DL-based tumor detectors can automate tedious tasks that are normally performed manually
⚫Classification performance (how well a DL classifier predicts a pre-specified endpoint) is typically measured 
by the area under the receiver-operating curve (AUROC)
✓DL-based tumor detectors often achieve AUROC values >0.99, indicating the almost complete accordance of 
the results from pathologists and DL networks
⚫Use of only a single dataset for method development and validation carries the risk of overfitting
✓Creation of a DL system that performs well in that particular cohort, but does not generalize to external cohorts
⚫Validation of the DL system in external datasets, ideally multicenter datasets, is paramount for its ultimate 
routine use and regulatory approval
⚫Performance of DL systems increases with patient number in the training set 
✓Reaching a plateau in performance after training on 10,000–15,000 histological whole-slide images
Clinical-grade computational pathology using weakly supervised deep learning on whole 
slide images. Nat. Med. 25, 1301–1309 (2019).
22

--- [PAGE 23/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Lee SH et al
DEEP LEARNING
GC WSIs
23

--- [PAGE 24/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫The m/c subtype (45-64% of GCs) 
⚫Composed of dilated or slit-like branching tubules of variable diameter 
⚫Tumors with solid structures and barely recognizable tubules are included in this category
⚫Poorly differentiated tubular (solid) carcinoma
⚫"poorly 1 (solid type): por1" in the JGCA classification
Tubular adenocarcinoma, 
well differentiated
Tubular adenocarcinoma, 
moderately differentiated
Tubular adenocarcinoma, 
poorly differentiated
24

--- [PAGE 25/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Rare subtype (2.7-9.9% of GCs)
⚫Usually shows an exophytic growth pattern
⚫Histologically most commonly well differentiated
⚫Elongated finger-like processes lined by columnar 
or cuboidal cells supported by fibrovascular
connective tissue cores 
⚫Despite being a well-differentiated tumor with a 
pushing invading edge, papillary adenocarcinoma 
is associated with a higher frequency of liver 
metastasis and poor survival
25

--- [PAGE 26/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫20-54% of GCs
⚫Composed of neoplastic cells that are isolated or arranged in small aggregates without well-formed glands 
⚫PCCs can be of either signet-ring cell type (SRCC) or non-signet-ring cell type (PCC-NOS)
⚫SRCC: composed predominantly or exclusively of signet-ring cells, which are characterized by a central, optically 
clear, globoid droplet of cytoplasmic mucin with an eccentrically placed nucleus
⚫PCC-NOS: include tumors composed of neoplastic cells resembling histiocytes or lymphocytes: others have deeply 
eosinophilic cytoplasm; some poorly cohesive cells are pleomorphic, with bizarre nuclei
⚫PCCs can be accompanied by marked 
desmoplasia, in particular when 
infiltrating into the submucosa or 
beyond (linitis plástica or scirrhous
carcinoma) 
⚫The worst prognosis, with a 5-year 
survival rate of < 15%
Poorly cohesive carcinoma, 
signet ring cell type
Poorly cohesive carcinoma, 
other cell type
26

--- [PAGE 27/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫2.1-8.1 % of GCs 
⚫Composed of malignant epithelium and extracellular mucin pools, accounting for > 50% of the tumor area 
⚫Two main growth patterns: 
⚫Glandular structures or tubules lined by columnar epithelium with interstitial mucin 
⚫Chains, nests, or single tumor cells (signet-ring cells can be seen) surrounded by mucin 
Malignant glands 
in extracellular mucinous pools
Nests of signet-ring cells 
floating in extracellular mucous
27

--- [PAGE 28/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫6-22% of GCs 
⚫Two or more distinct histological components: glandular 
(tubular/papillary) and signet-ring cell / poorly cohesive
⚫Any distinct histological component should be reported 
⚫Available data suggest that patients with mixed 
adenocarcinomas have a poorer prognosis than those with 
only one component
Tubular, MD + PCC
Tubular, MD + Tubular, PD
28

--- [PAGE 29/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
WHO
JGCA
Nakamura
Lauren
Papillary adenocarcinoma
Tubular adenocarcinoma, WD
Tubular adenocarcinoma, MD
Papillary: pap
Tubular 1: tub1
Tubular 2: tub2
Differentiated
Intestinal
Tubular adenocarcinoma, PD
Poorly 1 (solid type): por1
Undifferentiated
Indeterminate
Poorly cohesive carcinoma, SRC
Poorly cohesive carcinoma, other
Signet-ring cell: sig
Poorly 2 (non-solid type): por2
Undifferentiated
Diffuse
Mixed carcinoma
Description according to the
proportion
(e.g. Por2>sig>tub2)
-
Mixed
Mucinous adenocarcinoma
Mucinous adenocarcinoma
Differentiated/
Undifferentiated
Intestinal/Diffuse
Other histological subtypes:
Carcinoma, undifferentiated, NOS
Special types:
Undifferentiated carcinoma
Not defined
Not defined
29

--- [PAGE 30/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
TCGA dataset
⚫From the TCGA-STAD dataset, 396 FFPE slides from 371 patients were 
selected after the basic slide quality reviews
St. Mary dataset
⚫For the external validation of the classification models trained with the 
TCGA dataset, we collected stomach cancer tissue slides from 232 
patients who previously underwent surgical resection
Pathologic Diagnosis
⚫Histologic type of GC was diagnosed according to the Japanese 
classification
⚫Mucinous adenocarcinoma was classified separately
30

--- [PAGE 31/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Normal/Tumor classifier: trained with normal/tumor tissue patches collected 
⚫Based on the pathologists’ annotation
⚫Differentiated/Undifferentiated classifier: trained with differentiated/undifferentiated tumor tissue patches 
⚫Based on the pathologists’ annotation
31

--- [PAGE 32/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Representative heatmap overlaid on a tissue slide image demonstrating a mixed tumor tissue 
⚫Patch-level AUC for ROC curve of the Differentiated/Undifferentiated classifier (AUC = 0.932)
⚫Patch-level AUC for ROC curve of the Non-mucinous/Mucinous classifier (AUC = 0.979)
32

--- [PAGE 33/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Representative cancer tissue 
consisting of mainly undifferentiated 
and mucinous tissues
⚫Representative cancer tissue 
consisting of mainly differentiated 
and mucinous tissues
⚫Representative cancer tissue 
consisting of mixed differentiated, 
undifferentiated and non-mucinous 
tissues
33

--- [PAGE 34/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Representative gastric cancer tissue with 
mixed differentiated/undifferentiated 
tumor tissues using SSMH dataset
⚫Patch-level AUC for ROC curve of the 
differentiated/undifferentiated classifier 
(AUC = 0.895)
⚫Representative gastric cancer tissue with 
mixed non-mucinous/mucinous tumor 
tissues using SSMH dataset
⚫Patch-level AUC for ROC curve of the 
non-mucinous/mucinous classifier (AUC 
= 0.953)
34

--- [PAGE 35/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Pathologists’ classification for the TCGA 
and SSMH datasets
⚫Slide-level ROC curves of the 
differentiated/undifferentiated classifier 
for the TCGA and SSMH datasets
35

--- [PAGE 36/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Histological type is known to be one of the most important factors in determining endoscopic treatment in 
EGC and chemotherapy for the advanced stage of GC
⚫Presence of minor undifferentiated-type (>10% of total tumor volume) components should be considered when 
assessing the curative resection status of endoscopic resection for differentiated-type mucosal GC
⚫Clinical outcome of mucinous adenocarcinoma was far poorer than that of non-mucinous GC 
⚫Automatic classification of differentiated/undifferentiated and non-mucinous/mucinous tumor types and 
the calculation of the approximate composition ratio of each component is of great use for predicting the 
clinical outcomes of patients with GC
36

--- [PAGE 37/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Lee SH et al
DEEP LEARNING
GC WSIs
37

--- [PAGE 38/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫1,237 WSI datasets obtained from five different institutions 
⚫Tumor semantic segmentation was performed into three types: differentiated tumor, undifferentiated tumor, 
and normal
⚫70 morphologic features were computed and processed to predict LNM using machine learning
38

--- [PAGE 39/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Of the 70 morphologic features included in the model, the top 
5 ranked features were ‘filled area of total tumor’, ‘area of total 
tumor’, ‘equivalent diameter of total tumor’, ‘perimeter of total 
tumor’, and ‘perimeter of undifferentiated’ in sequential order
⚫In five of the nine false-negative cases, poorly differentiated 
tumor cells were scattered diffusely as individual cells in the 
stroma
39

--- [PAGE 40/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Increasing focus on predicting clinically relevant labels directly from histology in three major areas
⚫Inference of genetic alterations, prediction of survival & prediction of treatment response 
⚫Research in these three key applications of DL has been rapidly growing in the past few years
⚫Genetic driver mutations confer changes in the morphology of cancer cells, such as the nuclear and 
cytoplasmatic texture, size and shape within a histological image
⚫Tumor cells can also induce responses in neighboring non-tumor cells such as fibroblasts and lymphocytes
⚫Leading to second-order morphological changes in tumor tissue on a micrometer or millimeter scale
⚫Although each of these morphological features caused by single oncogenic driver mutations might be subtle, 
studies have shown that these changes can be reliably detected by DL 
⚫Merely observing these morphological patterns in H&E images allows the genotype of individual genes to be 
predicted directly from routine histology images
40

--- [PAGE 41/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Description    
Ext. 
validation
No of 
slides
No of 
patients
No of 
cohorts
AUROC
Mutation detection
Prediction of SPOP mutation in prostate cancer
Yes
365
N/A
2
0.86 (P = 0.0038)
Prediction of different genes in lung cancer and ext. validation of EGFR mutation
Yes
1975
N/A
3
0.68
Prediction of BRAF and NRAS in melanoma
Yes
361
N/A
2
0.75-0.77
Detection of HPV in head and neck cancer; detection of EBV in gastric cancer
Yes
1031
1031
4
0.7 (HPV); 0.81 (EBV)
Prediction of microsatellite instability in colorectal, gastric and endometrial cancer
Yes
2108
1952
5
0.84 (CRC)
Pan-cancer prediction of gene expression
No
10,514
8725
28
0.81 (MSI)
Prediction of tumor mutational burden in liver cancer
No
368
350
1
0.95
Prediction of PD-L1 status in non-small- cell lung cancer patients
No
130
130
N/A
0.8 (P < 0.01)
Therapy-response prediction
Prediction of response to ipilimumab in melanoma patients
No
31
31
1
N/A
Prediction of probability that tissue from non-small-cell lung cancer will respond to immunotherapy
No
56
56
2
0.65
Survival prediction
Prediction of 5-year disease-specific survival in patients with colorectal cancer
No
420
420
1
N/A
Consensus molecular subtyping of colorectal cancer and predication of overall survival
No
769
N/A
2
0.8
Stratification of patients into groups of short- and long-term survival by means of TIL
No
70
70
1
0.87
Prediction of survival in mesothelioma and identification of histological correlates
Yes
3037
3037
2
0.66
Stratification of patients with colorectal cancer to good, uncertain or poor prognosis
Yes
4515
3595
4
N/A
Prediction of overall survival of patients with hepatocellular carcinoma
Yes
732
522
2
0.7
Prediction of disease-specific survival in ten different cancer types
No
12,095
4880
10
61.1 (57.2, 65.1)
Deep learning in cancer pathology: a new generation of clinical biomarkers.
Echle A, et al. Br J Cancer. 2021. 
41

--- [PAGE 42/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Lee SH et al
DEEP LEARNING
GC WSIs
42

--- [PAGE 43/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫GCs were divided into four groups: 
⚫Epstein–Barr virus-positive (EBV; 9%), Microsatellite instability 
(MSI; 22%), Chromosomal instability (CIN; 50%), Genomically
Stable (GS; 20%)
Cancer Genome Atlas Research Network. 
Nature 513.7517 (2014): 202.
43

--- [PAGE 44/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫GC classification that correlates four molecular subtypes with 
distinct patterns of molecular alterations, disease progression 
and prognosis.
⚫TCGA subtypes, in fact, are associated with specific genetic 
‘druggable’ alterations. 
⚫ACRG subtypes could help physicians in modulating the intensity 
of a therapeutic regimen.
MSI 23%, 
MSS/EMT 20%, 
MSS/TP53+ (mutated) 26%,
MSS/TP53- (wild) 36%.
Cristescu, Razvan, et al. 
Nature medicine 21.5 (2015): 449.
44

--- [PAGE 45/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
TCGA dataset
⚫Number of frozen tissue slides: 34, 26, 50, 94, 221 for CDH1, ERBB2, KRAS, PIK3CA & TP53 genes
⚫Number of FFPE tissue slides: 27, 19, 34, 66, 174 for CDH1, ERBB2, KRAS, PIK3CA & TP53 genes
⚫183 patients with wild-type CDH1, ERBB2, KRAS, PIK3CA & TP53 genes
St. Mary dataset
⚫GC tissue slides were collected from 96 patients who had previously undergone surgical resection
⚫For CDH1, ERBB2, KRAS, PIK3CA & TP53 genes, 6, 6, 12, 11, 39 pts were confirmed to have mutations, respectively
⚫38 patients had wild-type genes for all five genes
45

--- [PAGE 46/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Tissue image patches with tumor probability > 0.9 were selected by sequential application of the tissue/non-
tissue and normal/tumor classifiers
⚫Then the tumor patches were classified into the wild-type or mutated patches 
⚫Patch-level probabilities of mutation are averaged to yield the slide-level probability
46

--- [PAGE 47/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Representative WSIs for TP53 mutation
⚫With correctly/falsely classified cases
⚫ROC curves 
⚫For the fold with lowest AUC (0.666)
⚫For the fold with highest AUC  (0.810)
⚫For the concatenated results of all ten folds (0.727)
⚫With the classifiers trained with the frozen tissues
⚫Representative WSIs for TP53 mutation
⚫With correctly/falsely classified cases
⚫ROC curves 
⚫For the fold with lowest AUC (0.702)
⚫For the fold with highest AUC  (0.847)
⚫For the concatenated results of all ten folds (0.727)
⚫With the classifiers trained with the FFPE
47

--- [PAGE 48/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Representative WSIs for PIK3CA mutation
⚫With correctly/falsely classified cases
⚫ROC curves 
⚫For the fold with lowest AUC (0.705)
⚫For the fold with highest AUC  (0.990)
⚫For the concatenated results of all ten folds (0.862)
⚫With the classifiers trained with the frozen tissues
⚫Representative WSIs for PIK3CA mutation
⚫With correctly/falsely classified cases
⚫ROC curves 
⚫For the fold with lowest AUC (0.675)
⚫For the fold with highest AUC  (1.000)
⚫For the concatenated results of all ten folds (0.828)
⚫With the classifiers trained with the FFPE
48

--- [PAGE 49/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Mutation prediction of PIK3CA & TP53 genes for the SSMH gastric cancer tissue slides by the classifiers 
trained with TCGA FFPE data
49

--- [PAGE 50/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Representative WSIs for PIK3CA mutation
⚫With correctly/falsely classified cases
⚫ROC curves 
⚫For the fold with lowest AUC (0.600)
⚫For the fold with highest AUC (0.100) 
⚫For the concatenated results of all ten folds (0.761)
⚫With the classifiers trained with both TCGA & SSMH data
⚫Representative WSIs for TP53 mutation
⚫With correctly/falsely classified cases
⚫ROC curves 
⚫For the fold with lowest AUC (0.722)
⚫For the fold with highest AUC (0.967) 
⚫For the concatenated results of all ten folds (0.775)
⚫With the classifiers trained with both TCGA & SSMH data
50

--- [PAGE 51/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
CIN
GS
MSI
EBV
TCGA-STAD with WSIs
CIN
215 cases
EBV
30 cases
GS
51 cases
MSI
75 cases
51

--- [PAGE 52/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
CIN
GS
MSI
EBV
52

--- [PAGE 53/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Open large-scale digital pathology data platform, by the CODiPAI (Collaborative Open Digital Pathology 
Artificial Intelligence) consortium, were used for external validation (1000 GC WSIs, 15% of MSI-H cases)
⚫DL-based classifiers for molecular alteration in tissue slides can yield better performance when more data are 
collected from various sources
53

--- [PAGE 54/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
AI for predicting TMB in various cancers
Lee SH et al
DEEP LEARNING
GC WSIs
54

--- [PAGE 55/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫TMB: the number of point mutations, insertion 
deletions, and other gene mutations in the 
coding region of somatic proteins contained in 
the average 1 Mb base range of the tumor 
genome.
⚫It is hypothesized that highly mutated tumors are 
more likely to harbor neoantigens which make 
them targets of activated immune cells. 
⚫Emerging evidence suggests that TMB may be an 
important predictive factor for response to ICIs 
across different disease types
⚫Initial assessment of TMB using WES has been 
replaced by NGS of targeted gene panels.
⚫WES was expensive and time consuming and 
therefore unsuitable for routine clinical practice.
55

--- [PAGE 56/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Proper tissue patches can be selected by the 
tissue/non-tissue classifier
⚫Annotated normal and tumor tissue regions of FFPE 
tissue slides were split into 360 x 360-pixel patches
⚫Only proper tissue patches were collected for the 
training of the normal/tumor classifiers
⚫Normal and tumor regions of a slide can be delineated 
by the sequential application of the tissue/non-tissue 
& normal/tumor classifiers
⚫For TMB classifiers, only tumor tissue patches with a 
tumor probability > 0.9 were collected
⚫Then, the TMB-H/TMB-L classifiers were trained on 
the tissue patches
56

--- [PAGE 57/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
57

--- [PAGE 58/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Currently, survival is estimated by clinical parameters such as age, gender, cancer stage, pre-existing 
conditions, genetic alterations and histology risk factors 
⚫Histology risk factors include tumor cell differentiation, stromal abundance, lymphocyte fraction, lymphatic vessel 
invasion, vascular invasion, perineural invasion and necrosis in almost any type of solid tumor
⚫In addition to these established risk factors, higher-level features carry prognostic information 
⚫Analysis of the spatial arrangement of lymphocytes showed that a high neutrophil-to-lymphocyte ratio is associated 
with unfavorable overall survival
⚫Examination of sub-visual features such as chromatin texture can serve as a prognostic indicator in different solid 
tumors
⚫While some studies have used manually defined prior parameters to train the DL network for survival 
predictors, other studies have used an unbiased approach and leave the feature selection entirely to the 
deep network, 
⚫No prognostic parameters, such as tissue type or cellular aspects, were manually identified during the process 
⚫This process could even reveal new morphological biomarkers by highlighting specific structures and regions
⚫In the future, this reverse engineering of relevant features might even be helpful in identifying targets for the 
development of new therapies
58

--- [PAGE 59/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Deep learning-based survival prediction of HCC
Lee SH et al
DEEP LEARNING
Liver tumor WSIs
59

--- [PAGE 60/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫A DL model for classifying good and poor prognosis was developed on a total of 458 patients with 2 
independent cohorts from Seoul St. Mary's Hospital
⚫The training set (SSM1, N = 293) included HCC patients that had undergone surgical resection
✓Follow-up time and outcome information (OS) is available for each of the patients as well as clinicopathological
characteristics of the tumor samples including established predictors such as T stage and histological grade 
⚫The classifier was then independently tested on the second HCC dataset (SSM2, N = 165) 
60

--- [PAGE 61/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Slide-level ROC curves of 
✓Fold with the lowest AUC 
✓Fold with highest AUC 
✓Concatenated results of all 5-folds (AUC 
= 0.850) 
⚫For the comparison with the DL prediction models, we made a 
logistic regression model with several clinicopathologic
parameters (AUC: 0.705) 
✓Edmondson-Steiner grade
✓T stage
✓Vascular invasion
✓Ki-67 index
✓CK19
61

--- [PAGE 62/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Good prognosis patches
Poor prognosis patches
Mixed cases
Clear cases
62

--- [PAGE 63/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Good prognosis patches
Poor prognosis patches
Mixed cases
Clear cases
63

--- [PAGE 64/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Result of t-SNE analysis on the last fully connected layer of the DNN 
⚫Histomorphology was investigated by pathologists to understand 
the characteristics of HCC tissues
Good vs Poor 
prognosis group 
(SSM1 & SSM2) 
64

--- [PAGE 65/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫DL might be key to the detection of structures and transformations in tumor tissue that could be used as 
predictive markers of a positive response to targeted therapies 
⚫Helps to identify responders while minimizing the negative effects on non-responders
⚫DL can identify features, mutations, hormone-receptor status or similar molecular alterations that are 
already known to be targets of therapy approaches or proxies for treatment response 
⚫DL can be used to predict treatment response directly from a histological slide without being trained to 
detect specific predefined molecular biomarkers. 
⚫This “end-to-end” workflow requires DL networks to be trained on large patient cohorts for which the specific type 
of treatment response is known
⚫Similarly to survival prediction networks, treatment response prediction might lead to the detection of new 
morphological markers on histology images, resulting in new therapeutic strategies
65

--- [PAGE 66/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Artificial intelligence-based pathology as a 
biomarker of sensitivity to atezolizumab-
bevacizumab in patients with hepatocellular 
carcinoma: a multicentre retrospective study
Lancet Oncol. 2023 Dec;24(12):1411-1422.
66

--- [PAGE 67/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Atezolizumab–bevacizumab response signature 
(ABRS), assessed by molecular biology profiling 
techniques, has been shown to be associated with PFS 
after Tx initiation. 
⚫Primary objective of this study was to develop an AI 
model able to estimate ABRS expression directly from 
histological slides (ABRS-P), and to evaluate if model 
predictions were associated with PFS.
67

--- [PAGE 68/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Genes in ABRS signature: CXCR2P1, 
ICOS, TIMD4, CTLA4, PAX5, KLRC3, 
FCRL3, AIM2, GBP5 & CCL4
⚫CTLA4 & ICOS: involved in the 
regulation of T-cell activation 
⚫KLRC3, FCRL3 & AIM2: involved in 
the innate immunity
⚫Gene signature scores: arithmetic 
mean of log2(CPM) expression of all 
genes in a given signature
68

--- [PAGE 69/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫TCGA HCC (TCGA-LIHC) dataset was used to train the model 
(patients treated by surgical resection, n=336) 
⚫Available digital histological H&E-stained FFPE slides 
⚫Available gene expression profiling (RNA sequencing)
⚫ABRS-P model was externally validated on two independent 
series of samples from patients with HCC (a surgical resection 
series, n=225; and a biopsy series, n=157).
⚫Predictive value of the model was further tested in a series of 
biopsy samples from a multicenter cohort of HCC (n=122).
⚫Tx with atezolizumab–bevacizumab 
⚫Available tumor biopsy sample from before Tx initiation
⚫No Tx with another anti-tumor Tx between biopsy and Tx
⚫Available follow-up data on progression
⚫RNA sequencing and spatial transcriptomics (Visium, n=4)
69

--- [PAGE 70/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫위에두세트의열쇠가열리는열쇠, 아래두세트의
열쇠가안열리는열쇠로가정
⚫맨오른쪽새로운세트가들어왔을때이세트가문을열
수있을지없을지맞추는문제가Multiple Instance 
Learning에서풀고자하는문제임.
⚫병리WSI의경우slide 단위의라벨값만있고, 어디가실제positive부분인지(ABRS-P-high) 라벨이없음. 
⚫각각의패치들을instance로했을때, instance별로classification을할수있는instance classifier을만듦.
⚫Negative 케이스에서는(ABRS-P-low) 패치들을negative로가정하여training / positive 케이스의경우positive 
로가정하여training. 
⚫열쇠문제에서키3개중에하나만맞는열쇠가있으면열리는것처럼, WSI 경우에여러패치중에하나라도
positive가있는경우그slide는positive라고판단을내릴수있다라는것이MIL의목적임.
⚫Instance classifier가잘작동을한다면실제영상어떤부위가실제positive부분인지까지도맞춰줄수있기
때문에어느정도weakly supervised learning과도연관성이있는내용임.
70

--- [PAGE 71/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫CLAM: Label을예측하는데도움이되는'discrimitive
regions of interest'를clustering-based attention 
mechanism을통해서예측하는방법. 
⚫비슷한feature를가지는patch들을그룹으로묶어, 
cluster를기반으로weight를부여하여최종bag-
level label을예측하는것을목표로함.
⚫Attention mechanism을활용하여어떤Patch가중
요했냐를추론하여, Histopathology 상에서중요한부
위를검증하고, 이를pathology knowledge와연결함.
71

--- [PAGE 72/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫DL network is based on the CLAM architecture that is 
modified for regression analysis.
⚫In accordance with the MIL assumption, each patch is 
treated as an instance and a WSI as a bag. 
⚫Unsupervised contrastive learning transformer 
(CTransPath) was deployed to encode each patch into a 
768-dimensional feature embedding. 
⚫Attention scores were softmax across the N patches and 
used as weights to aggregate the patch predictions into 
WSI prediction.
⚫Model was trained by minimizing the mean squared error 
loss between the predicted & true ABRS score
⚫High ABRS-P values (ABRS-P-high) or low ABRS-P values 
(ABRS-P-low) relative to the median split thresholds in the 
first biopsy series
72

--- [PAGE 73/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Training was performed with a ten-times Monte Carlo cross-
validation strategy, with 60%, 20%, and 20%, respectively, 
randomly partitioned into training, validation, and test sets.
⚫Monte Carlo cross-validation = Repeated random sub-sampling 
validation 
⚫Pearson’s correlation coefficient (r), 95% CIs, and p values 
were used for performance evaluation.
⚫ABRS-P were rescaled to [0, 1] for each time, with 1 
representing the highest prediction and 0 for lowest prediction 
⚫Spatial coordinates of each patch were used to create a 
colormap (red: 1 & blue: 0) to illustrate final patch predictions. 
⚫Heat-maps indicate which areas are potentially associated with 
the response to atezolizumab-bevacizumab, offering hints for 
clinical research.
73

--- [PAGE 74/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Using cross-validation, the best model reached a Pearson’s 
coefficient (r) of 0·71 (95% CI 0·58–0·81; p<0·0001). 
⚫Ensemble ABRS-P model had a Pearson’s coefficient of 0·86 
(0·83–0·89; p<0·0001) for the whole development set.
⚫Pathological review of image patches with high ABRS-P values 
(ie, predicted to have high ABRS values) showed an 
enrichment of immune cells.
74

--- [PAGE 75/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫ABRS-P generalized well on the 
external validation series (surgical 
resection series, r=0.60 [95% CI 0.51–
0.68], p<0.0001; biopsy series, r=0.53 
[0.40–0.63], p<0.0001). 
⚫In the 122 patients treated with 
atezolizumab–bevacizumab, those 
with ABRS-P-high tumors (n=74) 
showed significantly longer median 
PFS than those with ABRS-P-low
tumors (n=48) after Tx initiation (12 
months [95% CI 7–not reached] vs 7 
months [4–9]; p=0.014). 
75

--- [PAGE 76/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Spatial transcriptomics on four HCC 
samples from the surgical validation series
⚫Spatial transcriptomics showed 
significantly higher ABRS score, along 
with upregulation of various other 
immune effectors, in tumor areas with 
high ABRS-P values vs. areas with low 
ABRS-P values in three of the four cases. 
76

--- [PAGE 77/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫This study indicates that AI applied on HCC digital slides with different histological specimen types (resection 
or biopsy) is able to serve as a biomarker for PFS in patients treated with atezolizumab–bevacizumab. 
⚫DL prediction heatmaps with spatial transcriptomics showed, in situ, that areas predicted to have high ABRS 
values displayed higher ABRS expression than areas predicted to have low ABRS values.
⚫This methodology could be applied to other cancers or diseases and improve understanding of the biological 
mechanisms that drive responses to treatments.
⚫Utilization of surgically extracted whole-tumor samples rather than biopsies for the predictive process. 
⚫While certainly valuable in a scenario where immunotherapy is used as adjuvant therapy after surgical 
resection, the application to tissue originating from biopsy samples in advanced stage disease is not yet 
sufficiently established.
⚫Growing need for tissue sampling in HCC for the purpose of tumor characterization
77

--- [PAGE 78/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Strongly Supervised 
Models 
Weakly Supervised 
Models 
Multimodal Models 
Foundation Models 
Detect predefined 
structures
Count cells
Quantify IHC
One whole slide <-> One 
label
Diagnosis, Grading, 
Subtyping, Mutation, 
Response, Prognosis
Weakly supervision but 
additional data as input
Improve precisions
Train one model, fine 
tune on multiple 
downstream tasks
Facilitate & Improve 
precisions
https://jnkather.github.io/
78

--- [PAGE 79/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Patient data in the form of digitized high-resolution WSIs with corresponding molecular data are used as input 
⚫Three neural network modules together: (1) an attention-based multiple instance learning (AMIL) network for 
processing WSIs, (2) a self-normalizing network (SNN) for processing molecular data features, and (3) a multimodal 
fusion (MMF) layer to model pairwise feature interactions between histology and molecular features
Cancer Cell. 2022 Aug 8;40(8):865-878.e6.
79

--- [PAGE 80/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Strongly Supervised 
Models 
Weakly Supervised 
Models 
Multimodal Models 
Foundation Models 
Detect predefined 
structures
Count cells
Quantify IHC
One whole slide <-> One 
label
Diagnosis, Grading, 
Subtyping, Mutation, 
Response, Prognosis
Weakly supervision but 
additional data as input
Improve precisions
Train one model, fine 
tune on multiple 
downstream tasks
Facilitate & Improve 
precisions
https://jnkather.github.io/
80

--- [PAGE 81/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Foundation Model
⚫Foundation Model(FM): 대규모데이터에서Pre-training이완료된모델로, 다양한Downstream Task
에쉽게적용할수있는범용모델을뜻함
⚫대규모의비지도학습데이터를사용하여사전학습되는과정에서모델은데이터의일반적인패턴, 구조, 상관관계등을학습함
⚫파인튜닝(Fine-Tuning): 적은양의레이블된데이터를사용해사전학습된모델을특정한작업이나도메인
에맞게추가로학습시킴
⚫파인튜닝과정에서는모델이특정작업의특성을학습하여해당작업에서의성능을최적화함
⚫의료WSI 데이터는수집이나라벨링의비용이크기때문에, Foundation Model을활용하여Self/Semi-
supervised Learning 기반모델을개발하면적은데이터에서도더좋은성능을기대할수있음
⚫대규모모델을학습하고유지하는데필요한컴퓨팅자원과비용이매우큼
81

--- [PAGE 82/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
82

--- [PAGE 83/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
CNN-based Model vs Foundation Model
83

--- [PAGE 84/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
CNN-based Model vs Foundation Model
84

--- [PAGE 85/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Pathology Foundation Models
Characteristics
85

--- [PAGE 86/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Pathology Foundation Models
Performance across diverse downstream tasks
86

--- [PAGE 87/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Multimodal Foundation Models
Characteristics & Performance across diverse downstream tasks
87

--- [PAGE 88/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫UNI, a general-purpose self-supervised model 
for pathology, pretrained using more than 100 
million images from over 100,000 diagnostic 
H&E-stained WSIs (>77 TB of data) across 20 
major tissue types.
⚫UNI generally outperforms other pretrained 
encoders across 34 clinical tasks in anatomical 
pathology.
Nat Med. 2024 Mar;30(3):850-862.
88

--- [PAGE 89/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Endoscopic resection (ER) has emerged as a minimally invasive 
therapeutic approach for the management of EGC, demonstrating a 
reduced incidence of complications and shorter hospitalization 
durations compared to surgical interventions. 
⚫The decision regarding postoperative management following ER—
whether to proceed with surveillance or additional surgery—is 
determined based on the eCura scoring system. 
⚫Despite adherence to these established criteria for ER, extragastric
recurrence has been reported in 0.14–0.21% of cases. 
⚫The use of ER is increasingly being explored in patients with relative 
indications, a category that traditionally warrants surgical intervention. 
89

--- [PAGE 90/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫We assembled more than 6,500 ER cases from ten tertiary hospitals, 
securing a sufficient number of LNM events despite their low incidence. 
⚫We implemented a true end-to-end architecture that accepts WSIs as 
the sole input and outputs an LNM risk score without manual feature 
engineering. 
⚫We performed a head-to-head comparison with the eCura scoring 
system, using AUROC, net reclassification improvement and decision-
curve analysis to quantify any added clinical benefit. 
⚫These elements establish a robust foundation for translating AI-assisted 
LNM risk stratification into postoperative decision-making for EGC.
90

--- [PAGE 91/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫We propose a multi-resolution Multiple Instance 
Learning (MIL) framework enhanced with feature-
level knowledge distillation to predict LNM from 
WSIs of EGC.
⚫Our architecture employs a dual-branch MIL model 
composed of a teacher-student configuration, 
where both branches share the same attention-
based MIL aggregator. 
⚫Patch-level features are extracted using pretrained
encoders such as GigaPath, CTransPath, and Conch. 
Under review
Architecture of Proposed MIL. The central idea is to
leverage rich information from high-resolution patches (1.0
mpp) using a teacher model and distill this knowledge into
a more computationally efficient student model that
operates on lower-resolution patches (2.0 mpp).
91

--- [PAGE 92/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Our best-performing model, trained with GigaPath encoder under the 
random direction distillation, achieved substantial performance 
improvements over the clinical eCura rule.
⚫The effectiveness of distillation was consistent across multiple 
encoders. 
⚫Notably, GigaPath achieved the highest overall performance, but the 
proposed method was also beneficial for other encoders like Uni, Conch.
⚫Compared to rule-based systems such as eCura, our approach provides 
a more balanced decision-making capability, particularly for borderline 
or ambiguous cases where traditional heuristics fall short.
Under review
92

--- [PAGE 93/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫GMAI model is trained on multiple medical data modalities, through techniques such as SSL 
⚫Various sources of medical knowledge to carry out medical reasoning tasks 
⚫GMAI model builds the foundation for numerous applications across clinical disciplines
Nature 616, 259–265 (2023)
93

--- [PAGE 94/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Recently developed MLLMs that can provide textual descriptions of 
microscopical images
⚫Sun et al. utilized 207,000 pathology image‒text pairs to fine-tune a pre-
trained OpenAI CLIP base model, and combined it with a 13B parameter 
LLM to develop PathAsst, which exhibited an impressive performance in 
interpreting pathology images.
⚫Yu et al. developed a vision-language pathology AI assistant, named 
PathChat, by using 100 million histology images, 1.18 million pathology 
image‒caption pairs, and 250,000 visual language instructions.
arXiv 2023, arXiv:2312.07814.
In Proceedings of the AAAI Conference on Artificial Intelligence, February 2024.
94

--- [PAGE 95/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫The last few years have seen a tremendous growth in the development of novel AI approaches in pathology.
⚫These tools, when used intelligently, can improve diagnostic workflows, eliminate human errors, increase inter-
observer reproducibility and make prognostic predictions.
⚫AI has become a standard tool in cancer histopathology and has enabled numerous scientific insights, and it 
is likely to yield multiple new clinically approved biomarkers within the next five years.
⚫In addition to the use of AI to conduct human expert 
diagnostic tasks, we have only begun to scratch the 
surface with respect to the use of AI for discovery of 
prognostic features, prediction of therapy success or 
assessment of the relation between the morphological 
phenotypes and genotypes
⚫Future work will focus on developing more focused 
prognostic models by curating larger multimodal 
datasets for individual disease models, and using 
multimodal DL for predicting response and resistance to 
treatment
Annual Review of Cancer Biology. 2023 Apr 11;7:57-71.
95

--- [PAGE 96/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
⚫Sangjeong Ahn, co-PI: Korea University Anam Hospital
⚫Eunsu Kim, ML researchers
⚫Hyeseong Lee, ML researchers
⚫JongHyun Lee, ML researchers
⚫Dewan Bappy, ML researchers
⚫Harim Chun, BI researchers
⚫Moonyoung Lee, BI researchers
⚫Min Soo Kim, CRC
⚫Kwangil Yim, Pathologist: Uijeongbu St. Mary's Hospital
⚫Harim Oh, Pathologist: Korea University Anam Hospital
⚫Yeseul Jung, Pathologist: St. Vincent Hospital
⚫Won-ki Jung: Department of Computer Science and Engineering, 
Korea University 
https://www.pathfinderlab.org/
⚫Young Suk Lee, ML researchers
⚫Sung Man Hong, ML researchers
⚫Young In Jang, ML researchers
⚫Ho Heon Kim, BI researchers
⚫Yona Kim, BI researchers
⚫Sumin Lee, CRC
96

--- [PAGE 97/97] DL_Pathology_2026-대학원-ver1.3 (1).pdf ---
Thank you for your attention!
97



================ [DRAFT 분석(초안) — 토픽맵/가중치/모범답안 사실원] ================

260428_ 【예상 시험 문제 & 모범 답안】먼저 딱 드립니다

✅ Q1. [비교형] Basic DL applications vs Advanced DL applications의 차이점을 비교하고, 각각의 임상적 의의를 서술하시오.
[모범 답안]
Basic DL applications은 종양 검출(tumor detection), 서브타이핑, 그레이딩 등 병리의사가 루틴하게 수행하는 업무를 자동화한다. AUROC는 일반적으로 0.9 이상이며, TAT time과 비용을 절감할 수 있다. 그러나 치료 recommendation을 변경하지는 못한다.
Advanced DL applications은 H&E 슬라이드만으로 유전적 변이 예측, 생존 예측, 치료 반응 예측 등 병리의사가 수행할 수 없는 영역까지 확장한다. AUROC는 0.7~0.8 수준으로 Basic보다 낮으나, 이것이 잘 작동하면 새로운 클래스의 바이오마커로서 기능하여 임상 의사에게 루틴 재료에서 얻을 수 없는 추가 정보를 제공한다.
[출제 근거] 슬라이드 pp.19-20에 두 개의 별도 박스로 구성된 비교 다이어그램, S7(비교·대조) + S1(분량) + S5(반복). Summary 슬라이드(p.95)에서도 두 영역을 모두 명시.

✅ Q2. [기전 설명형] CNN(Convolutional Neural Network)이 병리 이미지에서 특징을 추출하는 과정을 단계별로 설명하시오.
[모범 답안]
WSI는 크기가 너무 크기 때문에 256×256~1024×1024 픽셀 단위의 패치로 분할한다. 각 패치는 행렬로 표현되며, 다음 과정을 거친다.
① Convolution(합성곱): 특정 크기의 필터를 일정 간격으로 이동하면서 입력 데이터의 행과 열에 필터 값을 곱하고 합산하여 새로운 행렬(feature map)을 생성한다. 차원이 축소된다.
② Pooling: 각 패치에서 예측된 결과를 집계하여 feature map 크기를 축소한다. 필요한 주요 특징만 학습하여 과적합을 방지한다.
③ 반복: Convolution → Pooling을 여러 번 반복하면 핵의 모양, 선구조, 세포밀도, 기질 패턴 등 형태학적 핵심 특징만 남은 feature map이 생성된다.
④ Fully Connected Layer(FC Layer): 추출된 특징들을 종합하여 최종 분류 또는 예측을 수행한다.
⑤ Softmax 함수: 입력값에 대한 각 클래스의 확률을 출력하여 최종 분류를 결정한다(예: 얼룩말 0.7, 말 0.2, 개 0.1).
[출제 근거] 슬라이드 pp.6-7에 걸쳐 2장 분량, S4(얼룩말 비유로 패턴 전환) + S1(분량) + S5(결국에는 키워드 반복). 스크립트에서 "결국에는"이라는 담화표지와 함께 반복 설명.

✅ Q3. [비교형] Computational pathology의 4가지 접근법(Strongly Supervised / Weakly Supervised / Multimodal / Foundation Models)의 특징과 적용 범위를 비교하시오.
[모범 답안]
모델 유형
어노테이션 단위
주요 용도
특징
Strongly Supervised
세포 단위
세포 검출, 카운팅, IHC 정량화
정밀한 어노테이션 필요
Weakly Supervised
슬라이드 단위 (1 slide ↔ 1 label)
진단, 그레이딩, 서브타이핑, 뮤테이션, 반응, 예후 예측
세포 단위 어노테이션 불필요
Multimodal
슬라이드 단위
Weakly supervised의 모든 용도
병리 이미지 + 유전체 데이터 등 이질적 데이터 결합으로 정밀도 향상
Foundation Model
대규모 pre-training
다양한 downstream task
하나의 모델로 fine-tuning하여 여러 task 수행, 컴퓨팅 비용 큼
Multimodal model은 weakly supervision + additional data(genomics, radiology 등)를 입력으로 활용하여 정밀도를 향상시킨다. Foundation model은 수백만~수천만 장의 데이터로 pre-training 후 적은 양의 레이블 데이터로 fine-tuning하여 다양한 downstream task에서 기존 CNN보다 높은 성능을 보인다(EBV: AUROC 0.947→0.988, MSI: 0.827→0.898).
[출제 근거] 슬라이드 pp.9, 10, 17, 78, 80에 5회 반복 등장 (강의 전체 틀로 사용됨) → 가장 높은 가중치. S5(반복) + S7(비교) + B2(각 항목 설명).

✅ Q4. [기전 설명형] Multiple Instance Learning(MIL)의 개념과 WSI 분석에서의 적용 원리를 설명하시오.
[모범 답안]
MIL은 슬라이드(bag) 단위의 라벨만 존재하고 어느 패치(instance)가 실제 positive인지 어노테이션이 없을 때 사용하는 학습 방법이다.
핵심 원리: 포지티브 케이스의 모든 패치를 positive로, 네거티브 케이스의 모든 패치를 negative로 rough하게 가정하여 학습한다.
열쇠/자물쇠 비유로 설명하면: 열쇠 세트에서 하나라도 맞는 열쇠가 있으면 문이 열리듯, WSI에서 하나라도 positive 패치가 있으면 해당 슬라이드를 positive로 판단한다.
CLAM: MIL의 확장으로, clustering-based attention mechanism을 활용한다. 각 패치에 대해 예측에 중요한 feature와 중요하지 않은 feature에 가중치를 부여하여 attention map을 생성한다. 이를 통해 병리학적으로 중요한 부위를 시각화하고 검증할 수 있다. Instance classifier가 잘 작동하면 실제 positive 부위를 역으로 특정할 수 있어 weakly supervised learning과도 연관된다.
[출제 근거] S4(열쇠 비유라는 강력한 패턴 전환) + S1(스크립트 내 매우 긴 설명 + 한국어 전용 슬라이드 p.70 별도 존재) + B1(S4+S6 동시). 슬라이드 두 장(pp.70-71)에 걸쳐 한국어로 상세 설명된 것은 핵심 출제 신호.

✅ Q5. [기전 설명형] Foundation Model의 개념을 설명하고, 기존 CNN 기반 모델과의 차이점 및 장단점을 비교하시오.
[모범 답안]
Foundation Model은 대규모 데이터(수십만~1억 장 이상의 WSI)에서 비지도 학습(self-supervised learning)으로 pre-training이 완료된 범용 모델이다. Pre-training 과정에서 데이터의 일반적인 패턴, 구조, 상관관계를 학습한다.
Fine-tuning: 적은 양의 레이블 데이터를 사용해 특정 task나 도메인에 맞게 추가 학습한다. 의료 WSI는 수집과 라벨링 비용이 크기 때문에 Foundation model의 이점이 크다.
CNN 대비 장점: 기존 CNN은 task별로 별도의 모델을 학습해야 하지만(MSI 예측 모델, EBV 예측 모델 각각 학습), Foundation model은 하나의 모델로 fine-tuning하여 여러 task를 수행할 수 있다. 실제로 UNI2 Foundation model은 CNN 대비 EBV 분류 AUROC 0.947→0.988, MSI 분류 0.827→0.898로 향상된 성능을 보였다.
단점: 대규모 모델을 학습하고 유지하는 데 필요한 컴퓨팅 자원과 비용이 매우 크다.
[출제 근거] S1(슬라이드 pp.81-88, 8장 분량) + S7(CNN vs Foundation Model 직접 비교 슬라이드 p.83-84) + S5(반복 언급). Summary 슬라이드에서 "THE FUTURE IS MULTIMODAL" → Foundation model이 핵심 축.

✅ Q6. [비교형] Lunit SCOPE IO를 이용한 Immune Phenotype 3가지 유형을 TIL 분포를 기준으로 정의하고, ICI 치료 반응과의 임상적 연관성을 서술하시오.
[모범 답안]
Immune Phenotype(IP)은 WSI를 1mm² 그리드 단위로 분할하여 cancer epithelium(CE)과 cancer stroma(CS)에서의 TIL density를 기준으로 분류한다.
Inflamed: CE 내 TIL density가 threshold(106/mm²) 이상인 경우. ICI 치료 후 OS와 PFS가 가장 우수.
Immune-excluded: CE 내 TIL density는 threshold 미만이나, CS 내 TIL density가 threshold(357/mm²) 이상인 경우.
Immune-desert: CE와 CS 모두 TIL density가 threshold 미만인 경우. 가장 불량한 예후.
임상적 의의: PD-L1 TPS 1-49% 서브그룹에서 IP 기반 ICI 반응 예측력(AUROC 0.761)이 PD-L1 TPS(AUROC 0.556)보다 유의하게 우수하였다(p<0.05). 따라서 AI 기반 IP 분류는 PD-L1 expression의 complementary biomarker로서 활용될 수 있다.
[출제 근거] S7(3가지 유형 상세 비교) + S5(inflamed type 반복 강조) + S1(슬라이드 pp.12-15, 4장 분량). 숫자(AUROC)를 슬라이드에서 직접 읽어줌(B2).

✅ Q7. [기전 설명형] H&E 슬라이드로 유전적 변이(mutation)를 딥러닝으로 예측할 수 있는 생물학적 근거를 설명하시오.
[모범 답안]
Driver mutation은 cancer morphology에 변화를 일으킨다. 구체적으로 핵의 형태, 세포질 texture, 세포의 크기와 모양 변화를 초래한다. 또한 주변의 fibroblast, lymphocyte 배열에도 변화를 일으키는 second-order morphological change가 발생한다.
이러한 변화들은 사람 눈에는 너무 subtle하여 잘 인식되지 않지만, 딥러닝은 이를 신뢰성 있게 탐지할 수 있다. 따라서 H&E 이미지에서의 morphological pattern 관찰만으로 개별 유전자의 genotype을 직접 예측하는 것이 가능하다. 이것이 바로 Summary 슬라이드에서 강조하는 "morphological phenotype과 genotype의 관계 파악"의 핵심이다.
단, TCGA 데이터셋으로 학습한 모델을 외부 데이터셋에 적용할 때 AUC가 하락하는 generalizability 문제가 있으며, 다기관 대용량 데이터셋으로 학습할수록 성능이 향상된다(CODiPAI dataset MSI 분류 AUC 0.915).
[출제 근거] S1(슬라이드 p.40 이론 + pp.42-53 실험, 총 12장) + S7(TCGA training vs external validation 비교) + Summary 슬라이드 직접 언급.

✅ Q8. [기전 설명형] DL 모델의 과적합(overfitting) 문제와 극복 방법을 설명하시오.
[모범 답안]
단일 데이터셋만으로 학습 시 해당 데이터셋에만 특화된 과적합이 발생하여 외부 데이터에 적용하면 성능이 저하된다.
극복 방법: ① External validation: 이상적으로 multicenter dataset을 이용한 외부 검증이 필수적이다. AUROC가 internal validation보다 하락하는 것이 일반적이다. ② 데이터셋 크기 증가: 학습 데이터가 많을수록 성능이 향상되나, 약 10,000~15,000장의 WSI에서 plateau(포화)에 도달한다. ③ 다기관 데이터 통합: 여러 기관의 데이터를 합쳐 학습하면 색상 정규화(color normalization) 등의 편차를 극복하고 범용성이 향상된다. CODiPAI 데이터셋 활용 시 MSI 분류 AUC가 TCGA 단독 학습 대비 크게 향상(AUC 0.915).
[출제 근거] S6(경고성 발화: "과적합에 빠집니다", "범용성이 좀 떨어진다") + S1 + B1(S4+S6: 반복 경고 후 데이터 통합 실험으로 전환).

✅ Q9. [비교형] TCGA에 의한 위암의 분자적 분류 4군의 각 특성, 비율, 딥러닝 예측력 차이를 비교하시오.
[모범 답안]
아형
비율
주요 분자적 특성
H&E 딥러닝 AUC
CIN
50%
TP53 mutation, RTK-RAS activation, 장형 조직학
0.825 (낮음)
MSI
22%
Hypermutation, MLH1 silencing, Gastric-CIMP
0.896 (높음)
GS
20%
CDH1/RHOA mutation, diffuse 조직학, CDH1 silencing
0.858
EBV
9%
PIK3CA mutation, PD-L1 overexpression, 면역세포 신호
0.938 (가장 높음)
MSI와 EBV는 H&E 조직학적으로 특징적인 형태학적 feature가 있어 딥러닝이 잘 탐지한다. 반면 CIN과 GS는 조직학적으로 less distinctive하여 AUC가 상대적으로 낮고, 외부 데이터셋 적용 시 성능 저하도 더 크다.
[출제 근거] S1(슬라이드 pp.43-53, 11장) + S7(4군 비교 표) + B2(표를 행별로 직접 읽어줌) + S5(반복 언급).

✅ Q10. [서술형] 위암(GC) WHO 조직학적 분류의 각 서브타입의 형태학적 특징과 예후를 비교하시오.
[모범 답안]
Tubular adenocarcinoma (45-64%): 가장 흔한 subtype. Well/Moderately/Poorly differentiated로 분류. Tubule 형성 정도에 따라 구분.
Papillary adenocarcinoma (2.7-9.9%): 손가락 모양의 elongated processes. 조직학적으로 well differentiated처럼 보이나 간 전이 빈도가 높고 예후 불량.
Poorly cohesive carcinoma (20-54%): Signet-ring cell type(SRCC)과 Non-signet-ring cell type(PCC-NOS)으로 구분. 5년 생존율 <15%로 예후 최불량. Linitis plastica 동반 가능.
Mucinous adenocarcinoma (2.1-8.1%): 종양 면적의 50% 이상이 세포외 mucin으로 구성. 예후 non-mucinous GC보다 불량.
Mixed adenocarcinoma (6-22%): 두 가지 이상의 조직학적 성분 혼재. 단일 성분보다 예후 불량.
임상적 의의: Differentiated type은 내시경 절제의 적응증 결정에, Undifferentiated component >10%는 mucosal GC 내시경 절제 후 완전 절제 판정에 영향을 준다.
[출제 근거] 슬라이드 pp.24-29에 걸쳐 6장 분량. S1 + S7 + B2(각 subtype을 개별 슬라이드로 설명). WHO/JGCA 분류 표(p.29) 포함.

✅ Q11. [서술형] "THE FUTURE IS MULTIMODAL" — AI 기반 디지털 병리의 현황과 향후 발전 방향을 논하시오. (Summary 슬라이드 기반)
[모범 답안]
현황: AI는 암 조직병리학의 표준 도구가 되었다. 진단 workflow 개선, 인간 오류 제거, 관찰자간 재현성 향상, 예후 예측이 가능해졌다. 5년 내 다수의 새로운 임상 승인 바이오마커가 등장할 것으로 예상된다.
아직 미개척 영역: 예후 인자(prognostic feature) 발굴, 치료 성공 예측, morphological phenotype과 genotype의 관계 파악은 아직 발전 여지가 있다.
미래 방향: ① 개별 질환 모델을 위한 더 큰 multimodal dataset 구축 ② 치료 반응 및 저항성 예측을 위한 multimodal DL 활용 ③ 구체적으로: 병리 이미지(histology) + 유전체 데이터(genomics) + 텍스트 + radiology 이미지를 통합하는 multimodal neural network가 대세
이처럼 "THE FUTURE IS MULTIMODAL"이 핵심 메시지이며, 단일 데이터 모달리티의 한계를 극복하고 더 정확한 예후·치료 반응 예측이 가능해질 것이다.
[출제 근거] Summary 슬라이드(p.95) 교수 명시 → 최우선 출제 신호. S2("Take Home Message" 담화 표지 직접 사용) + S5(Multimodal 반복). 슬라이드 pp.78-79에서도 "THE FUTURE IS MULTIMODAL" 명시.

【PHASE 1-4 분석 요약 & 교차검토】
PHASE 4 — 자기검증 결과
TIER 1 토픽 12개 중 12개 커버 = 커버율 100%
"TIER 1 토픽 12개 중 12개 커버. 누락 토픽: 없음"

교차검토: 이 문제들이 정말 최선인가?
강력히 지지하는 근거:
슬라이드 pp.9/10/17/78/80에 동일한 4가지 접근법 도표가 5번 등장한다. 이는 강의 전체의 뼈대 구조를 이 도표로 잡겠다는 의도이므로 Q3은 거의 확정적이다.
Summary 슬라이드(p.95)는 교수님이 직접 "여기서 나온다"고 지정한 가장 강력한 신호다. Q11은 반드시 준비해야 한다.
MIL 설명에 한국어 전용 슬라이드(p.70)가 별도로 존재하는 것은 영어 슬라이드 중심 강의에서 이례적으로 강한 강조 신호다. Q4는 높은 확률이다.
주의해야 할 Trap 포인트:
Papillary adenocarcinoma는 "well differentiated처럼 생겼는데 예후가 매우 안 좋다"는 점 — 반드시 암기. 외관과 예후가 역설적이므로 트랩 문제로 자주 출제된다.
GC 분자 분류에서 MSI와 EBV의 H&E AUC가 높은 이유 — 단순 AUC 암기가 아니라 "조직학적으로 특징적인 feature가 있기 때문"이라는 기전을 연결지어야 한다.
External validation 시 AUC가 하락하는 패턴 — "범용성이 떨어진다"는 결론과 "다기관 데이터 통합"이라는 해법을 세트로 암기해야 한다.

================ [RECORDING 녹음본 — 교수 오피셜 발화(해설/강조신호 사실원) | file: 04-28 강의 디지털 병리 WSI와 딥러닝 기반 AI 병리 —.txt] ================

04-28 강의: 디지털 병리 WSI와 딥러닝 기반 AI 병리 — 위암·간세포암 예측, 멀티모달·파운데이션 모델, 임상 성능 평가

00:00:02
Speaker 1
저는 충성 모병원의 공기과에 있고요. 이송학이라고 합니다. 제가 오늘 얘기해 드릴 거는 Digital AI Pathology, Morphology and Clinical Insight 그런 제목을 적어봤습니다. 병리 이미지 가지고 스캔을 해서 AI 연구를 했던 것들, 제가 했던 연구들, 다른 연구자들이 했던 연구들을 이렇게 좀 몇 개를 소개를 시켜 드릴 거고요.
00:00:40
Speaker 1
그다음에 병리 이미지를 이용한 AI 연구의 전체적인 트렌드가 어떻게 진행되고 있는지 이것에 대해서 좀 살펴보도록 하겠습니다. 딥러닝 연구에 대해서 잘 모르시는 분들이 대부분일 거라서 일단 쉽게 쉽게 좀 설명을 드리도록 하겠습니다. Digital Pathology 얘기는 많이 들어보셨을 거고요. 그래서 병리의사 하면 여러분들 생각하기에 현미경을 보고 유리 슬라이드를 보고 그런 사람들이 있잖아요.
00:01:20
Speaker 1
이렇게 생각을 하실 텐데, 요새는 유린슬라이드를 다 스캔을 해요. 대형병원들에서는 다 스캔을 해서 디지털화를 이루고요. 그래서 전용 뷰어를 해서 이렇게 현미경이 아닌 컴퓨터 스크린으로 봅니다. 그래서 이렇게 됨으로써 좀 편해지는 게 있겠죠. 그래서 어떤 케이스를 컨설테이션 할 때도 우편으로 가지 않고 그냥 파일만 보내면 되니까 편리하고요.
00:01:50
Speaker 1
전체적으로 랩 워플로도 빨라지겠죠 당연히. 그리고 무엇보다도 이제 중요한 게 여기에다가 AI 를 붙여가지고 여러 가지를 좀 해볼 수가 있습니다. 그래서 이제 풀 슬라이드 이미지 이것도 들어보신 분들은 꽤 될 거예요. 그래서 슬라이드 스캐너를 이용해서 유리 슬라이드 한 장을 모두 이렇게 스캔을 해가지고, 디지털 변환된 단일 고해상도 유리 슬라이드 영상 파일 이렇게 되어 있긴 한데요.
00:02:24
Speaker 1
일단은 스캔을 하고 다중 계층 피라미드 형식으로 이렇게 저장을 해요. 그래서 다양한 해상도 이미지 레벨에 저장이 되어 있고요. 이게 크기가 다 합하면 한 장에 수술 검체 같은 경우에는 한 4,5 기가 이렇게까지 될 수가 있어요. 일단 닫힌 피라미도 형식으로 저장이 있어서 스크롤을 하면 커졌다가 작아졌다 이런 거 있잖아요.
00:02:54
Speaker 1
그렇게 가능하고요. 뷰어를 봤을 때. 그래서 일단은 뭐를 하든지 간에 연구를 하든지 간에 이게 풀슬라이드 이미지 자체가 너무 크기 때문에 전체적으로 뭐를 하지는 못하고요. 패치 단위로 이렇게 끊어서 여기 보시면 이렇게, 갑자면으로 이렇게 되어 있잖아요. 그래서 패치 단위로 해가지고 분석을 합니다. 그래서 패치 크기는 250, 250 픽셀부터 1014, 1014 그런 픽셀까지 다양하게 설정을 할 수가 있습니다.
00:03:31
Speaker 1
그래서 이제 패치 중에서도 중요한 조직이 들어가 있는 패치가 있고 조직이 안 들어가 있고 빈 공간이 있는 패치도 있고, 슬라이드 제작하면서 이렇게 접히거나 뭔가 염색성이 나쁘거나 그런 데도 있을 거 아니에요. 그런 거는 다 불필요한 영역을 제거를 합니다. 그래서 배경도 제거해 가지고요. 일단 computation 하게 계산을 해야 되니까 계산 부담을 줄입니다.
00:04:02
Speaker 1
그리고 이제 슬라이드 하나만 가지고 분석하는 경우는 거의 없고요. 몇백 개 단위로 이렇게 슬라이드를, 데이터셋을 다 통으로 이렇게 분석을 합니다. 그래서 슬라이드마다 이미지가 조금씩 다릅니다. 염색성이 좀 다르고요. 그 다음에 병원마다 염색성이 좀 다릅니다. 그래서 그것을 보정을 해야 됩니다. Color Normalization 해가지고요. 슬라이드 간의 그 차이를 일관성 있게 유지를 해가지고 불균형을 줄이고 왜곡을 최소화한다.
00:04:35
Speaker 1
이 목적으로 이렇게 합니다. 그래서 이제, 그런 패치를 단위로 해가지고 CNN 으로 돌립니다. 그래서 뭐 많이 들어보신 분도 있을 거예요. Convolution 을 뉴럴레터고요. CNN 구조 합성복이라고 하죠. 그 컨볼루션 같은 경우에는 일단 결국에는 이미지 패치가 행렬로 계산이 되거든요.
00:05:08
Speaker 1
포함이 되거든요. 나타나거든요. 그래서 여기에다가 필터 조그만 필터로 해가지고 결국에는 곱합니다. 그러면 행렬 곱하기 행렬은 행렬이 되잖아요. 근데 적은 행렬이 곱해지면 차원이 축소가 되는 행렬이 되겠죠. 그겁니다. 그래서 일단 여기를 패치 단위로 쭉 훑으면서 이렇게 결과들을 모니터 해가지고 새로운 행렬에 넣고 그 다음에 그거를.
00:05:39
Speaker 1
풀링을 합니다. 그래서 각각의 개별 패치에서 예측의 결과를 집계를 합니다. 그래서 convolution 해가지고 줄이고 그 다음에 그것을 풀링 해가지고 이렇게 놓고 그래서 이제 convolution 풀링 convolution 풀링 이렇게 몇 번 하다 보면 이렇게 줄어듭니다. 그래서, 병리 이미지에서는 어쨌든 핵의 모양, 선구조, 회포밀도, 기질 패턴 이런 것 같은 형태학적 특징이 있잖아요.
00:06:11
Speaker 1
그래서 이런 형태학적인 중요한 특징만 남겨놓고 이렇게 피처맵으로 표현이 됩니다. 그래서 이렇게 주요 특이점만 남깁니다. 그래서 이렇게 피처를 뽑는 과정 그게 이제 CNN 이라고 생각하시면 됩니다. 그리고 이제 그 feature 를 뽑았으면요. 추출된 특징들을 종합해 가지고 분류를 해야 될 거 아니에요. 그래서 분류를 하는 과정이 이제 MC 의 레이어라고 이렇게 보시면 될 것 같습니다.
00:06:44
Speaker 1
그래서 여기 보시면은 이게 얼룩말이잖아요. 그래서 이렇게 얼룩말의 특징을 뽑아서 예측을 해서 예측 결과를 softmex 함수값으로 해서, 어떤 이미지가 무슨 이미지인지 확률을 통해서 이제 분류를 합니다 그래서 이 경우에는 지브라가 0.7 이고 홀스가 0.2 고 독이 0.1 이다 해가지고 이 슬라이드 이 패치는 지브라다 이렇게 해가지고 뱉어내게 됩니다 값을 그런 과정을 거치게 됩니다 그래서 일단 분류를 할 때는 패치 단위별로 어떻게 분류를 다 하겠죠 패치 단위별로.
00:07:30
Speaker 1
예측을 한 다음에, 그 다음에 이제 그것을 다 오리게 해서 슬라이드별로 예측을 하게 되겠습니다. 그래서 두 가지 개념이 있고요. 여기서 딥러닝 연구를 하는 데 있어서 되게 크게 4 가지 정도 알고리즘을 나눠볼 수가 있습니다. 그래서 Stongling Spervised Model, Nuclease Spervised Model Multimodel, Foundation Model 이렇게, 여기서부터 좀 설명을 드릴 텐데요.
00:08:01
Speaker 1
일단 얘는 셀을 디텍션한다. 셀 단위로 디텍션한다 이렇게 생각하시면 될 것 같습니다. 그래서 셀을 디텍션해서 예를 들면 튜머 셀이라든지 틸, 튜머 임필트라든지 인포사이트라든지 그런 거를 셀 단위 디텍션하면 그거를 카운팅할 수 있겠죠. 그 다음에 Unostochemist 같은 경우는 그거를 quatifying 할 수 있겠죠. 그래서 그런 것에 사용하는, 방법이라고 생각하시면 됩니다. 그래서 이제 실제로 이제 TIL 가지고 TIMO 인포 사이트에 와가지고 했던 AI 연고를 소개시켜 드리겠습니다.
00:08:36
Speaker 1
그래서 제가 했던 건 아니고 이제 루닛, 많이 들어보셨을 거예요. 회사 그래서 루닛에 보면은 호프 IO 라는 그런 알고리즘이 있습니다. 그래서 슬라이드를 텐서 슬라이드를 업로딩을 하면은 거기서, 다 어노테이션이 돼 가지고 이렇게 나옵니다. 그래서 이거는 IO 라는 거는 한 25 개 캔서 타입에 대해서 여러 가지 퍼실라이트 이미지를 가지고 트레이닝을 시켰던 그런 데이터셋이고요.
00:09:11
Speaker 1
알고리즘이고요. 그래서 여기서 나오는 게 cancer mpcelium, cancer stroma, 그 다음에 틸 이렇게 구분돼서 나옵니다. 그래서 이제. 이 연구에서는 서울대 분당이라든지 삼성이라든지 이런 데서 lung cancer 를 가지고 이미 체크 포인트 2m 투여했던 lung 환자들을 가지고 연구를 해봤던 것입니다. 그래서 이제 패치 단위로 이렇게 보면 cell cell 을 다 계산하고 cancer epitellium 이 뭔지 cancer stroma 가 뭔지 이렇게 다 계산이 되잖아요.
00:09:49
Speaker 1
팁이 계산되고 그래서 인제 인플레 미드 타입, 이메인 익스콜리드 타입, 이메인 제저트 타입 이렇게 세 구분으로 나눴습니다. 그래서 인플레 타입 같은 경우에는, cancer epichelium 사이사이에 til density 가 높은 것, 그 다음에 imen excluided type 같은 경우에는 cancer epichelium 에 있는 til 은 낮은데 cancer stroma 에 있는 til 이 높은 것, 그 다음에 imen desert 는 전체적으로 til 이 낮은 것, 이렇게 해서 세 군으로 나눠서 분석을 했어요.
00:10:22
Speaker 1
자동화를 다시 해서 분석을 했고요. 그러면 이제 패치 단위로 해서 이 슬라이드가 결국에는, inflaned type 이다. inmened type 이다. 이렇게 나눌 수가 있겠죠. 그래서 실제로 inmene 10.2m 했던 환자들에 대해서 PFS 를 봤더니 inflaned type 에서 PFS 도 좋고 oral survival 도 좋았다. 이렇게 되어 있고요. 그 다음에 이제 여러분 알던 PDL1 있잖아요.
00:10:55
Speaker 1
그래서 PDL1 이 Runkens 에서는, 높을수록 이미지 체크포인트 리미터에 잘 들 것 같다 이렇게 예측을 할 수 있잖아요. 근데 이게 50%, TPS 가 50% 이상 그룹에서는 그게 잘 맞는데 TPS 가 1,49% 같은 경우에는 이게 센서가 TPS 가 낮다고 해서 잘 듣거나 TPS 가 높다고 해서.
00:11:25
Speaker 1
안 듣거나 이런 경우가 꽤 있기 때문에 그래서 예측력이 좀 떨어진단 말이에요. 그래서 이거를 봤을 때 AOC 를 봤을 때 PDL-1, PPS 보다 Runit Scope Bio 가 더 이면 체크포인트 이미 더 예측이 더 좋았다. 이렇게 했던 연구입니다. 그래서 이제 AI 베이스로 해가지고 이렇게 분석을 할 수 있고요. 그래서 이제 저희가 또 해봤던 거는, 이제 이거는 gastric cancer 거든요.
00:11:55
Speaker 1
그래서 이게 cancer, epichellium 이고 이 사이에 stroma 하고 이렇거든요. 그래서 이거는 이제 호버넷 이라는 걸로 해봤고요. 이제 딱 봐도 cancer, epichellium, cancer cell 잘 어노테이션 돼 있고 stromal cell, remocite 이런 거 잘 어노테이션 돼 있고 하잖아요. 그래서 이런 것을 지금 진행하고 있고 이제 업데이트하는 중입니다. 그래서 이제 그런 알고리즘도 있고 그 다음에 weekly supervised model 같은 것도 있어요.
00:12:27
Speaker 1
그래서 이게 어노테이션 자체를 셀 단위가 아니고 영역별로 내지는 슬라이드별로 이렇게 할 수 있는 거죠. 그런 경우를 이제 weekly supervised model 이라고 합니다. 그래서 digansis 를 한다든지, 튜버 그레이딩을 한다든지, 서브타이핑을 한다든지, mutation, response programsis 예측이라든지 이런 것이 포함이 됩니다. 그래서 이제 제가 오늘 하려는 얘기는 HA 슬라이드 얘기입니다.
00:12:57
Speaker 1
그래서 여러분 알다시피 HA 슬라이드는 Cancer 환자면 대부분 다 있고요. 어쨌든 수술 환자면 다 있는 그런 조직입니다. 그래서 Routine 이 available 한다. 그죠? 그 다음에 이 자체가 information 되게 많은 데이터 소스입니다. 그래서 이게 lung cancer 환자거든요. 체스트 CT 이미지를 실제 픽셀 단위로 이렇게 봤을 때 테스트 이미지 크기가 요만하다면 병리 이미지는 요만합니다.
00:13:31
Speaker 1
그래서 엄청나게 크잖아요. 딱 봐도 엄청나게 많은 데이터가 들어가 있을 것 같잖아요. 그래서 이제 그런 high-formation density 자체가 딥러닝에 좋은 소스가 됩니다. 그래서 이제 h-slide 를 가지고 많은 것을 해볼 수가 있습니다. 그래서, 그 암 연구를 병리 이미지 가지고 딥러닝이 했던 암 연구를 크게 나눠보면요. Basic Application 하고 Advanced Application 이렇게 두 가지로 나눌 수가 있습니다.
00:14:01
Speaker 1
그래서 Basic 딥러닝 같은 경우에는 튜버 디텍션이라든지 서브타이핑이라든지 그레이딩이라든지 이런 겁니다. 그래서 병리의사들이 누구나 다 할 수 있고 늘상 하는 일인데, 이거를 딘서닝으로 자동화를 시키면서 TAT time 을 줄이고 cost 도 줄이고 이런 역할을 할 수 있겠죠. 근데 이 자체가 Treatment recommendation 을 바꾸거나 하지는 못하겠죠. 근데 반면에 Advanced application 같은 경우에는 어떤 H-Slide 를 가지고 서바이벌을 예측한다든지 Genectic markhol, mutation 이 있는지 없는지 이런 것을 예측한다든지 그 다음에 트리트먼트에 잘 됐는지 안 됐는지 이런 것을 예측할 수가 있습니다.
00:14:47
Speaker 1
그래서 이거는 이제 병리인사가 할 수 없는 영역까지 해보는 거죠. 그래서 이게 잘 되면 어쨌든 새로운 클래스의 바이오마커로서 이렇게 기능을 하게 될 것입니다. 그래서 이제 그렇게 두 가지 카테고리 중에 Basic 어플리케이션부터 좀 소개를 시켜드리면요. 일단은 뭐 tumor detection, subtyping grading 하는 그런 연구 과제들 되게 많습니다. 저도 많이 해봤고요. 그래서 그 딥러닝 연구하는 데서 기본적으로 제일 많은, 매트릭스가 있지만 AOROC 를 제일 기본적으로 하거든요.
00:15:19
Speaker 1
그래서 퍼포먼스가 알고리즘 퍼포먼스가 어떻게 되는지 이거를 할 때 이렇게 측정할 때 사용합니다. 그래서 AOROC 가 대게는 한 0.9 이상은 되는 그런 베이스 어플리케이션은 그렇습니다. 그래서 이거는 이제 Ground Truth 메소드 즉 이제 병리사가 이렇게 어노테이션을 해놓은 것을 딥러닝 알고리즘을 어느 정도 잘 따라하냐 이겁니다. 그게 본질입니다. 그래서 AORC 가 0.99 이상이다 그러면 영리사만큼 잘 따라하네 그렇게 낼 수가 있겠죠?
00:15:52
Speaker 1
근데 이제 하나의 데이터셋만으로 트레이닝을 시키면요 과적합에 빠집니다. 그 데이터셋에만 잘 작동하는 그런 알고리즘이 되기 때문에 internal dataset 으로 validation 하는 그런 과정이 필요하다고 생각합니다. 그리고, 데이터 셋이 데이터의 크기가 슬라이드 크기가 커지면 개수가 많아지면 트레이닝하는 그러면 성능이 좋아지긴 하는데 이게 어느 정도 되면 세츄레이션이 됩니다.
00:16:32
Speaker 1
그래서 플라투가 이르고요. 그게 한 만에서 만오천적이다. 이렇게 주장하는 논문도 있습니다. 그래서 제가 해봤던 건데요. 풀 슬라이드 이미지 가지고, 위암을 subclassification 에 해봤던 그런 연구입니다. 그래서 이제 인자제에는 병진에서만 있는 게 아니기 때문에 잠깐 위암의 histological subtype 에 대해서 소개시켜 드리면요. tubular adenocalcinoma 가 제일 많습니다. 그래서 딱 봐도 tubule 을 잘 형성하죠.
00:17:04
Speaker 1
그 다음에 중간 정도 형성하고 tubule 을 잘 형성하지 않죠. 그래서 이게 well deferentiated, moderately, poly diferentiated 라고 합니다. papillar lenocalcinoma 는 이렇게 손가락만 생겼는데 언뜻 보기에는 well deforentiate 처럼 생겼는데 매우 안좋습니다. porelyquoisebucalcinoma 해가지고 낱낱이 떨어져 있는 cell 로 되어 있는데요. 여러분 잘 알고 있는 signatic cell 이런 걸로 볼 수도 있고 signatic 이 아닌 그런 non-signatic cell 타입으로 보일 수도 있고 그렇습니다.
00:17:41
Speaker 1
그 다음에 mucinocid lenocalcinoma 도 있어요. 하얗게 보이는 게 뮤신이거든요. 그래서 뮤신이 50% 이상이 튜머에 차지할 때 musion shadn carcinome 이라고 합니다. 그리고 이제 mixed darn carcinome 가 있습니다. 그래서 여기 보시면 위쪽에는 뭔가 튜브를 형성하는데 아래쪽에는 puliqueson carcinome 형태로 되어 있고요. 이런 형태가 시터마켓에서는 꽤 되거든요. 한 22% 정도까지 보입니다. 그래서 하나의 컴포넌트보다 AO 가 안 좋은 걸로 되어 있습니다.
00:18:13
Speaker 1
그래서 이제 지금까지 말씀드렸던 것은 WHO classification 입니다. 그래서 이것을 1 번 classification 에는 papillar denocarcinoma, tubular Well, monoratry 를 differentiated type 이라고 하구요. tubular PD 와 poly differentiated 와 poly poysifcarcinoma 이것을 differentiated 라고 합니다. 그래서 이제 제가 여기서 해본 것은, deferentiated type undiferentiated type 그 다음에 유지하자. 이것을 구분을 해 보았습니다.
00:18:44
Speaker 1
그래서 TCGA 데이터셋, 여러 30 개 되는 암종이 있는 거기에 병리 이미지 들어와 있고 유전체에도 결과가 다 있는 동공 데이터셋입니다. 오버 5 이 396 케이스 정도 stoma cancer 를 사용했고요. 트레이닝 시켰고요. 그 다음에 Validation set 로는 저희 병원 데이터를 사용을 했습니다. 그래서 간단하게 말씀을 드리면, annotation, tubor 부분, notubor 부분을 제가 다 annotation 을 했고요.
00:19:18
Speaker 1
그것에 기반해서 normal tubor 를 가르는 deep lining classifier 를 만들었습니다. 그 다음에 tubor 중에서, deferentiated, undeferentiate, musinus, nomusinus 그런 것을 가르는 그런 classifier 를 만들었습니다. 그래서 이제 supercial 의 간단하게 만들어 봤고요. 그래서 이제 differentiated 와 undiferentiated 를 가르는 그런 classifier 의 avarus 는 0.93 입니다.
00:19:50
Speaker 1
굉장히 좋았죠. 그 다음에 nomusinus, musinus 같은 경우에도 0.979 로 상당히 좋았습니다. 그래서 이제 이렇게? 히스티맵으로 표현을 할 수가 있습니다. 그래서 여기는 undifferentiated 타입이면서 mucinous 타입인 것, 그 다음에 differentiated 타입이면서 mucinous 인 것, 그 다음에 섞여 있는 것, listed carcinous 인 것, 그래서 이렇게 visualization 을 잘 할 수가 있습니다. 그래서 이제 이거는 이제 TCA 로 다 데이터셋으로 트레이닝을 시켰기 때문에 그것을 이제 저희 병원 데이터셋에.
00:20:28
Speaker 1
이렇게 어플라이를 해봤습니다 그랬더니 AUC 가 differenciated 0.895, nommiciated 0.93 으로 아까보다 조금씩 떨어졌습니다 그래서 확실히 이제 데이터셋이 달라지면 성능이 떨어지기는 합니다 그런 다음에 지금까지는 이제 패치 레벨 단위로 이렇게 했던 거고 이제 슬라이드 레벨로 봤을 때는 differencated, undiferencated, mixed 이런 순서입니다 이게 당연하겠죠, undiferenced type 같은 경우에는 낱낱이 떨어져 있어서 inflamatory cell 처럼 cell 이 그렇게 보이는 경우가 있거든요.
00:21:05
Speaker 1
그래서 병리사들도 잘 모르는 경우가 있기 때문에 딥러닝 성적도 좀 떨어지는 것을 알 수가 있습니다. 그리고 mixed 는 두 개 섞여 있기 때문에 더 떨어지겠죠. 그래서 differenc undiferenced non-mission, mission type 을 나누고 각각의 퍼센트까지 이렇게 다 할 수가 있잖아요. 그래서 그거를 만든 알고리즘은, 예후 예측에도 좋고 유용하다는 결론이었고요. 그 다음에 이제 EGC, Oligastry cancer 를 HE 슬라이드만 가지고 Lymph node metastasis 를 예측을 해봤습니다.
00:21:41
Speaker 1
사실 이거는 미리 말하면 딥러닝은 아니고 머신러닝에 해당하는 기법으로 해본 겁니다. 그래서 총 1,237 개의 5 개 기관에서 모임 데이터셋을 가지고 해봤고요. 이게 XG 부트라는 그런 테크닉을 사용했고 70 케이스 그러니까 70 개의 morphological feature 를 이용을 해서 infulment metasis 를 갈라봤습니다. 이런 점을 예측을 해봤습니다.
00:22:13
Speaker 1
그래서 총 AUC 가 0.75 월 오브 AUC 가 그 정도 나왔습니다. 그래서 했던 그런 morphological feature 중에 70 개 중에 뭐가, 그 림프노드 메타시타스의 중요했냐 이거를 봤을 때 일단은 total tumor 의 양과 그 다음에 undifferenciated 의 양 그겁니다. 그래서 이제 뭔가 튜머가 되게 치밀하고 크고 내지는 undifferenciate 가 많거나 이러면은 림프노드 메타시타스가 많다 이렇게 알 수가 있었던 그런 과제가 되겠습니다.
00:22:51
Speaker 1
그래서 여기서는 0.75 였고요 뒤쪽에 또 한번 해봤는데, 다시 한번 설명을 드리겠습니다 그래서 이제 H 슬라이드 가지고 어떻게 mutation 을 예측하냐 요거는 일단 보시면은 드라이버 mutation 같은 경우에는 cancer orphology 의 change 를 일으킵니다 그래서 뭐 nuclei 라든지 cytoplasmic texture, size, shape 이렇게 변화를 시키겠죠 그 다음에 그 주변에 있는 vibrablast 라든지 lympocyte 의 변화도 시키겠죠 배열도.
00:23:25
Speaker 1
그래서 이제 그런 변화들이 사람 눈에는 되게 소프트해서 잘 안 보여도 딥러닝은 그런 거를 잘 캐치할 수 있지 않을까 해서 생각해 보게 된 겁니다. 그래서 여기서도 여러 가지 주제가 나왔고요. Mutation 을 예측한다든지 response 를 예측한다든지 survival 을 예측한다든지 이런 과제들이 AOC 를 보시면 확실히 아까는 0.9 이상이었잖아요. Base 는 Advanced 는 확실히, 이렇게 AOC 가 떨어지는 것을 알 수가 있습니다.
00:23:56
Speaker 1
확실히 이제 H 슬라이드만 가지고 예측하기에는 좀 한계가 있다 이렇게 알 수는 있겠죠. 그래서 이제 저도 Gastric cancer 가지고 Genantic alstoration 을 예측을 해봤습니다. 잘 아시는 분은 아시겠지만 TCJA 데이터셋에 보면 그걸 가지고, Moleclar Classification 네 군으로 나눕니다. CIN 그룹, EBV 그룹, MSI 그룹, GS 그룹 이렇게 네 군으로 나누고요.
00:24:27
Speaker 1
그 다음에 비슷하게 LCRJ 라고 해서 아시아 쪽에서 네 군으로 나눈 연구가 있었습니다. 그래서 MSI 그룹, EMT 그룹, TP54 인 그룹, 그 다음에 TP53, Negative In Group 이렇게 네 군으로 나누고요. 그래서 molecular alteration 이 다르고, 부분마다 disease prograction 이 다르고 proglosis 가 다릅니다. 그렇게 해서 어쨌든 네 군으로 나눴는데 그런 TCJ 나 ACRD 로 그런 네 군으로 나누는 데 있어서 중요한 유전자들이 몇 개가 있는데 그래서 그거를 한 다섯 개 정도 되는 유전자들을 mutation 이 있는지 없는지를 저희가 예측을 해봤습니다.
00:25:09
Speaker 1
그래서 TCJ datas 해가지고, 트레이닝 시켰고 저희 병원 데이터셋 가지고 또 validation 을 해봤습니다. 그래서 이제 어쨌든 non-tissue classifier 로 티슈 부분만 티슈 패치만 비플이 없는 부분 다 빼고 이거를 적용을 하고요. 그 다음에 normal tumor classifier 로 이제 tumor 부분 튜머 패치만을 뽑아내서 tumor patch 만 가지고 그 다음에 wild type mutation classifier 를 적용을 했습니다. 그래서 예측을 해본 결과입니다.
00:25:41
Speaker 1
P54 뮤테이션 같은 경우에는 어쨌든 프로젠 티슈에서 FFP 파라핀 티슈에서 똑같이 0.72 AC 가 그 정도 나왔고요 픽스레스 같은 경우에는 프로존에서 0.86 FFP 에서는 0.82 정도 이렇게 로테이션 예측력이 나왔습니다, 그래서 이제 그거는 TCA 에서 나왔던 결과고요. 그거를 이제 다른 데이터셋 저희병원 데이터셋에 적용했을 때 확실히 AOC 가 확실히 많이 떨어졌습니다.
00:26:15
Speaker 1
그래서 이 얘기는 이 데이터셋은 그러니까 이 알고리즘은 뭔가 범용성이 좀 떨어진다. 아직까지는 그렇게 봐서 이제 뭔가 개수를 늘렸습니다. 그래서 TCA 랑 저희병원 데이터셋이랑 다 이렇게 합쳐가지고 테이닝 시키고, 밸류에이션을 했더니 0.761, 0.775 이렇게 좀 높아지는 양상을 보였습니다 그래서 마찬가지로 해서 TCJ 네 군으로 나누는 클래스 파일을 만들어 봤습니다 그래서 결과를 보시면 MSI 랑 EBV 랑 ALC 가 좀 높은 것을 알 수가 있고요 확실히 CIM GIS 그룹보다 높습니다 이 얘기는.
00:27:01
Speaker 1
사실 MSI gas3 cancer 랑 그다음에 EBV positive cancer 인 경우에는 H 슬라이드가 조직학적으로 좀 특징적인 feature 가 있거든요. 그래서 병리사가 조금 봐도 이거는 MSI tumor 일 것 같은데 뭐 이런 게 예측이 좀 어느 정도는 됩니다. 그래서 그게 좀 반응이 된 것 같고요. 그래서 이제 그런 TCA 데이터셋을, 알고리즘을 저희 병원에다가 했더니 확실히 또 떨어집니다.
00:27:32
Speaker 1
그래서 MSI 랑 EBV 랑은 그래도 좀 덜 떨어지는데 CIU 와 GS Group 은 AOC 가 많이 떨어지는 그런 양상을 보였습니다. 그리고 이제 Codify Data 라고 해서 제가 Large Scale 의 데이터 플랫폼을 구축하는 그런 사업을 5 년 동안 했었거든요. 병리 이미지가 한 1,000 개 gastric cancer 이미지만 한 1,000 개 넘게 있고 MSI status 를 알 수 있는 데이터셋이 그 정도 있습니다.
00:28:04
Speaker 1
그래서 그거를 가지고 트레이닝을 시켜봤습니다. 그래서 MSI 트레이닝을 시켜봤고 거기에서 AUC 가 0.91 정도 이렇게 나왔습니다. 그래서 이 데이터셋은 TCJ 데이터셋으로 트레이닝 시킨 것보다 훨씬 더 AUC 가 높았습니다. 그래서 그 얘기는 이제, 어쨌든 성능을 높이려면 기본적으로 데이터셋의 크기가 좀 커야 된다. 그리고 다기관에 많은 데이터셋을 가지고 트레이닝 시켜야지 좋은 결과가 나올 수 있겠다. 이것을 예측을 해봤습니다.
00:28:37
Speaker 1
그래서 마찬가지로 TMB Status 로 지슬라이드만 가지고 예측을 해봤습니다. TMB 라는 것은 1MB 길이에서 뮤테이션이 몇 개 있냐 그겁니다. 그래서 보시면은 TMB 를 확실히 알려면은 Full Exom 시퀀싱이나 적어도 MGS Targeted Sequencing 은 해야지 알 수가 있습니다. 근데 이제 좀 비용이 많이 들잖아요. 아시다시피 그래서 H 슬라이드로만 이렇게 예측을 해봤습니다.
00:29:11
Speaker 1
그래서 TMB 가 중요한 게 요새 중요해지는 게 MSR 이나 TMB 가 중요한 게 MIC 체크 포인트인 미터에 대해서 예측을, 잘 들을 걸로 예측한 그런 닌자이기 때문에 그렇죠. 네 그래서 이제 똑같이 해봤습니다. 그래서 ts, non-tsuclassifier 로 Tsumer 를 꼽고 그 다음에 normal tmer classifier 를 또 적용시켜서 튜버 패치만을 꼽고 그래서 튜버 패치만 가지고 그 중에서 TMB-High, TMB-Long classifier 를 적용을 시켜서 CN 의 방법으로 또 이렇게 예측을 해봤습니다.
00:29:45
Speaker 1
그래서 다기관 다 여러가지 튜버에 대해서 예측을 해봤고요. 가장 예측이 안 됐던 게 리버캔서 HCC 는 0.754 정도 했고 잘 그래도 예측됐던 게 스토마캔서입니다. 0.90 까지 나왔습니다. 그래서 이렇게 어느 정도는 H-슬라이드만 가지고도 이렇게 예측을 해볼 수 있겠다. 이렇게 알 수가 있었습니다. 그리고 이제 딥러닝으로 H-슬라이드 가지고 서바이벌을 예측할 수 있습니다. 그래서 그 두 가지 방법으로 해볼 수가 있어요.
00:30:17
Speaker 1
그러니까 어떤 genetic alteration 이라든지 survival 관계된 그 다음에 cancer stail 이라든지 뭔가 다른 histological feature 라든지 그것을, 예측을 함으로써 서바이벌을 간접적으로 예측할 수 있겠죠. 그 다음에는 서바이벌을 직접적으로 예측할 수 있겠습니다. 다른 한 가지 방법은. 그래서 이 병리 이미지를 딱 주고서 이미지는 서바이벌이 좋았던 것, 이미지를 나빴던 것 이렇게 어노테이션을 딱딱 해놓고서 그거를 트레이닝 시키면 어쨌든 딥러닝은 결과값을 뱉으니까요.
00:30:51
Speaker 1
그래서 그 결과값에 해당하는 서바이벌에 관계된 그런 feature 를, 패치들을 병리의사들이 떠꾸로 이렇게 봐서 어떤 특징이 있는지 이런 것을 알 수가 있겠죠. 그런 것도 해볼 수가 있습니다. 그래서 이제 HCC 에서 서바이벌 예측도 한번 제가 해봤습니다. 그래서 이번에는 저희 병원 데이터셋으로 두 데이터셋 하나는 예전 것 하나는 최근 것 해가지고 두 개의 데이터셋으로 나눠서 진행을 해봤습니다.
00:31:27
Speaker 1
그래서 이제 이렇게 하게 된 게 이제 서바이벌은 서바이벌이 다 있는 데이터셋이 필요했기 때문에 이렇게 저희병원 거를 이렇게 나눠서 해봤고요. 그 다음에 이제 서바이벌에 관계된 인자들 있잖아요. HCC 에서 HCC Grading, Admonds Styner Grading 이라든지, T-Stage 라든지, Pascularing Bang 이라든지, KI 수치 인덱스라든지 CK19 가 높으면 여기가 안 좋다고 알려져 있거든요. 그래서 이런 것을 인자들을 바탕으로 해서 logistic reduction model 을 만들 수가 있습니다.
00:32:02
Speaker 1
서바이벌에 관계된 그래서 서바이벌을 예측해 봤을 때 0.7 정도 나와요. 근데 그냥 에디터 엔드로 예측을 해봤을 때는 0.85 딥러닝 방법을 해봤을 때는 확실히 서바이벌이 잘 예측이 되더라 이렇게 알았고요. 그래서 패치 단위로 서바이벌을 다 예측을 할 수 있으니까 서바이벌이 좋았던 패치들, 좋았던 슬라이드, 나빴던 슬라이드 이렇게 패치 단위로 다 알 수가 있습니다.
00:32:37
Speaker 1
그리고 이제 실제로 프리젝션을 했던 게 진짜로 서바이벌이 좋았냐 나빴냐 이렇게 봤을 때 서바이벌이 다 좋았던 것, 나빴던 게 잘 갈리고요. 그 다음에 서바이벌이 나빴던 걸로 예측했던 패치와 좋았던 걸로 예측했던 패치들을 대표적인 패치들을 제가 뽑아서 봤거든요. 그랬더니 확실히 서바이벌이 나빴던 패치들로 예측했던 것은 애드워던 스타이너 그레이드가 좀 높았고 좋았던 것은 좋았고 낮았고 이런 차이를 보이긴 합니다.
00:33:11
Speaker 1
그래서 어쨌든 병리의사들이 보는 대로 딥러닝도 같은, 그것을 잘 찍어서 보는구나 이렇게 알 수가 있었고요. 그 다음에 이제 Advanced Application 에서 Treatment Response 를 Application 을 예측하는 겁니다. 그래서 여기서도 마찬가지입니다. 그래서 트리트먼트의 일단 예측을 이 슬라이드는 트리트먼트 좋았던 것 이 슬라이드는 트리트먼트 나빴던 것 이렇게 어노테이션을 해주고 그것을 이렇게 트레이닝을 시킨 다음에.
00:33:47
Speaker 1
딥러닝이 예측했던 결과값을 보고 어떤 패치들이 서바이벌에 관계된 패치들을 분석해가지고 트리트먼트에 관계된 패치들을 분석해가지고 그런 병리적인 특징을 거꾸로 뽑아낼 수도 있겠습니다. 그래서 이것은 제가 했던 연구는 아니고 일단 HCC 에서 요새 이제 Tab Eva 트리트먼트를 하거든요. 잘 많이 하거든요. 이미 체크포인트 리미터, 치료를 많이 각광을 받고 있습니다.
00:34:19
Speaker 1
그래서 그것을 H 슬라이드를 이용해서 이 치료가 잘 들을지 안 들을지 이것을 예측했던 그런 연구가 되겠습니다. 그래서 그 연구 지금 하기 전에 이 연구를 진행하기 전에 previous 한 스터디를 했던 게 이겁니다. 그래서 이 네이처 메디슨에 나왔던 이 과제에서는, ATE VEVA Response Signature 라는 것을 만들었습니다.
00:34:50
Speaker 1
Signature 라는 것을 자기네들이 만들어가지고 이것이 PFS 에 연관이 있고 트리트먼트의 이니세이션에 연관이 있더라 하는 것을 밝혀낸 게 이 논문입니다. 그래서 ABRS 가 뭐냐 하면 signature 된 expression 데이터입니다. 그래서 한 10 개 정도 되는 진이고요. 여기서 이제 CTL4 라든지 IMOS 같은 경우에는 T-cell Activation 에 관계되고 뭔가 이런 것들을 이제 innature imminite 가 관계됩니다.
00:35:24
Speaker 1
그래서 결국에는 immine response 에 관계된 그런 gene 들의 발현이 높으면 AO 가 좋고 이미지 체크포인트 인히미터에 대한 잘 들릴 것으로 예측이 되고, 이게 낮으면 예측이 잘 안 되고, 트리트먼트가 잘 안되고 이런 것을 예측했던 그런 과제입니다. 그래서 이제 이 연구에서는 그 AVRS 를 H-Slide 로 예측했던 겁니다.
00:35:54
Speaker 1
그래서 그것이 AVRS-P 라고 만들었고요. 그것이 실제로 PFS 와 잘 연관이 되는지를 본 연구입니다. 그래서 트레이닝 시킬 때 여기서도 TCJ 데이터셋, HCC 를 가지고 트레이닝을 시켰습니다. 그래서 이제 트레이닝 시킨 다음에 밸리데이션을 해야 되잖아요. 그래서 두 개의 밸리데이션 셋으로 밸리데이션을 했습니다. Surgical Resection Data Set 이 있고 바이옵시 데이터 셋이 있고 그래서 밸리데이션을 해봤고 그 다음에 실제로 이제 바이옵시 샘플이 있고 실제로 아테베바 트리트먼트를 받았던 그런 결과가 있는 그런 데이터 셋을 122 케이스를 선정을 해가지고 그것에 대해서.
00:36:42
Speaker 1
예측을 해봤습니다. 그 다음에 이제 네 케이스에 대해서는 Special Transcription 도 진행을 했습니다. 그래서 여기서 만든 모델 지정했던 모델이 MIM 이라는 모델입니다. 그래서 Multiple Instance Learning 이라고 하는데요. 일단 이 그림이 유명하더라고요. 예시로 들 때 유명하더라고요. 그래서 일단 어떤 문은 열쇠로 열어요.
00:37:12
Speaker 1
여기 두 세트는 열쇠로 잘 열리는 그런 세트예요. 열리는 세트, 여기는 안 열리는 세트라고 하면 새로운 세트가 왔을 때 문은 문을 열 수 있을지 없을지 예측하는 게 MIR 이다 이렇게 보시면 될 것 같습니다. 그래서 또 다른 예를 말씀드리면 어떤 슬라이드가 있는데 이 슬라이드가 트리트먼트를 잘.
00:37:43
Speaker 1
들은 슬라이드에요. 그러면 병리의사가 보면 어떤 부분이 트리트먼트에 잘 들을지를 어노테이션 할 수는 없어요. 그렇죠? 근데 이제 어쨌든 잘 들은 걸로 결과는 되어 있으니까 이 슬라이드에 있는 패치 전체를 그냥 잘 들었다 얘는 잘 듣는 패치들이다 그렇게 가정하는 거예요. 그러면 이 슬라이드는 다른 슬라이드는, 트리트먼트 잘 안 들었던 슬레이드가 있으면 그 슬라이드에 있는 패치들은 전부 다 안 듣는 걸로 이렇게 가정하는 거죠.
00:38:13
Speaker 1
그래서 러프하게 가정하는 거예요. 그게 MIL 이고요. 그래서 이제 어쨌든 네거티브 케이스에서는 AVRSP 로우 패치들은 네거티브로 가정하고 그 다음에 포지티브 케이스는 가정은 AVRSP 하이인 걸로 가정해서 트레이닝 시킨다 그것이 그겁니다. 여기에서 썼던 MIL 은 CLAM 이라는 모델입니다. 그래서 어쨌든 기본적으로 MIL 모델을 써가지고 attention-based mechanism 을 활용해서 일단 아까 처음에 말씀드렸다시피 패치 단위로 feature 를 뽑잖아요.
00:38:57
Speaker 1
패치에서 CNM 모델로 feature 를 뽑잖아요. 그래서 많은 feature 중에, 어쨌든 예측을 하는 데 있어서 중요한 feature 가 있고 안 중요한 feature 가 있을 거 아니에요. 그래서 중요한 feature, 안 중요한 feature 를 가중치를 두는 거예요. 그래서 이제 좀 더 예측력을 좋게 만드는 그런 방법이라고 보시면 될 것 같습니다. 그게 이제 클램이라고 보시면 될 것 같습니다. 그래서 어쨌든 폴 슬라이드 이미지를 가지고 패치다임을 쪼갠 다음에 피쳐를 뽑은 다음에 그 다음에 피쳐를 쭉 뽑았어요.
00:39:32
Speaker 1
그래서 여기서, attention mi 모델을 적용시켜서 attention map 을 만들어서 실제로 prediction 을 진행을 했습니다. 그러면 이제 avrs 값이 score 가 나오겠죠. 뭔가 숫자로 스코어가 쫙 나올 거 아니에요. 그러면 그 숫자들을 가지고 그 다음에 riscal 을 시킵니다. 0 에서 1 사이로 avrsp 를. 0 에서 1 사이로 어딘가에 다 배치가 될 거 아니에요.
00:40:03
Speaker 1
그래서 그걸 히트면으로 만든 게 이렇게 보이게 되는 겁니다. 그래서 이렇게 보이면 그래서 예측값을 보면 실제로 AVRS 와. ABRS 값은 어쨌든 지니 익스프레션을 통해서 계산됐던 실제 값이잖아요. 그거와 그다음에 ABRS P 는 굉장히 예측했던 값이잖아요. 그래서 어느 정도 correlation 이 있는지를 본 겁니다. 그래서 correlation coefficient 가 0.7, 0.8 정도로 꽤 높았던 것을 알 수가 있고요.
00:40:37
Speaker 1
그다음에 이제 ABRS P 가 나빴던 것, 그러니까 low 인 것, 하이인 거를 패치를 볼 수가 있을 거 아니에요. 그래서 하이인 패치를 보면 확실히, 림보스틱 이민 셀에 enragement 가 있더라 그것을 확인할 수가 있었습니다 그 다음에 이제 트레이닝 세트만 이렇게 봤으니까 밸리데이션을 했을 때 surgical 섹션에서 밸리데이션을 한 것과 IOMC3 에 대해서도 그런 coefficient 가 0.6, 0.54 이렇게 해가지고 어느 정도는 잘 코릴레이션이 되는 것을 봤고요.
00:41:13
Speaker 1
그 다음에 AVRS High T1 에서 확실히 PFS 가 높았다 좋았다 이것까지 이렇게 증명을 했습니다. 그리고 이제 아까 비지움 Special Transciptum 도 같이 했다 그랬잖아요. 그래서 AVRS 가 공간적으로는 이렇게 보입니다. 그래서 이게 빨간 게 높은 것, Gnape Special 높은 것, 그 다음에 이것은 낮은 것이라고 보면, 이 AVRS-P 는 이 케이스에 대해서 어쨌든 비슷하게 보이잖아요.
00:41:47
Speaker 1
높은 것은 높게 측정이 되고 그렇잖아요. 그래서 이런 네 케이스 중에 세 케이스에서는 그렇게 잘 일치가 되더라 실제 진 익스프레션 데이터와 공간적으로 잘 일치가 되더라까지 이렇게 봤습니다. 그래서 어쨌든 여기서 알 수 있는 것은 HCC 디지털 슬라이드 이미지에서 AI 를 이용을 해가지고, 아테메바 트리트먼트를 받은 환자에서 PMPS 를 알 수 있는 그런 마커가 되더라, 새로운 마커가 되더라가 결론이었고요.
00:42:19
Speaker 1
근데 이게 TCA 데이터로 트레이딩 시켰다고 그랬잖아요. 근데 그게 결국에는 다 Surgical Section Speciman 이거든요. 근데 실제로 우리가 예측하는 거는 바이오시슬라이드거든요. 그래서 뭔가, 조금 리섹션 슬라이드랑 바이오시스 슬라이드랑 성상이 좀 다르기는 해요. 그래서 리섹션 슬라이드로만 트레이닝 시킨 게 좀 리미테이션이다. 차후에는 바이오시스로 슬라이드를 시켜봐야겠다 이런 게 리미테이션이 있었습니다.
00:42:54
Speaker 1
그 다음에 이제 멀티모달 딥러닝이 되겠습니다. 그래서 멀티모달이라고 하면 하나 이상의 헤테로지난스 데이터 셋을 얘기합니다. 예를 들어서, 병리 이미지라든지, 지노믹 데이터라든지, 텍스트 데이터라든지, Radiology 이미지라든지 이런 이질적인 데이터 셋을 한꺼번에 묶어서 분석을 하는 방식이 되겠습니다. 그래서 유명한 논문이 모어 논문이 있는데요. 한 22 년부터 해서 이렇게 각광을 받기 시작했습니다.
00:43:26
Speaker 1
그래서 요새는 이렇게 많이 쓰고 있고요. 그래서 이제 병리 이미지로부터 피처를 뽑고요. 그 다음에 molecular 데이터로부터 거기서도 feature 를 뽑습니다. 그래서 그것을 merging 을 시켜가지고 환자의 예후를 예측하는 risk stratification 을 하는 그런 연구과제였거든요. 그래서 이것이 나타나면서 많은 연구가 돼서 이렇게 하고 있고요. 저희도 이렇게 진행을 하고 있습니다.
00:43:58
Speaker 1
그래서 요새는 또 파운데이션 모델 많이 들어보셨을 분도 많을 것 같은데 파운데이션 모델도 각광을 받고 있습니다. 그래서 일단 모델 하나만 있고 하나의 모델을 트레이닝 시키는데 다양한 다운스트림 데스크에서 작동을 하는 모델이 되겠습니다. 그래서 좀 설명을 드리면요. 어쨌든 대규모 데이터에서 프리 트레이닝이 완료되는 모델입니다. 그래서 대규모라는 게 몇 백만장 슬라이드 몇 십만장 이런 대규모 데이터에서 일단 프리트레이닝을 다 시킨 모델이 있다 그렇게 보시면 될 것 같습니다 그래서 여기서는 어쨌든 일반적인 패턴 데이터의 일반적인 패턴, 구조, 상관관계 등을 일반적인 것을 학습하고요 그 다음에 이제 여기를 통해서 파이트닝.
00:44:55
Speaker 1
적은 양의 레이블렌 데이터를 이용을 해가지고 특정 도메인에 맞게 추가로 학습시키는 방법이 되겠습니다. 그래서 1 차적으로 Foundation Model 을 적용을 하고 2 차적으로 Fine 진입을 시켜가지고 예측을 한다고 보시면 될 것 같습니다. Foundation Model 이 좋기는 한데 이것이 컴퓨팅 자원과 비용이 많이 드는 것이기는 합니다. 그래서 제가 리뷰 논문이긴 한데 Foundation Model 에 대해서 최근에 쓴 논문이 있고요.
00:45:32
Speaker 1
거기서 나온 그림이고요. Foundation Model 에 대해서 설명을 하려고 했던 그림이고요. 일단은 MSI 를 예측을 하려고 하면 MSI 에 해당하는 CN 은 만들고 예측을 하게 되겠죠. 그 다음에. mutation 을 예측하려고 하면 mutation 을 예측하는 알고리즘을 만들어야지 예측이 되겠죠. 그런데 Foundation 모델 같은 경우에는 한 번만 트레이닝 시키면 MSI 도 예측하고 뮤테이션도 예측하고 이겁니다.
00:46:11
Speaker 1
그런 개념이고요. 실제적으로 저희 데이터 셋 가지고 해봤는데, 일단 CNN 모델을 가지고 EBV classification 하는 그런 알고리즘을 만들어 봤을 때 AOC 가 0.94 정도 나왔고 MSI 를 트레이닝 시킨 모델은 0.827 정도 나왔어요 그러면 이제 Gastric Cancer 거든요 파운데이션 모델로 돌려 봤을 때 유니 모델로 우니 모델로 돌려 봤을 때 EBV 는 0.988, 오히려 CNN 보다 더 높죠.
00:46:42
Speaker 1
그 다음에 MSI 도 0.898, CNN 보다 높습니다. 그래서 하나의 모델로 돌리면서 이렇게 예측력은 좀 더 좋아질 수 있는 그런 방법이 요새 이제 각광을 받은 파운데이션 모델입니다. 그래서 이제 격리 이미지를 가지고 많은 파운데이션 모델이 나와 있고요. 시트레스 펜스라든지, Vershow 라든지, Chief 라든지, 기가베이스 이런 Uni 라든지 많이 들어보신 분도 많을 것 같습니다.
00:47:16
Speaker 1
그래서 이제 트레이닝 데이터 보시면 1500 만 장 이상 그 다음에 몇십만 장 이상 단위가 이렇게 몇백만 장 이렇게 되겠죠. 그래서 여러 classification 하는 과제에서, Incuracy 도 높고 이렇게 좋은 데이터를 좋은 결과를 보였다. 이렇게 나타나 있습니다. 그 다음에 Multi Modal Foundation Model 이 있습니다.
00:47:46
Speaker 1
그래서 Multi Modal 이니까 이제 여러 개의 데이터셋으로 트레이닝 시켰겠죠. 이제 영리 이미지 뿐만 아니라 텍스트 이미지를 붙이거나 지너블 데이터를 붙이거나 해가지고 멀티모달로 Foundation Model 로 만든 게 요새 또 나와 있습니다. 그래서 멀티모달하게 여러가지 테스트에도 사용을 해서 좋은 결과를 만들고 있습니다. 우선 대표적으로 루니 모델 이렇게 설명을 드리면요. 그래서 한 10 만 장 이상의 분슬라이드 이미지를 가지고 트레이닝 시켰고 여러 가지 암종을 가지고 트레이닝 시켰고.
00:48:25
Speaker 1
한 34 개 이상의 테스크에 대해서 기존 테스크 CNL 로 했던 것보다 결과가 더 좋더라 이렇게 나와 있습니다. 그래서 이제 저희가 또 해봤는데요. endoscopy reception, EMR, EST 이런 걸 가지고 EGC 에서 lymphnod metastas 를 예측을 해봤습니다. 그래서 endoscopy reception 이 요새, erligastric cancer 에서 treatment modality 로 많이 사용을 하고 있잖아요.
00:48:57
Speaker 1
그런데 그것을 사용한 그 결과가 나온 다음에는 EQR scoring system 에 대해서 treatment strategy 를 가져갑니다. 그래서 새로 EST 를 다시 하거나 observation 을 하거나 surgery 로 가거나 이렇게 하잖아요. 그래서 저희가 했던 것은 6,500 개의 endoscopic recession 검체를 가지고 lymp node metassearch 를 예측을 했고요. EQLAS Scoring System 과 어느 게 좀 더 Limper Metastates 를 예측하는 데 있어서 좀 더 좋은지를 봤습니다.
00:49:32
Speaker 1
그래서 아까 말했던 MIL 모델을 기버그를 사용을 했고 여기서 이제 비처를 하는 데 있어서 인코더로 기가패스라든지 Ctrast Path, Ponch 같은 그런 파운데이션 모델을 사용을 했습니다. 그래서 이제 결과 저희 결과는, 그중에서 가장 베스트 모델인 이제 기가페스트로 돌렸을 때가 가장 결과가 높더라고 좋더라고요. 그래서 이제 그것을 결. 결과를 봤을 때 저희가 모델이 EQRA scoring system 으로 임상적으로 예측을 했던 것보다 Lifnometasis 했던 그런 예측이 좀 더 좋았다 이게 결과입니다.
00:50:13
Speaker 1
그래서 이제 이것은 이제 지금 submission 중이고요. 우선 요새는 Generalist medical AI 까지 나옵니다. 그래서 Foundation model 을 이용해서. Adiological 리포트를 만든다든지 병리 리포트를 만든다든지 그 다음에 텍스트 제너레이션을 한다든지 이런 과정까지 이렇게 나오고 있습니다. 그래서 이게 멀티 모델 나아지는 모델이거든요.
00:50:46
Speaker 1
그래서 Path Assist, Path Chat 이런 것들이 나오고 있는데요. 예를 들면 이제 이렇게 프롬프터로, 사람이 이렇게 이미지를 제너레이션해라. 그러면 L-Seal Low-Grade Schemus Extract Region L-Seal 에 대한 Low-Seal 에 대한 그런 이미지를 제너레이션해라. 그러면 패스트챗이 제너레이션을 합니다. 이렇게 그 다음에 반대로 이거에 해당하는 orphology 에 해당하는 것을 설명을 하라고 합니다.
00:51:26
Speaker 1
길게 설명을 다 해줍니다. 그리고 이제 면역염색에도 적용을 해서 면역염색을 이건 피델-1 이거든요. 그래서 피델-1 면역염색을 결과로 분석을 해라 그러면 잘 분석을 해줍니다. 그래서 이 단계까지 이렇게 랭귀지 모델까지 이렇게 나와 있다 이렇게 말씀을 드립니다. 그래서 이제 이게 이제 마지막 페이지이고요. 아까 CNN 모델 나온 것도 사실은 20 년도 21 년도 이런 때부터 이제 시작된 겁니다 그래서 최근에 한 5,6 년밖에 안 됐거든요 그 다음에 멀티 모델 나온 거는 한 22,3 년도 그 다음에 파운데이션 모델 나온 건 또 한 23,4 년도 해가지고 엄청나게 지금 발전을 하고 있습니다 그래서 최근 펜솔로지 분야에서 엄청나게 발전을 하고 있다 이렇게 보시면 될 것 같고요 그래서 이제.
00:52:23
Speaker 1
그것 중에 잘 돼서 새로운 클래스의 바이오마커로서 작동을 할 수도 있을 것 같다. 이렇게 말씀드릴 수 있고요. 그럼에도 이제 불구하고 이지슬라이드로 프로그노시스를 예측을 한다든지 그 다음에 트리트먼트 recommendation 을 예측을 한다든지 그 다음에 오폴로지와 그 다음에 지노타입, 지노타입과 지노타입을 맞춰본다든지 이런 거에 대해서는, 아직도 좀 해볼 여지가 있을 것 같습니다.
00:52:55
Speaker 1
그리고 이제 좀 전에 얘기했다시피 멀티모달 데이터셋을 이용해 가지고 멀티모달 딥러닝을 하는게 대세다 이렇게 말씀드릴 수가 있겠습니다. 여기서 이제 저희 랩 식구들이고요. 고대병원의 안상정 병리과 교수하고 저하고 코 PI 가 되어가지고 랩을 17 명 되는 그런, 연구진인 랩으로 운영을 하고 있습니다 경청해주셔서 감사합니다 감사합니다 질문이나 코멘트 있을까요?
00:53:41
Speaker 1
없으시면 이렇게 오늘 마치겠습니다 감사합니다