# BAALAVIDYA Prioritised Backlog for Beta & Public Launch

**Date:** 2026-11-22  
**Derived From:** Phase 11 Pilot Feedback, Teacher Content Reviews, and Architecture Roadmap  
**Methodology:** Impact vs. Effort Prioritization (P0: Must-Have for Beta Rollout, P1: High-Value Public Launch, P2: Long-Term Enhancements)

---

## 1. Backlog Overview

| Tier | Priority Focus | Target Release | Key Features |
| :--- | :--- | :---: | :--- |
| **P0** | **Statewide Beta Readiness** | Beta Q1 2027 | Multi-class curriculum expansion (Classes 6–9), Teacher Classroom Overview, Sync Conflict Visual Alerts |
| **P1** | **Public Launch & Voice Support** | Launch Q2 2027 | Full Voice Support (Telugu/English Speech-to-Text & Read-Aloud), Peer Offline Challenges, Printable Certificates |
| **P2** | **Future Enhancements** | Post-Launch 2027 | Regional Dialect Pronunciation Adaptation, Story Mode for Classes 1–5, On-device Quantization (Int8) |

---

## 2. P0: Must-Have for Statewide Beta Rollout

### 1. Multi-Class Curriculum Expansion (Classes 6 to 9)
- **User Need:** Teachers and school principals requested extending the pilot from Class 10 to include high-school Classes 6 to 9.
- **Scope:** Ingest Telangana SCERT textbooks for Physical Science, Social Studies, and English Medium / Telugu Medium editions.
- **Effort:** 3 weeks (automated ingestion pipeline with OCR caching already established in Phase 1).
- **Owner:** Curriculum Ingestion Lead.

### 2. Teacher Classroom Analytics Overview
- **User Need:** Subject teachers requested an aggregate classroom dashboard (e.g. "Lesson 2 Respiration: 65% of students scored below 60% on Calvin Cycle") to plan remedial classroom lectures.
- **Scope:** Aggregate class-level telemetry without exposing individual private student chat questions.
- **Effort:** 1.5 weeks.
- **Owner:** Backend & Analytics Lead.

### 3. Visual Offline Sync Conflict Notifications
- **User Need:** In shared household devices, siblings who study offline need clear visual cues when their offline progress events are successfully synced to the central server.
- **Scope:** Non-intrusive toast notifications and green checkmark icons indicating "Progress Synced 🌟".
- **Effort:** 4 days.
- **Owner:** Client UI Lead.

---

## 3. P1: High-Value Public Launch Features & Voice Support

### 1. Voice Support (Speech-to-Text & Read-Aloud) [Plan: Future Voice Scope]
- **User Need:** Younger students and rural children who struggle with typing requested speaking their doubts in Telugu and English, and hearing textbook passages read aloud.
- **Scope:**
  - Integrated Whisper / Conformer STT for Telugu and Indian English.
  - Natural sounding Telugu & English Text-to-Speech (TTS) for lesson explanations.
  - Architectural Decoupling: Audio pipelines remain decoupled from the core text RAG engine (R10), ensuring zero degradation of text-based offline search.
- **Effort:** 4 weeks.
- **Owner:** AI Research & Speech Lead.

### 2. Peer Offline Study Challenge (Local Wi-Fi / Bluetooth)
- **User Need:** Students in villages study in groups after school and requested competing in concept quizzes together without mobile data.
- **Scope:** Local peer-to-peer multiplayer quiz room over Wi-Fi hotspot or Bluetooth LE.
- **Effort:** 2.5 weeks.
- **Owner:** Client Systems Lead.

### 3. Printable High-Resolution Achievement Certificates
- **User Need:** Parents and students wanted to print and frame chapter mastery certificates for display at home and school.
- **Scope:** Client-side vector PDF generation (`pdf` package) with official Telangana SCERT styling and QR verification.
- **Effort:** 1 week.
- **Owner:** Client UI Lead.

---

## 4. P2: Long-Term Post-Launch Enhancements

### 1. Regional Dialect & Pronunciation Adaptation
- **User Need:** Students in northern and southern Telangana use localized vocabulary and phrasing.
- **Scope:** Fine-tune speech recognition models on regional Telangana Telugu accents (Warangal, Mahabubnagar, Adilabad).
- **Effort:** 6 weeks.
- **Owner:** Speech & Linguistics Team.

### 2. Extended Interactive Story Mode for Primary Classes (1 to 5)
- **User Need:** Teachers loved the Bala Rabbit division story in Phase 8 and requested 20+ narrative animated adventures for basic numeracy, foundational literacy, and environmental studies.
- **Scope:** Rich SVG animations and interactive branching stories for foundational learning.
- **Effort:** 5 weeks.
- **Owner:** Educational Content & Game Design Team.

### 3. On-Device Int8 Vector Quantization
- **User Need:** Further reduce memory consumption for ultra low-spec devices ($< 1\text{ GB}$ RAM feature phones).
- **Scope:** Apply 8-bit scalar quantization to the local SQLite vector database slice.
- **Effort:** 2 weeks.
- **Owner:** Performance & Hardening Lead.
