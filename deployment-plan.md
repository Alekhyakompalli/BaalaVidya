# BAALAVIDYA Deployment Plan

Backend on **Railway**, frontend on **Vercel**.

Status legend: **Verified** = checked against the repo by searching/reading. **Unverified** = taken from the existing review notes or inferred, not run or measured.

---

## 1. Overview and architecture

| Part | Location | Runtime | Target |
|---|---|---|---|
| Backend API | `backend/` (FastAPI, `app.main:app`) | Python | Railway |
| Frontend (primary) | `client/` (Flutter) built as Flutter web | Static files | Vercel |
| Frontend (alternative) | `backend/app/static/app.html` | Single HTML page served by backend at `/app` | Railway (same service) |
| Vector store data | `ingestion/data/qdrant_local` (outside `backend/`) | Embedded Qdrant on disk | Must be provided to backend |
| Curriculum chunks | `ingestion/data/chunks/class10_pilot.jsonl` | JSONL | Must be provided to backend |

Request flow:

```
Browser (Vercel: Flutter web)  --HTTPS-->  Railway: FastAPI (/v1/...)
                                              |-- embedded Qdrant (QDRANT_PATH)
                                              |-- sentence-transformers model (local cache)
                                              |-- offline LLM fallback (no external call)
```

Two frontend options:

- **Option A (recommended if Flutter web is acceptable):** Flutter web on Vercel, calling the Railway API via `API_BASE_URL` compiled in with `--dart-define`.
- **Option B (fallback):** serve `backend/app/static/app.html` from Railway at `/app`. Its API calls are root-relative (`/v1/...`), so no CORS is needed. Its only external dependency is Google Fonts (line 9).

---

## 2. Blockers to fix before deploying

Each item must be done before the first deploy. File:line references are from the review notes; items marked **Verified** were confirmed by search.

| # | Blocker | Where | Status | Fix |
|---|---|---|---|---|
| B1 | Start command hard-codes port 8000. Railway injects `$PORT`. | Start command / docs (`backend/` run instructions) | Unverified (line not re-checked) | Bind `$PORT`. Run from `backend/`: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| B2 | `backend/requirements.txt` has only `fastapi` and `uvicorn`, but the retriever imports `qdrant_client` at module top level. `sentence-transformers` and `torch` are imported lazily. | `backend/requirements.txt` | Unverified (contents from review notes) | Add a deploy requirements file that includes `qdrant-client`, `sentence-transformers`, and `torch`. Use the CPU wheel index for torch to keep the image smaller. |
| B3 | Python version mismatch. CI pins 3.11; `backend/uv.lock` is effectively empty (52 bytes). | `.github/workflows/ci.yml`, `backend/uv.lock` | Unverified (size from review notes) | Choose one version (recommend 3.11, matching CI). Pin it in the Dockerfile base image and regenerate `uv.lock`. |
| B4 | Hard-coded Windows chunks path `c:/Codebenders/ingestion/data/chunks/class10_pilot.jsonl`. On Linux it fails silently and leaves an empty chunk cache. | **Verified:** `backend/app/services/curriculum_service.py:3719` | Verified | Replace with `CHUNKS_PATH` env var, default relative to project root (for example `ingestion/data/chunks/class10_pilot.jsonl`). Log a clear error if the file is missing. |
| B4a | Same hard-coded path in a generator script. | **Verified:** `backend/generate_complete_curriculum.py:11` (`c:/Codebenders/backend/app/services/curriculum_data.py`) | Verified | Not on the runtime path. Make it relative too, or document it as a Windows-only dev script. |
| B5 | Client default base URL is `http://localhost:8000`. | `client/lib/services/chat_service.dart:12`, `client/lib/services/analytics_service.dart:16` | Verified (search) | Use `const String.fromEnvironment('API_BASE_URL', defaultValue: 'http://localhost:8000')`. Pass `--dart-define=API_BASE_URL=...` at build time. |
| B6 | Flutter web is not set up. `client/web/` does not exist. No `vercel.json`, no Dockerfile, no Railway config. | `client/` | Unverified (directory absence from review notes) | Run `flutter create --platforms=web .` inside `client/` (this adds `web/` and does not overwrite `lib/`). Build and verify locally. Add `vercel.json` (section 4). |
| B7 | Embedding model is loaded with `local_files_only=True`. First query fails unless the model is in the image or on a volume. | Retriever / embedding loader | Unverified | Pre-download the model in the Docker build (or mount a volume). See section 3.4. |
| B8 | `ingestion/` sits outside `backend/`. Config resolves the project root as the parent of `backend/`. With Railway root directory = `backend/`, `ingestion/` is not in the build context. `ingestion/data` is gitignored. | Build context; `.gitignore` | Unverified (gitignore status from review notes) | Use a repo-root Dockerfile with build context at repo root, and copy the required data explicitly. See section 3.2. |
| B9 | Parent PIN defaults to `1234`, in both client and backend. | `client/lib/services/analytics_service.dart:40`, `client/lib/l10n/app_strings.dart` (lines 132, 302), `backend/app/services/analytics_service.py:56` (fallback PIN, not in the original notes) | Verified (search) | Remove the default or make it configurable before any public pilot (section 5). |
| B10 | CORS is `allow_origins=["*"]`. | `backend/app/main.py:35` | Verified (search) | Replace with `CORS_ORIGINS` (section 5). |

