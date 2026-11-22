# ADR 0009: Video Source, Licensing, and Streaming Strategy (Risk R5)

## Status

Accepted.

## Context

The BAALAVIDYA problem statement and architecture require topic-related educational videos in Telugu and English for every topic [PS: 7. Video Section; Arch: Data model, Videos].
Furthermore:
1. Videos must be streamed **online only** [PS: Online Mode "Video Streaming"; Offline Compatibility "Only video streaming requires internet"].
2. **No video files may be downloaded or stored offline** on student devices [PS: Offline Compatibility; Phase 7 Exit Criteria].
3. Video metadata (titles, durations, language tags, streaming endpoints) must be cached offline in versioned chapter packages so that students can browse available lessons even when offline [Arch: Offline store and sync; Data flow (c) step 5].
4. An Architecture Decision (R5) is required to close open question R5 regarding content licensing, copyright compliance, student safety (no third-party tracking or ads), and streaming delivery on low-bandwidth networks.

## Decision

1. **Authorized Video Sources & Open Licensing:**
   - Primary source: Official **SCERT Telangana e-Vidya** and **T-SAT Vidya / Nipuna** educational television broadcast archives, released under State Open Educational Licensing for public school instruction.
   - Secondary source: **DIKSHA** (Digital Infrastructure for Knowledge Sharing - National Open Educational Resources) aligned to Telangana state curriculum under Creative Commons Attribution-NonCommercial (CC-BY-NC 4.0).
   - No unlicensed or ad-monetized third-party commercial content is used.

2. **Online-Only Streaming via Adaptive HLS / HTTPS:**
   - Video content is served strictly as online streaming media over HTTPS / HLS (HTTP Live Streaming).
   - Video media binaries (`.mp4`, `.ts`, video segments) are **never downloaded or stored** in the local SQLite/Drift database, app cache, or device filesystem.
   - Low-bandwidth adaptive bitrate options are provided (360p Data Saver, 480p Standard, 720p HD) to accommodate weak rural mobile networks [Arch: Limited bandwidth].

3. **Bilingual Pairing per Topic:**
   - Every pilot topic is paired with both a Telugu explanation video and an English explanation video where available [PS: 7. Video Section Example].
   - Topic views provide intuitive language filtering and switching between Telugu and English video lessons.

4. **Offline Metadata Caching and Friendly Fallback:**
   - When a chapter package is downloaded, only lightweight JSON metadata (titles, durations, language tags, stream URLs) is saved to the on-device `OfflineStore`.
   - When offline, video listings display with an "Online Stream Only" badge.
   - Tapping an offline video opens a friendly bilingual notice:
     - English: *"Video streaming requires an active internet connection. Please connect to Wi-Fi to stream video lessons! Your textbook lessons, Bala Buddy tutor, workbooks, and games remain fully available offline."*
     - Telugu: *"వీడియో స్ట్రీమింగ్‌కు ఇంటర్నెట్ కనెక్షన్ అవసరం. ఈ పాఠం వీడియో చూడటానికి దయచేసి ఇంటర్నెట్ లేదా వై-ఫైకి కనెక్ట్ అవ్వండి! గమనిక: మీ పాఠ్యపుస్తక పాఠాలు, బాల బడ్డీ ట్యూటర్, వర్క్‌బుక్‌లు మరియు ఆటలు ఆఫ్‌లైన్‌లో కూడా పనిచేస్తాయి."*

5. **Progress Attribution:**
   - Watching an educational video is recorded as a progress event (`video_watched`) with unique event and client IDs [Arch: Data flow (c) step 6; Sync Rule 3].
   - The event is enqueued in `SyncQueueService` locally first, awarding +15 XP upon watching, and syncing idempotently to the server.

## Consequences

- **Child Safety:** Ad-free, tracking-free streaming protects children from external advertisements or non-educational algorithms.
- **Storage Feasibility:** Eliminates multi-gigabyte video storage requirements, ensuring compatibility with entry-level Android devices (16 GB / 32 GB storage).
- **Compliance:** Full compliance with Phase 7 Exit Criterion: *"No video file is stored offline"*.
- **Low Bandwidth:** Low-data quality tier (360p) allows continuous streaming even on 2G/3G rural networks.

## Revisit-by

Review when expanding beyond the Class 10 pilot to Classes 1-9 or when integrating state CDN video hosting infrastructure.
