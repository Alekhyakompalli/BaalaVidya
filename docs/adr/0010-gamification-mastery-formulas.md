# ADR 0010: Gamification, Mastery Formulas & Play and Learn Specification

## Status
Accepted

## Context
Phase 8 implements the complete learning loop: Workbooks, Educational Games, Rewards, and Topic Mastery.
It resolves open architectural risk **R8 (Mastery and XP formulas)** and open questions from `docs/architecture.md`:
- XP formula and level thresholds
- Weighting of topic mastery inputs
- Reconciliation of Coins and Learning Points
- Day definition for Learning Streak
- Asset and interaction pattern for 6 Smart Workbook types (including Drag-and-Drop and Picture-based)
- Chapter-specific games per subject (Mathematics, Science, Social Studies, English, Telugu)
- Progress-based unlockables
- End-of-chapter Mission Challenges
- Ownership and format of Achievement Certificates
- AI-Generated Personalized Practice for struggling learners
- Story Mode for Classes 1 to 5

## Decisions

### 1. XP Formula & Level Thresholds
Students earn Experience Points (XP) for completing educational activities:
- `read_topic`: **+20 XP**
- `watch_video`: **+15 XP**
- `workbook_question`: **+10 XP** per correct answer (+30 XP base on completing workbook)
- `game_completed`: **+30 XP**
- `mission_challenge`: **+50 XP** (bonus for chapter mastery)
- `question_asked` (Bala Buddy AI doubt): **+5 XP**
- `streak_bonus`: **+10 XP** per day maintained

**Level Calculation:**
`level = floor(xp / 100) + 1`
- **Level 1 (0–99 XP):** Curious Scout 🌱 (పరిశోధక స్కౌట్)
- **Level 2 (100–199 XP):** Eager Explorer 🚀 (ఉత్సాహ అన్వేషకుడు)
- **Level 3 (200–349 XP):** Knowledge Seeker 📚 (జ్ఞాన పిపాసి)
- **Level 4 (350–499 XP):** Rising Scholar 💡 (వర్ధమాన పండితుడు)
- **Level 5+ (500+ XP):** Master Learner 🏆 (నైపుణ్య సాధకుడు)

### 2. Reconciliation of Coins with Learning Points
- **1 Coin = 1 Learning Point.**
- Coins represent fungible learning points earned through active practice:
  - +5 Coins per topic read
  - +5 Coins per video watched
  - +10 Coins per workbook / game completed
  - +25 Coins per chapter mission challenge completed

### 3. Star Rewards (⭐)
Awarded on workbook activities and quizzes based on score percentage:
- Score $\ge 90\%$: 3 Stars ⭐⭐⭐
- Score $70\% - 89\%$: 2 Stars ⭐⭐
- Score $50\% - 69\%$: 1 Star ⭐
- Score $< 50\%$: 0 Stars (retry encouraged with supportive tip)

### 4. Topic Mastery Formula (R8)
Each topic progresses through 4 mastery levels:
1. `Beginner 🌱` (Score < 30)
2. `Learning 📖` (Score 30 to 59)
3. `Practicing 💪` (Score 60 to 84)
4. `Mastered 🏆` (Score $\ge 85$)

**Weighted Multi-Input Formula:**
Total Score $S = (0.20 \times R + 0.30 \times W + 0.20 \times Q + 0.20 \times G + 0.10 \times A) \times 100$
Where each input is normalized between 0.0 and 1.0:
- $R$ (Reading Progress): 1.0 if topic read, else 0.0
- $W$ (Workbook Score): accuracy percentage on topic workbook (0.0 to 1.0)
- $Q$ (Quiz Score): accuracy percentage on topic practice questions (0.0 to 1.0)
- $G$ (Educational Game Score): completion accuracy on chapter game (0.0 to 1.0)
- $A$ (AI Doubts / Interaction): 1.0 if at least 1 doubt asked to Bala Buddy, else 0.0

**Hand-computed Verification Sample:**
- Fixed Input: $R=1.0, W=0.8, Q=0.9, G=0.7, A=0.5$
  $S = (0.20 \times 1.0 + 0.30 \times 0.8 + 0.20 \times 0.9 + 0.20 \times 0.7 + 0.10 \times 0.5) \times 100$
  $S = (0.20 + 0.24 + 0.18 + 0.14 + 0.05) \times 100 = 81.0\%$
  Level: `Practicing 💪`
- Fully completed Input: $R=1.0, W=1.0, Q=1.0, G=1.0, A=1.0 \implies S = 100.0\% \implies \text{Mastered 🏆}$.

### 5. Learning Streak Day Definition
- A "Day" is defined strictly from 00:00:00 to 23:59:59 in local time (Indian Standard Time, UTC+5:30).
- Completing $\ge 1$ educational activity (reading, video, workbook, game, doubt) on calendar day $D$ maintains or increases streak:
  - If last active day was $D - 1$ day: streak increments by 1.
  - If last active day was $D$ (same day): streak is maintained.
  - If last active day was $< D - 1$ (gap > 1 day): streak resets to 1.

### 6. Badges Collection
- `explorer`: Explorer Badge 🧭 (మొదటి పాఠం అన్వేషణ)
- `science_genius`: Science Genius Badge 🔬 (సైన్స్ ప్రతిభావంతుడు)
- `math_champion`: Math Champion Badge 📐 (గణిత విజేత)
- `reading_hero`: Reading Hero Badge 📖 (చదువుల వీరుడు)
- `mission_master`: Mission Accomplished Badge 🏅 (అధ్యాయం మిషన్ విజయం)
- `streak_star`: Streak Master Badge 🔥 (5 రోజుల నిరంతర సాధన)

### 7. Smart Workbook 6 Activity Types (100% Offline)
1. `mcq`: Multiple Choice Questions with 4 options and immediate bilingual explanation.
2. `fill_blank`: Fill in the blanks with tap-friendly word bank chips (zero virtual keyboard typing).
3. `match`: Touch-to-pair matching column.
4. `true_false`: Large friendly True / False (సత్యం / అసత్యం) buttons.
5. `drag_drop`: Draggable keyword chips and DragTarget receptor container.
6. `picture_based`: Visual diagram / illustration card with contextual identification questions.

### 8. Chapter-Specific Educational Games Across 5 Subjects
- **Mathematics:** Number Puzzle & Fraction Builder
- **Science:** Plant Growth Simulator & Photosynthesis Chef
- **Social Studies:** Heritage Treasure Hunt & Map Explorer
- **English:** Word Builder & Vocabulary Match
- **Telugu:** Akshara Match (అక్షర జతపరచడం) & Word Formation Challenge

### 9. End-of-Chapter Mission Challenge
Combines 4 interactive phases:
1. Multi-concept Quiz question
2. Concept Puzzle
3. Scenario Question
4. Speed Mini Game
Awards Chapter Badge, +50 XP bonus, and unlocks Achievement Certificate.

### 10. Achievement Certificates
Owned by the Gamification Engine:
- Issued upon completing Chapter Mission Challenge or reaching Mastered level.
- Formatted with unique certificate ID, learner name, subject, chapter title, date, score, and Bala Buddy verified seal.

### 11. AI Generated Personalized Practice
Triggered when a learner scores $< 60\%$ on a workbook:
- Provides simplified analogies using familiar everyday items.
- Generates 2 easier targeted exercises to rebuild foundational confidence.
- Offers encouraging, empathetic feedback from Bala Buddy without criticism.

### 12. Story-Based Learning (Classes 1 to 5)
- Interactive narrative adventures featuring cartoon characters (such as Bala Rabbit).
- Translates core curriculum concepts into playful interactive stories.
