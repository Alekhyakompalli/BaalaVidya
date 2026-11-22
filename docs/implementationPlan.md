# BAALAVIDYA - Implementation Plan

Derived from `docs/architecture.md`. Items marked **Proposed:** are decisions or targets that the source documents do not state. Everything else traces to a section of the problem statement [PS: ...] or of the architecture [Arch: ...].

## Purpose and how to read this plan

This plan turns `docs/architecture.md` into ordered phases. Each phase delivers a working, testable slice. Durations are not given. Phases are ordered by dependency, and sizing is left to the team **Proposed:**. Each phase has the same six parts, in this order: **Goal**, **Scope**, **Deliverables**, **Exit criteria**, **Depends on** and **Risks**. Risk IDs (R1 to R12) refer to the table in [Arch: Key risks and open questions].

## Guiding principles

- **Offline-first.** Progress is written to the local store first, and the UI never waits for the network [Arch: Sync rules 1].
- **Syllabus-grounded answers only.** Tutor answers come from retrieved SCERT chunks, and a kind decline is given when no chunk matches [PS: Data Ingestion Pipeline; Chatbot Guardrails 5].
- **Telugu and English end to end.** Content, UI, retrieval and answers work in both languages [PS: Supported Languages].
- **Low-resource device as the performance target.** [PS: Hackathon Alignment 6; Arch: Deployment and runtime considerations].
- **Child safety before features.** Safety rules and tests are in place before any child-facing feature is released to pilot users [PS: Chatbot Guardrails; Arch: Security, safety and child privacy]. **Proposed:** this gate.
- **Each phase ends with a working, testable slice.** **Proposed:** this rule for sequencing.

## Phase overview

| Phase | Name | Main outcome | Depends on |
|-------|------|--------------|------------|
| 0 | Foundations and technical decisions | Repo skeleton, CI, and decisions R1, R2, R3 and state management recorded | None |
| 0A | Git repository and push | Code and docs pushed to a GitHub remote | 0 |
| 1 | Curriculum ingestion pipeline | Pilot SCERT chunks and embeddings indexed in Qdrant | 0 |
| 2 | Backend core APIs | Curriculum, Search, Chat/RAG and Progress APIs over the pilot index | 0, 1 |
| 2A | Backend deployment on Railway | FastAPI backend and its Qdrant service running on Railway | 2 |
| 3 | Flutter client shell and navigation | Child-facing screens navigable with pilot content | 0 (2 for pilot content) |
| 4 | Bilingual UI and online Bala Buddy | Telugu and English end to end, online chatbot | 2, 3 |
| 4A | Frontend deployment on Vercel | Flutter web build of the client served on Vercel | 4 |
| 5 | Offline mode | Downloaded chapter works with no network | 0, 1 |
| 6 | Sync and cloud progress | Progress from many devices reaches the server safely | 5 |
| 7 | Video section | Topic videos, streamed online only | 3, 1 |
| 8 | Progress, gamification and Play & Learn | Workbooks, games, rewards and mastery | 5, 6 |
| 9 | Parent dashboard and analytics | Parents see progress and weak areas | 6, 8 |
| 10 | Safety, privacy and hardening | Safety tests, privacy review and performance report | Runs alongside 5 to 9; gate before 11 |
| 11 | Pilot, beta and launch | Success metrics measured with real students and teachers | All |
| Future | Voice support | Speak and listen in Telugu and English | After 11 **Proposed:** |

## Phase 0: Foundations and technical decisions

**Goal:** remove the open technical choices that block everything else.

**Scope:**

- Create the repo layout: Flutter client, FastAPI backend, ingestion pipeline and docs **Proposed:** folder names.
- Set up development environments for the client and the backend.
- Run Qdrant in a dev container [Arch: System context diagram].
- Decide the embedding model (R1, multilingual-e5-base or BGE-M3), the offline LLM (R2, Phi-3 Mini or Gemma 2B) and the cloud provider (R3, Azure OpenAI or GPT API) using the evaluation in Phase 1 and the Phase 5 criteria [Arch: Key risks and open questions].
- Choose a state-management approach and a local database library. **Proposed:** the architecture leaves both open [Arch: Flutter client].
- Fix the route layout. **Proposed:** the prefixes in [Arch: FastAPI backend].

