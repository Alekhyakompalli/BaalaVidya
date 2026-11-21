# BAALAVIDYA - Evaluation Plan

Derived from `docs/implementationPlan.md`. Items marked **Proposed:** are thresholds, methods or decisions that the source documents do not state. Everything else traces to a phase of [Plan: Phase N], a section of the problem statement [PS: ...] or a section of the architecture [Arch: ...].

## Purpose and scope

This evaluation plan defines how each phase of `docs/implementationPlan.md` is judged as done, which measurements prove each exit criterion, and what evidence is recorded for each run. It covers model and retrieval quality, answer quality, app behaviour, deployments and pilot metrics. It does not replace the phase exit criteria in [Plan: Phases 0 to 11]. It makes them measurable: each exit criterion is given a method, a data set and a pass rule. Where the source does not state a threshold, it is marked **Proposed:**.

## Evaluation principles

- Each metric names its data set, its method and its pass rule. A metric without all three is not a valid gate. **Proposed:** this rule.
- Numeric thresholds are **Proposed:** and must be agreed with the product owner and the subject teachers before Phase 0 ends [Plan: Open items to resolve before Phase 0 ends].
- Results are recorded per run, with the date, the commit hash and the model version (see Evidence and reporting). **Proposed:** this rule.
- Telugu and English are measured separately, and both must pass. A pass in one language does not cover the other [PS: Supported Languages; Plan: Guiding principles].
- A failed safety check blocks release. A failed quality check blocks only the phase that owns it [PS: Chatbot Guardrails; Plan: Guiding principles "Child safety before features"]. **Proposed:** this split between safety and quality.

## Evaluation types

| Type | What it judges | Phases |
|------|----------------|--------|
| Unit and contract tests | Each service and API route returns the agreed shape and status codes; lint and unit tests pass in CI [Plan: Phase 0, Phase 2] | 0, 2, 2A, 4A |
| Retrieval quality (RAG evaluation) | Whether the expected chapter appears in the top results for Telugu and English questions [Plan: Phase 1] | 1, 2 |
| Answer quality (grounding, language, style) | Whether answers cite only retrieved chunks, use the selected language and follow the Bala Buddy style [Plan: Phase 2, Phase 4] | 2, 2A, 4, 4A |
| Safety and refusal tests | Whether unsafe, off-topic and personal-information questions get a refusal, and whether prompt injection fails [PS: Chatbot Guardrails; Plan: Phase 10] | 2, 4, 10 |
| Offline behaviour tests | Whether each activity works with the network off [Plan: Phase 5] | 5, 7, 8 |
| Sync and idempotency tests | Whether replayed and two-device event streams give the same totals [Plan: Phase 6] | 6, 8, 9 |
| Performance on the target device | Answer latency and peak memory on the lowest-spec target device [Plan: Phase 5, Phase 10] | 5, 10 |
| Deployment smoke tests | Whether the deployed backend and web build respond and serve the expected content [Plan: Phase 2A, Phase 4A] | 2A, 4A |
| Usability and accessibility checks | Navigation depth, tap targets, font scaling and minimal typing [PS: Accessibility; Plan: Phase 3, Phase 10] | 3, 10 |
| Pilot outcome measurement | The six success metrics with real students and teachers [PS: Success Metrics 1 to 6; Plan: Phase 11] | 11 |

## Evaluation data sets

Test data for children must not contain real student data. Use synthetic items or items written by subject teachers [PS: Chatbot Guardrails; Plan: Phase 10]. **Proposed:** this rule.

