# BAALAVIDYA Privacy Review Record

**Date:** 2026-11-22  
**Status:** Approved & Validated  
**Scope:** Child Data Protection, Cloud LLM Age Terms, Shared Device Storage, and SDK Auditing  
**Regulatory Standards:** India DPDP Act 2023 (Section 9), COPPA (15 U.S.C. §§ 6501–6506), GDPR Article 8

---

## 1. Executive Summary

BAALAVIDYA is an educational technology platform deployed for primary and secondary school children (Classes 1–10) in Telangana. Because the target users are minors, strict safety-by-design and privacy-by-default principles govern all software components. This privacy review verifies regulatory compliance, third-party dependency safety, shared hardware isolation, and verifiable data deletion capabilities.

---

## 2. Legal Review of Cloud LLM Age Terms (R11)

### A. Cloud LLM Provider Terms
- **Provider API Agreements (Azure OpenAI / Google Gemini API / OpenAI API):**
  - Cloud provider API terms permit educational usage by minors provided the software application enforces verifiable parental consent (R11) and provides effective safety guardrails against adult/harmful material.
  - **Zero Training Guarantee:** Both Azure OpenAI and Gemini API Enterprise terms explicitly guarantee that student prompts, queries, and generated completions are **never used to train or fine-tune public foundation models**.
  - **Data Processing Addendum (DPA):** Data submitted via API endpoints is processed ephemerally with zero long-term retention on provider infrastructure beyond transient abuse monitoring.

### B. India Digital Personal Data Protection Act (DPDP Act 2023) — Section 9
- **Verifiable Parental Consent (Sec. 9(1)):** BAALAVIDYA implements a parental consent gate (`/v1/analytics/parent/consent` & 4-digit PIN verification) before parental dashboard access and profile telemetry aggregation are activated.
- **Prohibition on Behavioral Tracking (Sec. 9(2)):** The platform enforces a strict ban on tracking, profiling, or behavioral monitoring of children for commercial purposes.
- **Prohibition on Detrimental Processing (Sec. 9(3)):** All AI prompts are bounded by strict SCERT textbook RAG grounding and two-tier safety guardrails, preventing outputs harmful to a child’s well-being.

### C. US COPPA & Global Minor Protections
- **Zero Transcripts to Parents:** Child chat transcripts with Bala Buddy are strictly private to prevent parental surveillance from discouraging natural learning curiosity.
- **Data Minimization:** No biometric data, geolocation, camera footage, or real-world addresses are ever requested, recorded, or stored.

---

## 3. Third-Party SDK & Dependency Audit

A comprehensive audit of the client application codebase (`client/pubspec.yaml`) and backend dependencies (`backend/pyproject.toml`) was conducted:

| Category | Permitted in BAALAVIDYA? | Audit Result | Verified Packages |
| :--- | :---: | :---: | :--- |
| **Ad Networks** | ❌ Strictly Prohibited | **CLEAN (0 found)** | No AdMob, AppLovin, or Unity Ads SDKs. |
| **Commercial Analytics** | ❌ Strictly Prohibited | **CLEAN (0 found)** | No Firebase Analytics, AppsFlyer, Mixpanel, or Facebook SDKs. |
| **Crashlytics / Trackers** | ❌ Strictly Prohibited | **CLEAN (0 found)** | No third-party device fingerprinters or diagnostic trackers. |
| **Local Storage** | ✅ Permitted (Internal) | **CLEAN** | `drift: ^2.20.0`, `sqlite3_flutter_libs: ^0.5.24` (Local sandboxed SQLite). |
| **Network Client** | ✅ Permitted (Internal) | **CLEAN** | `http: ^1.2.0` (Direct project API calls only). |

---

## 4. Shared Device Isolation & Local Storage Minimization

In rural and peri-urban Telangana, multiple siblings and classmates frequently share a single mobile phone or tablet:
1. **Isolated Learner Profiles:** Multi-learner data stores are partitioned strictly by `learner_id`. Activity logs, topic mastery breakdowns, and sync events for Learner A cannot be read or altered by Learner B.
2. **Local Sandbox Encryption:** All offline textbook packages, vector database slices, and progress records reside within the protected Android application sandbox (`/data/data/org.codebenders.baalavidya/`), preventing unprivileged apps from reading student data.
3. **Parental Gate Isolation:** Access to aggregated academic metrics is gated behind a 4-digit parental PIN code (`1234` default, customizable), preventing children from accidentally altering parent configuration.

---

## 5. Right to be Forgotten (Data Purge Protocol)

Parents and students hold the fundamental right to permanently delete all stored telemetry and personal records:
- **API Purge Endpoint:** `DELETE /v1/analytics/parent/{learner_id}/data` permanently removes the learner profile, mastery breakdowns, certificates, and event logs from server memory/databases.
- **Local Purge Action:** A single tap on "Delete Student Learning Data" in the Parent Zone UI purges the local SQLite database, clears the pending sync queue (`SyncQueueService`), and unlinks the parent account.

---

## 6. Logging Policy & Retention Schedule

1. **Retention Cap:** Central server logs and telemetry records are subjected to an automated 30-day retention schedule. Logs older than 30 days are automatically pruned.
2. **PII Redaction:** Automated middleware sanitizes server logs: IP addresses are hashed/zeroed (`0.0.0.0`), and regex filters mask any detected phone numbers, email addresses, or 12-digit Indian Aadhaar patterns.
3. **No Persistent Chat Transcripts:** Chat queries and LLM responses are processed in-memory and are never stored in permanent database tables.

---

## 7. Sign-off & Conclusion

The BAALAVIDYA platform architecture fulfills all safety, privacy, and child data protection criteria set forth in Phase 10 of the implementation plan and complies with applicable national and international regulatory frameworks for minor users.
