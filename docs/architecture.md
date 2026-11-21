# BAALAVIDYA - Architecture

Derived from `docs/problemStatement.md`. Items marked **Proposed:** are design decisions that the source does not state. Everything else traces to a section of the problem statement, cited in brackets such as [PS: Offline Mode].

## Overview and scope

BAALAVIDYA ("AI Powered Last-Mile Tutor") is a kid-friendly, bilingual (Telugu and English) educational mobile application for Telangana State Board students in Classes 1 to 10 [PS: Overview]. It is built on Telangana SCERT textbook and syllabus content and uses a Retrieval Augmented Generation (RAG) system so that tutor answers are grounded in that curriculum [PS: Data Sources; RAG Architecture]. The product is aimed at students with limited connectivity, shared devices and no access to tutors, and it is meant to support self-learning without a teacher [PS: Overview; Hackathon Alignment].

Primary users are Telangana State Board students in Classes 1 to 10. Secondary users are parents, teachers and volunteers [PS: Target Users]. The source describes parent visibility into progress, but does not describe teacher or volunteer features in any detail, so the scope of those roles is an open question (see Key risks and open questions).

The product runs in two modes [PS: Offline Mode; Online Mode]:

- **Offline mode:** syllabus data, embeddings and a local vector database are stored on the device, and a small on-device model handles tutoring. Only video streaming needs internet.
- **Online mode:** a cloud LLM provides richer explanations, video streaming, latest updates and cloud synchronization.

Out of scope for this document: detailed UI pixel design, the content of individual games, and the choice of final model vendors. These are noted as open questions where relevant.

## Architectural goals

Each goal is derived from the source section named in brackets.

| # | Goal | Source basis |
|---|------|--------------|
| G1 | **Fast topic retrieval.** Opening a topic, searching and asking a question should feel immediate. | [PS: Success Metrics 1; Search Functionality] |
| G2 | **Offline usability.** Chapter reading, topic explanations, workbooks, games, local RAG search and progress tracking must work with no network. | [PS: Success Metrics 2; Offline Mode; Offline Support] |
| G3 | **Accurate, syllabus-grounded answers.** Tutor responses should come from curriculum content whenever possible. | [PS: Success Metrics 3; Chatbot Guardrails 5] |
| G4 | **Low-resource device support.** The app and its on-device model must run on low-resource mobile devices. | [PS: Hackathon Alignment 6; Technical Stack] |
| G5 | **Bilingual by default.** Telugu and English content, UI and answers, with an instant language switch. | [PS: Supported Languages; Bilingual design in this document] |
| G6 | **Child engagement and child-friendly UI.** Bright, large, rounded, cartoon-style interface with gamified learning. | [PS: UI/UX Requirements; Success Metrics 4; Play & Learn] |
| G7 | **Accessibility.** Large fonts, easy navigation, minimal typing and a voice-ready design. | [PS: Accessibility; Voice Ready Design] |
| G8 | **Parent visibility.** Progress, time spent, weak areas and gamification metrics visible to parents. | [PS: Parent Dashboard; Parent Insights; Success Metrics 6] |
| G9 | **Safe, educational-only tutoring.** Child-safe, age-appropriate responses only. | [PS: Chatbot Guardrails] |
| G10 | **Shared-device friendliness.** Multiple children on one device must have their own progress. | [PS: Overview "shared devices"] — the source names shared devices as a constraint; per-learner separation is **Proposed:**. |

## System context diagram

