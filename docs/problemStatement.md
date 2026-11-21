# BAALAVIDYA - Problem Statement

BAALAVIDYA - AI Powered Last-Mile Tutor

## OVERVIEW

BAALAVIDYA is a kid-friendly bilingual educational mobile application designed for Telangana State Board students from Classes 1 to 10.

The application aims to provide high-quality educational assistance in both Telugu and English, especially for students with limited internet connectivity, shared devices, and lack of access to tutors.

The application must support online and offline learning through an AI-powered Retrieval Augmented Generation (RAG) system built using Telangana State Board syllabus content.

The application should be visually attractive for children, easy to navigate, colorful, engaging, and accessible for young learners.

## HACKATHON ALIGNMENT

This solution addresses the "Last-Mile Tutor" problem by:

1. Teaching students in their preferred local language.
2. Supporting poor internet connectivity through offline access.
3. Providing an AI tutor that explains topics in simple language.
4. Supporting self-learning without requiring a teacher.
5. Enabling personalized learning and syllabus navigation.
6. Running on low-resource mobile devices.
7. Providing progress tracking for learners and parents.

## TARGET USERS

**Primary Users:**

- Telangana State Board Students
- Classes 1 to 10

**Secondary Users:**

- Parents
- Teachers
- Volunteers

## SUPPORTED LANGUAGES

1. Telugu
2. English

The user must be able to switch instantly between Telugu and English using a Language Toggle button placed at the Top Right Corner of the application.

## CORE OBJECTIVES

1. Provide syllabus-based learning.
2. Provide AI-powered doubt clarification.
3. Provide chapter-wise explanations.
4. Provide topic-related educational videos.
5. Work both online and offline.
6. Support bilingual learning.
7. Be engaging and child-friendly.

## DATA SOURCES

**Source Curriculum:**

- Telangana SCERT Textbooks
- Telangana State Board Syllabus
- Classes 1 to 10

**Subjects Include:**

- Telugu
- English
- Mathematics
- Science
- Social Studies
- Environmental Science

## DATA INGESTION PIPELINE

1. Fetch Telangana SCERT curriculum and textbook content.
2. Extract chapter and topic information.
3. Generate embeddings.
4. Store embeddings in vector database.
5. Use RAG architecture for retrieval.
6. Provide contextual responses from curriculum data.

The application should strictly answer based on syllabus-aligned content.

## RAG ARCHITECTURE

```
Data Source
      |
      V
SCERT Curriculum
      |
      V
Text Extraction
      |
      V
Chunking
      |
      V
Embeddings
      |
      V
Vector Database
      |
      V
Retriever
      |
      V
AI Tutor
      |
      V
Student Response
```

## FUNCTIONAL REQUIREMENTS

### 1. SPLASH SCREEN

**Display:**

- BAALAVIDYA logo
- Fun educational theme
- Friendly animation

### 2. HOME SCREEN

**Display:**

- Search Bar
- Language Toggle
- Class Selection Grid

**Classes:**

Class 1
Class 2
Class 3
Class 4
Class 5
Class 6
Class 7
Class 8
Class 9
Class 10

### 3. CLASS SELECTION

When a student selects a class:

**Display:**

- Available Subjects
- Syllabus Overview

**Example:**

Class 6

**Subjects:**

- Telugu
- English
- Mathematics
- Science
- Social Studies

### 4. SUBJECT VIEW

**Display:**

- Chapters
- Topics
- Progress Percentage

### 5. TOPIC VIEW

**Display:**

- Topic Title
- Explanation
- AI Tutor
- Related Videos
- Practice Questions

### 6. AI CHATBOT

**Features:**

- Powered by RAG
- Kid Friendly
- Educational only
- Simple explanations
- Telugu answers
- English answers
- Voice support (future scope)

**Example Questions:**

> "What is Photosynthesis?"
>
> "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?"

**Responses must:**

- Use age-appropriate language
- Avoid difficult terminology
- Give examples
- Encourage learning

### 7. VIDEO SECTION

For every topic:

**Show:**

- Relevant educational videos
- Language-aware recommendations

**Example:**

Topic:
Fractions

**Display:**
- Telugu explanation video
- English explanation video

### 8. SEARCH FUNCTIONALITY

Students can search:

- Subjects
- Chapters
- Topics
- Concepts

**Example:**

Search:
"Photosynthesis"

**Results:**

Class 6 Science
Class 7 Science
Related Videos
Ask Tutor

### 9. LEARNING PROGRESS

**Track:**

- Completed Topics
- Chapters Covered
- Questions Asked
- Learning Streak

### 10. PARENT DASHBOARD

**Display:**

- Learning Progress
- Time Spent
- Subjects Completed
- Weak Areas

## OFFLINE MODE

**Requirements:**

1. Download syllabus data.
2. Download embeddings.
3. Store vector database locally.
4. Allow AI tutoring without internet.
5. Sync progress when internet is available.