**Deliverables:**

- Repo skeleton.
- Architecture decision records (ADRs) for R1, R2, R3 and the state-management choice. **Proposed:** ADR format.
- CI that runs lint and unit tests for both the client and the backend. **Proposed:** CI tool.

**Exit criteria:**

- A hello-world Flutter screen and a FastAPI health route run in CI.
- Decisions are recorded in the ADRs.

**Depends on:** none. Phase 0 blocks all other phases.

**Risks:**

- R1 embedding choice, R2 offline LLM choice, R3 cloud provider choice [Arch: Key risks and open questions].
- Decisions made before Telugu test data exists may need revisiting in Phase 1 **Proposed:** mitigation is to record each decision as provisional.

## Phase 0A: Git repository and push

**Goal:** put the project under version control and push it to a remote on GitHub, so that every later phase can be deployed from the remote. **Proposed:** GitHub as the remote host.

**Scope:**

- Initialise a git repository at the project root if one does not exist. The project has no repository yet, so this is needed. [Phase 0: repo skeleton]
- Add a .gitignore covering Flutter build output, Python virtual environments, .env files, model weight files and any local Qdrant storage. **Proposed:** these rules. Secrets (API keys for Azure OpenAI, GPT API and Azure Document Intelligence) must never be committed; they go in environment variables.
- Create a GitHub repository and add it as the remote. **Proposed:** a single monorepo holding the client, backend, ingestion pipeline and docs.
- Commit the Phase 0 skeleton and push the default branch. Use a feature-branch and pull-request flow for later phases. **Proposed:** protect the main branch.
- The push itself is a git command run by the tester role. The create_pull_request tool opens pull requests and is used later.

**Deliverables:**

- A .gitignore file committed at the root.
- A GitHub repository with the skeleton on the main branch.
- A short README.md at the root describing the repo layout and the environment variables needed, with no secret values.

**Exit criteria:**

- git status is clean after the initial push.
- The remote repository shows the Phase 0 skeleton and the docs folder.
- No file containing a secret or a model weight file is tracked. Check with git ls-files.

**Depends on:** Phase 0 (repo skeleton and ADRs).

**Risks:**

- Secrets committed by mistake. Mitigation: .gitignore and a pre-push check. **Proposed.**
- Large model files exceed GitHub's file-size limit. Mitigation: keep weights out of git and download them. **Proposed.**

## Phase 1: Curriculum ingestion pipeline

**Goal:** turn SCERT content into chunks and embeddings in Qdrant, for a pilot set of classes and subjects.

**Scope:**

- Confirm the rights and access to SCERT content (R6) before any download [Arch: Source websites; Key risks R6].
- Fetch content from the sites listed in [Arch: Source websites (ingestion to RAG)]. If automated download is not allowed, use a manually supplied, versioned PDF set [Arch: Source websites, last paragraph].
- Extract text and chapter and topic structure [PS: Data Ingestion Pipeline 1, 2].
- Run OCR with Azure Document Intelligence for scanned pages, and test the quality on Telugu script (R7) [PS: Technical Stack OCR].
- Chunk the content and tag each chunk with class, subject, chapter, topic, language and source page **Proposed:** metadata fields [Arch: Ingestion pipeline].
- Embed a sample with both candidate models and compare retrieval for Telugu and English [Arch: Retrieval and RAG].
- Index the pilot chapters in Qdrant [PS: Data Ingestion Pipeline 4].
- The pilot covers the subjects named in [PS: Data Sources] for the classes the team selects **Proposed:** class range.

**Deliverables:**

- Pipeline job per class and subject.
- Chunk schema **Proposed:** field names as in [Arch: Data model].
- Embedding comparison report for Telugu and English retrieval on real SCERT chunks. This is the evidence for R1.
- Pilot index for a set of chapters.

**Exit criteria:**

- A retrieval test set of Telugu and English questions returns the expected chapter in the top results, at a threshold the team sets **Proposed:** threshold value to be set by the team.
- Re-running the pipeline on the same input gives the same chunk IDs **Proposed:** determinism check.

**Depends on:** Phase 0 (model candidates and the dev Qdrant instance).

**Risks:**