Verification run for B4: one repo-wide search for `c:/Codebenders` returned the two backend hits above. The other hits are in `docs/eval-results/*.md` links (documentation only, no runtime effect).

---

## 3. Backend on Railway

### 3.1 Service settings

| Setting | Value |
|---|---|
| Service type | Web service from the GitHub repo |
| Root directory | Repo root (`/`) if using the repo-root Dockerfile (recommended). Use `backend/` only if the data is copied into the image by another means. |
| Builder | Dockerfile (recommended over Nixpacks, because the Python version, torch CPU wheel, and model pre-download need explicit control) |
| Start command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (run from `backend/` inside the image, i.e. `WORKDIR /app/backend`) |
| Health check path | `GET /health` |
| Replicas | **1** (see 3.5) |
| Public domain | Generate a Railway domain; record it as `https://<railway-domain>` |

### 3.2 Dockerfile outline (repo root)

Build context is the repo root so that `ingestion/data` and `backend/` are both available.

```
FROM python:3.11-slim
WORKDIR /app
# 1. Install deps (CPU torch wheel index), then app deps
COPY backend/requirements.deploy.txt backend/requirements.deploy.txt
RUN pip install --no-cache-dir -r backend/requirements.deploy.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu
# 2. Pre-download the embedding model into the image cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('<EMBEDDING_MODEL>')"
# 3. Copy code and data
COPY backend/ backend/
COPY ingestion/data/ ingestion/data/     # only if data is baked in (see 3.3)
ENV HF_HOME=/root/.cache/huggingface PYTHONUNBUFFERED=1
WORKDIR /app/backend
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
```

Notes:

- `<EMBEDDING_MODEL>` must equal the `EMBEDDING_MODEL` value in `backend/app/config.py`. Unverified: confirm the exact model id before building.
- Because the code forces `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`, the pre-download step is mandatory. Without it, the first query fails.
- `CMD` uses `sh -c` so that `$PORT` is expanded at runtime.
- `backend/requirements.deploy.txt` is a new file. It must list `fastapi`, `uvicorn`, `qdrant-client`, `sentence-transformers`, and `torch` (CPU), with pinned versions.

### 3.3 Data artifacts (ingestion/data)

`ingestion/data` is gitignored, so it will not come from git. Choose one:

