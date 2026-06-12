# 강의 번들: 03-31 LLM/NGS/정밀의료 바이오인포
- 교수: 의료정보학교실
- 슬라이드 PDF: ['3월 31일_대학원공개강의 (1).pdf', '3월 31일_대학원공개강의_summary.pdf']
- 비고: summary 1장


================ [SLIDE TEXT — 출제범위(C1) 닫힌 우주의 사실원] ================

--- [PAGE 1/40] 3월 31일_대학원공개강의 (1).pdf ---
Bio-big data and bioinformatics
의료정보학교실김태민

--- [PAGE 2/40] 3월 31일_대학원공개강의 (1).pdf ---


--- [PAGE 3/40] 3월 31일_대학원공개강의 (1).pdf ---
Stanford researchers reported that ChatGPT passes the test; they found that ChatGPT-
4 "passes a rigorous Turing test, diverging from average human behavior chiefly to be more 
cooperative", making it the first computer program to successfully do so.

--- [PAGE 4/40] 3월 31일_대학원공개강의 (1).pdf ---


--- [PAGE 5/40] 3월 31일_대학원공개강의 (1).pdf ---
DeepResearch achieved the ‘PhD’ level inference capability!

--- [PAGE 6/40] 3월 31일_대학원공개강의 (1).pdf ---
ChatGPT helps your coding (Lv2 AI)
(Query) I have a spatial transcriptome data 
(Visium). I am focusing two types of fibroblast 
subtypes (SFRP2+ and SFRP4+). In the VISIUM 
field (~5000 spatial spots) of a cancer, there are 
two distinct regions that are separated from each 
other, one regions with dominant SFRP2+ 
fibroblasts and the other regions with dominant 
SFRP4+ fibroblasts. Is it possible to apply or 
measure an spatial index for each spot in the field 
to represent the transition of SFRP2+ to SFRP4+? 
For example, a spot located in the middle of two 
regions will have an index value of 0.5 while those 
spots close to SFRP2+ dominant regions will have 
value close to 0 (those close to SFRP4+ dominant 
regions will have value close to 1). Can you 
suggest such spatial index and how to calculate? 
### --------- 1. Data Setup ---------
# Assume:
# data: a data frame with 5000 spots and columns "X" and "Y" for coordinates.
# sfrp2_scores: numeric vector of SFRP2+ scores (length = 5000)
# sfrp4_scores: numeric vector of SFRP4+ scores (length = 5000)
# For demonstration, here's how you might simulate such data:
# (Remove or replace this simulation with your actual data.)
set.seed(123)
n_spots <- 5000
data <- data.frame(X = runif(n_spots, 0, 100),
Y = runif(n_spots, 0, 100))
sfrp2_scores <- runif(n_spots)
sfrp4_scores <- runif(n_spots)
# Identify the indices of the 100 spots with the highest scores in each group.
sfrp2_indices <- order(sfrp2_scores, decreasing = TRUE)[1:100]
sfrp4_indices <- order(sfrp4_scores, decreasing = TRUE)[1:100]
### --------- 2. Build the Affinity Matrix ---------
# Use the spatial coordinates (X, Y)
coords <- as.matrix(data[, c("X", "Y")])
# Compute the full pairwise Euclidean distance matrix.
dist_mat <- as.matrix(dist(coords))
# Choose a kernel bandwidth sigma.
# Here, we use the median distance as a simple choice.
sigma <- median(dist_mat)
# Compute the Gaussian (RBF) kernel similarity matrix.
W_full <- exp(- (dist_mat^2) / (sigma^2))
# Optionally, restrict to k-nearest neighbors (to sparsify the graph).
k <- 10  # number of nearest neighbors to keep for each spot
W <- matrix(0, nrow = n_spots, ncol = n_spots)
for (i in 1:n_spots) {
# Get indices of the k nearest neighbors (exclude self by taking indices 2:(k+1))
neighbors <- order(dist_mat[i, ])[2:(k+1)]
W[i, neighbors] <- W_full[i, neighbors]
}
# Symmetrize the matrix to ensure it is undirected.
W <- (W + t(W)) / 2
### --------- 3. Normalize to Create the Diffusion Operator ---------
# Compute the degree matrix.
D <- diag(rowSums(W))
# Compute D^(-1/2)
D_inv_sqrt <- diag(1 / sqrt(diag(D)))
# Construct the symmetric normalized affinity matrix (often called the diffusion operator).
L <- D_inv_sqrt %*% W %*% D_inv_sqrt
### --------- 4. Compute Diffusion Map Coordinates ---------
# Perform eigen decomposition on L.
eig <- eigen(L)
# The first eigenvalue should be 1 (trivial constant eigenvector).
# Choose a number of components (excluding the first trivial one).
n_comp <- 10
# Extract eigenvalues and eigenvectors (from 2nd to n_comp+1).
lambda <- eig$values[2:(n_comp+1)]
V <- eig$vectors[, 2:(n_comp+1)]
# Compute the diffusion coordinates by scaling each eigenvector by its eigenvalue.
# Each row now represents the diffusion coordinates for a spot.
diffusion_coords <- t(t(V) * lambda)
### --------- 5. Compute "Diffusion Pseudotime" Relative to Two Groups ---------
# For each spot, compute the average Euclidean distance (in diffusion space)
# to the spots in each endpoint group.
dpt_sfrp2 <- numeric(n_spots)
dpt_sfrp4 <- numeric(n_spots)
for (i in 1:n_spots) {
# Distances in diffusion space from spot i to each spot in the SFRP2+ group.
dists2 <- sqrt(rowSums((diffusion_coords[i, , drop = FALSE] - diffusion_coords[sfrp2_indices, ])^2))
dpt_sfrp2[i] <- mean(dists2)
# Distances in diffusion space from spot i to each spot in the SFRP4+ group.
dists4 <- sqrt(rowSums((diffusion_coords[i, , drop = FALSE] - diffusion_coords[sfrp4_indices, ])^2))
dpt_sfrp4[i] <- mean(dists4)
}
# Combine the two distances into a single spatial index.
# A spot close to SFRP2+ (small dpt_sfrp2) will yield an index near 0,
# while a spot close to SFRP4+ (small dpt_sfrp4) will yield an index near 1.
spatial_index <- dpt_sfrp2 / (dpt_sfrp2 + dpt_sfrp4)
# Optionally, re-scale the spatial_index to exactly range between 0 and 1.
spatial_index <- (spatial_index - min(spatial_index)) / (max(spatial_index) - min(spatial_index))
### --------- 6. Visualization ---------
# Plot the diffusion map (first two diffusion coordinates) colored by the spatial index.
plot(diffusion_coords[,1], diffusion_coords[,2], 
col = heat.colors(n_spots)[rank(spatial_index)],
pch = 16, xlab = "Diffusion Component 1", ylab = "Diffusion Component 2",
main = "Diffusion Map Colored by Spatial Index")
colorbar <- function(col) image(1, seq_along(col), matrix(seq_along(col), nrow=1), col=col, 
xlab="", ylab="", xaxt="n", yaxt="n", main="Color scale")
colorbar(heat.colors(100))
# Also, overlay the spatial index on the original tissue coordinates.
plot(coords[,1], coords[,2], 
col = heat.colors(n_spots)[rank(spatial_index)], pch = 16,
xlab = "X Coordinate", ylab = "Y Coordinate",
main = "Tissue Coordinates Colored by Spatial Index")

--- [PAGE 7/40] 3월 31일_대학원공개강의 (1).pdf ---
“Context’ matters
“인간이병목돼버렸다”…AI에
휘둘리는‘클로드블루’ 확산
-
AI과제keyword
-
Central dogma AI
-
Virtual cell 
-
Self-driving lab

--- [PAGE 8/40] 3월 31일_대학원공개강의 (1).pdf ---
‘Genomic big data’
‘What context’ matters in big-data of healthcare?

--- [PAGE 9/40] 3월 31일_대학원공개강의 (1).pdf ---
Context #1. Genomic big data with NGS

--- [PAGE 10/40] 3월 31일_대학원공개강의 (1).pdf ---
Why is the genomic data so BIG?
A genome of a single individual has ~3,000,000,000 letters 
(letter = nucleotide – per haploid genome)

--- [PAGE 11/40] 3월 31일_대학원공개강의 (1).pdf ---
Sequencing Cost for 
WGS – 1000$ per 
Genome
~13 years
~3,000,000,000$
International HGP project
~2 days
~1,000$
Desktop 
sequencer
X
Illumina X10
Next-generation sequencing
(=massively paralleled, high-
throughput sequencing)

--- [PAGE 12/40] 3월 31일_대학원공개강의 (1).pdf ---
To sequence a 
person’s genome:
$3,000,000 (2000)
$1,000 (2015)
$100 (2022, Jun)

--- [PAGE 13/40] 3월 31일_대학원공개강의 (1).pdf ---


--- [PAGE 14/40] 3월 31일_대학원공개강의 (1).pdf ---
Original book = 
Genome
Sequencing data
NGS (next-generation 
sequencing) = massively 
paralleled sequencing 
(of short reads)

--- [PAGE 15/40] 3월 31일_대학원공개강의 (1).pdf ---
How to map ‘short reads’ onto the genome
Burrows-Wheeler algorithm:
- The fastest algorithm
- Requires <3Gb memory
- Using ‘zipping’ techniques

--- [PAGE 16/40] 3월 31일_대학원공개강의 (1).pdf ---


--- [PAGE 17/40] 3월 31일_대학원공개강의 (1).pdf ---
Context #2. Precision medicine (worldwide)

--- [PAGE 18/40] 3월 31일_대학원공개강의 (1).pdf ---
맞춤의학(‘personalized medicine’) –
‘Right Drug for Right Patient’
•
Personalized medicine (=tailored medicine, 맞춤의학)
•
Precision medicine (정밀의학)
•
Companion diagnostics (동반진단)
•
Targeted therapy (타겟치료)

--- [PAGE 19/40] 3월 31일_대학원공개강의 (1).pdf ---
Nature 520:609, 2015
IMPRECISION 
MEDICINE 
…For every person 
they do help (blue), the 
ten highest-grossing 
drugs in the United 
States fail to improve 
the conditions of 
between 3 and 24 
people (red)…

