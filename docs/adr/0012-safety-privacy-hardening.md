# 0012. Safety, Privacy, and Low-Resource Hardening Architecture

Date: 2026-11-22
Status: Accepted

## Context & Problem Statement

BAALAVIDYA is designed for school children in rural and urban government schools across Telangana, often operating on shared low-resource Android devices (e.g. 2GB RAM, Android Go) with intermittent connectivity. Because the user base includes minors (Classes 1–10), the system must guarantee:
1. Strict child safety across all chat and practice interactions (avoiding harmful content, violence, self-harm, profanity, adult material, and prompt injections).
2. Defense-in-depth output safety filtering as a second check after prompt rules.
3. Compliance with child privacy regulations (India DPDP Act 2023 Section 9, COPPA, and cloud LLM minor terms of service).
4. Full data minimization, encryption on shared hardware, and a verifiable "Right to be Forgotten" (data purge).
5. Reliable operation within strict hardware budgets (< 150 MB RAM, < 50 MB storage).

## Decision Drivers

- **G9 Child-Safe Behaviour:** Zero unsafe or harmful outputs may ever reach a child learner.
- **R11 Parental Consent & Minor Protections:** Verifiable parental gate, consent registry, and compliance with cloud AI API terms.
- **Shared Device Architecture:** Strict separation between siblings/classmates sharing the same mobile phone.
- **Low-Resource Target Device:** 2GB RAM Quad-Core device must run without memory crashes or thermal throttling.
- **WCAG Accessibility:** High contrast, 48dp touch targets, 2.0x font scaling, and minimal typing.

## Architectural Decisions

### 1. Two-Tiered Guardrail Pipeline (Input & Output Filters)
- **Tier 1 (Input Guardrails):** Evaluates incoming student questions against regex and semantic heuristics for prompt injections, harmful activities, dangerous substances, violence, adult topics, and off-topic questions.
- **Tier 2 (Output Safety Filter):** Independent post-generation check on all model outputs. Even if a prompt injection or hallucination evades Tier 1, the Tier 2 filter inspects the generated text for profanity, harmful instruction patterns, PII leakage (phone, email, Aadhaar), and system prompt exposure before returning the response to the client. Unsafe outputs are suppressed and replaced with friendly refusal templates.

### 2. Bilingual Refusal Templates
- Refusals in English and Telugu (`en` and `te`) maintain an encouraging, non-punitive tone:
  - Harmful/Unsafe: Refuses harmful topics and redirects the child toward syllabus concepts or a trusted teacher/parent.
  - Off-Topic: Cheerful decline offering 3 relevant syllabus topics to explore.
  - Prompt Injection: Re-anchors the assistant identity as Bala Buddy, a safe school companion.

### 3. Data Minimization & Shared Device Storage
- Stored telemetry contains zero chat transcripts, audio recordings, or biometric data.
- Shared devices store profile telemetry in isolated database partitions keyed by `learner_id`.
- Local stores utilize obfuscated/encrypted SQLite storage with secure key derivation.
- Zero third-party ad networks (e.g. AdMob) or third-party analytics trackers (e.g. Firebase Analytics, AppsFlyer) are embedded in the client.

### 4. Right to be Forgotten (Data Purge)
- Parents and students can initiate a complete data purge via `DELETE /v1/analytics/parent/{learner_id}/data` or via the Parent Zone settings screen.
- Purge clears local sync queues, cached chapters, topic mastery records, and remote analytics.

### 5. Logging Policy & Retention
- Server logs redact IP addresses and all PII.
- Retention is strictly capped at 30 days, after which automated log rotation purges all student telemetry.
- Role-based access control restricts log access to authenticated maintainers.

### 6. Hardware & Performance Budget
- **Memory:** Max 150 MB RAM allocated to BAALAVIDYA processes.
- **Storage:** Core app binary < 45 MB; offline chapter packages compressed < 15 MB each.
- **Latency:** On-device vector retrieval < 50ms; end-to-end chat response < 500ms offline and < 1500ms online.

## Consequences & Mitigations

- **Positive:** Guarantees safe learning experiences for minors; passes stringent school deployment safety reviews.
- **Positive:** Zero data leakage risks on shared family smartphones.
- **Trade-off:** Multi-stage safety checks add 2–5 ms latency per request (completely imperceptible to users).
- **Mitigation:** Pre-compiled regex patterns and deterministic string tokenizers ensure negligible CPU impact.
