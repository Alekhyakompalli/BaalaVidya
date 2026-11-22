# Backend (FastAPI) - BAALAVIDYA

FastAPI backend application serving Curriculum, Search, Chat/RAG (Bala Buddy), and Progress services over the Telangana SCERT Class 10 pilot vector index.

## Prerequisites & Setup (Windows PowerShell)

Ensure virtual environment dependencies are installed:

```powershell
# Using project virtual environment
ingestion\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

## Running Tests & Quality Checks

Run the contract test suite (21 contract tests):

```powershell
cmd /c "set PYTHONPATH=backend;. && ingestion\.venv\Scripts\pytest.exe backend\tests -v"
```

Lint with Ruff:

```powershell
ingestion\.venv\Scripts\ruff.exe check backend
```

## Running the API Server

Start the local development server:

```powershell
cmd /c "set PYTHONPATH=backend;. && ingestion\.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --reload"
```

The port defaults to 8000 (uvicorn's default). In deployment, Railway runs `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. For a local run on another port, pass `--port <n>`.

Interactive API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Implemented API Endpoints

### 1. Health
- `GET /health` - Service health status

### 2. Curriculum
- `GET /v1/classes` - List all supported school classes (Classes 1–10)
- `GET /v1/classes/{class_id}/subjects` - List subjects for a class
- `GET /v1/classes/{class_id}/subjects/{subject_id}/chapters` - List chapters and topics for a subject
- `GET /v1/curriculum/latest-updates` - Fetch latest syllabus and textbook notices

### 3. Search
- `GET /v1/search?q={query}&subject={subject}&class_name={class_name}` - Hybrid search over syllabus metadata and Qdrant chunks

### 4. Chat & RAG (Bala Buddy)
- `POST /v1/chat` - Chat with Bala Buddy AI companion (strict syllabus grounding, citations, kind decline for out-of-syllabus questions, safety guardrails)
- `POST /v1/chat/revision-notes` - Generate structured revision notes and key points for a chapter

### 5. Learner Progress & Gamification (Phase 8)
- `GET /v1/progress/{learner_id}` - Get learner profile, completed topics, XP, streak, stars, coins, questions asked, badges, level, and topic mastery breakdown
- `POST /v1/progress/{learner_id}/activity` - Log educational activities and award XP, coins, and recalculate topic mastery
- `POST /v1/progress/{learner_id}/personalized-practice` - Generate simplified analogies and booster exercises for struggling learners (score < 60%)
- `POST /v1/progress/{learner_id}/certificate` - Generate verified digital Achievement Certificates for chapter completion
- `GET /v1/progress/{learner_id}/certificates` - List all earned achievement certificates
- `GET /v1/progress/{learner_id}/unlockables` - List progress-based unlockables (games, themes, badges)
- `POST /v1/progress/{learner_id}/mission-challenge` - Submit and evaluate 4-part End-of-Chapter Mission Challenges (+50 XP, Chapter Badge)

### 6. Progress Synchronization & Conflict Resolution
- `POST /v1/sync` - Idempotent batch sync endpoint for offline student telemetry:
  - Client-ID & Event-ID deduplication (Rule 3)
  - Append-only event store with deterministic CRDT reduction (Rule 4)
  - Order-independent convergence across multiple devices
  - Strict learner separation on shared hardware (Rule 7)
  - `video_watched` event processing (+15 XP, +5 coins, topic progress)

### 7. Videos & Streaming Metadata (Phase 7)
- `GET /v1/topics/{topic_id}/videos?language={te|en}` - List topic educational videos in Telugu and English
- `GET /v1/videos/{video_id}` - Fetch video metadata, HLS streaming endpoints, and adaptive quality levels (360p Data Saver, 480p Standard, 720p HD)
- `GET /v1/curriculum/packages/{subject_id}/{chapter_id}` - Includes cached video metadata in offline chapter packages (strictly zero offline video media blobs)

### 8. Parent Dashboard & Analytics (Phase 9)
- `GET /v1/analytics/parent/{learner_id}` - Aggregated parent dashboard metrics:
  - Total learning time spent and time spent today
  - Subjects completed and in progress (Biology, Mathematics, Telugu)
  - Workbook completion rate and game performance score
  - Weak concepts (< 60% accuracy) with actionable support recommendations
  - Strength areas (>= 80% accuracy) with family engagement guidance
  - Minimum data notice when activity sample is small (< 2 activities)
  - Full gamification metrics matching underlying progress records (XP, Level, Streak, Stars, Coins, Badges)
  - Strict Child Privacy: Zero chat transcripts or messages exposed
- `POST /v1/analytics/parent/consent` - Register parent account and store consent & PIN (R11)
- `POST /v1/analytics/parent/verify-pin` - Verify parental gate PIN for shared mobile devices

### 9. Safety, Privacy & Hardening (Phase 10)
- `DELETE /v1/analytics/parent/{learner_id}/data` - Permanently purge all student telemetry, parent linkages, and progress records (Right to be Forgotten - ADR 0012)
- `DELETE /v1/progress/{learner_id}` - Direct student progress record deletion
- **Two-Tiered Safety Architecture:**
  - Tier 1: Input guardrails against prompt injection, harmful content, and off-topic queries in English & Telugu
  - Tier 2: Output safety filter intercepting profanity, harmful instruction leakage, PII (email, phone, Indian Aadhaar), and API key exposure
- **Logging & Retention Policy:**
  - Zero student chat transcripts persisted to disk or parent databases
  - IP masking (`0.0.0.0`) and automatic PII redaction
  - Automated 30-day rolling data retention enforcement
- **Safety Test Benchmark:**
  - 22-case benchmark suite in `docs/eval-results/safety_test_set.json` with 100% verified refusal rate

### 10. Pilot, Beta & Launch (Phase 11)
- `GET /v1/pilot/metrics` - Evaluates official measured values against agreed product owner targets for all 6 Success Metrics:
  1. Fast Topic Retrieval (<= 3 taps, < 500ms query latency)
  2. Offline Usability (>= 95% offline task completion, 0 media crashes)
  3. Accurate Syllabus-Based Answers (>= 90% grounding, 0% hallucinations, 100% safety refusals)
  4. Child Engagement (>= 70% 5-day streak retention, >= 3 activities/week)
  5. Ease of Learning (>= 80% positive feedback, < 50ms language switch latency)
  6. Parent Visibility into Progress (>= 70% adoption, 100% child privacy compliance)
- `POST /v1/pilot/feedback` - Submit stakeholder feedback from students, teachers, parents, and Vidya volunteers
- `GET /v1/pilot/feedback/summary` - Aggregate pilot feedback sentiment, star ratings, and key improvement themes
- **Pilot Deliverables & Operating Model:**
  - Evaluation Report: `docs/pilot-report.md`
  - Prioritised Backlog: `docs/prioritised-backlog.md`
  - Teacher & Volunteer Guide: `docs/teacher-volunteer-guide.md`
  - Architectural Decision Record: `docs/adr/0013-pilot-success-metrics-and-launch.md`