```text
                         +-----------------------------+
                         |   Parent (dashboard view)   |
                         +--------------+--------------+
                                        |
+----------------+     +----------------v----------------+        +-----------------------+
|    Student     |---->|   Flutter mobile app (client)   |<------>|  Video source          |
|  (Bala Buddy)  |     |  Splash, Home, Subject, Topic,  |  stream|  (online only; source  |
+----------------+     |  Chatbot, Video, Play & Learn,  |        |  not named in source)  |
                       |  Progress, Parent Dashboard     |        +-----------------------+
                       +-------+-----------------+-------+
                               |                 |
               online: REST/   |                 | offline: local
               sync (HTTPS)    |                 | on-device stores
                               v                 v
                 +-------------------------+   +--------------------------------------+
                 |  FastAPI backend        |   |  On-device offline store             |
                 |  curriculum, search,    |   |  - syllabus data                     |
                 |  chat/RAG, progress,    |   |  - local vector DB (embeddings)      |
                 |  sync, analytics        |   |  - cached video metadata             |
                 +----+-----------+--------+   |  - saved progress + sync queue      |
                      |           |            |  - on-device LLM                     |
                      |           |            |    (Phi-3 Mini or Gemma 2B)          |
                      v           v            +--------------------------------------+
        +----------------+   +----------------------+
        |  Qdrant        |   |  Cloud LLM           |
        |  (vector DB,   |   |  (Azure OpenAI or    |
        |  server-side)  |   |   GPT API)           |
        +-------^--------+   +----------------------+
                |
                |  indexed embeddings
        +-------+------------------------------+        +---------------------------+
        |  Ingestion pipeline (offline batch)  |<-------|  Telangana SCERT          |
        |  extract, OCR, chunk, embed, index  |        |  textbooks / syllabus     |
        +-------+------------------------------+        +---------------------------+
                |
                v
        +-----------------------------+
        |  Azure Document Intelligence|
        |  (OCR)                      |
        +-----------------------------+
```

Notes on the diagram:

- The Flutter app talks to the FastAPI backend when online and to the on-device store when offline [PS: Offline Mode; Offline Support].
- Qdrant is the vector database named in the technical stack. The source also requires a local vector database on the device, so the server-side Qdrant instance and the on-device store are two separate deployments [PS: Technical Stack; Offline Mode 3].
- The video source is shown as an external stream. The source only says "video streaming" and "educational videos" and does not name a provider [PS: Online Mode; Topic View].
- The parent dashboard is shown as a view inside the Flutter app. The source does not say whether it is a separate app or a web page [PS: Parent Dashboard].

## Components

### Flutter client

The client is built with Flutter [PS: Technical Stack]. The screens and modules below come from the functional requirements.

| Screen or module | Responsibility | Source |
|------------------|----------------|--------|
| Splash | Shows the BAALAVIDYA logo with a fun educational theme and friendly animation. | [PS: 1. Splash Screen] |
| Home | Search bar, language toggle at top right, class selection grid (Class 1 to Class 10). | [PS: 2. Home Screen; Supported Languages] |
| Class Selection | When a class is selected, shows available subjects (Telugu, English, Mathematics, Science, Social Studies, plus Environmental Science in the data sources) and a syllabus overview. | [PS: 3. Class Selection; Data Sources] |
| Subject View | Chapters, topics and progress percentage for the subject. | [PS: 4. Subject View] |
| Topic View | Topic title, explanation, AI tutor entry, related videos, practice questions. | [PS: 5. Topic View] |
| AI Chatbot "Bala Buddy" | Conversational tutor, RAG-grounded, Telugu or English answers. | [PS: 6. AI Chatbot; 12. Bala Buddy] |
| Video Section | Relevant educational videos per topic with language-aware recommendations (Telugu and English explanation videos). | [PS: 7. Video Section] |
| Search | Searches subjects, chapters, topics and concepts; results link to class and subject, related videos and "Ask Tutor". | [PS: 8. Search Functionality] |
| Learning Progress | Completed topics, chapters covered, questions asked, learning streak. | [PS: 9. Learning Progress] |
| Parent Dashboard | Learning progress, time spent, subjects completed, weak areas. | [PS: 10. Parent Dashboard; Parent Insights] |
| Play & Learn module | Smart workbook, learning games, rewards, unlockables, mastery display, mission challenges, story mode for Classes 1 to 5. | [PS: 11. Play & Learn Module; 12. Bala Buddy] |

Client-side design notes:

- Large fonts, rounded cards, large buttons and fun icons are required [PS: UI/UX Requirements; Accessibility].
- Navigation should be easy and typing should be minimal. Class and subject selection use grids and taps rather than free text [PS: Accessibility 3, 4].
- The client holds the offline store and the sync queue (see Offline and sync design).
- **Proposed:** a state-management approach and a local database library are not named in the source and are left to the implementation.

### FastAPI backend

The backend is built with FastAPI [PS: Technical Stack]. The source lists the functional areas below. Route layout is **Proposed:**.

