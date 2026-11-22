# ADR 0011: Parent Dashboard, Analytics & Child Privacy Architecture

## Status
Accepted

## Context
Phase 9 delivers the Parent Dashboard and Analytics module, enabling parents to understand their child's learning journey, time spent, weak concepts, and improvement areas [PS: 10. Parent Dashboard; Parent Insights].

This ADR addresses key architectural risks and questions from `docs/architecture.md`:
1. **Child Privacy & Chat Visibility [Arch: Parent visibility; Security, safety and child privacy]**:
   Whether parents should see their child's chat transcripts with Bala Buddy.
2. **Parent Access & Consent (R11)**:
   Account linking, parental consent, and parental gate on shared mobile devices.
3. **Analytics Aggregation & Weak-Area Labeling**:
   How weak concepts and strengths are derived from progress telemetry without premature or unfair labeling.

## Decisions

### 1. Strict Child Privacy: No Chat Transcripts for Parents
- **Decision:** Parents see learning progress, completion metrics, time spent, weak concepts, and gamification rewards, but **ZERO chat transcripts**.
- **Rationale:** Bala Buddy is designed to be a safe, pressure-free learning companion where children can ask questions and express doubts without fear of criticism or judgment. Exposing raw transcripts to parents could cause learning anxiety and discourage curious inquiries.
- **Privacy Assurance:** The analytics API strictly filters and never serializes conversational chat logs to parent endpoints.

### 2. Parental Gate & Consent (R11)
- On shared household devices, a **Parental Gate** (simple PIN or math verification challenge) guards the Parent Dashboard view, preventing accidental switches.
- **Parental Consent:** Recorded via `/v1/analytics/parent/consent` with parent name, contact, linked learner profile, and consent timestamp.

### 3. Analytics Aggregation & Metrics
The Analytics service aggregates learner events and progress records into parent-facing metrics:
- **Total Time Spent:** Aggregated in minutes across topic reading, video viewing, workbooks, and games (e.g. 15 min per topic + video duration + practice time).
- **Workbook Completion Rate:**
  $$\text{Completion Rate} = \left( \frac{\text{Workbooks Completed}}{\text{Workbooks Attempted}} \right) \times 100$$
- **Game Performance Score:** Average score on educational game pairs and challenges.
- **Weak Concepts & Improvement Areas:**
  - Classified as `Weak Concept` if accuracy score $< 60\%$ or Topic Mastery is `Beginner` after attempts.
  - Classified as `Needs Practice` if score is between $60\%$ and $84\%$.
  - Classified as `Strength Area` if score $\ge 85\%$ or `Mastered`.
- **Minimum-Data Notice:**
  If a topic or subject has fewer than 2 completed activities, the dashboard displays:
  *"Minimum data notice: Needs more learning sessions to accurately identify weak concepts."*
  This prevents misleading or discouraging classifications from a tiny sample size.

### 4. Improvement Recommendations
Actionable, positive suggestions for parents (e.g. "Encourage your child to describe how leaves cook food during family meals").

### 5. API Surface
- `GET /v1/analytics/parent/{learner_id}`: Comprehensive parent metrics and insights.
- `POST /v1/analytics/parent/consent`: Parent profile linking and consent recording.
- `POST /v1/analytics/parent/verify-pin`: Parental gate verification.