- R6 SCERT content acquisition and licence; R7 Telugu OCR and text extraction quality [Arch: Key risks and open questions].
- Telugu retrieval quality (R1) [Arch: Bilingual design].

## Phase 2: Backend core APIs

**Goal:** serve curriculum data, search and grounded chat from FastAPI.

**Scope:**

- Build the Curriculum, Search, Chat/RAG and Progress services [Arch: FastAPI backend].
- Build a retriever with class and subject filters [Arch: Retrieval and RAG].
- Write a prompt template with guardrails and the Bala Buddy persona. **Proposed:** one shared template for the online and offline models [Arch: LLM routing].
- Add the cloud LLM call using the Phase 0 choice (R3) [PS: Technical Stack "Cloud LLM"].
- Add the no-match behaviour: decline kindly and offer a related topic [Arch: Retrieval and RAG, Syllabus-only grounding].
- Serve "Latest Updates" from the Curriculum API **Proposed:** [Arch: Key risks, Latest Updates].
- Serve "Generate Revision Notes" through the Chat/RAG API **Proposed:** output format not defined in source [Arch: Key risks, Generate Revision Notes].

**Deliverables:**

- API with OpenAPI docs.
- Contract tests for each service.
- The Chat/RAG path working against the pilot index.

**Exit criteria:**

- For a fixed set of questions, answers cite retrieved chunks only.
- A question with no matching chunk gets the kind decline response, not an invented answer [PS: Data Ingestion Pipeline "strictly answer based on syllabus-aligned content"].

**Depends on:** Phase 0 (route layout, cloud provider), Phase 1 (pilot index).

**Risks:**

- Invented answers when retrieval is weak (G3) [Arch: Architectural goals].
- Cloud LLM failure or timeout (R12) **Proposed:** fall back to the on-device model in Phase 5 [Arch: LLM routing].

## Phase 2A: Backend deployment on Railway

**Goal:** run the FastAPI backend and its Qdrant vector database on Railway, reachable over HTTPS, so that the client and the pilot can use the Phase 2 APIs. [Arch: System context diagram; Technical Stack]. Railway as the host is **Proposed:**.

**Scope:**

- Create a Railway project linked to the GitHub repository from Phase 0A. **Proposed:** auto-deploy on push to the main branch.
- Deploy the FastAPI service from the backend folder, with a Dockerfile or the Railway Python build. **Proposed:** choice to be recorded.
- Start command served by uvicorn, bound to the port Railway provides through the PORT environment variable. **Proposed.**
- Deploy Qdrant as a separate Railway service from its Docker image, with a persistent volume for storage. **Proposed.** Alternative: Qdrant Cloud. Record the choice in an ADR. **Proposed.**
- Set environment variables in Railway for the cloud LLM key, the Azure Document Intelligence key and the Qdrant URL and API key. No values in the repository.
- Add a health route and point Railway's health check at it. **Proposed.**
- Restrict CORS to the Vercel frontend origin from Phase 4A. **Proposed.**
- Load the Phase 1 pilot index into the Railway Qdrant instance.
- Confirm the Railway plan limits (memory, sleep behaviour, volume size) on Railway's current pricing page before choosing a plan. **Proposed:** check, do not assume.

**Deliverables:**

- Live backend URL, with the OpenAPI docs reachable.
- Qdrant service with a persistent volume holding the pilot index.
- Deployment notes in the README: how to deploy, roll back and rotate keys.

**Exit criteria:**

- The Phase 2 contract tests pass against the deployed URL. **Proposed:** smoke test set.
- The Chat/RAG route returns a grounded answer for one fixed question from the pilot index after a restart of the service [Phase 2 exit criteria].
- The Qdrant data survives a service restart.

**Depends on:** Phase 2 (APIs), Phase 1 (pilot index), Phase 0A (remote repository).

**Risks:**

- Cold starts or sleeping on the hosting plan. **Proposed:** these affect the response-time goal G1; measure them.
- Secrets exposed in logs. Mitigation: no request bodies containing keys in logs. **Proposed:** [Phase 10 logging policy].
- Qdrant data loss without a volume. Mitigation: persistent volume and a backup of the index. **Proposed.**
- Cross-origin errors from the frontend. Mitigation: explicit CORS origins.