| API service | Responsibility | Source |
|-------------|----------------|--------|
| Curriculum | Returns classes, subjects, chapters, topics and per-language content. | [PS: Database Structure; Class Selection] |
| Search | Keyword and concept search over subjects, chapters, topics and concepts. Uses Qdrant for semantic matching. | [PS: Search Functionality; Technical Stack] |
| Chat / RAG | Accepts a student question and language, calls the retriever, builds the grounded prompt and calls the cloud LLM. | [PS: AI Chatbot; RAG Architecture] |
| Progress | Stores and returns learner progress: completed topics, chapters, questions asked, streak, mastery. | [PS: Learning Progress; Topic Mastery System] |
| Sync | Receives queued offline progress and returns server updates. | [PS: Offline Mode 5] |
| Analytics | Aggregates progress into parent-facing metrics (time spent, weak areas, completion rates). | [PS: Parent Insights] |

**Proposed:** route prefixes such as `/v1/classes`, `/v1/search`, `/v1/chat`, `/v1/progress`, `/v1/sync` and `/v1/analytics`, with JSON bodies and bearer-token auth. The source does not define an API surface.

### Ingestion pipeline

An offline batch pipeline that turns SCERT textbook content into searchable embeddings [PS: Data Ingestion Pipeline].

1. **Fetch** Telangana SCERT curriculum and textbook content from the SCERT and state e-textbook websites listed in "Source websites (ingestion to RAG)" (Proposed).
2. **Extract** chapter and topic structure.
3. **Text extraction with OCR** for scanned or image-based content, using Azure Document Intelligence [PS: RAG Architecture "Text Extraction"; Technical Stack OCR].
4. **Chunking**, splitting content into retrievable pieces tied to a topic and a language.
5. **Embeddings** using either multilingual-e5-base or BGE-M3 [PS: Technical Stack].
6. **Indexing** embeddings into Qdrant. A packaged subset is also produced for offline download [PS: Offline Mode 2, 3].

**Proposed:** each chunk stores metadata (class, subject, chapter, topic, language, source page) so that answers can cite a chapter and so that the offline package can be built per chapter.

The source does not say how SCERT content is obtained, whether it is re-fetched on a schedule, or what licence applies. These are open questions.

### Retrieval and RAG

The RAG path follows the flow in the source: Retriever, then AI Tutor, then Student Response [PS: RAG Architecture].

- **Retriever:** embeds the student's question with the same embedding model used for indexing. Queries Qdrant (online) or the local vector DB (offline) for the top matching chunks, filtered by class and subject where known [PS: Search; Offline Mode 3].
- **Syllabus-only grounding:** the prompt instructs the model to answer from the retrieved chunks. When no chunk matches, the tutor should say so kindly and offer a related topic instead of inventing an answer [PS: Data Ingestion "strictly answer based on syllabus-aligned content"; Chatbot Guardrails 5].
- **Guardrails:** educational-only responses, child-safe content, age-appropriate language, and no harmful or inappropriate information [PS: Chatbot Guardrails 1 to 4]. The guardrail rules are enforced in the prompt and in an output filter. **Proposed:** an output filter as a second check, since the source states only the rules.
- **Language:** the answer is produced in the language the student selected (Telugu or English) [PS: AI Chatbot "Telugu answers / English answers"].
- **Style:** simple explanations, examples, encouragement, no difficult terminology [PS: AI Chatbot "Responses must"; Bala Buddy Communication Style].

The Telugu question example ("కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?") shows that Telugu queries must be supported end to end, including embedding and retrieval. Whether the chosen embedding model handles Telugu well is an open question (see Key risks).

### LLM routing

Selection between the on-device model and the cloud model is by connectivity [PS: Offline Mode; Online Mode; Offline Support].

| Condition | Model used | Source |
|-----------|-----------|--------|
| No network, or network too weak | On-device LLM: Phi-3 Mini or Gemma 2B | [PS: Technical Stack "Offline LLM"; Offline Support] |
| Network available | Cloud LLM: Azure OpenAI or GPT API, for enhanced and advanced responses | [PS: Technical Stack "Cloud LLM"; Online Mode; Offline Support "Advanced AI responses"] |

**Proposed:** the routing rule uses a connectivity check plus a fallback. If a cloud call fails or times out, the app answers with the on-device model rather than showing an error. The source does not describe failure handling.

Both models receive the same grounded prompt and retrieved context, so guardrails are shared. **Proposed:** a single prompt template for both models.