| Data set | Contents | Owner | Built in phase | Notes |
|----------|----------|-------|----------------|-------|
| Retrieval set **Proposed:** | Telugu and English questions, each mapped to the expected class, subject, chapter and topic | Team, reviewed by a subject teacher **Proposed:** | 1 | Built from SCERT chunks [Plan: Phase 1]. Keep Telugu and English items separate |
| Grounded-answer set **Proposed:** | The fixed questions from the Phase 2 exit criteria, including "What is Photosynthesis?" and "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?" [PS: 6. AI Chatbot "Example Questions"] | Team **Proposed:** | 2 | Both source examples must be in the set [Plan: Phase 4] |
| Decline set **Proposed:** | Questions with no matching chunk in the pilot index | Team **Proposed:** | 2 | Each must get a kind decline and a related topic [Plan: Phase 2] |
| Safety set **Proposed:** | Unsafe, off-topic and personal-information questions in Telugu and English, each with an expected refusal | Teacher-written items; reviewed by the safety reviewer **Proposed:** | 10 | Refusal templates are in both languages [Plan: Phase 10] |
| Injection set **Proposed:** | Prompts that try to override the grounding and safety rules | Team **Proposed:** | 2, 10 | Run against the Chat/RAG route and the safety filter [Plan: Phase 10] |
| Offline set **Proposed:** | Scripted scenarios with the network off, one for each activity in the Phase 5 exit criteria | Team **Proposed:** | 5 | Activities: chapter reading, topic explanations, local search, tutor, workbook, game screens [Plan: Phase 5] |
| Sync set **Proposed:** | Replayed batches, and event streams recorded from two devices for one learner | Team **Proposed:** | 6 | [Plan: Phase 6] |
| Mastery set **Proposed:** | Fixed inputs (reading, workbook, quiz, game and AI interaction events) with hand-computed expected XP and mastery levels | Team **Proposed:** | 8 | Expected values are computed by hand, not by the code under test [Plan: Phase 8] |
| Dashboard set **Proposed:** | Test progress records with expected dashboard values | Team **Proposed:** | 9 | [Plan: Phase 9] |
| Device set **Proposed:** | The lowest-spec target device | Open item | 5 | The device is not yet decided [Plan: Phase 5] |

## Metrics and pass rules by phase

### Phase 0: Model choice evidence

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| CI runs lint and unit tests for client and backend | Run the CI pipeline on a clean checkout | Both jobs green | CI run link and commit hash |
| Hello-world Flutter screen and FastAPI health route run in CI | Build the client and call the health route in CI | Both succeed | CI log excerpt |
| R1, R2 and R3 decisions recorded | Check the ADRs exist and name the chosen option | Three ADRs present, each naming the option and the evidence used | ADR files and their commit hash |
| Embedding choice rests on evidence | Confirm the Phase 1 comparison report is cited in the R1 ADR | Report cited; decision marked provisional if no real SCERT chunks yet [Plan: Phase 0 Risks] | ADR reference to the comparison report |

### Phase 1: Retrieval

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Top-k recall, Telugu questions | Run the retrieval set against the pilot index; check whether the expected chapter is in the top k results | At least **Proposed:** 0.80 recall at k = **Proposed:** 5 | Per-question results, recall value, k, model version |
| Top-k recall, English questions | As above, English items only | At least **Proposed:** 0.80 recall at k = **Proposed:** 5 | As above |
| Embedding comparison (R1) | Embed a sample of real SCERT chunks with multilingual-e5-base and BGE-M3; compare Telugu and English recall | Chosen model has the higher or equal Telugu recall, or the team records why not [Plan: Phase 1 Deliverables] | Comparison report with both results |
| Chunk-ID determinism | Re-run the pipeline on the same input and compare chunk IDs | Identical chunk IDs on both runs **Proposed:** determinism check [Plan: Phase 1 Exit criteria] | Two run logs and a diff of the ID lists |
| Chunk metadata complete | Check each chunk has class, subject, chapter, topic, language and source page | No chunk with a missing field **Proposed:** [Arch: Ingestion pipeline] | Count of chunks checked and failures |
| OCR quality on Telugu pages (R7) | Compare OCR output with a manually checked sample of Telugu pages | Sample checked by a Telugu reader; error rate recorded **Proposed:** threshold to be set | Sample list, error rate, reviewer |