## Phase 3: Flutter client shell and navigation

**Goal:** the child-facing app skeleton, with the screens from the functional requirements.

**Scope:**

- Splash: BAALAVIDYA logo, fun educational theme and a friendly animation [PS: 1. Splash Screen]. **Proposed:** the animation runs while the local store opens [Arch: Startup].
- Home: search bar, language toggle at the top right, and a class grid for Class 1 to Class 10 [PS: 2. Home Screen; Supported Languages].
- Class Selection: subjects and a syllabus overview [PS: 3. Class Selection].
- Subject View: chapters, topics and progress percentage [PS: 4. Subject View].
- Topic View skeleton: title, explanation, AI tutor entry, related videos and practice questions [PS: 5. Topic View].
- Theme: bright and colourful, large fonts, rounded cards, large buttons, fun icons, with Blue and Yellow as primary and Green and Orange as secondary colours [PS: UI/UX Requirements; Accessibility 1].
- Navigation by taps, not typing [PS: Accessibility 3, 4; Arch: Client-side design notes].

**Deliverables:**

- All screens reachable and navigable with pilot content from Phase 2.
- Widget tests for navigation.

**Exit criteria:**

- A child can reach a topic from Home in three taps or fewer **Proposed:** target.
- Fonts scale when the system font size is increased **Proposed:** check method.

**Depends on:** Phase 0 (repo and state management). Pilot content from Phase 2 is needed for the exit criteria. Phase 3 can run in parallel with Phase 1.

**Risks:**

- Small tap targets and text overflow on low-resource devices **Proposed:** mitigation is to test on the target device from Phase 5.
- Navigation depth that a child cannot follow [PS: Accessibility 3].

## Phase 4: Bilingual UI and online Bala Buddy

**Goal:** Telugu and English end to end, and the AI chatbot in the app.

**Scope:**

- UI strings as resource files for Telugu and English **Proposed:** [Arch: Bilingual design].
- Instant language toggle with no reload, placed at the top right [PS: Supported Languages].
- Topic content in both languages [Arch: Data model, Content].
- AI Chatbot screen wired to the Chat/RAG API [PS: 6. AI Chatbot].
- Bala Buddy personality and language rules: friendly, cheerful, no jargon, no criticism [PS: Character Personality; Communication Style].
- Log each question as "Questions Asked" [PS: 9. Learning Progress].
- Offer next steps after each topic: Play Game, Practice Workbook, Watch Video, Ask Doubts [PS: Interactive Learning].

**Deliverables:**

- Both languages on every screen.
- Chatbot answers in the selected language.
- A Telugu test pass with the Telugu example question from the source.

**Exit criteria:**

- Toggling the language changes all visible text without a restart.
- The two example questions from the source, "What is Photosynthesis?" and "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?", return grounded answers [PS: 6. AI Chatbot "Example Questions"].

**Depends on:** Phase 2 (Chat/RAG API), Phase 3 (screens).

**Risks:**

- Telugu answers that are weak or mixed with English (R1, R2) [Arch: Key risks].
- Answers that do not match the Bala Buddy style **Proposed:** reviewed by subject teachers in Phase 11.

## Phase 4A: Frontend deployment on Vercel

**Goal:** build the Flutter client for the web and serve it from Vercel, so that testers and pilot staff can open the app in a browser before any store release. Vercel as the host is **Proposed:**. The child-facing mobile app is still delivered as an Android package for low-resource devices [PS: Hackathon Alignment 6; Technical Stack Frontend]. Vercel does not replace that. This is a scope limit: the web build is not the child-facing mobile release.

**Scope:**

- Connect the Vercel project to the GitHub repository and set the root directory to the Flutter client. **Proposed:** folder name.
- Build with flutter build web, with the output folder configured in Vercel. **Proposed.** Vercel's build environment does not include Flutter by default, so either use a build script that installs Flutter, or build in CI and deploy the built folder. **Proposed:** choose one and record it in the README.
- Set the backend URL for the web build through a build-time define or a config file, pointing to the Phase 2A Railway URL. No secrets in the web build, since web code is public.
- Add a rewrite or fallback rule so that deep links resolve to the app entry page. **Proposed:** a vercel.json file.
- Set preview deployments for pull requests. **Proposed.**
- Check that the language toggle (Phase 4) and the navigation still work in a browser. Check the offline-first behaviour (Phase 5) separately: the on-device LLM and local vector DB may not run in a browser. State this as an open item. **Proposed:** a separate web fallback is a decision for the team.
- Confirm Vercel's current plan limits on its pricing page before choosing a plan. **Proposed:** check, do not assume.