### Gamification engine

Implements the Play & Learn module and Bala Buddy rewards [PS: 11. Play & Learn; 12. Bala Buddy].

- **XP and levels:** learning points and experience points are earned for completed activities. Total XP and current level are shown to parents [PS: Learning Rewards; Parent Insights].
- **Stars, coins, badges and certificates:** rewards for completing activities. Examples include Explorer Badge, Math Champion Badge and Reading Hero Badge [PS: Learning Rewards; Achievements and Rewards].
- **Mastery levels per topic:** Beginner, Learning, Practicing, Mastered. Calculated from reading progress, workbook completion, quiz scores, game scores and AI interactions [PS: Topic Mastery Score; Topic Mastery System].
- **Unlockables:** new games and rewards unlock when chapters, workbooks or practice sessions are completed [PS: Progress-based Unlockables].
- **Mission challenges:** at the end of each chapter, Bala Buddy presents a Mission Challenge combining quiz, puzzle, scenario or activity and mini game. Rewards are chapter badge, bonus XP and new challenges [PS: End-of-Chapter Challenge; Mission Challenges].
- **Personalized practice:** when a student struggles, the engine asks the RAG layer for simpler explanations and generates extra workbook and game items [PS: AI Generated Personalized Practice; Personalized Learning].

**Proposed:** the exact XP formula, the level thresholds, and the weighting of the four mastery inputs are not defined in the source. They need a product decision.

Workbook activity types (fill in the blanks, match, MCQ, true/false, drag and drop, picture-based) are generated per topic [PS: Smart Workbook]. Game lists per subject are given in the source [PS: Learning Games].

### Offline store and sync

On-device storage that makes offline mode work [PS: Offline Mode; Offline Support].

- **Local syllabus data:** chapter and topic content per language.
- **Local vector DB:** embeddings for the downloaded chapters, used by the on-device RAG search.
- **On-device LLM:** Phi-3 Mini or Gemma 2B, loaded for tutoring without internet.
- **Cached video metadata:** titles and language tags, so the video list shows offline. Video files are streamed online only [PS: Offline Compatibility "Only video streaming requires internet"].
- **Saved progress and sync queue:** progress events written locally and sent when a connection returns [PS: Offline Mode 5].

The sync rules are described in the Offline and sync design section.

### Parent insights

A view for parents, fed by the Analytics service [PS: Parent Insights; Parent Dashboard].

- Learning progress, time spent, subjects completed and weak areas.
- Topics learned, games completed, learning streak, badges earned, strength areas.
- Workbook completion rate, game performance, weak concepts, improvement areas.
- Total XP and current level.

**Proposed:** parents see a summary, not the child's chat transcripts. The source lists metrics and does not mention chat history visibility. See the privacy section.

## Data flow

### (a) Ingestion pipeline

1. A pipeline job fetches SCERT textbook content for a class and subject [PS: Ingestion 1].
2. The extractor reads chapter and topic structure from the text [PS: Ingestion 2].
3. Scanned pages or images go to Azure Document Intelligence for OCR [PS: Technical Stack OCR].
4. Text is chunked and each chunk is tagged with class, subject, chapter, topic and language [Proposed: metadata fields].
5. Each chunk is embedded with multilingual-e5-base or BGE-M3 [PS: Ingestion 3; Technical Stack].
6. Embeddings are written to Qdrant [PS: Ingestion 4].
7. The same records are packaged per chapter for the offline download [PS: Offline Mode 1, 2, 3].

### (b) Student asks a question in Telugu or English through Bala Buddy

1. The student types or taps a question in the chatbot, selecting Telugu or English through the language toggle [PS: AI Chatbot; Supported Languages].
2. The Flutter client checks connectivity [PS: Offline Mode].
3. **Online:** the client sends the question and language to the Chat/RAG API.
   **Offline:** the client uses the on-device retriever and on-device LLM.
4. The retriever embeds the question and fetches the top chunks from Qdrant (online) or the local vector DB (offline) [PS: RAG Architecture "Retriever"].
5. The prompt includes the retrieved chunks, the guardrail rules and the Bala Buddy persona [PS: Chatbot Guardrails; Bala Buddy Character Personality].
6. The model answers in the selected language, in simple words with an example [PS: AI Chatbot "Responses must"].
7. The output passes the guardrail check [Proposed: output filter].
8. The answer is shown. The question is logged as "Questions Asked" in progress [PS: Learning Progress "Questions Asked"].
9. Bala Buddy offers next steps: Play Game, Practice Workbook, Watch Video or Ask Doubts [PS: Interactive Learning].