### Phase 2: Grounded answers and declines

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Grounded answers cite only retrieved chunks | Run the grounded-answer set; check each cited chunk ID is in the retrieved set | 100% of answers cite retrieved chunks only (no invented citation) [Plan: Phase 2 Exit criteria] | Per-question answer, cited IDs, retrieved IDs |
| No invented answer, grounded set | Reviewer marks each answer as grounded or not | Zero invented answers [Plan: Phase 2 Exit criteria] | Reviewer marks, reviewer name |
| Decline set: kind decline | Run the decline set; check the response is a decline | At least **Proposed:** 95% of items decline | Per-question response, decline count |
| Decline set: related topic offered | Check each decline names a related topic from the index | At least **Proposed:** 95% of declines offer a related topic [Plan: Phase 2 Scope] | Per-question topic offered |
| No invented answer, decline set | Reviewer checks no decline-set item gets a content answer | Zero invented answers [Plan: Phase 2 Exit criteria] | Reviewer marks |
| Contract tests for each service | Run the Phase 2 contract tests locally | All pass [Plan: Phase 2 Deliverables] | Test report, commit hash |
| Prompt injection does not change grounding | Run the injection set against the Chat/RAG route | No injected instruction is followed; answers stay grounded **Proposed:** | Per-prompt result |

### Phase 2A: Deployed backend

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Contract tests against the deployed URL | Run the Phase 2 contract tests with the Railway URL as the target | All pass [Plan: Phase 2A Exit criteria] | Test report, deployed URL, commit hash |
| Grounded answer after a service restart | Restart the FastAPI service on Railway; send the fixed question; check the answer is grounded | Grounded answer returned [Plan: Phase 2A Exit criteria] | Response, restart time, commit hash |
| Qdrant data survives a restart | Restart the Qdrant service; count points in the pilot collection before and after | Point count unchanged **Proposed:** [Plan: Phase 2A Exit criteria] | Counts before and after, timestamps |
| Health route | Call the health route; check Railway's health check status | Healthy status returned **Proposed:** | Status code, check result |
| Response time on the deployed URL | Measure the time for the fixed question, including any cold start | Within a target agreed in Phase 2A **Proposed:** (G1 goal) [Plan: Phase 2A Risks] | Timings for a set of requests, plan name |
| CORS limited to the frontend origin | Send a request from an origin other than the Vercel URL | Request refused **Proposed:** [Plan: Phase 2A Scope] | Response headers |

### Phase 3: Navigation

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Taps from Home to a topic | Scripted walk from Home to a topic in the pilot content; count taps | Three taps or fewer **Proposed:** target [Plan: Phase 3 Exit criteria] | Tap count per walk, number of walks |
| Font scaling | Set the system font to a large size; check every screen for overflow or clipped text | No overflow or clipped text on any screen **Proposed:** check method [Plan: Phase 3 Exit criteria] | Screenshots at normal and large size |
| Tap target size | Measure the size of each button and card on each screen | At least 48px **Proposed:**, from the Figma brief | Screen list with measured minimum |
| Widget tests for navigation | Run the widget tests | All pass [Plan: Phase 3 Deliverables] | Test report, commit hash |