**Deliverables:**

- Live frontend URL on Vercel, with preview deployments per pull request.
- vercel.json and the build script or CI step, documented in the README.

**Exit criteria:**

- The home screen, language toggle, class grid and Bala Buddy chat load from the Vercel URL and call the Railway backend.
- Each Phase 4 exit criterion holds on the web build: toggling the language changes all visible text without a reload, and the two example questions return grounded answers.

**Depends on:** Phase 4 (bilingual UI and chatbot), Phase 2A (backend URL), Phase 0A (remote repository).

**Risks:**

- Flutter web differs from the mobile build (rendering, fonts, storage). Mitigation: run the Phase 3 navigation tests against the web build. **Proposed.**
- Browser storage limits for offline data. Mitigation: state that offline mode is a mobile feature until a decision is made. **Proposed.**
- Vercel build time, or Flutter missing from the build environment. Mitigation: the build step above.

## Phase 5: Offline mode

**Goal:** a downloaded chapter works with no network.

**Scope:**

- Versioned chapter package **Proposed:** [Arch: What is downloaded per chapter].
- On-device store for syllabus data, the local vector DB slice, cached video metadata and progress [Arch: Offline store and sync].
- On-device LLM (Phi-3 Mini or Gemma 2B, the Phase 0 choice) with local retrieval [PS: Offline Support].
- Chapter download flow. **Proposed:** download over Wi-Fi only, as an option [Arch: Limited bandwidth].
- Offline indicator.
- Sync queue: write locally first, send in order, keep on failure with back-off [Arch: Sync rules 1, 2, 6].
- Rebuild the local vector DB from the chapter package **Proposed:** [Arch: Vector DB sync strategy; R4].

**Deliverables:**

- Chapter download, offline reading, local RAG search and the on-device tutor.
- Sync queue with retry.

**Exit criteria:**

- With the network off, chapter reading, topic explanations, local search, the tutor, the workbook and the game screens all work [PS: Offline Support "Available Offline"].
- On-device answer latency and memory are measured on the lowest-spec target device **Proposed:** target values to be set in this phase; the device is an open item.

**Depends on:** Phase 0 (LLM choice), Phase 1 (chunks and embeddings for the package).

**Risks:**

- On-device model too big for low-resource devices (R2) [Arch: Deployment and runtime considerations].
- Package size of the vector DB slice (R4) [Arch: Key risks].
- Model packaging: shipped with the app or downloaded on first install **Proposed:** [Arch: Model packaging].

## Phase 6: Sync and cloud progress

**Goal:** progress from many devices reaches the server safely.

**Scope:**

- Sync API under the route prefix from Phase 0 [Arch: FastAPI backend].
- Each event carries a unique client ID, so a re-sent event is not counted twice [Arch: Sync rules 3].
- Append-only event log, with mastery and XP recomputed from it **Proposed:** conflict policy [Arch: Sync rules 4].
- Content updates flow one way, from server to device, through the versioned package [Arch: Sync rules 5].
- Learner profiles and separation of progress on shared devices **Proposed:** learner switch on Home [Arch: Shared devices; Sync rules 7].
- Progress view endpoints for Learning Progress: completed topics, chapters covered, questions asked, learning streak [PS: 9. Learning Progress].

**Deliverables:**

- Sync endpoint with idempotency tests.
- Conflict tests with two devices.

**Exit criteria:**

- A replayed batch leaves totals unchanged.
- Two devices that both record events for one learner produce the same totals regardless of sync order.

**Depends on:** Phase 5 (sync queue on the device).

**Risks:**

- Double counting on re-send [Arch: Sync rules 3].
- Learner data sent to another learner's account **Proposed:** mitigation is the learner ID check in Sync rules 7.

## Phase 7: Video section

**Goal:** topic-related videos, language-aware, streamed online only.