### (c) Student opens a topic and watches a video

1. The student taps a class, then a subject, then a chapter and a topic [PS: Home, Class Selection, Subject View, Topic View].
2. The Topic View loads the title and explanation for the selected language from local or cached data [PS: Topic View; Topic Explanations].
3. The Video Section lists videos for the topic, filtered by language, with Telugu and English explanation videos shown where available [PS: Video Section].
4. If online, the student taps a video and it streams from the video source [PS: Online Mode "Video Streaming"].
5. If offline, the video list shows from cached metadata, and streaming is disabled with a friendly message [PS: Offline Compatibility; Cached Videos Metadata]. The message wording is **Proposed:**.
6. Watching a video is recorded as a progress event for the topic [Proposed: progress event type; source says progress is tracked, not which events].
7. Mastery for the topic is recalculated [PS: Topic Mastery Score].

### (d) Offline usage and later sync

1. Before going offline, the student (or a parent or volunteer) downloads a chapter. The download includes topic content, workbook activities, educational games and progress tracking [PS: Offline Compatibility "Downloaded chapters should include"].
2. While offline, the student uses chapter reading, topic explanations, local RAG search, the on-device tutor, workbooks, games and progress tracking [PS: Offline Support].
3. Every progress event (topic read, workbook answer, game score, question asked) is written to the local store and added to the sync queue [PS: Offline Mode 5; Saved Progress].
4. When connectivity returns, the client sends queued events to the Sync API in order [Proposed: ordering and batching].
5. The server merges events into the learner's record and returns updated mastery, XP and unlockables [PS: Progress tracking; Progress-based Unlockables].
6. The client clears sent events from the queue after an acknowledgement [Proposed: acknowledgement rule].
7. The Analytics service updates parent views [PS: Parent Insights].

## Source websites (ingestion to RAG)

Proposed: the websites below are the sources and services used at each stage. The problem statement does not name them. Each URL must be checked before use, and the SCERT portal's terms of use must be read before any content is downloaded.

| Stage | Website | Used for | Status |
|-------|---------|----------|--------|
| 1. Fetch curriculum and textbooks | https://scert.telangana.gov.in | Telangana SCERT: official curriculum and textbook publications | Proposed |
| 1. Fetch curriculum and textbooks | https://textbooks.telangana.gov.in | Telangana state e-textbook portal (PDF textbooks by class and subject) | Proposed |
| 2 and 3. Extract text and OCR | https://learn.microsoft.com/azure/ai-services/document-intelligence/ | Azure Document Intelligence: OCR for scanned or image-based pages | Proposed |
| 5. Embeddings | https://huggingface.co/intfloat/multilingual-e5-base | multilingual-e5-base embedding model | Proposed |
| 5. Embeddings | https://huggingface.co/BAAI/bge-m3 | BGE-M3 embedding model | Proposed |
| 6. Index into vector DB | https://qdrant.tech/documentation/ | Qdrant: server-side vector database | Proposed |
| 6. Index into vector DB | https://qdrant.tech/documentation/guides/installation/ | Qdrant installation and deployment options | Proposed |
| Retrieval and generation (online) | https://learn.microsoft.com/azure/ai-services/openai/ | Azure OpenAI: cloud LLM option | Proposed |
| Retrieval and generation (online) | https://platform.openai.com/docs | GPT API: cloud LLM option | Proposed |
| Retrieval and generation (offline) | https://huggingface.co/microsoft/Phi-3-mini-4k-instruct | Phi-3 Mini: on-device LLM option | Proposed |
| Retrieval and generation (offline) | https://huggingface.co/google/gemma-2b | Gemma 2B: on-device LLM option | Proposed |
| Backend | https://fastapi.tiangolo.com | FastAPI backend framework | Proposed |
| Client | https://flutter.dev | Flutter mobile client framework | Proposed |