--- [PAGE 20/40] 3월 31일_대학원공개강의 (1).pdf ---
Personalized to Precision medicine –
“Paradigm shift”

--- [PAGE 21/40] 3월 31일_대학원공개강의 (1).pdf ---
One-size doesn’t fit all!

--- [PAGE 22/40] 3월 31일_대학원공개강의 (1).pdf ---
Personalized to ‘Precision medicine’ – What is it?
ih.gov/sites/default/files/research-training/initiatives/pmi/pmi-infographic.pdf

--- [PAGE 23/40] 3월 31일_대학원공개강의 (1).pdf ---
• President Obama has specifically requested a $215 
million investment, which was included in today’s 
budget proposal. Funds will be spread among the 
NIH—including $70 million to the NCI —the U.S. FDA, 
and the Office of the National Coordinator for Health 
Information Technology (ONC).

--- [PAGE 24/40] 3월 31일_대학원공개강의 (1).pdf ---
A national research cohort of one million or more U.S. participants
•
Nation-wide규모의cohort
•
정상인(volunteer) 100만명
•
의료정보+ 유전정보
•
Prospective follow-up
Research based upon the cohort data will: 
• Advance pharmacogenomics, the right drug for the right patient at the right dose 
• Identify new targets for treatment and prevention 
• Test whether mobile devices can encourage healthy behaviors 
• Lay scientific foundation for precision medicine for many diseases

--- [PAGE 25/40] 3월 31일_대학원공개강의 (1).pdf ---
Precision medicine –
“Why now?”
“Genotype-big data확보와분석이가능해짐”

--- [PAGE 26/40] 3월 31일_대학원공개강의 (1).pdf ---
World-wide big-data and trends

--- [PAGE 27/40] 3월 31일_대학원공개강의 (1).pdf ---
우리나라는?

--- [PAGE 28/40] 3월 31일_대학원공개강의 (1).pdf ---
Bio big data to precision medicine (accelerated by AI)

--- [PAGE 29/40] 3월 31일_대학원공개강의 (1).pdf ---
Context #3. Genomics + Precision medicine

--- [PAGE 30/40] 3월 31일_대학원공개강의 (1).pdf ---
Angelina Jolie’s effect
“Do I need a genetic test?”
One example (BRCA1/2) among 22,000 genes in the human genomes….

--- [PAGE 31/40] 3월 31일_대학원공개강의 (1).pdf ---
Whole genome (3,000,000,000 = 3 billion 
bp/nucleotides/letters) as 1D array
Chr17
BRCA1
“Perfect example of
phenotype (breast 
cancers) and genotype 
(BRCA1/2 mutations) 
relationship!”

--- [PAGE 32/40] 3월 31일_대학원공개강의 (1).pdf ---
…… Understanding human disease requires comprehensive interpretation of the genome, 
including characterization of the impact of any variant on gene function and regulation. 
Broadly, this means that for any letter change in DNA, we must precisely identify its effects on 
biochemical properties such as protein structure, splicing and levels of expression, and then 
interpret these effects in terms of their phenotypic consequences. 
(Olga G. Troyanskaya, “Decoding disease: from genomes to networks to phenotypes”, Nature 
Reviews Genetics. 2021 Aug 2.)
Ultimate goal of 
human genetics 
(and precision 
medicine)?

--- [PAGE 33/40] 3월 31일_대학원공개강의 (1).pdf ---
SNP (single nucleotide polymorphism)
Genomic difference between two individuals?
~0.1% of total genome (2-3 millions geno-wide)

--- [PAGE 34/40] 3월 31일_대학원공개강의 (1).pdf ---
Ultimate goal of human/medical genetics?
= “Genotype-based prediction of phenotypes”
“Genotyping”
“Interpretation”

--- [PAGE 35/40] 3월 31일_대학원공개강의 (1).pdf ---
Genetic tests that are marketed 
directly to consumers without the 
involvement of a health care provider 
are called direct-to-consumer tests 
(also referred to as DTC). 
국내DTC 유전자검사의제도적도입>
2015년12월9일「생명윤리및안전에관한법률」의
개정에따라질병의예방과관련된12가지항목에
대해소비자들이비의료기관을통해직접유전자
검사를받을수있는DTC 유전자검사제도가
도입되었습니다. (12가지항목: 체질량지수, 
중성지방농도, 콜레스테롤, 혈당, 혈압, 색소침착, 
탈모, 모발굵기, 피부노화, 피부탄력, 비타민C농도, 
카페인대사). 
Today’ 
special 
recommend
ation!

--- [PAGE 36/40] 3월 31일_대학원공개강의 (1).pdf ---
21 & me – DCT (Direct-to-Consumer Tests)

--- [PAGE 37/40] 3월 31일_대학원공개강의 (1).pdf ---
Genome-wide association study (GWAS)

--- [PAGE 38/40] 3월 31일_대학원공개강의 (1).pdf ---
Backs of the arrowheads show pre-test probabilities and arrows point in the direction of change in 
probability. Blue lines show lowered post-test probabilities, and red increased post-test probabilities

--- [PAGE 39/40] 3월 31일_대학원공개강의 (1).pdf ---
유전체해독의3단계
(1) Sequencing nucleotides (or
base pairs)
(2) Annotate 
(3) (functional) Interpret
How to read the genome (= sequencing)?

--- [PAGE 40/40] 3월 31일_대학원공개강의 (1).pdf ---
Summary
•
AI/LLMs are becoming practical tools for biomedical research, coding, 
and bio-big data analysis, but their usefulness depends on the right 
context.
•
Genomic data are massive: one human genome has about 3 billion 
base pairs, and NGS enabled massively parallel short-read sequencing.
•
Whole-genome sequencing has become dramatically faster and 
cheaper, making large-scale genomic analysis and precision medicine 
feasible.
•
Precision medicine moves beyond a one-size-fits-all approach toward 
the right drug, for the right patient, at the right dose.
•
Global initiatives combine genomic, clinical, and cohort data to improve 
prevention, diagnosis, treatment, and pharmacogenomics.
•
A central goal of human genetics is genotype-based prediction of 
phenotype through sequencing, annotation, and functional interpretation.
•
AI can accelerate the management and interpretation of genomic big 
data and help translate bioinformatics into real-world precision medicine.


--- [PAGE 1/1] 3월 31일_대학원공개강의_summary.pdf ---
Summary
•
AI/LLMs are becoming practical tools for biomedical research, coding, 
and bio-big data analysis, but their usefulness depends on the right 
context.
•
Genomic data are massive: one human genome has about 3 billion 
base pairs, and NGS enabled massively parallel short-read sequencing.
•
Whole-genome sequencing has become dramatically faster and 
cheaper, making large-scale genomic analysis and precision medicine 
feasible.
•
Precision medicine moves beyond a one-size-fits-all approach toward 
the right drug, for the right patient, at the right dose.
•
Global initiatives combine genomic, clinical, and cohort data to improve 
prevention, diagnosis, treatment, and pharmacogenomics.
•
A central goal of human genetics is genotype-based prediction of 
phenotype through sequencing, annotation, and functional interpretation.
•
AI can accelerate the management and interpretation of genomic big 
data and help translate bioinformatics into real-world precision medicine.



================ [DRAFT 분석(초안) — 토픽맵/가중치/모범답안 사실원] ================

260331_슬라이드 1장 + 스크립트 기반 예상 문제
슬라이드 bullet 7개를 출제 단위로 삼되, 스크립트에서 강조된 내용을 모범답안 논리로 활용합니다.

Q1. [개념 설명형]
NGS(Next-Generation Sequencing)가 등장하기 전과 후의 전장유전체 시퀀싱 비용 변화를 설명하고, 이것이 Precision Medicine 추진에 어떤 의의를 가지는지 서술하시오.
[모범 답안] Human Genome Project(1990~2000)는 국제 컨소시엄이 10년에 걸쳐 수십억 달러를 투입해 1인의 유전체를 해독했다. 2007년 NGS 등장 이후 비용은 급격히 하락하여 2015년경 약 $1,000/genome 수준에 도달했다. 이는 대규모 코호트(예: All of Us 100만 명, UK Biobank 50만 명)의 개인별 전장유전체 시퀀싱을 현실화시켰고, 유전체 정보를 EMR 등 임상 데이터와 결합한 Precision Medicine 이니셔티브의 기술적 토대가 되었다.

Q2. [비교·적용형]
Genotyping과 Phenotype prediction을 구분하고, 현재 Precision Medicine에서 전자는 가능하나 후자가 여전히 제한적인 이유를 설명하시오.
[모범 답안] Genotyping은 NGS를 통해 개인의 30억 염기쌍을 수일 내 $100~$1,000 수준으로 해독하는 것으로, 현재 기술적으로 충분히 구현된다. 반면 Phenotype prediction은 해독된 서열을 바탕으로 개인의 질환 발생·약물 반응 등을 예측하는 것으로, BRCA1/2처럼 일부 단일 유전자 질환에서는 가능하지만, 대부분의 복잡 질환은 수많은 SNP의 복합 효과(다유전자적 특성)와 환경 인자가 관여하기 때문에 해석에 필요한 population-level evidence가 아직 부족하다. 이를 해결하기 위해 대규모 코호트 데이터 축적과 Polygenic Risk Score(PRS) 방법론이 연구되고 있다.

Q3. [기전 설명형]
NGS 데이터의 특성과, 이를 처리하기 위한 sequence alignment의 필요성을 설명하시오.
[모범 답안] NGS는 전장유전체를 짧은 단편(short read)으로 파편화하여 병렬 시퀀싱하는 방식이다. 결과물은 수억 개의 무작위 단편 서열이며, 이 자체로는 생물학적 의미를 갖지 못한다. 따라서 이 단편들을 참조 유전체(reference genome)에 정렬(alignment)하여 원래의 서열 정보를 재구성하는 과정이 필수적이다. BWA(Burrows-Wheeler Aligner)가 표준 도구로 사용되며, 이는 데이터 압축 알고리즘에서 차용된 방법으로 대용량 서열 데이터를 효율적으로 처리한다.