**Scope:**

- Videos entity and metadata API [Arch: Data model, Videos].
- Telugu and English video list per topic, with both shown where available [PS: 7. Video Section].
- Streaming when online only [PS: Online Mode "Video Streaming"].
- Cached metadata offline, with a friendly offline message **Proposed:** wording [Arch: Data flow (c) step 5].
- Video source decision (R5), with rights confirmed before any video is listed [Arch: Key risks R5].
- Video watched is recorded as a progress event **Proposed:** event type [Arch: Data flow (c) step 6].

**Deliverables:**

- Video list on Topic View.
- Offline message.
- Metadata cache.

**Exit criteria:**

- No video file is stored offline [PS: Offline Compatibility "Only video streaming requires internet"].
- Metadata lists correctly in both languages.

**Depends on:** Phase 3 (Topic View), Phase 1 (topic structure). Video source decision (R5) must be closed first.

**Risks:**

- Video rights and source (R5) [Arch: Key risks].
- Video stream on a weak connection **Proposed:** low-bandwidth quality option [Arch: Limited bandwidth].

## Phase 8: Progress, gamification and Play & Learn

**Goal:** the learning loop: workbooks, games, rewards, mastery.

**Scope:**

- Smart Workbook types: fill in the blanks, match the following, multiple choice, true or false, drag and drop, picture-based [PS: 11. Smart Workbook].
- Drag and drop and picture-based types need asset and rendering components that the source does not describe [Arch: Key risks, Drag and Drop].
- Chapter-specific games per subject from [PS: 11. Learning Games] (Mathematics, Science, Social Studies, English, Telugu).
- Stars, coins, badges, XP and levels. The XP formula and level thresholds are **Proposed:** (R8).
- Mastery levels Beginner, Learning, Practicing, Mastered, from reading, workbook, quiz, game and AI interaction inputs [PS: 11. Topic Mastery Score; Topic Mastery System]. Weights are **Proposed:**.
- Progress-based unlockables [PS: 11. Progress-based Unlockables].
- Mission Challenge at the end of each chapter, with badge, bonus XP and new challenges [PS: 11. End-of-Chapter Challenge; Mission Challenges].
- Achievement Certificates. **Proposed:** owned by the gamification engine [Arch: Key risks].
- AI-generated personalized practice for a struggling learner [PS: 11. AI Generated Personalized Practice].
- Story mode for Classes 1 to 5 [PS: 11. Story-Based Learning]. The authoring pipeline is not defined in the source **Proposed:** a content step to be scoped in this phase.
- Learning Progress screen with a day definition for the learning streak **Proposed:** [Arch: Key risks, Learning Streak].
- Reconcile Coins with Learning Points **Proposed:** see Open items.

**Deliverables:**

- All activity types working offline [PS: Offline Compatibility].
- Mastery calculation with tests on fixed inputs.

**Exit criteria:**

- Mastery and XP match a hand-computed sample.
- Activities complete offline and sync later [Arch: Sync rules].

**Depends on:** Phase 5 (offline activities), Phase 6 (progress events).

**Risks:**

- Mastery and XP formulas (R8) [Arch: Key risks].
- Drag-and-drop and picture components (see Scope) **Proposed:** a spike in this phase.

## Phase 9: Parent dashboard and analytics

**Goal:** parents can see progress and weak areas.

**Scope:**

- Analytics service that aggregates progress [Arch: FastAPI backend, Analytics].
- Parent Dashboard screens: learning progress, time spent, subjects completed, weak areas, workbook completion rate, game performance, total XP, current level, learning streak, badges [PS: 10. Parent Dashboard; Parent Insights].
- Parent access and consent **Proposed:** account linking to child profiles (R11) [Arch: Recommendations].
- No chat transcripts for parents **Proposed:** [Arch: Parent visibility].
- Weak concepts and improvement areas [PS: 10. Parent Insights].

**Deliverables:**

- Dashboard in the app.
- Analytics endpoints.

**Exit criteria:**

- Dashboard values match the underlying progress records in test data.

**Depends on:** Phase 6 (progress data), Phase 8 (workbook, game and mastery data).

**Risks:**