Pipeline order: fetch (SCERT sites) -> extract and OCR (Azure Document Intelligence) -> chunk -> embed (multilingual-e5-base or BGE-M3, from the model hub) -> index (Qdrant) -> retrieve (Qdrant online, local vector DB offline) -> generate (cloud LLM online, Phi-3 Mini or Gemma 2B offline) -> student response.

Proposed: if the SCERT portal does not allow automated download, content is supplied by hand as a versioned set of PDFs. This is an open question (see R6).

## Data model

The source gives the entity list: Class, Subject, Chapter, Topic, Language, Content, Videos, Embeddings and Progress [PS: Database Structure]. Key fields below are **Proposed:** unless marked otherwise, since the source names entities but not fields.

| Entity | Purpose | Key fields (Proposed) | Relationships |
|--------|---------|------------------------|---------------|
| Class | One of Classes 1 to 10. | `class_id`, `number` (1 to 10) | has many Subjects |
| Subject | Telugu, English, Mathematics, Science, Social Studies, Environmental Science. | `subject_id`, `class_id`, `name` | belongs to Class; has many Chapters |
| Chapter | Chapter from SCERT textbook. | `chapter_id`, `subject_id`, `order`, `title` | belongs to Subject; has many Topics |
| Topic | Teachable unit inside a chapter. | `topic_id`, `chapter_id`, `order`, `title` | belongs to Chapter; has Content per Language, Videos and Embeddings |
| Language | Telugu or English. | `code` (te, en) | referenced by Content, Videos and Embeddings |
| Content | Explanation text for a topic in one language. Also holds workbook and game definitions. | `content_id`, `topic_id`, `language_code`, `body`, `source_ref` | belongs to Topic and Language |
| Videos | Educational video for a topic. Metadata is cached offline. | `video_id`, `topic_id`, `language_code`, `title`, `url`, `duration` | belongs to Topic and Language |
| Embeddings | Vector for a content chunk. Stored in Qdrant (server) and in the local vector DB (device). | `embedding_id`, `content_id` or chunk id, `model`, `vector`, `chunk_text` | belongs to Content chunk; indexed for search |
| Progress | Links a learner to topics, workbooks, games and mastery. | `learner_id`, `topic_id`, `reading_pct`, `workbook_pct`, `quiz_score`, `game_score`, `mastery_level`, `xp`, `updated_at` | learner to Topic (many); links to Workbook, Game and Mastery |

Other entities implied by the source and not listed in the database section: **Learner** (student profile), **Parent**, **Workbook**, **Game**, **Badge** and **Unlockable**. These are **Proposed:** and are needed for the Play & Learn and Parent Dashboard features.

Relationships in short:

- Class has Subjects. Subject has Chapters. Chapter has Topics.
- Topic has Content per Language, Videos and Embeddings.
- Progress links a Learner to Topics, Workbooks, Games and Mastery.

## Bilingual design

- Every topic has content in Telugu and English [PS: Supported Languages; Topic View; Video Section].
- The language toggle sits at the top right of the app and switches the UI and content instantly [PS: Supported Languages].
- The chatbot answers in the language the student selected. The sample answers in the source show Bala Buddy speaking Telugu and English in the same friendly style [PS: Bala Buddy Communication Style].
- Telugu and English videos are both recommended when available [PS: Video Section].
- Embeddings and retrieval must handle Telugu and English. The two candidate models are both multilingual, but the source does not say which handles Telugu better (see open questions).
- **Proposed:** the Telugu UI strings and the English UI strings are stored as resource files so the toggle changes the language without reloading the app.
- Telugu game names (Akshara Match, Word Formation Game, Sentence Building Challenge) are language-specific [PS: Learning Games "Telugu"].

## Offline and sync design

### What is downloaded per chapter

Per the source, a downloaded chapter includes [PS: Offline Compatibility; Offline Mode]:

- Topic content (both languages, where available).
- Workbook activities for every topic in the chapter.
- Educational games for the chapter.
- Progress tracking for the chapter.
- Embeddings and the local vector DB slice for the chapter, so local RAG search works.
- Cached video metadata (titles and links, not video files).

**Proposed:** the offline package for a chapter is versioned, so a client can tell when the content has been updated.

### What needs internet

- **Video streaming only** [PS: Offline Compatibility; Online Mode].
- Cloud LLM answers, advanced AI responses, latest updates, cloud sync and enhanced recommendations [PS: Offline Support "Available Online"].