Q4. [개념 적용형]
DTC(Direct-to-Consumer) 유전자 검사의 개념을 설명하고, 현재 임상적 활용이 제한되는 이유를 논하시오.
[모범 답안] DTC 검사는 의료진이나 유전상담사를 거치지 않고 소비자가 직접 회사에 검체(예: 구강 스왑)를 보내 유전 정보를 제공받는 방식이다. 일부 형질(눈 색깔, 음주 후 홍조 등)과 질환 위험도 정보를 제공하지만, 현재 임상 적용이 제한적인 이유는 대부분의 유전 변이와 표현형 간 연관성에 대한 population-level evidence가 충분하지 않기 때문이다. 즉 genotyping 자체는 가능하나, 그 해석의 근거(유전형-표현형 데이터베이스)가 아직 부족하여 임상 결정에 활용하기 어렵다.

Q5. [통합 서술형 — 고난도]
"Genomic big data 시대에 AI/LLM이 Precision Medicine 구현에 기여할 수 있는 방향을 논하시오."
[모범 답안] Precision Medicine의 궁극 목표는 개인의 유전형(genotype)을 해독하여 표현형(phenotype) 및 최적 치료 전략을 예측하는 것이다. 현재 genotyping은 NGS를 통해 기술적으로 가능하나, 30억 염기쌍과 2만여 유전자의 임상적 해석은 대규모 데이터의 통합 분석을 요구한다. AI/LLM은 ① 대용량 유전체-임상 데이터의 패턴 인식 및 annotation, ② 이기종(multimodal) 데이터(유전체, EMR, 영상 등) 통합 해석, ③ 연구자의 가설 수립과 코딩 작업 보조 등을 통해 이 과정을 가속화할 수 있다. 단, AI의 성능은 연구자가 제공하는 context(전문적 질문과 배경 지식)의 질에 의존하므로, 연구자 고유의 도메인 지식이 여전히 핵심이다.

시험 대비 한 줄 요약:
이 강의의 핵심 서사는 "NGS → 비용 감소 → 대규모 코호트 → Genotyping은 됨 → 해석(Phenotype prediction)이 숙제 → AI가 도울 수 있음" 이 하나의 흐름입니다. 이 논리 구조를 서술할 수 있으면 어떤 형태의 문제가 나와도 대응 가능합니다.

================ [RECORDING 녹음본 — 교수 오피셜 발화(해설/강조신호 사실원) | file: 03-31 강의 LLM, NGS, 정밀의료와 바이오인포매틱스 해.txt] ================

03-31 강의: LLM, NGS, 정밀의료와 바이오인포매틱스 해석 혁신

