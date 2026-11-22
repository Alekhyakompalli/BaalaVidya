# BAALAVIDYA Client (Flutter)

Child-facing mobile and web client for **BAALAVIDYA** — a bilingual (Telugu and English) AI-powered learning companion for school children.

## Tech Stack & Architecture

- **Framework:** Flutter (Material 3)
- **Language:** Dart (SDK >= 3.4.0 < 4.0.0)
- **State Management:** Flutter Riverpod (`flutter_riverpod: ^2.5.1`)
- **Offline Storage:** Drift (`drift: ^2.20.0`), `sqlite3_flutter_libs`
- **Design System:**
  - **Primary Colors:** Fun Sky Blue (`#1E88E5`) and Sunshine Yellow (`#FFB300`)
  - **Secondary Colors:** Meadow Green (`#43A047`) and Coral Orange (`#FF7043`)
  - **Typography:** Large, accessible fonts with dynamic scaling support (`TextScaler`)
  - **Cards & Buttons:** 20px rounded corners, tactile shadows, min 48px tap targets

---

## Directory Structure

```
client/
├── lib/
│   ├── main.dart                      # App entrypoint with ProviderScope & MaterialApp
│   ├── models/
│   │   ├── curriculum_models.dart     # Class, Subject, Chapter, Topic models
│   │   └── mock_data.dart             # Pilot curriculum data (Class 10 Biology, Math, Telugu)
│   ├── screens/
│   │   ├── splash_screen.dart         # Animated BAALAVIDYA logo & auto-transition
│   │   ├── home_screen.dart           # Search bar, language toggle, Class 1-10 grid, tappable progress hero, Parent Zone entry
│   │   ├── class_selection_screen.dart# Subjects list, syllabus overview & Story Mode launcher
│   │   ├── subject_view_screen.dart   # Progress bar, chapters & topics list, Chapter Mission Challenge
│   │   ├── topic_view_screen.dart     # Concept explanation, mastery badge, AI tutor entry, videos, 4 Next Steps
│   │   ├── workbook_screen.dart       # Smart Workbook with 6 activity types (MCQ, Fill in blanks, Match, True/False, Drag & Drop, Picture-based)
│   │   ├── game_screen.dart           # Chapter-specific educational games across 5 subjects (Math, Science, Social, English, Telugu)
│   │   ├── mission_challenge_screen.dart # 4-part End-of-Chapter Mission Challenge (Quiz, Puzzle, Scenario, Mini Game)
│   │   ├── story_mode_screen.dart     # Interactive narrative story adventure for Classes 1 to 5 (Bala Rabbit division)
│   │   ├── personalized_practice_screen.dart # AI Generated personalized practice with analogies for struggling learners
│   │   ├── learning_progress_screen.dart # Full Learning Progress, Level, Streak, Coins, Topic Mastery & Badges
│   │   └── parent_dashboard_screen.dart  # Parent Dashboard with PIN gate, time spent, weak concepts & zero chat transcripts (Phase 9)
│   ├── state/
│   │   └── app_state.dart             # Riverpod state providers (language, XP, level, coins, badges, mastery, certificates)
│   ├── services/
│   │   ├── analytics_service.dart     # Parent analytics aggregator & PIN gate verification with offline fallback (Phase 9)
│   │   ├── offline_store.dart         # SQLite / Drift offline chapter store, games, workbooks, certificates & vector slice
│   │   ├── on_device_tutor.dart       # On-device grounded RAG tutor engine
│   │   └── sync_queue_service.dart    # Offline event queue with exponential backoff & batch dispatch
│   ├── theme/
│   │   └── app_theme.dart             # Palette, typography, card and button styles
│   └── widgets/
│       ├── class_card.dart            # Grid card for classes (Class 1 to 10)
│       ├── subject_card.dart          # Subject overview card with progress indicator
│       ├── chapter_card.dart          # Expandable chapter card with topic list
│       ├── language_toggle.dart       # Instant bilingual toggle (EN <-> తెలుగు)
│       ├── learner_switcher.dart      # Shared-device multi-learner profile selector
│       ├── offline_banner.dart        # Visual indicator when running in offline mode
│       ├── next_steps_bar.dart        # 4 interactive actions (Play Game, Workbook, Video, Doubts)
│       ├── video_section_widget.dart  # Bilingual video section with adaptive streaming & offline notice
│       ├── certificate_widget.dart    # Achievement Certificate card & interactive dialog
│       └── pilot_feedback_dialog.dart # Phase 11 Pilot feedback dialog for students, teachers, parents, and volunteers
└── test/
    ├── widget_test.dart               # Splash & Home screen rendering tests
    ├── navigation_test.dart           # 3-tap navigation walk from Home to Topic View
    ├── accessibility_test.dart        # 2.0x font scaling & 48px tap targets verification
    ├── phase6_sync_test.dart          # Learner profile switching and sync queue isolation tests
    ├── phase7_video_test.dart         # Phase 7 bilingual video metadata, streaming & offline notice tests
    ├── phase8_gamification_test.dart  # Phase 8 Mastery hand-computed sample, 6 workbook types, 5 subject games, mission challenge tests
    ├── phase9_parent_dashboard_test.dart # Phase 9 Parent dashboard values match underlying records, PIN gate & child privacy tests
    ├── phase10_safety_hardening_test.dart # Phase 10 Offline safety refusals, data purge & low-resource device benchmarks
    └── phase11_pilot_test.dart        # Phase 11 Pilot feedback dialog, bilingual strings & rating tests
```

---

## Running the App & Tests

### Running Tests in Flutter
```bash
flutter pub get
flutter test
```

### Running Static Analysis
```bash
flutter analyze
```

### Running the App (Web / Android / Windows)
```bash
flutter run -d chrome
# or
flutter run -d windows
```

---

## Navigation Flow (Exit Criteria: <= 3 Taps)

1. **Home Screen:** Child taps **Class 10** (`ClassCard`) -> **[Tap 1]**
2. **Class Selection Screen:** Child taps **Biology** (`SubjectCard`) -> **[Tap 2]**
3. **Subject View Screen:** Child taps **What is Photosynthesis?** (`ChapterCard` topic) -> **[Tap 3]**
4. **Topic View Screen Reached!**
   - Concept Explanation
   - AI Tutor Entry ("Ask Bala Buddy")
   - Related Videos
   - Practice Questions
   - 4 Next Steps: Play Game, Practice Workbook, Watch Video, Ask Doubts