Everything else works offline: tutor conversations on the on-device model, topic explanations, workbooks, games and progress tracking [PS: Offline Support "Available Offline"].

### Sync rules

The source says progress syncs "when internet is available" and that cloud synchronization happens online [PS: Offline Mode 5; Offline Support]. The rules below are **Proposed:**.

1. Progress events are written locally first, always. The UI never waits for the network.
2. Events are sent in the order they occurred, in batches.
3. The server stores each event with a unique client ID so a re-sent event is not counted twice.
4. **Conflict policy:** progress is append-only. Server and device events are both kept as separate events, and mastery and XP are recomputed from the event log. Simple "last write wins" is not used for scores.
5. Content updates flow one way from server to device, through the versioned chapter package.
6. The sync queue is kept after a failed send and retried with back-off.
7. A learner's data is never sent to another learner's account. The sync is tied to the learner ID on the device.

### Vector DB sync strategy

The source requires a local vector database but does not say how it stays current [PS: Offline Mode 3]. **Proposed:** the local vector DB is rebuilt from the versioned chapter package. It is not synced item by item. This is one of the open questions.

## Security, safety and child privacy

### Guardrails stated in the source

- Educational responses only [PS: Chatbot Guardrails 1; AI Chatbot "Educational only"].
- Child-safe content [PS: Chatbot Guardrails 2].
- Age-appropriate language [PS: Chatbot Guardrails 3; Responses must].
- No harmful or inappropriate information [PS: Chatbot Guardrails 4].
- Answers stay within syllabus context whenever possible [PS: Chatbot Guardrails 5].
- Bala Buddy never criticizes students, never discourages learners and never uses complex jargon [PS: Bala Buddy Character Personality].

### Recommendations (not stated in the source)

Each item below is **Proposed:**, because the source does not state it.

- An output safety filter, separate from the prompt, that checks every answer before it is shown.
- A refusal template in both languages for off-topic or unsafe questions.
- Logging of questions for review, with strict access control and a retention limit. The source does not ask for chat logs.
- Child data minimisation: store only what the progress features need.
- Parent consent and account linking to child profiles. The source does not describe how a parent gets access.
- Age-gating of the cloud LLM route, if the cloud provider's terms require it for minors. This needs a legal review.
- No third-party ad or tracking SDKs in a children's app.
- Encryption of local storage on shared devices, since the source names shared devices as a constraint.
- Local data deletion when a learner or parent asks for it.

### Parent visibility

Parents see progress and metrics [PS: Parent Dashboard; Parent Insights]. The source lists these metrics: topics learned, games completed, learning streak, badges earned, weak concepts, strength areas, workbook completion rate, game performance, improvement areas, total XP and current level. Parents do not appear to be given chat transcripts in the source. **Proposed:** keep it that way unless the product owner decides otherwise.

## Deployment and runtime considerations

- **Low-resource Android devices.** The app and the on-device model must run on low-resource mobile devices [PS: Hackathon Alignment 6]. The on-device model choice (Phi-3 Mini or Gemma 2B) should be sized against the device targets. **Proposed:** a minimum device spec, which the source does not give.
- **Shared devices.** Several children may use one device [PS: Overview]. Each learner should have a separate profile and separate progress. **Proposed:** a learner switch on the Home screen.
- **Limited bandwidth.** The app must work offline and sync later. Video streaming is the only online-only feature [PS: Offline Mode; Offline Compatibility]. **Proposed:** a setting to download over Wi-Fi only, and a low-bandwidth video quality option.
- **Startup.** The Splash screen is the first screen [PS: Splash Screen]. Animation should not delay the Home screen when the user is offline. **Proposed:** the splash animation runs while the local store opens.
- **Backend hosting.** Qdrant and the FastAPI backend are server-side [PS: Technical Stack]. Hosting location and cloud region are not stated in the source.
- **Model packaging.** The on-device model must ship with or be downloaded by the app. The source does not say which. **Proposed:** a one-time download on first install with Wi-Fi.

## Key risks and open questions

