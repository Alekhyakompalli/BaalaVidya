# R1 Embedding Model Comparison Report (Bilingual Pilot: Telugu & English)

**Date:** 2026-11-21 11:07:05 UTC
**Total Pilot Chunks Evaluated:** 1822
- English chunks: 1647
- Telugu chunks: 175
**Total Evaluation Queries:** 78

## 1. Summary Comparison Table

| Model | Dimension | Encode Time (s) | English Recall@5 | Telugu Recall@5 | Overall Recall@5 | Overall MRR@5 |
|---|---|---|---|---|---|---|
| `intfloat/multilingual-e5-base` | 768 | 495.7s | 0.887 | 0.938 | 0.897 | 0.866 |
| `BAAI/bge-m3` | 1024 | 1693.5s | 0.903 | 0.938 | 0.910 | 0.910 |

## 2. Detailed Performance Breakdown

### Model: `intfloat/multilingual-e5-base`
- **Embedding Dimension:** 768
- **Encoding Latency:** 495.7s across 1822 chunks
- **English Queries (62):** Recall@1 = 0.839, Recall@5 = 0.887, MRR@5 = 0.855
- **Telugu Queries (16):** Recall@1 = 0.875, Recall@5 = 0.938, MRR@5 = 0.906
- **All Queries (78):** Recall@1 = 0.846, Recall@5 = 0.897, MRR@5 = 0.866

### Model: `BAAI/bge-m3`
- **Embedding Dimension:** 1024
- **Encoding Latency:** 1693.5s across 1822 chunks
- **English Queries (62):** Recall@1 = 0.903, Recall@5 = 0.903, MRR@5 = 0.903
- **Telugu Queries (16):** Recall@1 = 0.938, Recall@5 = 0.938, MRR@5 = 0.938
- **All Queries (78):** Recall@1 = 0.910, Recall@5 = 0.910, MRR@5 = 0.910

## 3. Curated Ground-Truth Queries Results

| # | Lang | Subject | Expected Chapter | Query | `e5_base` Rank | `bge_m3` Rank |
|---|---|---|---|---|---|---|
| 1 | en | Biology | Lesson 1 | What is Photosynthesis? | 3 | **1** |
| 2 | en | Biology | Lesson 1 | Explain how green plants prepare food using sunlight and chlorophyll | **1** | **1** |
| 3 | en | Biology | Lesson 2 | What is the difference between aerobic and anaerobic respiration? | **1** | **1** |
| 4 | en | Biology | Lesson 2 | Describe the function of mitochondria in cellular respiration | **1** | **1** |
| 5 | en | Biology | Lesson 3 | How does the human heart pump blood through double circulation? | **1** | **1** |
| 6 | en | Mathematics | Lesson 1 | State the fundamental theorem of arithmetic and prime factorisation | ❌ Miss | ❌ Miss |
| 7 | en | Mathematics | Lesson 2 | Find zeroes of quadratic polynomials and relation with coefficients | ❌ Miss | ❌ Miss |
| 8 | en | Mathematics | Lesson 3 | Solve pair of linear equations in two variables algebraically | ❌ Miss | ❌ Miss |
| 9 | en | Mathematics | Lesson 4 | Find the roots of a quadratic equation using quadratic formula | ❌ Miss | ❌ Miss |
| 10 | en | Mathematics | Lesson 5 | Find the nth term and sum of n terms of arithmetic progression | ❌ Miss | ❌ Miss |
| 11 | te | Biology | Lesson 1 | కిరణజన్య సంయోగక్రియ అంటే ఏమిటి? | **1** | **1** |
| 12 | te | Biology | Lesson 1 | మొక్కలు ఆహారాన్ని ఎలా తయారుచేసుకుంటాయి? కాంతి చర్య ప్రాముఖ్యత | **1** | **1** |
| 13 | te | Biology | Lesson 1 | హరితరేణువు నిర్మాణం మరియు పిండిపదార్థం తయారీ విధానం | **1** | **1** |
| 14 | te | Biology | Lesson 1 | జీవులలో పోషణ రకాలు మరియు స్వయంపోషణ విధానం | **1** | **1** |
| 15 | te | Biology | Lesson 2 | శ్వాసక్రియ అంటే ఏమిటి? ఉచ్ఛ్వాస నిశ్వాసాల ప్రక్రియ | **1** | **1** |
| 16 | te | Biology | Lesson 2 | వాయు సహిత శ్వాసక్రియ మరియు వాయు రహిత శ్వాసక్రియల మధ్య తేడాలు | **1** | **1** |
| 17 | te | Biology | Lesson 2 | కణ శ్వాసక్రియలో మైటోకాండ్రియా పాత్ర ఏమిటి? | **1** | **1** |
| 18 | te | Biology | Lesson 2 | ఊపిరితిత్తులలో వాయువుల మార్పిడి రక్త ప్రసరణతో ఎలా సంబంధం కలిగి ఉంటుంది? | **1** | **1** |
| 19 | te | Telugu | Lessons 01-03 | దానశీలము పాఠం యొక్క ముఖ్య ఉద్దేశ్యం మరియు కవి పరిచయం | **1** | **1** |
| 20 | te | Telugu | Lessons 01-03 | బలి చక్రవర్తి శుక్రాచార్యుని వారించిన సందర్భం మరియు దాన గుణం | **1** | **1** |

## 4. Architectural Recommendation for ADR 0001

Based on the empirical evidence on real SCERT textbook chunks:
- `multilingual-e5-base` (dim=768): Telugu Recall@5 = 93.8%, Overall Recall@5 = 89.7%, Size = ~1.1 GB
- `bge-m3` (dim=1024): Telugu Recall@5 = 93.8%, Overall Recall@5 = 91.0%, Size = ~2.2 GB

> **Recommendation:** Accept `multilingual-e5-base` as the primary embedding model.
> **Rationale:** It meets the >= 0.80 Recall@5 target on both Telugu and English while offering a 768-dimension vector (vs 1024) and half the memory footprint (~1.1 GB vs ~2.2 GB), which is significantly more suitable for low-resource target environments and on-device indexing constraints (Arch: Low-resource device target).