- Child privacy and consent (R11) [Arch: Key risks].
- Incorrect weak-area labels from a small sample **Proposed:** mitigation is to show a minimum-data notice.

## Phase 10: Safety, privacy and hardening

**Goal:** child-safe behaviour and reliable low-resource operation.

**Scope:**

- Output safety filter as a second check after the prompt rules **Proposed:** [Arch: Retrieval and RAG, Guardrails].
- Refusal templates in both languages for off-topic and unsafe questions **Proposed:** [Arch: Recommendations].
- Logging policy with access control and a retention limit **Proposed:** [Arch: Recommendations].
- Data minimisation and encryption of local storage on shared devices **Proposed:** [PS: Overview "shared devices"].
- Local data deletion when a learner or parent asks for it **Proposed:** [Arch: Recommendations].
- Removal of any third-party ad or tracking SDKs **Proposed:** [Arch: Recommendations].
- Legal review of cloud LLM age terms (R11) [Arch: Key risks R11].
- Performance and memory profiling on the target low-resource device [PS: Hackathon Alignment 6].
- Accessibility checks: large fonts, navigation and minimal typing [PS: Accessibility].

**Deliverables:**

- Safety test set of unsafe and off-topic questions in both languages, with expected refusals.
- Privacy review record.
- Performance report.

**Exit criteria:**

- No unsafe test question gets a non-refusal answer.
- The performance target from Phase 5 holds on the target device.

**Depends on:** Phase 0 (decisions), with checks from Phases 2, 4 and 5 in place. Runs alongside Phases 5 to 9.

**Risks:**

- Unsafe output from the cloud or on-device model (G9) [Arch: Architectural goals].
- Child privacy and consent (R11) [Arch: Key risks].

## Phase 11: Pilot, beta and launch

**Goal:** prove the success metrics with real students and teachers.

**Scope:**

- Closed pilot in a small set of schools with a chosen class range **Proposed:** [PS: Target Users].
- Measure the success metrics: fast topic retrieval, offline usability, accurate syllabus-based answers, child engagement, ease of learning, parent visibility [PS: Success Metrics 1 to 6].
- Feedback loop with students, parents and teachers **Proposed:** [PS: Target Users].
- Content review by subject teachers for accuracy **Proposed:** [PS: Data Sources].
- Decide the teacher and volunteer roles (R9) [PS: Target Users; Arch: Key risks R9].

**Deliverables:**

- Pilot report against each success metric.
- Prioritised backlog.

**Exit criteria:**

- Each success metric has a measured value and a target agreed with the product owner **Proposed:** targets.

**Depends on:** all earlier phases. Gate: Phase 10 must pass before pilot use.

**Risks:**

- Teacher and volunteer roles undefined (R9) [Arch: Key risks].
- Pilot feedback that the teams cannot act on in time **Proposed:** mitigation is the prioritised backlog.

## Future: Voice support

**Scope:**

- Speak Telugu and speak English.
- Listen to student questions.
- Read lessons aloud [PS: 6. AI Chatbot "Voice support (future scope)"; 12. Voice Ready Design].
- The architecture keeps chat input and output separate, so speech can be added later [Arch: Key risks R10].

**Start:** only after the pilot **Proposed:** [Arch: Key risks R10].

## Dependencies and critical path

- Phase 0 blocks all other phases.
- Phase 1 blocks Phase 2.
- Phase 2 blocks Phase 4.
- Phase 3 can start after Phase 0, in parallel with Phase 1.
- Phase 5 needs Phase 0 (LLM choice) and Phase 1 (chunks and embeddings).
- Phase 6 needs Phase 5.
- Phase 7 can run after Phase 3 and Phase 1.
- Phase 8 needs Phase 5 and Phase 6.
- Phase 9 needs Phase 6 and Phase 8.
- Phase 10 runs alongside Phases 5 to 9, with a gate before Phase 11.
- Phase 11 needs all earlier phases.
- Phase 0A needs Phase 0. Phase 2A needs Phases 2, 1 and 0A. Phase 4A needs Phases 4, 2A and 0A.
- Phase 11 also needs Phases 2A and 4A, since the pilot runs on the deployed services.