**Offline Features:**

- Chapter Reading
- Topic Explanations
- Local RAG Search
- Cached Videos Metadata
- Saved Progress

## ONLINE MODE

**Features:**

- Cloud AI Support
- Latest Updates
- Video Streaming
- Enhanced Explanations

## UI/UX REQUIREMENTS

**Design Theme:**

- Bright
- Colorful
- Child Friendly
- Cartoon Inspired

**Components:**

- Rounded Cards
- Large Buttons
- Fun Icons
- Friendly Illustrations

**Colors:**

**Primary:**

- Blue
- Yellow

**Secondary:**

- Green
- Orange

## ACCESSIBILITY

1. Large fonts
2. Voice-ready architecture
3. Easy navigation
4. Minimal typing required

## TECHNICAL STACK

**Frontend:**

- Flutter

**Backend:**

- FastAPI

**Vector Database:**

- Qdrant

**Embeddings:**

- multilingual-e5-base
  or
- BGE-M3

**Offline LLM:**

- Phi-3 Mini
  or
- Gemma 2B

**Cloud LLM:**

- Azure OpenAI
  or
- GPT API

**OCR:**

- Azure Document Intelligence

## DATABASE STRUCTURE

Class
Subject
Chapter
Topic
Language
Content
Videos
Embeddings
Progress

## CHATBOT GUARDRAILS

1. Educational responses only.
2. Child-safe content.
3. Age appropriate language.
4. No harmful or inappropriate information.
5. Answers should stay within syllabus context whenever possible.

## SUCCESS METRICS

1. Fast topic retrieval.
2. Offline usability.
3. Accurate syllabus-based answers.
4. Child engagement.
5. Ease of learning.
6. Parent visibility into progress.

## TAGLINE

> "BAALAVIDYA - Every Child's AI Learning Companion"

## 11. PLAY & LEARN MODULE (GAMIFIED LEARNING)

**Purpose:**

After a learner completes reading or understanding a topic,
the application should provide interactive activities that
reinforce learning in a fun and engaging manner.

**Objective:**

- Improve retention
- Encourage self-learning
- Reduce learning fatigue
- Make studying enjoyable
- Increase student engagement

**Features:**

### 1. Smart Workbook

For every topic, generate:

- Fill in the blanks
- Match the following
- Multiple Choice Questions
- True or False
- Drag and Drop Activities
- Picture-based Questions

**Examples:**

Topic:
Plants

**Workbook Activities:**

✓ Match plant parts to functions
✓ Identify leaf types
✓ Fill missing words

### 2. Learning Games

Every chapter should have chapter-specific educational games.

**Examples:**

**Mathematics:**

- Number Puzzle
- Fraction Builder
- Math Race
- Shape Hunt

**Science:**

- Plant Growth Simulator
- Human Body Puzzle
- Food Chain Builder

**Social Studies:**

- Map Explorer
- Heritage Treasure Hunt

**English:**

- Word Builder
- Vocabulary Match
- Grammar Quest

**Telugu:**

- Akshara Match
- Word Formation Game
- Sentence Building Challenge

### 3. Learning Rewards

Reward students for completing activities.

**Rewards:**

- Stars ⭐
- Badges 🏅
- Achievement Certificates 📜
- Learning Points 🎯

**Examples:**

Explorer Badge
Science Genius Badge
Math Champion Badge
Reading Hero Badge

### 4. Progress-based Unlockables

Students unlock new games and rewards by completing:

- Chapters
- Workbooks
- Practice Sessions

### 5. AI Generated Personalized Practice

Using RAG and student performance data:

If a student struggles with a topic:

**Example:**

Topic:
Fractions

BAALAVIDYA automatically generates:

- Easier explanations
- Extra workbook exercises
- Additional practice games

### 6. Story-Based Learning

For younger classes (1-5):

Convert concepts into:

- Story Adventures
- Cartoon Characters
- Interactive Narratives

**Example:**

Character:
Bala Rabbit

Mission:
Help Bala Rabbit distribute 10 carrots equally among friends.

Concept:
Division

### 7. Topic Mastery Score

Each topic should display:

Beginner 🌱
Learning 📖
Practicing 💪
Mastered 🏆

based on performance in:

- Reading
- Workbook Completion
- Quiz Scores
- Game Scores

### 8. End-of-Chapter Challenge

After completing a chapter:

Present:

> "Mission Challenge"

which combines:

- Quiz
- Puzzle
- Scenario Questions
- Mini Game

**Completion rewards:**

- Chapter Completion Badge
- Experience Points (XP)
- New Unlockables

### 9. Offline Compatibility

All workbook activities and games should work offline.

Only video streaming requires internet.

Downloaded chapters should include:

- Topic content
- Workbook activities
- Educational games
- Progress tracking

### 10. Parent Insights

Parents can view:

- Workbook completion rate
- Game performance
- Weak concepts
- Improvement areas