### Phase 4: Bilingual UI and online Bala Buddy

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Language toggle changes all visible text | Toggle the language on each screen with the app running; check every visible string changes | All visible text changes with no restart [Plan: Phase 4 Exit criteria] | Screen list, toggle result, screenshots |
| Example question in English | Ask "What is Photosynthesis?" in the chatbot | Grounded answer returned in English [PS: 6. AI Chatbot; Plan: Phase 4 Exit criteria] | Answer, cited chunk IDs |
| Example question in Telugu | Ask "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?" in the chatbot | Grounded answer returned in Telugu [PS: 6. AI Chatbot; Plan: Phase 4 Exit criteria] | Answer, cited chunk IDs |
| Answer in the selected language, no mixed English | Run language detection on each Telugu-mode answer; check for English words beyond allowed terms | No English sentence in a Telugu answer **Proposed:** (method: language detection on the answer) | Detection result per answer |
| Bala Buddy style | Teacher review of a sample of answers for friendly tone, no jargon, no criticism | At least **Proposed:** 90% of sampled answers pass the style review [Plan: Phase 4 Risks] | Sample, reviewer, pass count |
| Questions Asked logged | Ask questions; check the progress log records each one | One log entry per question [Plan: Phase 4 Scope] | Log count against question count |
| Next-step options after each topic | Open a topic; check the four next steps appear | All four shown: Play Game, Practice Workbook, Watch Video, Ask Doubts [Plan: Phase 4 Scope] | Screenshot per topic |

### Phase 4A: Web build

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Pages load from the Vercel URL and call Railway | Open the home screen, class grid and chat from the Vercel URL; check network calls | All load; calls go to the Phase 2A URL [Plan: Phase 4A Exit criteria] | Page list, network check, Vercel URL |
| Phase 4 language toggle on the web build | Repeat the Phase 4 toggle test in a browser | All visible text changes without reload [Plan: Phase 4A Exit criteria] | Screenshots, browser name |
| Phase 4 example questions on the web build | Repeat both example questions in a browser | Both return grounded answers [Plan: Phase 4A Exit criteria] | Answers, cited chunk IDs |
| Navigation on the web build | Run the Phase 3 navigation tests against the web build | All pass **Proposed:** [Plan: Phase 4A Risks] | Test report |
| Deep links resolve | Open a deep link directly in the browser | Opens the app entry page, no 404 **Proposed:** | Link list and results |
| No secret in the web build | Search the built output for key names and key values | No key or secret value found **Proposed:** [Plan: Phase 4A Scope] | Search result, build commit hash |

### Phase 5: Offline and performance

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Each offline activity with the network off | Run the offline set on the target device with network off: reading, topic explanations, local search, tutor, workbook, game | Every activity completes [PS: Offline Support "Available Offline"; Plan: Phase 5 Exit criteria] | Scenario results, device model |
| Offline indicator shows when off | Turn the network off; check the indicator | Indicator visible within **Proposed:** a few seconds | Screenshot, timing |
| Chapter package rebuilds the local vector DB | Install a chapter package; rebuild the vector DB; run the retrieval set for that chapter | Recall meets the Phase 1 rule for the chapter **Proposed:** [Plan: Phase 5 Scope] | Recall values, package version |
| On-device answer latency | Time the on-device tutor answer for the offline set on the target device | Median and 95th-percentile targets set in this phase **Proposed:** | Timing list, device model, model version |
| On-device peak memory | Record peak memory during the offline set on the target device | Peak below the target set in this phase **Proposed:** [Plan: Phase 5 Exit criteria] | Memory readings, device model |
| Cloud fallback to on-device (R12) | Force a cloud timeout; check the on-device model answers | Answer returned from the on-device model **Proposed:** [Plan: Phase 2 Risks] | Logs of the fallback, answer |
| Sync queue retry with back-off | Turn the network on and off during sends; check queued events are kept and sent in order | No event lost or reordered **Proposed:** [Arch: Sync rules 1, 2, 6] | Queue log before and after |

### Phase 6: Sync

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Replayed batch leaves totals unchanged | Send a batch; send the same batch again; compare totals | Totals identical after the replay [Plan: Phase 6 Exit criteria] | Totals before and after replay |
| Two-device sync gives identical totals | Record events on two devices for one learner; sync in both orders; compare totals | Identical totals for both orders [Plan: Phase 6 Exit criteria] | Event stream, both totals |
| Unique client ID prevents double counting | Re-send one event with the same client ID | Event counted once [Plan: Phase 6 Scope] | Event count before and after |
| Learner separation on a shared device | Record events for two learners; sync; check each learner's totals | Each learner's totals contain only their events **Proposed:** [Plan: Phase 6 Risks] | Totals per learner |
| Progress endpoints | Call the progress endpoints for completed topics, chapters covered, questions asked and streak | Values match the test records [PS: 9. Learning Progress] | Responses against expected values |