| # | Question or risk | Options from the source | Notes |
|---|------------------|-------------------------|-------|
| R1 | Embedding model choice. | multilingual-e5-base or BGE-M3 [PS: Technical Stack] | Need a Telugu retrieval test on real SCERT chunks before choosing. Size also matters on low-resource devices. |
| R2 | Offline LLM choice. | Phi-3 Mini or Gemma 2B [PS: Technical Stack] | Trade-off between answer quality, model size and speed on low-resource devices. Telugu quality must be tested. |
| R3 | Cloud provider choice. | Azure OpenAI or GPT API [PS: Technical Stack] | Decision depends on hosting, pricing, data-residency and child-safety requirements. |
| R4 | Vector DB sync strategy for offline use. | Not stated in source | Proposed: rebuild from a versioned chapter package. Needs a size check. |
| R5 | Video licensing and source. | Not stated in source. The source says "educational videos" and "video streaming". | Must confirm rights to stream each video. Source of videos is not named. |
| R6 | SCERT content acquisition and licence. | "Fetch Telangana SCERT curriculum" [PS: Ingestion 1] | How content is fetched and whether it may be redistributed inside an offline package is not stated. Proposed sources: the websites in "Source websites (ingestion to RAG)"; terms of use not yet checked. |
| R7 | Telugu OCR and text extraction quality. | Azure Document Intelligence [PS: Technical Stack] | Quality on Telugu script must be checked. |
| R8 | Mastery and XP formulas. | Inputs listed, no weights [PS: Topic Mastery Score] | Needs product decision and testing with children. |
| R9 | Teacher and volunteer roles. | Listed as secondary users [PS: Target Users] | No features are described for them. |
| R10 | Voice support. | "Future scope" [PS: AI Chatbot; Voice Ready Design] | Architecture keeps the chat input and output separate so speech can be added later. Voice engines are not chosen. |
| R11 | Child privacy and consent. | Guardrails only [PS: Chatbot Guardrails] | Needs legal review, see Security section. |
| R12 | Failure handling when online calls fail. | Not stated in source | Proposed: fall back to on-device model. |

Source items not clearly mapped to a component:

- "Achievement Certificates" [PS: Learning Rewards] are listed as a reward type but no component owns certificate generation. **Proposed:** the Gamification engine.
- "Latest Updates" [PS: Online Mode] has no defined content source. **Proposed:** the Curriculum API.
- "Generate Revision Notes" [PS: AI Tutor Capabilities 7] is an AI capability with no defined output format. **Proposed:** the Chat/RAG API.
- "Learning Streak" [PS: Learning Progress] needs a definition of a day. Not stated.
- "Coins" [PS: Bala Buddy Achievements] are named in Bala Buddy but not in the Learning Rewards list. Both lists should be reconciled.
- "Drag and Drop" and "Picture-based Questions" workbook types [PS: Smart Workbook] need asset and rendering components not described in the source.
- "Story Mode" for Classes 1 to 5 [PS: Story-Based Learning; Story Mode] has no defined content pipeline. The source does not say how stories are authored.

## Glossary

- **RAG (Retrieval Augmented Generation):** a method in which the system first retrieves relevant passages from a trusted source and then asks a language model to write an answer using only those passages. In BAALAVIDYA the trusted source is the SCERT syllabus [PS: RAG Architecture].
- **Embeddings:** numeric vectors that represent the meaning of a piece of text, so that similar meanings are close to each other. Used for search and retrieval [PS: Technical Stack "Embeddings"].
- **Chunking:** splitting a long text, such as a textbook chapter, into smaller pieces that can be embedded and retrieved separately [PS: RAG Architecture "Chunking"].
- **Vector database:** a database that stores embeddings and finds the nearest ones to a query. Qdrant is the server-side choice; the device needs a local equivalent [PS: Technical Stack "Vector Database"; Offline Mode].
- **OCR (Optical Character Recognition):** reading text from images or scanned pages. Azure Document Intelligence is the named service [PS: Technical Stack "OCR"].
- **Mastery levels:** the four stages each topic moves through: Beginner, Learning, Practicing and Mastered [PS: Topic Mastery Score].
- **Bala Buddy:** the AI learning companion inside BAALAVIDYA. It is a friendly guide that teaches, encourages and recommends next steps, and it is not a generic chatbot [PS: 12. Bala Buddy].
- **Syllabus grounding:** the rule that answers should come from the Telangana SCERT syllabus content whenever possible [PS: Chatbot Guardrails 5].
- **Sync queue:** the list of progress events stored on the device and waiting to be sent when the network returns. **Proposed:** term used in this document.