**Critical path (Proposed):** Phase 0, then Phase 1, then Phase 2, then Phase 2A, then Phase 4, then Phase 4A, then Phase 5, then Phase 6, then Phase 8, then Phase 9, then Phase 11. The deployment branch (2A and 4A) runs alongside Phase 5 and must finish before Phase 11. The branch Phase 2 then Phase 4 must also finish before Phase 11.

## Risks and mitigations

| Risk | Phase | Mitigation |
|------|-------|------------|
| R1 embedding choice: Telugu retrieval quality | 0, 1 | Embedding comparison on real SCERT chunks before the choice is final **Proposed** |
| R2 on-device model too big for low-resource devices | 0, 5, 10 | Size and latency measured on the lowest-spec target device **Proposed** |
| R6 SCERT licence and acquisition | 1 | Confirm terms before download; manual versioned PDF set as fallback [Arch: Source websites] |
| R5 video licensing and source | 7 | Confirm rights for each video; metadata only offline |
| R7 OCR on Telugu script | 1 | Test Azure Document Intelligence output on Telugu pages before indexing |
| R8 mastery formula | 8 | Fixed-input tests and hand-computed samples; product decision on weights |
| R11 child privacy | 9, 10 | Legal review; no chat transcripts for parents; data minimisation |
| R4 vector DB sync for offline use | 5 | Rebuild from the versioned chapter package; size check **Proposed** |
| R12 cloud call failure | 2, 5 | Fall back to the on-device model **Proposed** |
| Secrets committed to git or exposed in the web build | 0A, 4A | .gitignore, environment variables only, no keys in the Flutter web build. **Proposed** |
| Backend cold start or plan limits slow the first answer | 2A | Measure response time on the deployed URL; choose the plan after checking current limits. **Proposed** |
| Qdrant index lost on restart | 2A | Persistent volume and index backup. **Proposed** |
| Web build behaves differently from mobile, or offline features do not run in a browser | 4A | Web-specific test pass; scope offline mode to mobile until decided. **Proposed** |

## Traceability to the problem statement

| Functional requirement | Delivered in phase(s) |
|------------------------|----------------------|
| Splash [PS: 1. Splash Screen] | 3 |
| Home [PS: 2. Home Screen] | 3, 4 |
| Class Selection [PS: 3. Class Selection] | 3 |
| Subject View [PS: 4. Subject View] | 3 |
| Topic View [PS: 5. Topic View] | 3, 7 |
| AI Chatbot [PS: 6. AI Chatbot] | 2, 4 |
| Video Section [PS: 7. Video Section] | 7 |
| Search [PS: 8. Search Functionality] | 2, 3 |
| Learning Progress [PS: 9. Learning Progress] | 6, 8 |
| Parent Dashboard [PS: 10. Parent Dashboard] | 9 |
| Offline Mode [PS: Offline Mode] | 5 |
| Online Mode [PS: Online Mode] | 2, 6, 7 |
| Play & Learn [PS: 11. Play & Learn Module] | 8 |
| Bala Buddy [PS: 12. Bala Buddy] | 2, 4, 8 |
| Pilot, Beta & Launch [PS: Success Metrics 1 to 6] | 11 |

## Open items to resolve before Phase 0 ends

- Confirm the SCERT websites and their terms of use (R6) [Arch: Source websites].
- Choose the embedding model (R1), the offline LLM (R2) and the cloud provider (R3).
- Confirm the state-management approach and the local database library **Proposed:** [Arch: Flutter client].
- Decide the target low-resource device **Proposed:** [Arch: Deployment and runtime considerations].
- Confirm the video source (R5) [Arch: Key risks].
- Confirm the teacher and volunteer roles (R9) [PS: Target Users].
- Reconcile the Coins list [PS: 12. Achievements and Rewards] with the Learning Points list [PS: 11. Learning Rewards] [Arch: Key risks, Coins].
- Confirm the GitHub repository name and owner, and whether the main branch is protected. **Proposed:** [Phase 0A].
- Choose the Railway plan, and whether Qdrant runs as a Railway service or on Qdrant Cloud. Check current limits on each provider's pricing page. **Proposed:** [Phase 2A].
- Decide how the Flutter web build is produced for Vercel (built in Vercel or built in CI), and whether the web build is a pilot tool only. **Proposed:** [Phase 4A].