**Gamification Metrics:**

- Total XP
- Current Level
- Learning Streak
- Badges Earned

## 12. BALA BUDDY – AI LEARNING COMPANION

**Overview:**

Bala Buddy is the official AI-powered learning companion of BAALAVIDYA.

Instead of interacting with a generic chatbot, students interact with Bala Buddy, a friendly virtual guide specifically designed for children.

Bala Buddy should feel like a helpful friend, mentor, and study partner who makes learning fun, engaging, and stress-free.

## PRIMARY GOALS

1. Make learning enjoyable.
2. Encourage curiosity and confidence.
3. Explain concepts in a child-friendly manner.
4. Motivate students to continue learning.
5. Provide emotional encouragement during studies.
6. Personalize the learning experience.

## CHARACTER PERSONALITY

Bala Buddy should be:

- Friendly
- Cheerful
- Encouraging
- Supportive
- Patient
- Positive

Bala Buddy should never:

- Sound robotic
- Use complex educational jargon
- Criticize students
- Discourage learners

## COMMUNICATION STYLE

**Language:**

- Telugu
- English

**Example:**

Student:
What is photosynthesis?

Bala Buddy:

> "Plants are like little chefs!
> They use sunlight, water and air to prepare their own food.
> Let's see how it works with a fun activity!"

**Example Telugu:**

Student:
కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?

Bala Buddy:

> "మొక్కలు చిన్న చిన్న వంటవాళ్లలాంటివి!
> సూర్యకాంతి, నీరు మరియు గాలిని ఉపయోగించి తమ ఆహారం తామే తయారుచేసుకుంటాయి.
> ఇప్పుడొక సరదా గేమ్ ద్వారా చూద్దాం!"

## AI TUTOR CAPABILITIES

1. Explain Concepts
2. Answer Questions
3. Simplify Difficult Topics
4. Generate Practice Questions
5. Recommend Activities
6. Suggest Videos
7. Generate Revision Notes
8. Track Learning Progress

## INTERACTIVE LEARNING

After every topic:

Bala Buddy should ask:

> "Would you like to play a quick game?"

**Options:**

- Play Game
- Practice Workbook
- Watch Video
- Ask Doubts

## GAMIFIED LEARNING ASSISTANT

Bala Buddy should guide students during:

- Puzzles
- Quizzes
- Story Activities
- Workbook Exercises

**Example:**

> "Great job! You answered 4 out of 5 correctly!"
>
> "Awesome! Let's try one more challenge!"

## ACHIEVEMENTS AND REWARDS

Bala Buddy rewards students with:

- Stars ⭐
- Coins 🪙
- Badges 🏆
- XP Points 🎯

**Examples:**

Reading Hero
Math Champion
Science Explorer
Curious Learner
Knowledge Master

## PERSONALIZED LEARNING

Using student performance data:

If a student struggles with a topic:

Bala Buddy should:

- Provide simpler explanations
- Recommend extra practice
- Suggest beginner exercises
- Offer additional examples

## TOPIC MASTERY SYSTEM

Every topic should have mastery levels:

🌱 Beginner
📖 Learning
💪 Practicing
🏆 Mastered

Bala Buddy continuously updates mastery based on:

- Reading progress
- Workbook completion
- Quiz scores
- Game performance
- AI interactions

## STORY MODE FOR YOUNGER STUDENTS

For Classes 1-5:

Bala Buddy should teach through stories.

**Examples:**

**Mathematics:**
Help Bala Bunny distribute carrots.

**Science:**
Help a plant grow using sunlight and water.

**English:**
Help characters find missing words.

**Telugu:**
Build words using Telugu letters.

## VOICE READY DESIGN

**Future Feature:**

Bala Buddy can:

- Speak Telugu
- Speak English
- Listen to student questions
- Read lessons aloud

This helps students who struggle with reading or typing.

## PARENT INSIGHTS

Parents can view:

- Topics learned
- Games completed
- Learning streak
- Badges earned
- Weak concepts
- Strength areas

## MISSION CHALLENGES

At the end of every chapter:

Bala Buddy presents:

> "Mission Challenge"

which includes:

- Quiz
- Puzzle
- Activity
- Mini Game

**Rewards:**

- Chapter Badge
- Bonus XP
- Unlock New Challenges

## OFFLINE SUPPORT

Bala Buddy should work in offline mode using:

- Downloaded syllabus data
- Local vector database
- On-device AI model

**Available Offline:**

- Tutor conversations
- Topic explanations
- Workbooks
- Educational games
- Progress tracking

**Available Online:**

- Video streaming
- Advanced AI responses
- Cloud synchronization
- Enhanced recommendations

## BALA BUDDY TAGLINE

> "Learn. Play. Explore. Grow."

Bala Buddy is not just a chatbot.

Bala Buddy is every child's friend, tutor, guide, motivator, and learning companion within BAALAVIDYA.