| Option | How | Pros | Cons |
|---|---|---|---|
| a. Bake into image | `COPY ingestion/data/...` from a local build machine or CI artifact | Simple, no volume | Image grows; rebuild needed to change data; data must be present on the build machine |
| b. Railway Volume + seed | Mount a volume, set `QDRANT_PATH` to it, run a seed/ingest command once | Data changes without rebuild | Extra step; volume is tied to one replica |
| c. Qdrant server (ADR Phase 2A) | Run Qdrant as a separate Railway service, set `QDRANT_URL` | Removes single-process limit; can scale | Code change to the retriever; more infra to run |

**Recommendation for the pilot: (a) bake the data into the image**, because the data set is small, read-only, and changes rarely. It needs no volume and no seed step. Revisit (c) if the data must change without a redeploy or if more than one replica is needed. This follows the single-process constraint in `docs/adr/0007-vector-store.md`.

Unverified: the size of `ingestion/data/qdrant_local` and the chunks JSONL has not been measured.

### 3.4 Embedding model and image size

- The model is loaded with `local_files_only=True`, so it must be in the image (pre-download step in 3.2) or on a volume.
- torch CPU plus sentence-transformers adds several GB to the image. Unverified: exact size not measured.
- RAM: loading the model plus torch needs more memory than a minimal instance. Unverified: a figure is not measured here. Start with the largest Railway plan you can afford and check actual usage in the first deploy.

### 3.5 In-memory state (single replica)

The following is held in process memory only (no database):

- learner progress
- sync event log
- parent consent / PIN registry
- pilot feedback
- telemetry logs (`backend/app/services/logging_policy.py`, 30-day retention, in memory)

Consequences:

- All of this is lost on every restart or redeploy.
- Replicas do not share it, so **run exactly 1 replica**.
- Decision needed (section 8): accept for a pilot, or add persistence first.

### 3.6 Health check

- `GET /health` returns `{"status": "ok"}`.
- It does **not** reflect search readiness (whether Qdrant and the model loaded). A healthy response does not prove retrieval works. Use the smoke tests in section 7 for that.
- Optional improvement: add a `/ready` endpoint that checks the collection and model load.

### 3.7 Environment variables

| Name | Required | Secret | Purpose |
|---|---|---|---|
| `PORT` | Injected by Railway | No | Port uvicorn binds to. Do not set manually. |
| `QDRANT_PATH` | Yes | No | Path to embedded Qdrant store (e.g. `/app/ingestion/data/qdrant_local`). |
| `COLLECTION_NAME` | Yes | No | Qdrant collection name. Must match the data. |
| `EMBEDDING_MODEL` | Yes | No | Sentence-transformers model id. Must match the pre-downloaded model. |
| `SCORE_THRESHOLD` | No (has default) | No | Minimum retrieval score. Check default in `backend/app/config.py`. |
| `TOP_K` | No (has default) | No | Number of chunks returned. Check default in `backend/app/config.py`. |
| `CHUNKS_PATH` | Yes (new, blocker B4) | No | Path to `class10_pilot.jsonl`. Default relative to project root. |
| `CORS_ORIGINS` | Yes (new, blocker B10) | No | Comma-separated allowed origins: Vercel prod and preview domains. |
| `AZURE_OPENAI_API_KEY` | No | **Yes** | Defined in `backend/app/config.py` (~lines 27-30) but **unused**. Not needed. |
| `AZURE_OPENAI_ENDPOINT` | No | No | Same as above, unused. |
| `OPENAI_API_KEY` | No | **Yes** | Same as above, unused. |
| `OPENAI_MODEL` | No | No | Same as above, unused. |

Not set by the operator: `HF_HUB_OFFLINE` and `TRANSFORMERS_OFFLINE` are forced to `1` in code.

Do not put real secrets in this file or in git. Set secret values only in the Railway dashboard.

---

## 4. Frontend on Vercel

### 4.1 Option A: Flutter web (recommended)

Vercel has no Flutter SDK preinstalled. Choose one of:

- **A1. Custom build command** that installs Flutter during the Vercel build (slower, depends on network access to the Flutter SDK download; unverified).
- **A2. Prebuilt artifact**: build locally or in GitHub Actions, commit or upload `client/build/web`, and have Vercel serve it as a static directory. Simpler and more reproducible.

Build command (run in `client/`):

```
flutter build web --release --dart-define=API_BASE_URL=https://<railway-domain>
```

Output directory: `client/build/web`.

Pin the Flutter version (see section 6) so that the build is reproducible.

`vercel.json` (new file, place in `client/` or as directed by the Vercel project root). SPA rewrite so that deep links return `index.html`:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

Vercel environment variable: set `API_BASE_URL` for the build (used by the custom build command in A1). For A2 the value is baked in at build time, so changing it requires a rebuild.

Unverified: the Flutter web build has **not** been run. `client/web/` must be created first (blocker B6).

### 4.2 Option B: app.html from Railway

- No Vercel project is needed. The backend serves `backend/app/static/app.html` at `/app`.
- API calls are root-relative (`/v1/...`), so the same origin is used and CORS does not apply.
- Only external dependency: Google Fonts (line 9 of `app.html`). If the fonts are blocked, the page still works with fallback fonts (unverified).
- Trade-off: fewer features and less polish than the Flutter app. Confirm with the product owner (section 8).

---

## 5. CORS and security

| Item | Current | Target |
|---|---|---|
| CORS origins | `allow_origins="*"` in `backend/app/main.py` | `CORS_ORIGINS` env var listing Vercel prod domain and preview domain(s) |
| `allow_credentials` | Not needed (no cookies set) | `False` |
| Parent PIN default | `1234` in `client/lib/services/analytics_service.dart:40` and `backend/app/services/analytics_service.py:56`; shown to parents in `client/lib/l10n/app_strings.dart` (lines 132, 302) | Remove default, or require parents to set a PIN; do not show the default in UI |
| Authentication | None | Required before public exposure. Unverified scope. |
| Learner ID exposure | `learner_id` is in path and body; anyone who knows an ID can read/write that learner's data | Add auth or unguessable IDs before public use |
| Children's data | Telemetry and progress are collected | Read `docs/privacy-review.md` before any public launch |

Limit CORS to exact origins; do not use wildcards on the Vercel preview domain pattern unless you have checked the risk.

---

## 6. CI/CD

- `.github/workflows/ci.yml` runs tests and lint only. It has **no deploy step** (verified by review notes; unverified in this pass).
- Railway and Vercel can each auto-deploy on push to the main branch from GitHub. This is the simplest path; no deploy job is needed in CI.
- Flutter CI uses an unpinned `stable` channel. Pin a Flutter version so web builds are reproducible. Unverified: the exact version to pin is not chosen here.
- Python: CI pins 3.11. Use the same version in the Dockerfile (blocker B3).
- Consider adding a CI job that runs the smoke tests (section 7) against a Railway preview or staging deploy.

---

## 7. Runbook

### 7.1 Ordered checklist

| Step | Task | Done when |
|---|---|---|
| 1 | Decide open items in section 8 that block deploy (Python version, Flutter web vs app.html, data source) | Decisions recorded |
| 2 | Fix B1 (`$PORT`), B3 (Python pin), B4 (`CHUNKS_PATH`), B5 (`API_BASE_URL`), B10 (`CORS_ORIGINS`) in code | Lint passes; local run works |
| 3 | Add `backend/requirements.deploy.txt` with pinned versions; regenerate `uv.lock` | File exists; install succeeds |
| 4 | Create `client/web/` (`flutter create --platforms=web .`); run `flutter build web` locally | Local build output in `client/build/web` (B6, unverified until run) |
| 5 | Provide `ingestion/data` (qdrant store + chunks JSONL) to the build (option 3.3a) | Data present in build context |
| 6 | Write repo-root Dockerfile (3.2); build locally if Docker is available | Image builds |
| 7 | Create Railway service: Dockerfile, start command, health check `/health`, 1 replica, set env vars (3.7) | Deploy is green |
| 8 | Smoke-test backend (7.2) | All backend checks pass |
| 9 | Create Vercel project; set build command/output (4.1) and `API_BASE_URL` | Vercel build is green |
| 10 | Smoke-test frontend (7.3), including CORS | App loads, calls hit Railway, no CORS errors |
| 11 | Remove/rotate PIN default (section 5); review `docs/privacy-review.md` | Sign-off recorded |
| 12 | Pilot go-live; monitor logs and memory | Stable for first day |