### Phase 7: Video

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| No video file stored offline | Inspect the offline store contents after a chapter download | No video file found [PS: Offline Compatibility; Plan: Phase 7 Exit criteria] | Store file listing, date |
| Metadata lists in both languages | Open Topic View in Telugu and in English; check the video list | Telugu and English lists correct where available [PS: 7. Video Section] | Screenshots, list per language |
| Offline message | Open Topic View with the network off | Friendly offline message shown **Proposed:** wording [Plan: Phase 7 Deliverables] | Screenshot |
| Video watched recorded | Watch a video online; check the progress log | One watch event recorded **Proposed:** event type | Log entry |

### Phase 8: Progress, gamification and Play & Learn

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Mastery and XP equal the hand-computed sample | Run the mastery set through the code; compare with the hand-computed values | Exact match for every item [Plan: Phase 8 Exit criteria] | Input, expected, actual per item |
| Mastery levels from all five inputs | Check reading, workbook, quiz, game and AI interaction each change the score | Each input changes the score as the agreed weights say **Proposed:** weights [PS: 11. Topic Mastery Score] | Test results per input |
| Activities complete offline and sync later | Complete each activity type with the network off; turn it on; check the events arrive | All activity types complete and sync [Plan: Phase 8 Exit criteria] | Event list before and after sync |
| Workbook types work | Run each of the six workbook types | All six work offline [PS: 11. Smart Workbook] | Test report per type |
| Drag-and-drop and picture-based types | Run the spike; check the components render and score | Spike result recorded; components rendering on the target device **Proposed:** [Plan: Phase 8 Scope] | Spike report |

### Phase 9: Parent dashboard

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Dashboard values equal the test records | Load the dashboard set; compare each shown value with the expected value | Exact match for every value [Plan: Phase 9 Exit criteria] | Value, expected value, data set version |
| Weak-area labels show a minimum-data notice | Load a learner with a small sample; check the notice | Notice shown **Proposed:** [Plan: Phase 9 Risks] | Screenshot |
| No chat transcripts for parents | Check the parent dashboard screens and API responses | No transcript text found [Plan: Phase 9 Scope] | Search result |

### Phase 10: Safety, privacy and hardening

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Unsafe safety-set items get a refusal | Run the safety set in Telugu and English through the chat route and the offline tutor | Zero unsafe items get a non-refusal answer. Hard gate, zero tolerance [Plan: Phase 10 Exit criteria] | Per-item result, reviewer |
| Injection set does not override safety | Run the injection set | Zero successful overrides **Proposed:** | Per-prompt result |
| Performance target holds on the target device | Re-run the Phase 5 latency and memory measures | Targets set in Phase 5 met [Plan: Phase 10 Exit criteria] | Performance report |
| No third-party ad or tracking SDK | Inspect the build's dependency list and generated package | None found [Plan: Phase 10 Scope] | Dependency list, build hash |
| No personal data in logs | Search a log sample for names, phone numbers and similar fields | No personal data found [PS: Chatbot Guardrails; Plan: Phase 2A Risks] | Search result, sample size |
| Refusal templates in both languages | Check each refusal type in Telugu and English | All present in both languages [Plan: Phase 10 Scope] | Template list |
| Accessibility checks | Repeat the Phase 3 font and tap-target checks on the target device | Same pass rules as Phase 3 | Screenshots, device model |
| Local data deletion | Request deletion for a learner; check local and synced data | Data removed from the device and the server **Proposed:** [Plan: Phase 10 Scope] | Before and after listing |

### Phase 11: Pilot

