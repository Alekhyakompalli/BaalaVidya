# BAALAVIDYA Teacher and Volunteer Operating Model (R9)

**Date:** 2026-11-22  
**Purpose:** Formal specification of roles, access rights, and ethical boundaries for Subject Teachers and Community Volunteers in accordance with [Arch: Key risks R9] and [PS: Target Users].

---

## 1. Operating Model Overview

In Telangana government schools and village learning centers, teachers and community volunteers ("Vidya Volunteers") are critical enablers of educational technology adoption. This guide establishes a clear division of responsibilities:
- **Teachers** lead classroom pedagogy, verify curriculum accuracy, and use aggregated insights for remedial instruction.
- **Volunteers** facilitate device accessibility, manage offline Wi-Fi synchronization hubs, and guide parents on mobile settings.
- **Ethical Boundary:** Neither teachers nor volunteers have access to individual private student chat conversations with Bala Buddy.

---

## 2. Role of the Subject Teacher

### Responsibilities:
1. **Curriculum & Content Verification:**
   - Review ingested SCERT textbook chapters and verify that practice questions reflect board examination patterns.
   - Flag regional nomenclature or errors for rapid textbook patch updates.
2. **Classroom Instruction Integration:**
   - Direct students to Smart Workbooks and Chapter Games to reinforce concepts taught in class.
   - Use End-of-Chapter Mission Challenges as fun milestone assessments.
3. **Remedial Action from Aggregate Insights:**
   - Review aggregate topic mastery heatmaps (e.g., *"Lesson 1: Photosynthesis — 42% accuracy on Calvin Cycle"*).
   - Tailor classroom explanations to address common conceptual hurdles without singling out individual children.

### Permissions & Privacy Boundaries:
- ✅ **Can View:** School and section aggregate progress, topic mastery rates, and average practice times.
- ❌ **Cannot View:** Individual student chat transcripts or queries asked to Bala Buddy.
- ❌ **Cannot Alter:** System mastery formulas or tamper with student XP/badges.

---

## 3. Role of the Community / Vidya Volunteer

### Responsibilities:
1. **Offline Synchronization Hub Management:**
   - Establish school or community center Wi-Fi hotspots once a week to allow students to download versioned chapter packages and sync offline progress telemetry.
   - Assist in device charging and memory management on shared smartphones.
2. **Parent Orientation & Awareness:**
   - Explain the 4-digit PIN Parental Gate (`1234` default) to rural parents during village education committee meetings.
   - Demonstrate the Parent Zone dashboard to help parents understand study times and badges.
3. **Shared Device Facilitation:**
   - Show siblings how to switch profiles (`LearnerSwitcher`) on a single mobile device so their XP and streaks remain independent.

### Permissions & Privacy Boundaries:
- ✅ **Can View:** Public syllabus packages, app update status, and connectivity diagnostics.
- ❌ **Cannot View:** Any student academic records, test scores, or personal identifiers.
- ❌ **Cannot Alter:** Syllabus content, student scores, or parental PIN codes.

---

## 4. Conflict Resolution & Child Safeguarding Protocol

1. **Child Privacy Mandate:** If any student reports discomfort regarding surveillance, the teacher and volunteer must re-affirm that Bala Buddy chat conversations are strictly private.
2. **Hardware Damage or Loss:** Volunteers report hardware faults to the school headmaster without penalizing the student.
3. **Safety Incident Reporting:** Any algorithmic safety defect or inappropriate response is immediately escalated to the state education technical committee using the feedback protocol (`/v1/pilot/feedback`).