### 7.2 Backend smoke tests

Replace `<railway>` with the Railway domain.

| # | Request | Expected |
|---|---|---|
| 1 | `GET https://<railway>/health` | `200`, body `{"status":"ok"}` |
| 2 | `GET https://<railway>/` | `200` (root page or JSON, confirm exact response) |
| 3 | `GET https://<railway>/v1/curriculum/packages/...` (fill in a real package id from the data) | `200` with package content. Empty or 404 means the chunks cache or data is missing (B4/B8). |
| 4 | `POST https://<railway>/v1/chat` with a sample question | `200` with an answer from the offline fallback. A slow first call is expected (model load). Errors here usually mean the model or Qdrant store is missing (B7/B8). |

Unverified: exact request bodies and package ids for tests 3 and 4 must be taken from the API routes and data.

### 7.3 Frontend smoke tests

1. Open the Vercel URL; the app loads (no blank page on refresh of a deep link, which tests the SPA rewrite).
2. Browser devtools, Network tab: API calls go to `https://<railway>/...`, not `localhost`.
3. No CORS errors in the console. If there are, check `CORS_ORIGINS` includes the exact Vercel origin (scheme and host, no trailing slash).
4. Run one chat and one curriculum action end to end.

### 7.4 Rollback

- Railway: redeploy the previous successful deployment from the Railway dashboard. Because state is in memory, a rollback also clears in-memory learner data (section 3.5).
- Vercel: promote the previous deployment from the Vercel dashboard (instant).
- If the data artifacts change, keep the previous image tag so the old data can be restored with it.

---

## 8. Open decisions

| # | Decision | Options | Recommendation | Owner |
|---|---|---|---|---|
| D1 | Qdrant embedded vs server | Embedded (single process, data baked in) / Qdrant server (ADR Phase 2A) | Embedded for pilot | Tech lead |
| D2 | In-memory state acceptable for pilot? | Accept (lose data on restart) / add persistence first | Accept only if pilot users are told data may reset | Product |
| D3 | Flutter web vs app.html | Flutter web on Vercel / app.html on Railway | Flutter web if build is verified; app.html as fallback | Product + tech |
| D4 | Parent PIN policy | Fixed default / per-parent PIN / remove PIN | Per-parent PIN, no shown default | Product |
| D5 | Python version | 3.11 (matches CI) / other | 3.11 | Tech lead |
| D6 | Source of data artifacts | Bake into image from build machine / Railway volume / regenerate in CI | Bake into image for pilot | Tech lead |
| D7 | Offline content host `stream.scert.telangana.gov.in` reachability and permission | Confirm reachable from build/runtime and that use is permitted | Confirm before pilot; unverified | Content owner |

---

## 9. Unverified items

These were not run or measured in this plan. Verify before relying on them.

- Flutter web build has **not** been run (`client/web/` does not exist yet).
- torch and embedding model size have **not** been measured; image size and RAM needs are estimates.
- Line numbers other than B4 (`curriculum_service.py:3719`) and B4a (`generate_complete_curriculum.py:11`) are from review notes and were not re-checked.
- `uv.lock` size (52 bytes) and the empty-file claim are from review notes.
- Railway and Vercel behaviour (build/health/CORS) has not been tested with these exact settings.
- Startup time of the model pre-download and first-query latency are not measured.
- `docs/privacy-review.md` contents were not reviewed as part of this plan.
- The offline content host is not tested for reachability.
