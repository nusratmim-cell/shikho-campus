# Shikho Campus — Product Requirements (v5)

The PRD is an HTML document set. Read it in a browser.

## Open it

```bash
cd "/home/shikho/Brac Platform Explore/prd-local"
python3 -m http.server 8000
```

Then open http://localhost:8000/index.html

## What changed in v5

Rewritten as a **functional specification in plain language**. No code, no data
formats, no technical interface detail. Every module document has the same three
parts:

1. **Introduction** — what the module is, who uses it, a day in their life, what it
   owns and what it deliberately leaves to other systems, how it fits with the other
   three modules.
2. **Feature list** — every feature in one table with a one-line description, priority
   and what it connects to.
3. **Feature details** — per feature: what it does, why it exists, who uses it and
   when, what the screen shows (including the exact wording), the step-by-step flow,
   the information it uses and creates, what it connects with, the rules a university
   can configure, what must never happen, unusual situations, and how we know it works.

## The pages

| Page | Contents |
| --- | --- |
| `index.html` | What the product is, how to read the document, the four modules, coverage, rules we never break, configurable settings, glossary |
| `student.html` | Student module — 27 features: learning, assessment, attendance, fees and payment, advising, registration, documents, campus services, clubs, evaluation, AI help, mobile |
| `faculty.html` | Faculty module — teaching, content, blueprint and import, syllabus, announcements, assignments and quizzes, weightage and posting policy, moderation, grading with AI assistance, gradebook and submission, attendance, advisees, supervision |
| `admin.html` | Administrator module — staffing, cross-listing, academic and fee policy, exam eligibility, exam schedule, grade certification, scholarships, discipline, quality and accreditation, entitlements, analytics |
| `coordinator.html` | Coordinator module — records loading, routine and rooms, unstaffed section flags, invoice sync, payment verification, documents, clearance, registrar export, notices, alumni handover |
| `university-activities.html` | Every activity that happens in a university (A–N), each mapped to a module and feature and marked Now / Next / Later / Outside |
| `ai.html` | Shikho Campus AI — how it is built (in-house, on the Teacher OS approach), Tutor, Practice, Smart Class, Assistant, draft grading, Analyst, usage caps |
| `platform.html` | How everything connects — the signals between modules, five cross-module chains, outside systems, who can see what, Bangladesh realities, failure behaviour |
| Live demo | https://shikho-brac-platform.vercel.app/ |
| LMS references | Overview → [LMS references](prd-local/index.html#references) — Docebo tour, Canvas 101, Canvas for teachers |

Every page carries a numbered document map in the menu: **1 Overview** (always first), **2 Modules**, **3 supporting pages**, **4 LMS reference videos**, **5 our live demo**. Click the brand or Overview from anywhere to return to the start.

## The rules every feature obeys

1. The chairperson certifies; the teacher marks. No administrator screen edits a mark.
2. AI drafts; a person decides. Nothing reaches a student without teacher approval.
3. The platform never holds university money.
4. Fee amounts come from the finance office, never from inside the platform.
5. Marks, attendance, payments, holds and approvals keep full history.
6. Every automated decision can show the records that produced it.
7. Differences between universities are settings, not new software.
8. Teachers never invite students — rosters come from university records.
9. No public ranking of students.
10. One responsive web app across phone, tablet, laptop, desktop and classroom smart TV.

## Product decisions written into the spec

- **Campus AI is built in-house, on the Teacher OS approach.** No third-party
  "copilot" dependency. The three modes are Tutor (student), Assistant (faculty)
  and Analyst (administrator). See `ai.html#build`.
- **Tuition access gate.** Unpaid tuition past its grace window can restrict
  classes and content, not only registration — designed humanely (advance
  warnings, one-tap pay, already-earned work stays, never removed mid-class,
  advisor/finance can extend). See `admin.html#ADM-FEE-01`.

## Research appendix

`PRD-Research-Foundation.md` — competitor analysis, architecture patterns, workflow
edge cases, Bangladesh regulatory requirements.
`PRD-BD-Regulatory-Requirements.md` — PDPA 2026, accreditation, e-signature detail.