00:00:16
Speaker 1
1시간 정도 지켜달라고 하셔서, 1시간 수리하기 위해서, 여러 분야 교수님들이 이렇게 1시간씩 가보시죠 저는 이제, 인포마틱스 사실 1시간 동안 많은 얘기를 하는 것도 곤란하고.
00:00:47
Speaker 1
인포마틱스나, 바이오인포마틱스 메디컬인포마틱스, 인공지능, 지너믹스나 그러한 부분에 대해서, 저는 전문적인 지식을 들으시면 그 해당 강의를 들으셔야죠. 그래서 벌써 2년이 지났는데 아직도 사람들이 얘기를 합니다. 너무 유명하죠. 노벨상의 두 필드를 휩쓴 그게 2024년이고.
00:01:20
Speaker 1
저희가 각 필드에서 이런 부분을 다 사용하고 계시는 분도 있고 아직은 좀 관심이 나죠. 이런 부분이 너무나 빨리 발전을 하고 있는데 당장 자기가 생각해볼 때는 계시는 분이 다 리서치를 하고 계시니까 다 진학을 하고 계시고 리서치를 하고 계세요. 이런 부분들을 어떻게 좀 논문 쓰기 리서치라고 이용을 할 수 있을까.
00:01:52
Speaker 1
그런 걸 생각을 좀 해보는데, 굉장히 작년에 딱 이 시기에 했던 것 같은데, 장난이야기에요. 여기 보면은 이거 제가 쓴 건 아니고 제가 캡쳐를 해가지고 근데 대충 아시겠죠? 그쵸? CHPT가 2가 유치원, 3이 초딩, 4가 고등학생, 이때 작년에 딥리서치 그런 개념이 처음 나왔는데 그런 개념이 나오면서 PhD레벨의 박사수준의 인텔리전스에 도달했다 그런 얘기를 합니다.
00:02:25
Speaker 1
사실 우리가 인공지능이 진짜 이게 인공지능이냐 아니냐고 튜링 테스트라고 되게 유명한 게 있어요. 이렇게 대화를 해서 얘가 사람인지 아닌지 구분이 안되면 그게 인공지능이다라고, 50년대 튜링이라는 사람이 얘기를 하는데 사실 GPT-2에서 그 테스트를 통과를 했거든요. 2만 돼도 사실 얘가 사람인가 인공지능인가 이제 컴퓨터가 구분을 못할 정도니까, 이게 벌써 1년 전 얘기니까 몇 개월, 1년 사이에 엄청난 발전을 하고 있는 건 맞습니다.
00:02:58
Speaker 1
그리고 지금 쓰고 있는 LLM 여러분이 다 average person의 intelligence는 넘었다, 그건 확실하다고 얘기를 하고 있죠. 문제는 이제 범용인공이 언제 등장을 할 것인가, 그리고 당장 우리한테 떠오르는 게 내가 논문을 쓰고 졸업을 해야 되는데 어떤 모델을 어떻게 이용해야 되는가에 빠지게 되죠. 이거를 세계가 가장 유명하잖아요. 지금 당장.
00:03:30
Speaker 1
234 얘기하고 있었는데, 지금 GPT 5.4 얘기하고 있고, 클로드가 너무 유명해졌고, 그리고 제미나이. 업체력도 지나갑니다. 그리고 여러 개를 다 써본 사람들이 장단점을 다 얘기를 해요. 어떤거 쓰세요? 채찍피트는 여기 있습니다. 범용적이죠. 캡처한 건데 일반적으로 아주 범용적인 모델이죠. 클로드는 여기 딱 적어놨네요. 코딩의 최강이다. 그렇게 얘기를 하고 있고 재미나에는 특성이 없는 것 같은데 사실은 구글이 오랫동안 주기 때문에.
00:04:03
Speaker 1
멀티모델에 강하고 최종적으로 구글 쪽으로 가지 않을까 사람들이 예상을 하고 있는데 아직까지는 이중에서 맞는 모델을 써서 여러분들의 리서치를 보강하는 방향으로 하는 게 지금 당장은 최선의 방법이라고 생각합니다. 작년에 했던 걸 또 나왔죠. 작년에 채찍피트 4, 5 안 해가지고 딥리서치 그런 게 처음 나왔어요. 드디어 이제 필진하게.
00:04:33
Speaker 1
이제야 좀 쓸만하다 사실 이게 에버리징 레벨의 person 이다 그러면 일단 대화 밖에는 안된다, 근데 각 전문적인 분야에서 이제 phd 정도의 지식을 공유할 수 있게 우리가 어떤 리서치를 하든 어떤 이태리젼트한 어떤 behavior 에서 실제적으로 도움이 된게 작년 초 작년 중반부터 그래서 작년에 레벨을 1,2모로 이제는 막 안쓰면 없어요 제가 왜 이런 얘기를 바이오인포메틱스에서 하면 바이오인포메틱스가 정의가 무엇인가 보면 예전에 그거부터 얘기를 했었는데 컴퓨테이셔널 바이오 로지가 이퀄 바이오인포메틱스다.
00:05:12
Speaker 1
그런 얘기를 하고 결국 바이오인포메틱스라는 컴퓨테이션과 관련해서 작업을 해야되는데 가장 큰 버틀렉이 있죠 코딩을 해야되다 말이든 파이썬이든 코딩을 해야된다는 문제가 있고 그 버틀렉에서 대부분 다 갈라집니다 하시는 분 안하시는 분은 갈라지면서, 할 수 있는 사항이 있어요 그렇습니다, 근데 이제 그게 완전히 멈춰졌죠. 완전히 멈춰졌죠. 코딩이라고 하는 거를 이제는 뭐 LLM이 원하는 대로 다 해주기 때문에, 물론 코딩을 알고 있는 사람, 보는 사람하고는.
00:05:44
Speaker 1
차이가 좀 있을 수는 있지만, 예전엔 포즈를 불가능할 것 같다는 예, 바로 이거예요. 아까 전 슬라이드에서도 넘어가진 않는데 그냥 단순한 대화를 하는 수준으로 넘어서 이제 각 전문력의 코딩이다. 코딩에서도 이제 PhD 레벨의 성능을 가지고 있기 때문에, 이렇게 나를 비서처럼 불려서, 바이올리포르틱스라고 하는 것도 저는 뭐 코딩을 이한테 시켜서 이제 충분히 진행을 할 수 있는 그런 작업이 되었습니다. 세상이 막 1년 사이에 완전히 바뀌어 버렸죠. 오늘 이건 재미로 보시면 돼요.
00:06:16
Speaker 1
가장 최근에 나온 게 이제 인기만 아시죠? 강상윤 작가가 이제 성함을 적으려고 쇼에 나왔어요. LLM이라고 얘기를 하는데, 이분이 얘기하는 건 그거죠. 모든 사람들이 얘기하는 게 조금씩 다르지만 다 비슷합니다. 자기의 콘텐츠가 있어야 쓸 수 있다 자기의 콘텐츠가 없고, 이제 LLM의 PHD레벨 수준을 쓰려고 하지 않으면 그건 그냥 챗, 일반 Average person과의 그냥 챗 수준에 지나지 않기 때문에.
00:06:52
Speaker 1
우리가 실제 활용을 하려면 PHD를 Recruit 할 수 있는 그 정도의 질문을 주어야 한다 그래서 결국 이거 제가 한번 봤는데 결국 핵심은 콘텐츠를 가지고 있어야 한다 자기의 콘텐츠, 저는 이제 컨텍스트라고 생각하는데, 컨텍스트가 있어야 한다, 읽기만 하면 정말 파워풀해진다는 거죠 박사학위 10명, 펜쿠크 이상 이제 이게 결국 핵심이잖아요 전문적인, 내가 어떤 핵심적인 콘텐츠를 가지고 있는데.
00:07:23
Speaker 1
Interdisciplinary Work을 하잖아요 내가 통계학을 잘 모를 수도 있고 코딩이 필요할 수도 있고 다른 전문적인 그런 각 부분에, 박사들로서 쓸 수 있는 그게 가장 현재로서 가장 현명한 방법이 아니라고 생각을 하고, 최근에 논문이 나왔죠. 최근 논문이 아닌데요. 근데 퍼블리시가 2016년 4월이니까 최근 만들었죠. 작년에 이게 엔드 투 엔드 진짜 퓨리 인공지능을 쓴 논문이 작년에.
00:08:00
Speaker 1
협의가 돼서 나왔지만 작년에 완전한 엔드 투 엔드 논문이 올해 초에 나왔고 그런 거 많이 하잖아요. 각 분야에서 수술하시는 분은 로보틱스 각 분야에서 하고 리서치하는 사람들은 이 엔드 투 엔드 리서치라고 하는 게 가능할 것이라고 수많은 모델이 있습니다. 정말 수많은 모델이. 이런 얘기가 있는데 사실 이거는 조금 이제, 당장 받아들이기는 조금 곤란하다 그런 얘기하잖아요.
00:08:30
Speaker 1
천 번 돌려가지고 한 번 나온 거를 당장 얘기하기만 하고, 제가 사실 업데이트를 못했는데 최근에 하버드 물리학 교수가. 기초 물리, 이론 물리를 클로드를 가지고 쓴 그런 게 있는데 나중에 한번 찾아보세요 그게 현재 리서처가 그 사람의 인공지능도 실제 하시고 진짜 어떻게 클로드라고 하는 거를 재미나게 같이 묶어서 써야 되는지 그런 개념에 대해서 잘 알고 계신데, 실제 그 이론 물리라고 하는 걸 보통 한 1년 정도, 2주 정도에 썼다가.
00:09:05
Speaker 1
뭐 당연한 거 같잖아요 근데 실제 그 패트폴이 뭐고 어떤 식으로 트러닝하고 뭐 말하들 때 어떻게 칠 것인가 그런 부분에 대해서 좀 자세히 적은 물리학에 있어서 나중에 한번 찾아보시면 좋겠습니다, 그래서 이제 컨텍스트라고 하는 건 맨날이잖아요 맨날 그래서 최근에 하나 하는 얘기가, 질문에 따라서 정해지기 때문에 질문을 너무 하지 말라고 컨텍스트만 줘라구 엔드 투 엔드로 가는데 뭐를 하든 컨텍스트를 줘라구.
00:09:37
Speaker 1
너무 이렇게 쿼리를 자꾸 제한을 주려고 하면, 그 자체가 병력이다라구, 그래서 뭐 지금 당장은 여러분 리서치에서 이런 모델들을 써서, 현명한 진짜 박사학위 10명한테 하는 그런 작업을 할 수 있는, 그런 능력을 키우고 이상한 부분을 활용하는 게 중요하지 않을까, 얘가 결국 모든 거를 진짜 엔드 투 엔드가 완벽하게 쓰였는데만 정말 그런 것도 필요 없어질 수 있는, 당장은 여러분들 자체가 그런 컨텍스트를 가지고.
00:10:11
Speaker 1
이거를 이제 학습을 하셔야 되겠고, 그런 부분에 맞춰서 학도 뭐 장망하게 쓰던, 올해 AM, VI 같은 거 썼는데, 올해 AI 과정에서는 센트럴 도구만 있고 버추얼셀 있고 그리고 자율실험실을 했죠. 셀프스라이딩을 해서 어떻게 진행될지 모르겠어요. 여튼 지금 당장 공부하시는 여러분들 입장에서는 여러분들만의 컨텍스트를 가져야 되죠.
00:10:41
Speaker 1
그런 측면에서 조금 남은 시간을 좀 가져볼까요. 저는 빅데이터, 바이오 데이터, 헬스케어에서 여러 종류의 데이터가 있죠. 헬스케어에서 정말 더러운 헬스케어가 포괄할 수 있는 게 환자의 여러 정보들을 다 모아서 멀티모달을 개념해서 총합을 하는데.
00:11:11
Speaker 1
그래도 의외로 목적은 단순해요. 환자들에게 도움을 줄 수 있는 파이딩을 찾아야 합니다. 근데 문제가 지금 데이터가 너무 부족해졌기 때문에, 어떤 부분의 데이터를 어떻게 멀티모델 할까 인공지능에 연결해주면 다 떼어넣어가지고 일단 보자 그런 계정이지만 그래서 오늘 저는 바이오인포메틱스를 사용했기 때문에 그래도 공통으로 보여지는 그런 게 있어요 공통으로 보여지는 게 여기 DNA 있죠 저는 DNA 아니면 오믹스 기반의 인포메틱스를 하고 있기 때문에.
00:11:44
Speaker 1
여기서 지너믹 빅데이터라고 해서 간단하게 설명을 좀. 그래서 이제 지너믹 빅데이터라고 하는 거를 말씀을 드리려면, 이제 최신 기술과 관련해서는 사실 최신 기술은 아니에요 제가 말씀드려야 되는 게 시퀀싱과 관련한 일을 하고 계시는 분들은 잘 알고 계시겠지만 이제 NGS, 차세대 시퀀싱에 대한 얘기를 해야 되는데.
00:12:15
Speaker 1
이게 사실은 이 NGS라고 하는 기술이 2007년에 나왔기 때문에 벌써 20년 다 되어가는 목적이죠. 지금 뭐 우리가 하고 있는 여러 완전히 다 들어왔어. NGS를 통해서 여러모로 흐름을 했었을 거에요. 실제 그 이런 인포마틱스 하시는 분들 중에 NGS 데이터를 로데이터 하시는 분이 의외로 그렇게 많지 않거든요. 여기 왜 그냥 잠깐 NGS라고 하는 게 무엇이고 기본 구조가 무엇이라고 알고 계시면 컨텍스트 찾는 컨텍스트가 도움이 되지 않을까라고.
00:12:52
Speaker 1
그래서 이제 조금 거슬러 가면 2007년보다 조금 더 거슬러 올라가면 이제 우리가 Human Genome Project이라고 하는 게 있었죠. Human Genome Project이 한 사람 가지고 있는 지넘을 풀 시퀀싱을 했어야죠. 그걸 대중의 커뮤니티에 공개하는 그런 목적이었는데, 이게 이제 3 빌리언 레터라고 하는 거를 읽어야 되는 그런 목적이 있었죠 그래서 이제 휴먼저널 프로젝트가 완료가 되고, 문제는 이제 그 당시 휴먼저널 프로젝트에 잠깐만 거슬러 올라가 보면.
00:13:25
Speaker 1
그게 이제 1990년에 시작해서 이제 2000년에 끝난 프로젝트 딱 10년 걸렸죠 그죠? 이제 인터내셔널 프로젝트인데, 돈을 너무 많이 썼어요 왜냐하면 이제 그때는 시퀀싱 기술이라고 하는 게 아주 올드했고, 로스로프시죠? 예, 2000년에 시퀀싱 하시던 거 기억도 못 나시죠? 예전에 ABRM 머신이라고 해서 정말 큰 머신이 있는데, 하루 고안에 돌아서 들어가 있는 그 캐필러리 하나가 하루 종일 돌려서 한 500베이스, 500자 있거든.
00:13:57
Speaker 1
그거 생각해 보세요 3 빌리언 베이스페어로 읽어야 되는데 기계가 막 하루 종일 돌아서 500베이스를 이렇게 읽어요, 그러니까 이게 언제 읽을까 그런 생각을 하게 돼서 결국 인터내셔널하게 팀이 모여서 10년을 구매하면 주구장창 글을 보내가지고 한 사람의 진엄을 다 읽어냈죠. 그런데 그 두 개로 읽으면 돈이 너무 많이 든다는 거죠. 그래서 프랙티컬한 솔루션이 좀 필요하다 그래서 2007년에 NGS라는 기술이 등장을 했는데.
00:14:27
Speaker 1
여기 나온 그림은 한 사람의 진엄을 시퀀싱하는 가격이, 한 사람의 진엄을 시퀀싱하는 가격이 2000년 휴먼 전원 프로젝트의 거의 로스케일이었는데 그게 계속 떨어지다가 갑자기 드라마틱하게 떨어지는데 이 시점이 NGS라는 기술이 등장하고 그래서 NGS라는 건 사실 자세히 설명합니다. 우리가 한 500베이스 정도 읽는다. 그거를 칩 위에다가 촘촘하게 붙여가지고 하이솔프스로 읽을 수 있는 그런 기술이다라고 생각을 하시면 됩니다.
00:15:01
Speaker 1
그래서 그 기술이 나오면 가격이 엄청나겠다. 그래서 그 기술이 나오면 가격이 엄청나게 떨어지다가, 쭉쭉쭉쭉 내려가다가 여기서 잠깐 정체가 되는 거예요. 여기서 잠깐 정체가 되는 포인트의 가격이 얼마죠? 한 사람의 지넘을 잇는 데 한 천 달러 정도. 이게 한 2015년이에요. 그래서 NGS라고 하는데 가격을 어마어마하게 떨어뜨려서 여기 보시면은 매니아가 아니고 오버스케어리입니다. 진짜 어마어마하게 떨어뜨려서 엄청난 가격에 인디비주얼을 쓴 가격을 한 달러 수준까지 줬다.
00:15:33
Speaker 1
그래서 천 달러가 되면 누구나 다 해볼 수 있잖아요. 인디비주얼 지넘 시퀀스라고 하는 게 2015년부터 실제 대중화되고 많은 사람한테 시도를 해서 아까 그 결론으로 여러 바이오빅 데이터, 핵심 데이터에 지넘 데이터가 중주적인 역할을 했습니다. 7만 전원 프로젝트에 한 사람에서 쓴 가격이 2015년 천 달러 정도.
00:16:04
Speaker 1
아 아 아, 아 아 아 아 아.
00:17:00
Speaker 1
아 아 아 아, 그런데 이제 일루미나가 그렇게 오래 독점을 할 수 있는 이유가 페이턴트입니다. 페이턴트, 특허가 아주 깨끗하게 읽어있습니다. 아주 핵심 기술입니다. 그런데 이제 특허가 완료가 됐죠. 우리가 1,000달러 한동안 유지했던 1,000달러를 훨씬 더 낮출 수 있는 그런 기술이 아니라, 실제 100달러는 아니죠. 100달러에 비해 하고 실제 그렇게 시작이 됐습니다.
00:17:37
Speaker 1
가격이 계속 떨어진다는 건 결국 뭐를 의미하겠어요? 인디비주얼 시퀀싱이라고. 정말 2000년에 한 사람의 지능을 탁 놓고 전 세계 사람들이 한 사람의 지능을 놓고 그런 걸 찾던 시대가 있었는데, 이제는 관심 있는 사람들의 지능을 인디비주얼하게 다 시퀀싱해서, 차이가 무엇이고 실제 우리가 최종적인 에임, 그 사람들의 어떤 시퀀스를 통해서 얻을 수 있는 신호파일을 어떻게 우리가 임상적으로 의의가 있고 환자한테 도움이 되는 신호파일을 발휘할 수 있을 것인가. 그런 질문에 직접적인 질문입니다.
00:18:16
Speaker 1
문제는 데이터가 크거든요. 한 사람의 지분이 그렇게 지분이 크다고 얘기할 수는 없지만 진짜 1달러, 100달러, 진짜 1만 명, 10만 명, 100만 명 이렇게 해드리기 시작하면 꽤 데이터 분석하고 그런 버든이 쌓일 것이라고 할 수 있습니다. 이런 질문을 보시면 돼요. 왜냐하면 바이오인포메틱스에서 저는 대학원에서 강의를 할 때 뭐부터 강의를 할까 하는데, 예전에 한 2000년 초반대 바이오인포메틱스 교과서입니다.
00:18:49
Speaker 1
그 교과서를 보면 맨 처음에 나와 있는 게 로이거든요. 뭘까 가만히 생각을 해보면, 저는 이제 시퀀스를 하는 사람이니까 이 시퀀스를 어떻게 얼라인하는 것인지 두 종, 두 개의 시퀀스가 있어요, TTCATA 그리고 TGCTCGT 아니, 일괄적으로 하면 헷갈려요 두 개의 시퀀스가 관련이 있다라고 가정을 하고 둘을 얼라인하게 하는 그런 알고리즘.
00:19:20
Speaker 1
이게 이제 스미스 워터만 알고리즘, 이전에 전통적인 바이오 유포모틱스 교과서에서 맨 처음 다가오는 주제거든요, 이거 스미스 워터만 알고리즘이라고 하는 게 그 조금 어퍼레벨에 가만히 그걸 다이나믹 프로그래밍, 되게 그럴싸하죠 저는 이걸 왜 기억하냐면 제가 옛날에 유학 갈 때, 다이나믹 프로그래밍이 뭐야? 이걸 전화 인터뷰, 물어봤는데 제가 뭐 알 리가 있나?
00:19:53
Speaker 1
전통 스태틱 프로그래밍이 반대말인가? 지금 생각해보면 참 황당한 얘기인데, 하여튼 인포머틱스 하는 사람이 중요하게 생각하는 다이내믹 프로그래밍 자 근데 이 그림만 봐도 벌써 이 시퀀스 얼라인먼트를 어떤 식으로 해야 되는지 대충 감이 잡힙니다, 하나의 시퀀스 그리고 두 번째 시퀀스를 넣은 다음에 그걸 페어와이스 2D 매트릭스로 만들어가지고 매칭되는 부분에 가점을 주고.
00:20:23
Speaker 1
매칭이 안 되는 부분에 페널티를 주고 이거를 한 방향으로 쭉 가장 점수가 높은 로컬 맥시멀에 찾아가지고 빨간색을 쭉 이어나가면 이렇게. 이거 보면 어? 그럴싸한데? 그리고 어떻게 보면 너무 뻔한 거 아니야? 라고 생각하실 수 있는데 뻔한 건 아니에요 만약에 우리가 이 두 개의 세퀀스가 전혀 연관이 없는 작업이다 전혀 연관이 없고 정말 모든 세퀀스의 어떤 베리러브리버트의 조합을 따진다 그러면.
00:20:55
Speaker 1
이 조합의 개수가 폭발적으로 증가하는 거죠, 근데 이거는 약간의 휴리스틱이 들어가긴 하지만요 휴리스틱이 들어가지만 둘을 2D 매트릭스에서 아주 심플하게, 계산 차원을 엄청나게 낮춰서 바로 우리가 인지할 수 있고, 어떻게 보면 우리가 손으로도 계산할 수 있고 아주 심플한 거예요 그래서 다이나믹 프로그래밍이라고 하는 게 그게 아니고 작가 중에 한 번 찾아봤어요, 계산 차원을 줄이고 약간의 휴리스틱을 넣어서 계산 차원을 줄이고.
00:21:28
Speaker 1
계산 차원을 조금만 줄여도 전체적인 컴퓨터 시스템을 엄청나게 낮추기 때문에, 이런 부분을 이제 발현하고, 제가 이 얘기를 왜 하냐면요. NGS 데이터의 특징 중에 하나가 여기서는 다른 버전의 시퀀싱도 있지만 저희가 2007년에 처음에 NGS라고 하는 걸 봤을 때 이런 식으로 많이 설명을 했거든요. 30억 글자가 있는 거대한 책인데 이거를 파편화해서 읽는 게 NGS이기 때문에.
00:22:05
Speaker 1
이렇게 파편화되면 문제가 보여요. 원래 책이 있었는데 NGS에서 나온 오프싱이었다. 근데 우리가 원하는 건 책이잖아요. 이거는 만약에 책이 아니면 이건 그냥 쓰레기죠. 이렇게 눈으로 딱 보면 그냥 쓰레기잖아요. 여러분 이게 원래 책으로 다시 구성이 돼야지만 우리가 information으로 될 수가 있어요. NGS에서 나온 거는 파편. 그래서 이제 초창기에 이제 이런 NGS 테크닉에 대해서 이런 파편의 데이터를 어떻게 다시 모아가지고.
00:22:39
Speaker 1
옛날에 스파이 영화 같은 경우는 그런 거 주러딩 된다고 하면 다 조합을 해가지고 책을 도플멘테이션으로 만드는 그런 게 나오는데 그런 알고리즘이 아주 적실하게 필요했잖아요. 근데 책이 보통 책이 아니에요. 30억 개 책을 재구성한다는 거는, 그래서 제가 그냥 하나 여기에서 설명드렸습니다. 예전에 그래서 그런 원래의 파편을 원래의 책으로 만들 수 있는 어떤 효율적인 알고리즘을 생각할 수 있을까.
00:23:13
Speaker 1
사람들이 몇 년 동안 많이 고민을 했었는데, 실제 그 솔루션이 어디서 나오냐면 압축 기술에서 나왔어요. 그래서 이제 실제 시퀀스 해보시는 분은 배스킷과정 보지 않더라도, 이 버러 휠러 알라이먼트에 대해서 익숙하게 쓰시는 분 계실거에요 우리가 진짜 랜덤한 파편을, 처음에 지눔에 알라이먼트를 할 때, 이거 표준이 뭐더라구요? BWA, 그래서 BWA가 결국 뭐하는 사람이에요?
00:23:47
Speaker 1
사람 이름 같긴 하죠 그죠? 스미스 워터만의 알고리즘이죠 버러 휠러라는 사람도 두 사람이에요 두 사람 두 사람이 예전에 알고리즘을 낸 걸 가지고 차용을 해서 고속으로 아까 말씀드린, 이것들을 막 조합을 해가지고 원래 책을 만들어내는 그런 알고리즘, 우리가 생각할 수 있는 것 중에서 가장 빠른 알고리즘 근데 이 버러 휠러라는 사람들이, 그거를 계산을 하고 만들었냐 이 사람들은 그 허드슨 영어소에서 근무하던.
00:24:18
Speaker 1
이 알고리즘도 70, 80년대에 나온 건데, 압축하려고 만든 압축하려고 만든, 기술인데 그거를 이후 사람들이 막 돌리고 돌리고 하다가 와 이거 얼라이먼트에서 가장 빠른, 가장 빠른 알고리즘, 아까 말씀드린 정말 대용량의 데이터, 사실 3기가의 책으로 만든 가장 효율적인 알고리즘이다. 그래서 그 이름을 아직까지 따서 버럭 흘러갈 겁니다. 이 사람들은 자신들은 압축 테크닉을 만들었는데 이게 자신들의 이름인 얼라이너의 표준이 되죠. 그래서 이런 어떤 알고리즘들이 어떻게 생겨나고 하는지 보면.
00:25:00
Speaker 1
결국 어떤 그 인터 디스플레이, 인사이트 이런 것들은 정말 아직까지는 휴먼의 영향을 생겨나는 여러 클레버한 자신만의 컨텍스트를 가질 수 있지 않을까 해서 그냥 제가 잠깐 이렇게 된다는 거죠. 그냥 관심이 있을지 못 찾아봤어요 이게. 보타이라고 초창기에는 BWA라고 안하고 자기들이 억지로 이름을 붙여서 그걸 출하였네.
00:25:35
Speaker 1
요거는 이제 특회에서 들었지. 보타이 그런거 말이지. 이게 이 시퀀스를 내가 어떤 서브 시퀀스, 서브 시퀀스를 이 원래 시퀀스 안에서 얼마나 빠르게 찾을 수 있을 것인가 예제해. 2010년 전에 이제 아까 말씀드린 바와 같이 뭐 어떻게 보면 좀 생뚱맞은 축 테크닉을 이렇게 바꾸다 보니까 가장 효율적이고 빠른 얼라인먼트 기술이 됐다.
00:26:08
Speaker 1
그런 어떤 컨텍스트는 아직까지는 저는 사람의 역할이 아닌, 그런 어떤 전혀 관련 없어 보이지만 그런 걸 잘 생각하고 있어요. 보통 저만 아니지만 사람들이 좋아하는 가장 그 격언 중에 그런 거 있잖아요. 스티븐 잡스가 커넥팅 단추라고 하는 게 있잖아요. 전혀 상관없어 보이지만 결국 그 단추를 연결하는 그거는 정말 휴먼의 연결이 아닐까라고 생각을 하는데 이런 게 바로 그런 좋은 예가 아닐까라고 생각합니다.
00:26:40
Speaker 1
그래서 빅바이오 데이터, NGS만 나왔고, 100,000불, 100불 되니까 사람들을 찍어 대니까 이걸 가지고 프리스젼 메디슨 얘기를 사람들이 하는 거죠. 두 번째 콘텍스트는 그런 얘기입니다. 그래서 맞춤이야기라고 하는, 맞춤이야기라고 하는 얘기는 너무나 뻔하죠. 지금은 너무 프리스젼 메디슨이라고 하는 얘기를 너무 해서, 코스놀라이스드는 좀 올드한 얘기를 하는데.
00:27:11
Speaker 1
코스놀라이스드 맞춤이야기라고 하는 거는 그냥 여러분 말 듣자마자 뻔한 얘기잖아요. 환자가 다 생긴 게 다르듯이 약에 대해서도 좀 다를 것 같고 환자에 대해서 그 환자의 정말 적절한 그 환자의 진짜 싱글 플러스메탈 맞는 진단 치료 전략을 찾을 수 있을까 그리고 하는 게 미래의학의 방향이다 그런 도구도 있고, 지금은 빅데이터가 이렇게 저렇게 굴려가지고 결과 할 수 있는 건 뻔해요 그 환자한테.
00:27:41
Speaker 1
그런 빅데이터의 조합을 가지고 그 환자한테 가장 맞는 진단 치료 전략을 찾아야 된다 어떻게든 찾아야죠 어떻게 썼으니, 그럴 수밖에 없기 때문에, 여러 자리로 흘러간다 어쩔 수 없는 얘기, 이건 뭐 옛날 대책은 약마다 다르죠 어떤 환자에 대해서 뻔하게 쓰고 너무나 뻔한 어떤 치료 결과를 기대할 수 있는 약이 있는데 그렇지 않은 약도 있죠, 당뇨약같이 비교적이죠.
00:28:13
Speaker 1
로버스트한 치료 결과를 기대할 수 있는 약도 있고 정신과나 항암제같이 완전히 환자들로 천양지체의 치료를 가져올 수 있는 극단적인 얘기는 하지만 실제 빨간색이 효과가 없는, 빨간색이 똑같은 약을 써도 파란색 이 사람만 효과 있고 빨간색은 효과가 있는 그런 것만 뽑아왔으니까 그렇지만, 이러한 것들 결국 어디서 나온 것인가, 사람마다 보는 관점이 다르죠.
00:28:46
Speaker 1
유전하는 사람은 유전체에서 찾을 것이고 다른 부분은 좀 포커스된 사람이 그런 자료를 찾을 것인데 이제는 그런 것도 없는 것 같아요 지금은 멀티모덜하게 탁 때려놔서 그런 조합들을 가지고 환자한테 딱 맞는 답을 찾을 수 있어요. 예전에 우리가 의사가 인투이션, 이 환자한테 이 약을 쓰는 게 제일 좋다는 거예요. 내 양심에 따라서 이 약을 주는 게 그럼 그게 정답이고.
00:29:18
Speaker 1
그리고 그거를 인정해주는 그런 방도 있죠. 유럽 같은 데는. 지금은 이제 에비던스입니다. EDM이라고 해서. 학부에서부터 이걸 듣죠. 환자한테 쓰기 전에 이미 임상시험이 돼야 돼요. 그런데 임상시험은 뭐예요? 그 환자랑 거의 비슷할 것이라고 간주하는 어떤 코트를 본 다음에 치료 효과를 받아요. 그런데 결국 이 코트라고 하는 게 결국 우리가 실제 적용해야 되는 환자라고.
00:29:49
Speaker 1
얼만큼 잘 대변할 수 있을 것인가. 그거에 대한 퀘스천이 생기고, 그리고 이걸 조금 더 정밀한 크리스티안 메디슨으로 가야 된다. 그건 당연한 얘기지만 말이 쉽지 않죠. 그래서 이제 결국 싱글 퍼스너한테 가장 적합한 진단 치료 전략을 찾는 프리스전 메디슨으로 갈 수도 있지만 지금은 최소한 서브 타이핑을 하고 중간 단계로, 하지만 제가 뒤에 말씀드린 여러 종류의 빅데이터, 월드와이드 수준의 국가 수준의 코어트들의 자료가 다 모이면.
00:30:26
Speaker 1
훨씬 더 빅프로 만족할 수는 없지만 훨씬 더 가까워지지 않을까요? 그래서 그런 과정에서 가장 중요한 역할을 한 게 NGS를 통해서 프리스전 메디슨이 처음 시작될 수 있었기 때문에, 프리스전 메디슨 잠깐 말씀을 좀 드리면 이게 2015년에 나온 거죠. 프리스전 메디슨에서 예전에 퍼스널라이스드 메디슨 하면 되지 그래도 뭔가 새로운 프로젝트를 하니까 이름이 좀 바뀌어서 예전에 정미래야라고 처음 시도를 해서.
00:31:02
Speaker 1
2015년에 당되면 이제 오바마 대통령이 미국에서 프리스전을 했으면 시작을 한다고 해서 선언을 합니다. 그리고 하도 죽이니까 그걸 알다 하는 거죠. 제가 항상 들리는 게 휴먼저넘 프로젝트를 한 분이 있었어요. 휴먼저넘 프로젝트가 2000년에 끝났는데 1990년에 시작을 한 거예요. 1990년에 미국 주도로 했는데 사실 그 프로젝트 처음에는 왔으니까 알고 계십니다.
00:31:35
Speaker 1
최근에 돌아가실 때 제임스 왓슨 DNA를 보고 하신 분이 사실은 처음 리더였는데 그분이 사실은 좀 말도 거친 문제가 좀 있으신 거예요. 그래서 중간에 프렌스 컬린스라고 바뀌어서 그분이 휴먼저넘 프로젝트를 10년 동안 리딩해서 끝나고 그래서 미국 NIH를 20년 넘게 헤드로 달리면서 마지막 끝나기 전에 내놓은 프로젝트가 이거예요. 프리스저넷슨, 프린스코넷슨, 헤롤드 배드슨, 이 당시에 미국 NCC 암센터 헤드였는데.
00:32:10
Speaker 1
이분이 전체적인 휴먼 전원 프로젝트, 빅데이터를 모아서 의학의 미래를 어떻게 가야 하는지, 여러 차세대 기술을 제시하는 데요. 이분 대로 런칭이 됐고, 이런 데이터를 가지고 새로운 의학 미래를 생각해볼 수 있는 거죠. 프리스저넷슨은 미국에서 별론티어 100만 명을 모았다. 100만 명을 모아서 계속 관찰을 하다 보면 이런 질환도 나오고, 저런 질환도 나오고, 100만 명 생각해봐서 얼마나 많다는 거죠.
00:32:44
Speaker 1
100만 명의 코어트를 계속 관찰하고, 미국에서는 프리밍엄 코어트 그런 거 있잖아요. 미국에 보스턴 가면 옆에 두 블럭 정도 가면 프리밍엄이라고 하는 조그만 도시가 있는데, 보스턴 사람들이 자기는 하기 싫으니까 하버드에만. 프레밍홈을 딱 찍어가지고 거기 있는 사람들한테 레드컬 필을 다 내주고 너희들을 몇 십 년 동안 관찰을 해서 그런 코어트를 찾으죠, 프레밍홈이. 그런 게 중요해요. 100만 명을 모아서, 널른 티어를 모아서.
00:33:15
Speaker 1
10년, 20년 관찰을 하는데, 여러 질환이 다 생기거든요, 100만 명은. 그 몇 십 년을 모으고 관찰을 하다 보면 그러니까 거기서 결국 처음에 우리가 보는 거고 멀티모델에 다 떼져놓을 수 있는 그런 데이터가 다르거든요. 근데 지금 당장은 아니다. 몇 십 년 관찰을 해야 된다. 그렇게 생각을 하는 건데 왜 2015년에 프리시저메디슨을 했을까? NGS. 여러 종류의 데이터를 다 떼요. 제가 처음에 보여드렸던 거.
00:33:45
Speaker 1
EMI, 라디오 그래픽 데이터, 환자, 생체 여러 데이터를 다 떼져놔야 되는데 가장 중요한 게, 가장 비싼 게 휴먼저널의 시퀀싱 가격이었는데, 2015년에 뭐가 가능하다고 그랬어요? 1000달러에요 1000달러 1000달러가 되니까 100만명 과잉도 해보지 그래서 이제 2015년에 드디어 Precision Medicine을 런칭을 했고 가장 큰 기술적인 진보는 아까 말씀드린 NGS 1000달러.
00:34:18
Speaker 1
2015년에 딱 맞춰서 100만명을 쭉 시퀀스를 다해서 유전정보를 다 모아두고, 그 위에다가 계속 모니터링 의료정보를 50명 관찰을 해서, 최종적인 의료정보를 환자한테 멀티모델 분석을 통해서, 각 환자한테 딱 맞는 치료 전략과 진단 전략을, Precision Medicine에 기반을 마련하겠다는 그런 계획을, 그래서 100만명이기 때문에 미국에서 하는 이름이 뭐겠어요?
00:34:54
Speaker 1
오로버스 프로젝트인데 여기 100만명이 있습니다 몇 십 년 동안, 조금 다른게 UK바이오뱅크. 영국에서는 UK바이오뱅크가 프로젝트. 이거는 50만명이에요. 조금 작으니까 50만명일 수 있겠다. 근데 UK는 처음에 좀 디파인을 좀 하고 들어왔어요. 환자를. 그래서 지금 벌써 아주 유용한 데이터였죠. 워러버스는 사실 월런티어를 보기 조금 브로드한 그런 데이터인데, UK는 처음부터 아주 환자를 그리기를 많이 했었기 때문에.
00:35:27
Speaker 1
지금 UK바이오뱅크와 관련해서 쓰는 그런 자료들. 저희 기관도 많이 쓰고 있죠. 가만히 보시면 모든 국가가 핀란드, 핀젠, 네덜란드, UK, 아이슬란드도 디코드젠. 아이슬란드는 어떻게 해요? 아이슬란드는 태어날 때 그냥 해버려요. 애들 피 뽑아서, 애들 피 뽑으면 태어나는 애들한테 다 그냥 해버려요. 나라별로. 몇 십만 명에서 한 백만 명 정도까지 국가 수준으로 이런 작업들을 다 합니다.
00:36:02
Speaker 1
NGS가 있으니까요. 시작이 뭐냐 하면 처음에 입을 열어서 피 뽑는 거예요. UK 바이오미크는 설문조서만 40회지 50회지 지금, 처음에 와서 피 뽑아서 시퀀싱해서 1000달러 지금 떨어져요. 그래서 유전 정보 먼저 확보해 놓고 계속 이제 임상 관련한 그런 EMR, 의료 정보를 모아서, 계속 나라별 데이터를 축적을 한다. 여기 보시면 우리나라는 뭐 내셔널 뱅크라고 돼.
00:36:33
Speaker 1
근데 이거는 아니고 되게 오래전 국가 통합 바이오미크 데이터라고 해서 이런 거 다 지하철 가면 붙어있더라고요. 지하철 100만 명이에요. 좀 늦게 시작하기에는 작년에, 아 죄송합니다. 10년도 안에 7년 안에 끝나겠다고 그러는데 어떻게 될지는 잘 모르겠고 망가지고 있다고 들었는데, 우리나라도 비슷한 규모의 국가보육이 진행을 하고 있고 나라별로 거대한 인상과 데이터베이스를 보고 있는데.
00:37:07
Speaker 1
시작된 계기 그리고 외모를 생각을 해보시면 나라별로 힘을 쓰고 있는 효과를 생각하실 수 있을 거예요. 이런 데이터들을 다 빼놓고 어떤 룰을 찾고 환자한테 적용을 해서 그 환자한테 가장 적합한 진단, 치료 전략을 만들어야 된다라고 하는 프레스 장관이 있으니, 실제 여기까지 보면 그럴싸하죠. 그런데 실제 어디까지 할 수 있는 거 생각해보면 조금 당혹스러운 점은 있어요.
00:37:47
Speaker 1
이게 마지막인데 실제 제가 지너미스 관련해서 할 수 있는 게 어디까지 얘기를 할 수 있는지. 유명하죠. 우리가 휴먼지넘 안에 유전자가 2만개 이상, 그 유전자가 각각 독특한 역할이 있죠. 우리가 2만개 유전자에 대해서 동일한 수준으로 knowledge를 가지고 있습니다. 많이 연구한 유전자는 우리가 지식을 더 많이, 아직도 애매모호한 유전자가 많습니다.
00:38:18
Speaker 1
그리고 실제 우리 몸에 중요한 역할을 하는 유전자, 그렇지 않은 유전자들이 있죠. 가장 유명한 유전자는 아무래도 cancer가 되는 유전자가 많아요. 가장 유명한 유전자는 일반인들 PO13 같은 유전자 있잖아요. TPO13, tumor suppressor, 그리고 이런 유전자 있어요. 이런 이벤트가 나와서 다 알게 됩니다. 안절리나졸리는 block out 유전자와 함께 문제가 있는 거잖아요. 유방암이 패밀리얼하게 생기는데, 90년대에 시퀀싱도 없을 때에.
00:38:49
Speaker 1
짐, 포지셔널 클러닝 해가지고 브라카 유전자를 처음 찾아서 아 이게 문제가 있으면 패밀리어 브레스트 캔서가 생긴다. 그리고 그렇게 생기면 사람들이 코트를 모으고 그 부위만 시퀀싱하는 것은 아주 쉬운 일이니까 그 부분만 시퀀싱해서 임상적인 치료 전략을 만듭니다. 그래서 브라카 1, 2 사실은 두 개의 유전자가 있는데 둘 중에 하나가 문제가 있으면 코케시안 피메일은 50세 1분의 1의 확률로 브레스트 캔서가 생긴다.
00:39:21
Speaker 1
거기까지 되면 정말 많은 거죠. 정말 많은 거죠. 최소한 그 유전자에 대해서. 그 이후는 환자가 결정하는 거죠. 환자가 계속 따라오라고 할 수도 있고 필락틱하게 뭘 해버리고. 이거는 아주 다 잘랐죠. 제거하고 난소도 다 제거하고. 그러면 환자의 초이스에 가있다. 그런데 환자가 초이스를 할 수 있는 정보를 줘야 되잖아요. 브라카라고 하는 유전자는 90년대부터 알려진 거죠. 환자도 어느정도 많기 때문에 우리가 많은 정보를 줄 수 있다.
00:39:53
Speaker 1
환자가 의료진 그 많은 정보 하에서 우리가 decision을 내리죠, 자 브라카1,2라고 하는 유전자가 과연 그 우리 유전체 안에서 어느정도, 자 유전체라고 하는게 3 billion에 있습니다, 근데 우리가 압축을 하면 3 billion을 요만큼을 보여줄 수 있어요 그죠, 크로노점 1번 2번 3번에서 y까지 3 billion 30억개 글자가, 여기 1번부터 30억개 글자가 쭉 쌓여있다 생각해보실 수가 있고, 여기서 그 책의 섹션에 해당하는게 크로노점인데.
00:40:24
Speaker 1
브라카라고 하는 유전자가 크로노점 17번에 있거든요 크로노점 17번이 전체의 지놈에서 요만해, 요거를 다시 확대해서 이렇게, 크로노점 17번 안에 브라카1이 85kb 정도 사이즈가 요만큼인거에요, 여기 뭔가 하나가 트럼펙팅무테이션이니까 어디서든 사시면 되잖아요, 요 안에 사실 엑손이겠지만 엑손에 뭔가 트렁케이션이 탁 생기면 여기 뭐 하나가 글자가 딱 바뀌어서 이 유전자가 제대로 워킹을 안한다.
00:40:56
Speaker 1
그러면 어떻게 되요? 브라커는 튜머 서프레서진이죠 그쵸? 튜머 서프레서진인데 되게 두 쌍이 있잖아요 그쵸? 엄마한테서 받은 게임에서, 이게 만약에 엄마한테서 받은 거라고 생각을 해보세요 문제가 있는게 엄마한테서 받은 거는 워킹을 못해요 근데 아빠한테서 받은 거는 워킹을 하거든요 등장은 문제가 없으니까 잘 살고 있다가 이제 한 40세쯤 되면은, 아빠한테서 받은 거에 딱 맛이 갈 때.
00:41:27
Speaker 1
보통 사람들은 쌍이 있으니까 둘 중에 하나가 40세 맛이 가도, 두 번째 알릴로 남은 말씀을 하실 수가 있는데 하나가 벌써 문제가 있는 분이라서 40세 되면 이제 그때부터. 여기 뭔가 문제가 발생한 것을 받아서 이네르티드, 패밀리어 브레스트 캔서가 될 수도 있고 실제 소마틱하게, 스프라딕하게 발생하는 것도 진짜 큰 문제인 것 같아요. 그래서 그것을 시퀀싱을 통해서 어떤 식의 피노타입으로 갈지 예측할 수 있는 것은.
00:42:01
Speaker 1
정말 NGS를 통해서 휴먼저널 프로젝트 이후에 10년 이상 살아보면서 얻어낸 가장 큰 가치인 것 같아요. 그래서 결국 이제 프리스전 메디싱, 우리가 알고 있는 제네틱스가 메디컬 제네틱스로 바뀌면서 프리스전 메디싱으로 들어와서 결국 어떤 일을 해야 될 것인가. 사람마다 가지고 있는 것을 인디뮤지얼 시퀀싱 하는 것은 이제는 1도 아니고 1,000달러. 그 30억 개의 글자를 잘 해독을 해서.
00:42:33
Speaker 1
이 사람이 결국 어떤 피노타입을 가질 것인지 그걸 예측하는 것이 최종적인 Ultimate Code가 되어야죠. 프리스저메디슨에서 해야되는 일은 지금 당장은 가야될 길이 아주 멉니다. 그래서 이제 사람마다 차이를 이렇게 먼저 피노타이핑을, 지노타이핑을 먼저 해놓고, 그 다음에 그 지노타입별로 에비던스를 다 랩핑을 해요. 제가 좋아하는 영화 중 하나인데, 이 영화 항상 강혜택이 이 얘기 하잖아요.
00:43:07
Speaker 1
처음에 이게 안 보신 분은 제가 꼭 보라고 얘기를 해요. 정말 아주 인사이트풀하고 영화적 재미까지 있는, 이게 이 분이 애다, 그쵸? 2000년에 나온 영화니까 얼마나 이 분은 주도로, 이 분은 부모. 두 분이 결혼했잖아, 그쵸? 딸도 있어요. 딸이 우리나라는 그렇게 좋아한다. 그렇게 그래서 이때는 2000년에 근데 이 영화 스토리를 딱 잠깐만 말씀드리면.
00:43:41
Speaker 1
자연 잉태, 주인공이 에다모크인데 에다모크가 자연 잉태를 해서 태어나거든요 자연 잉태를 해서 미래의 세계로, 태어났는데 태어나자마자 피를 조금 뽑은 다음에 그거를 기계에다 딱 넣은 다음에 기계가 바로 밀고 내리니, 간호사가 쭉 읽습니다 뭐가 기계에서 출력된 거를 그게 뭐냐면 대충 짐작하실 거예요 얘는 지능이 몇이고 지능이 100이 안 되고, 눈 색깔은 없고.
00:44:12
Speaker 1
심장병이 있고 얘는 지능지수가 몇이고 서른 살 이전에 죽은 거 그 얘기를 쫙 해주는 거예요, 이게 2000년에 나온 거예요, 그래서 부모가 그 얘기 듣고 힙합해가지고, 뭐를 하냐면 동생은 디자인드 베이비, 눈 색깔, 키, 면, 되게 재밌어요, 근데 실제 맨 마지막에는 주인공이 동생을 이기고 우주비행사 가면서 날아가거든요, 이 영화의 작품인데, 이 장면에 사실 많은 부분이 포함이, 어떻게 보면 우리 진짜 그거잖아요.
00:44:46
Speaker 1
우리가 워러버스, 프로젝트, 프리스.뮤, 케이바이 다 이거를 원하는 거예요. 근데 지금 우리가 과연 이 솔루션이 있는가, 지금은 없다. 근데 당장 없다고 하기도 곤란해요. 이제는 우리가 기술적으로 이걸 분류를 하죠. 피를 넣어서, 뽑아서, 기계에 넣었더니 바로 뭔가 이러고서 나오는 거는 정말 SF 소식인데, 이 과정을 가만히 생각해보면 이 과정은 두 개의 작업으로 나뉠 수가 있거든요. 하나는 블러드를 채취해서 그 사람의 진호타이핑이죠.
00:45:17
Speaker 1
이제는 우리가 뭘 읽어야 되는지 알잖아요. 30억 개 읽어야 되잖아요. 30억 개 읽었을 때. 진호타이핑이죠, 지금 진호타이핑. 이거는 돼요. 이건 계속 말씀드리는데 그거죠. NGS 가지고 피 뽑아서, 17C 뽑아서 회사 맡게 되면 어디에 기계, 서울, 성남도 들어와야죠. 뭐가 세? 그거 맡기면 이틀이면 나옵니다. 이틀이면 쭉. 30억대 글자가, 지노타이핑은 1번, 예전에는 너무 브로드한 얘기였고 뭐를 시퀀싱해야 하는지도 몰랐으니까 기계들만 징징이며 결혼을 했다.
00:45:50
Speaker 1
그런데 지금은 뭐를 읽어야 하는지 명확하고, 그리고 뭐를 읽어야 하는 기술도 있고 그리고 NGS에 사람들이 돈을 써서, 하루면 30억개 글자 다 100달러 그런데 지금 안된다고 하는 것은 뭐가 안된다는 거예요? 해석이 안된다, 30억개 글자 2만개 유전자 중에서 브라카처럼 이미 알고 있는 유전자도 있고, 해석이 가능한 유전자.
00:46:20
Speaker 1
그리고 유전체에 대한 부분도 있지만 그렇지 않은 부분도 더 많다, 그렇지 않은 부분에 대해서 브라카만큼 해석력을 주기 위한 게 아까 말씀드린 프로젝트입니다, 남은 부분에 대해서도 다 해석이 가능하고 최종적으로 20년 전 이후에 한 사람의 지방을 다 읽어서 그 사람이 어떤 피노타입을 가질지 어떻게 쓰일지는 나중에는 모르겠죠. 최소한 그걸 위해서 읽어야죠.
00:46:51
Speaker 1
그런데 문제는 아직까지 정보가 많이 부족하다고 생각합니다. 한때는 이런 회사도 있었어요. 23&B라고 하는 회사. 이 회사 최근에 지난주에 들었을 때 상장 폐지한다고 하더라고요. 이 회사가 이 사람이 누군가 하면 23&B. 여자 버스죠. 이 사람이 구글을 만든 두 사람 보고 있어요. 제가 세르게이 부인인 거예요. 이원은 했는데. 그래서 예전에 이 사람이 23&B를 위한 한다고 했을 때.
00:47:24
Speaker 1
드디어 구글이 생명적으로 정복을 하려고 나오고. 이 회사가 얘기하는 게 뭐냐 하면 지금 현재 완전히 망했지만, 집에다가 내가 이 회사 여기 보면 100달러 있잖아 100달러 99달러 되면 집으로 이 박스가 오거든요 이 박스를 딱 열어보면 예전에 이거 한번도 학생 중에, 면봉이나 그런 거 있어요 뭔지 아시겠죠 그쵸? 자기 면봉 이렇게 해가지고 버컬 스왑 해가지고 딱 넣어가지고 이 회사 보면 이 회사가 풀 지놈 시퀀스는 아니지만.
00:47:56
Speaker 1
우리가 알고 있는 유전자 몇 부분 로커스를 시퀀싱 해가지고 이 환자 이 사람한테 당신의 몇 개의 질환의 리스크는 어떻고, 그런 얘기를 이렇게 해줍니다 요런 식으로, 4개로 나눠서 하는 게 여기 보면 재밌는 거 같아요 툴 할 때 보면 술 마시면 빨개지는가 쓴맛을 느끼는가 네가 금발인가 귀지가 우리나라 사람은 다 드라이 타입이죠 그쵸? 근데 외국 사람은 웹 타입이.
00:48:28
Speaker 1
이제 눈 색깔 이거 맞추면 왜 그럴싸 하죠? 왜 그럴싸하고 다른 것들도 진짜 같아 보일 거야. 이건 맞출 수 있어요. 지금 다 맞출 수 있어요. 이거 맞춘 다음에 옆에 거 보고 아 내가 좀 조심해야 되는 질환들이, 코로나가 내 나이에 내 레이스의 사람이, 성별의 사람이 24.4% 리스크인데, 나는 좀 증가했잖아요. 아 뭔가 막 주의해야 될 것 같아가지고, 이거 가지고 떼돈 벌려고 하다가.
00:49:02
Speaker 1
밴 먹고 회사가 망해하면 문제 있을 것 같잖아요. 이런 검사를 DTC라는 DTC Direct to Consumer 이게 뭐 비슷하냐면, OTC죠 OTC 약국 가서 OTC, OTC는 일반의 약품이잖아요. 오버 더 카운터죠. 가서 약 달라고 해서 그냥 받아오는 거 의사를 거치지 않고 그냥 바로 약국 가서, DTC도 같은 얘기예요. 어감도 비슷하고, 다이렉트 컨슬머라고 하죠. 의료진을 격려하지 않고 어떤 카운슬러를 격려하지 않고.
00:49:33
Speaker 1
그냥 바로 그냥 회사에다가 맡겨서 그걸 하는 건데, 우리나라가 일부 허용해주긴 했는데 전체적으로 아직까지는 다 믿을 수가 없어요. 그래서 결국 근데 최종적으로 그렇게 됐죠. DTC라고 하는 거를 정말 지금 왜 금지냐 이게 말이 안 되는 게 아니고 근거가 없으니까, 아직만 있어요. 이 DTC라고 하는 거를 20년 후에는 진짜 좀 가능하게 하려고 아까 말씀드린 그런 다양한 동매죠.
00:50:04
Speaker 1
프리스젼에서 프로젝트들이 만들어져 있다. 제가 이 얘기를 해드릴 테니까요. 예전에는 사람들이 천명씩 모아서 그 어떤 다이렉트에 대한 질병과 이런 것을 지웠어요. 몇 십 년 전에 많이 했죠. 지웠어 하시는 분들은 정말 정말 존경한 게, 처음에 2000년에 지우아스를 할 때 100명 해서 논문을 했어, 다음 해에 논문이 나오려고 했더니 1000명을 알아, 1000명 어떻게 맞췄어.
00:50:34
Speaker 1
당뇨 환자를 당뇨 1000명 정상인 1000명 모아서, 지우아스를 한 명당 100만원 200만원 넣은 걸 해가지고, 지우아스에서 그 다음에 됐더니 만 명을 알아 어떻게 막 거기서부터 이제 포기, 이게 왜냐하면 이펙트가 그렇게 크지 않거든요 진짜 만 명 십만 명이나 조금 이제 우리가 볼 수 있는 그런 이펙트들이 나오는 건데 우리가 결국 왜 100만 명이 사람마다 나라마다 100만 명이 이거를 그냥 이제 인디비주얼하게 하지 말고.
00:51:06
Speaker 1
국가가 그냥 해버리겠다는 뜻이죠 그렇게 한다는 뜻이죠, 그래서 이제 이런 데이터베이스가 이제 자꾸 모이면 이거는 이제 아까 말씀드린 영화. 폴리제닉 리스크 스코어라고 해서 실제 이런 지화수들의 데이터가 로버스트하게 보일 때, 임상에서 어떻게 쓸 수 있는지 이런 질환들의 데이터가 보이면 이런 식으로 해석을 할 수 있다, 530에 대해서 이 사람이 에이지의 어떤 섹스 그리고 레이스를 고려할 때 25%인데 이 사람의 유전정보를 고려했던 530 리스크가 70%까지 올라간다.
00:51:47
Speaker 1
아 이거 안 쓴 논문에 나온 거고 아까 DTC랑 뭐가 다릅니까? 이 논문은 돈을 받지는 않잖아요 그렇죠? 이런 식으로 할 거다 PRS라는 계정을 도입해서 이런 식으로 가야 된다라는 방법을 제시한 거고 아직은 많이 좀 진료도가 떨어진다 물론 임상에서 메이저 탈퇴 단위로 해서 임상에서 많이 쓸 수 있어요 근데 다른 여러 가지 질환을 다 포괄적으로 하기 위해서 10년 이상 기다려서 아까 말씀드린 브리스젼 매그싱크.
00:52:22
Speaker 1
우리나라 에스너스틱 스페시피컬 인포메이션이 있어요 그래서 다 임상에 쓸 수 있는 그런 정보가 나오지 않을까라고 생각해요, 그래서 휴먼 제넘 시퀀스를 읽는 게 휴먼 제넘 프로젝트였으면 지금 이제 그것들을 다 해석을 해서 이 정보를 가지고 있는 이 책을 가지고 있는 사람이 어떤 피노타입을 가지고 있을까 이제 그거를 예측을 해야 되는데 지금은 아직 진행이 안 돼요 그죠 그 번호는 어떻게 보면 환자 입장에서는 안 좋은 얘기지만 리서치 하는 사람들은 좋은 거 같이 공부하고 많이 남아있다는 뜻이니까.
00:52:57
Speaker 1
또 이제 해외 테스트 쪽에 얘기를 했지만 이제 그런 어떤 멀티모달 개념 그런 부분들을 많이 공부를 하시고 처음에 얘기를 했죠, 에러를 한 번 했어서 저번에도 연구를 하시고 있습니다 한 시간 조금 더 돼요 오늘은 그냥 이 정도로 같이, ya, terima kasih