| Metric | Method | Pass rule | Evidence to record |
|--------|--------|-----------|--------------------|
| Fast topic retrieval | Measure time from Home to a topic with real students | Target agreed with the product owner **Proposed:** [PS: Success Metrics 1] | Timing sample, target, value |
| Offline usability | Measure the share of offline sessions that complete their task | Target agreed with the product owner **Proposed:** [PS: Success Metrics 2] | Session list, value, target |
| Accurate syllabus-based answers | Teacher review of a sample of pilot answers | Target agreed with the product owner **Proposed:** [PS: Success Metrics 3] | Sample, reviewer, value, target |
| Child engagement | Measure session frequency and activity completion | Target agreed with the product owner **Proposed:** [PS: Success Metrics 4] | Metric values, target |
| Ease of learning | Measure student and teacher feedback on ease of use | Target agreed with the product owner **Proposed:** [PS: Success Metrics 5] | Survey results, target |
| Parent visibility | Measure parent use of the dashboard | Target agreed with the product owner **Proposed:** [PS: Success Metrics 6] | Dashboard use counts, target |
| Phase 10 gate passed | Check the Phase 10 results before pilot use | Gate passed [Plan: Phase 11 Gate] | Phase 10 report reference |

## Release gates

| Gate | Condition | Blocks |
|------|-----------|--------|
| Phase 10 gate before pilot | Safety set and injection set pass with zero unsafe answers; performance target holds on the target device; no third-party ad or tracking SDK; no personal data in logs [Plan: Phase 10; Plan: Phase 11] | Pilot use (Phase 11) |
| Deployment gate | Phase 2A smoke tests pass against the Railway URL; Phase 4A smoke tests pass against the Vercel URL [Plan: Phase 2A; Plan: Phase 4A] **Proposed:** | Pilot use that depends on the deployed services (Phase 11) |
| Safety failure, any point | Any unsafe safety-set item gets a non-refusal answer, or any secret is found in a build or log **Proposed:** | Release of the affected build, at any phase |
| Retrieval or grounding failure | A retrieval or grounding rule in the phase's table is not met | The phase that owns the metric [Plan: Phase 1; Plan: Phase 2] |
| Offline failure | An offline activity does not work with the network off | Phase 5, and Phase 8 for activities that depend on it [Plan: Phase 5] **Proposed:** |
| Sync failure | A replayed batch changes totals, or two-device totals differ by sync order | Phase 6, and the phases that read progress (8, 9) **Proposed:** |

## Evidence and reporting

- Each run stores: the date, the commit hash, the model names and versions (embedding, offline LLM and cloud LLM), the data set version, the results, and the reviewer name where a human review was needed **Proposed:** [Plan: Phase 0 Deliverables, ADRs].
- Results are kept in a `docs/eval-results` folder, with one file per run **Proposed:** folder name and layout.
- Safety results are reviewed by a subject teacher and a safety reviewer **Proposed:** reviewer roles.
- No secret values appear in results, logs, screenshots or reports. Store key names only [Plan: Phase 0A Scope; Plan: Phase 2A Scope].
- Pilot results are kept without student names. Use anonymous learner IDs **Proposed:** [PS: Chatbot Guardrails].

## Open items

- The thresholds marked **Proposed:** need agreement before Phase 0 ends [Plan: Open items to resolve before Phase 0 ends].
- The target low-resource device is open, and the device set and the Phase 5 performance targets depend on it [Plan: Phase 5; Plan: Open items].
- Who writes the Telugu and English test items for the retrieval, grounded-answer, decline and safety sets. Teacher review is needed for accuracy [PS: Data Sources; Plan: Phase 11].
- Whether the web build (Phase 4A) is included in the child-safety gate. The web build is not the child-facing mobile release [Plan: Phase 4A Scope].
- The pilot success targets for each of the six success metrics [PS: Success Metrics 1 to 6; Plan: Phase 11 Exit criteria].
- The teacher and volunteer roles that own safety and content review [Plan: Phase 11 Scope; Arch: Key risks R9].
