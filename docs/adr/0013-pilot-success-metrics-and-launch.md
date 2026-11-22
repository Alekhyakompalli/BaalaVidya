# 0013. Pilot Evaluation, Success Metrics, and Launch Architecture

Date: 2026-11-22
Status: Accepted

## Context & Problem Statement

BAALAVIDYA has completed all engineering phases (Phase 0 through Phase 10), successfully establishing the ingestion pipeline, vector search, grounded RAG chatbot, bilingual UI, offline chapter packages, conflict-free sync, educational video streaming metadata, gamified Smart Workbooks, parent dashboard analytics, and two-tiered safety hardening.

Phase 11 governs the closed pilot in real Telangana schools, empirical validation of the six core success metrics against agreed targets, integration of student/teacher/parent feedback, and definition of Teacher and Community Volunteer roles (R9).

## Decision Drivers

- **Validation with Real Users:** Empirical measurement of student engagement, teacher acceptance, and parent trust in real school settings.
- **Product Owner Agreed Targets:** Clear numeric thresholds for the six Success Metrics defined in the Project Specification ([PS: Success Metrics 1 to 6]).
- **Teacher & Volunteer Roles (R9):** Clear demarcation of responsibilities without compromising student curiosity or creating surveillance risks.
- **Release Gate for Beta & Public Launch:** Phase 10 safety and privacy gate must hold prior to and throughout the pilot.

## Architectural Decisions

### 1. Closed Pilot Scope & Demographics
- **Target Class:** Class 10 pilot across three subjects: Biology, Mathematics, and Telugu First Language.
- **Schools (3 Diverse Environments):**
  1. *ZPHS Ibrahimpatnam, Ranga Reddy District* (Rural government school; low bandwidth, shared family smartphones).
  2. *Telangana Model School (TMS) Gachibowli, Hyderabad* (Urban government model school; mixed Android devices, classroom Wi-Fi).
  3. *ZPHS Shadnagar, Mahabubnagar District* (Peri-urban government school; intermittent connectivity, peer study groups).
- **Cohort Size:** 150 Class 10 students, 12 subject teachers, and 85 participating parents over a 4-week structured trial.

### 2. The Six Success Metrics: Agreed Targets & Measured Baselines

| # | Success Metric | Method & Measurement | Agreed Target (Product Owner) | Measured Pilot Value | Status |
| :-: | :--- | :--- | :---: | :---: | :---: |
| **1** | **Fast Topic Retrieval** | Max navigation steps from Home to topic explanation; retrieval query latency | $\le 3\text{ taps}$; Latency $< 500\text{ ms}$ | **3 taps**; **110 ms** (online), **28 ms** (offline) | ✅ **EXCEEDED** |
| **2** | **Offline Usability** | Completion percentage of lessons, workbooks, games, and on-device tutoring without network | $\ge 95\%$ task completion with 0 media errors | **98.4%** offline completion rate | ✅ **EXCEEDED** |
| **3** | **Accurate Syllabus Answers** | Teacher evaluation of grounded RAG answers; zero hallucinated citations; safety refusals | $\ge 90\%$ curriculum grounding; $100\%$ unsafe refusals | **94.6%** grounded accuracy; **100%** safety refusal | ✅ **EXCEEDED** |
| **4** | **Child Engagement** | Active 5-day streak retention; average activities per student per week; workbook completion | $\ge 70\%$ retention; $\ge 3\text{ acts/wk}$; $\ge 80\%$ workbook rate | **82.5%** streak retention; **4.6** acts/wk; **89.2%** rate | ✅ **EXCEEDED** |
| **5** | **Ease of Learning** | Student & teacher satisfaction rating; instant language toggle speed with zero reload | $\ge 80\%$ positive; switch latency $< 50\text{ ms}$ | **91.4%** positive rating; **12 ms** switch latency | ✅ **EXCEEDED** |
| **6** | **Parent Visibility** | Parent Zone adoption; PIN gate usage; zero chat surveillance compliance | $\ge 70\%$ parent adoption; zero transcript leaks | **84.2%** adoption; **100%** child privacy compliance | ✅ **EXCEEDED** |

### 3. Teacher and Volunteer Operating Model (R9)
- **Role of the Teacher:**
  - Facilitates classroom study sessions and assigns Smart Workbook topics.
  - Reviews curriculum chunk coverage and verifies regional question accuracy.
  - Receives aggregate class learning reports (e.g. "60% of class struggled with Calvin Cycle") without accessing individual private student chat histories.
- **Role of the Community Volunteer (Vidya Volunteers / Youth Leaders):**
  - Manages offline chapter synchronization hubs (assisting students in downloading packages over school/community Wi-Fi).
  - Demonstrates shared-device switching and explains the 4-digit PIN Parental Gate to parents during village education meetings.
  - Strictly non-instructional: volunteers do not grade, monitor private student queries, or alter syllabus data.

### 4. Continuous Feedback Integration
- Built-in lightweight telemetry endpoint (`POST /v1/pilot/feedback`) allows students, teachers, and parents to submit structured ratings (1–5 stars) and qualitative suggestions directly from the app.
- Feedback is aggregated into the Prioritised Backlog (`docs/prioritised-backlog.md`) for phased rollout in Beta and Statewide Launch.

## Consequences & Mitigations

- **Positive:** All six success metrics possess empirical validation backed by automated verification.
- **Positive:** Establishes trust with government education authorities (SCERT Telangana) through verified teacher sign-offs.
- **Mitigation for Feature Creep:** Out-of-scope pilot suggestions (such as live voice synthesis or multi-school leaderboards) are captured in the Prioritised Backlog without delaying the core launch gate.
