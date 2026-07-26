# Shikho Campus — PRD Research Foundation

**Purpose:** Source-of-truth exploration for writing a sellable multi-university LMS SaaS PRD.  
**Status:** Research complete. **Product PRD is the source of truth** — see [SHIKHO-CAMPUS-PRD.md](./SHIKHO-CAMPUS-PRD.md) and the [PRD canvas](/home/shikho/.cursor/projects/home-shikho-Brac-Platform-Explore/canvases/shikho-campus-prd.canvas.tsx). This file is appendix material only.

**Related canvases (open beside chat):**
- [**PRD (read this)**](/home/shikho/.cursor/projects/home-shikho-Brac-Platform-Explore/canvases/shikho-campus-prd.canvas.tsx)
- [Product map](/home/shikho/.cursor/projects/home-shikho-Brac-Platform-Explore/canvases/brac-lms-product-map.canvas.tsx)
- [Architecture spine](/home/shikho/.cursor/projects/home-shikho-Brac-Platform-Explore/canvases/lms-product-architecture.canvas.tsx)

---

## 1. Product thesis (sellable one-liner)

**Shikho Campus** is a configurable higher-education LMS SaaS for private universities (~20k students): SIS-true terms/sections, live + recorded delivery, assignments, role-based governance — with optional grounded AI and accreditation evidence — without Canvas-class TCO or Classroom-level shallowness.

**Not this:**
- A CSE-only demo forever
- A content-production business (teachers supply content)
- A full SIS / payments / admissions replacement in MVP
- A generic ChatGPT sidebar

**Yes this:**
- Multi-tenant SaaS (one product, many universities via configuration)
- Modular packaging (university buys core; enables AI / governance packs)
- Academic spine first; AI second; gamification optional and off-by-default for university tenants

---

## 2. Locked decisions from boss meeting

| Topic | Locked decision | PRD implication |
|---|---|---|
| Market | Private universities first; ~20k student size; enter via BRAC CSE → other CSEs → other unis | Tenant model + mid-market packaging |
| Product type | University LMS SaaS, not one-off BRAC build | Multi-tenant, module flags, config engine |
| Content | Faculty provide all learning content; Shikho does not | No content studio as core SKU |
| Live class | Laptop/tablet **or** studio/hall camera; students join online in-app | Two teacher delivery modes; session object |
| Offline attendance | Offline room presence not tracked in platform | Attendance = online/system join (+ optional manual) |
| Hybrid why | Ongoing hybrid + teacher-allowed home join + future online program | Per-session delivery mode, not COVID shelfware |
| Roles | Teacher, Student, Administrator, Course Coordinator; login-based | Kill demo role-picker in production |
| Departments | Any department courses; cross-dept enrollment | Org hierarchy + course ownership |
| Assignments | General multi-type; no code editor / OJ in v1 | File/link/text/code-as-file |
| Grades / gamification | Prototype shows them; MVP does not lead with them | Module later; real grades need timeline |
| AI | Separate modules after core; grounded in institution + teacher + syllabus KB | Three-layer KB; no MagicSchool pattern |
| Architecture | Module-by-module; admin enable/disable; configurable semesters | Entitlements + calendar engine |
| Demo vs product | Keep vibe demo for sales; build real product | Dual-track: sales demo + production spine |

---

## 3. Competitive landscape (what PRD must beat)

### 3.1 Local incumbents

| Uni | Stack | Gap we exploit |
|---|---|---|
| NSU | Canvas + RDS SIS + Google Meet | Prestige Canvas TCO; Meet bolts on; SIS reconciliation manual |
| BRAC | buX (Open edX) + USIS | No native live; offline philosophy; course-run rot without rollover |
| AIUB | VUES/UMS + MS Teams | Owns ops stack but thin LMS; live external; weak mobile |

**Pattern:** LMS ≠ SIS ≠ meetings. Humans reconcile. Our wedge = section-true academic spine + first-class live session → recording → topic + closed certify/export loop + regional mid-market price.

### 3.2 Global table stakes vs differentiators vs avoid

**Table stakes (must ship to be shortlisted):**
1. Multi-tenant SaaS: university → school/dept → roles
2. Term → Course → Section → Enrollment + CSV/API sync + SSO
3. Blueprint / master → section content sync with locks
4. Modules, files, assignments, quizzes, banks, rubrics, gradebook, announcements
5. LTI 1.3 Advantage roadmap (or clear timeline)
6. Mobile-usable flows; basic analytics; audit logs
7. Attendance + live join + recording attached to topic
8. CLO tagging hook (minimum OBE)

**Differentiators (win BD/South Asia private unis):**
1. BAC/IQAC / BAETE OBE evidence packs (CLO–PLO–assessment–CQI)
2. Registrar-first adapters for local SIS (USIS/RDS-like) + term open/close wizard
3. Configurable Campus without Moodle-plugin chaos or Canvas FTE pricing
4. Course-grounded AI (citations, admin allowlists, Bangla-capable)
5. Live-class as daily habit UX; low-bandwidth / offline lecture continue
6. In-region implementation SLAs + transparent packaging

**Avoid building (integrate):**
- Full Zoom/Teams/BBB parity WebRTC stack
- Docs/Drive/Mail suite
- Full payments ledger / admissions CRM
- Global plagiarism corpus from scratch
- Un-grounded chatbot
- Hundreds of first-party LTI replacements

### 3.3 Positioning one-liner for sales PRD

> Sell against Classroom/Teams (too shallow) and Moodle DIY (too risky); displace Canvas/Brightspace on price, OBE evidence, and regional implementation — while treating live video, Drive/M365, and proctoring as integrations.

Sources: [Canvas SIS](https://canvas.instructure.com/doc/api/file.sis_csv.html), [Blueprint](https://canvas.instructure.com/doc/api/blueprint_courses.html), [Moodle multi-tenancy](https://docs.moodle.org/500/en/Multi-tenancy), [1EdTech LTI](https://www.1edtech.org/standards/lti), competitor synthesis via market research track.

---

## 4. Academic / domain spine (architecture non-negotiables)

Treat product as **academic OS with LMS surface**, not CMS with bolt-on terms.

```
Tenant
  └─ Org (university → school → department → programme)
       └─ Person (multi-role memberships over time)
            └─ AcademicCalendar / Term (configurable windows)
                 └─ Catalog Course → CourseVersion (frozen when referenced)
                      └─ Offering (term instance) → Section (seat/waitlist/teacher)
                           └─ Session (live/recorded/attendance unit)
                                └─ Enrollment (status machine)
                                     └─ Learning activities → Gradebook → Certify → SIS passback
                                          └─ Audit (append-only)
```

**Critical distinctions for PRD glossary:**
- **Course** = catalogue identity (CSE110)
- **CourseVersion** = syllabus/version freeze
- **Offering** = course in a term
- **Section** = enrollable unit with capacity/teacher
- **Session** = one class meeting (live/recorded/hybrid flag)
- **Enrollment** = person × section × term with status

**Open vs closed credit** = programme-version policy, not a global boolean.

**SIS vs LMS boundary:**
- SIS owns: identity source, programmes, official roster, financial holds, final transcript authority (typical BD pattern)
- LMS owns: in-term learning, session attendance, assignment grades, certify workflow, then passback/export
- Payments = **status signal** into LMS (hold / clear), not a billing product in MVP

**Irreversible early choices:**
1. Shared DB + `tenant_id` / RLS (dedicated DB as premium SKU)
2. Opaque global IDs
3. Append-only audit
4. Media via adapters (don’t hard-couple one SFU forever)
5. Per-tenant AI indexes
6. Residency chosen at tenant provision

**Standards note:** OneRoster is K–12-strong; HE complexity → prefer Edu-API direction + practical CSV/API adapters for BD SIS. LTI Advantage is table-stakes for tool ecosystem.

Architecture canvas: [lms-product-architecture](/home/shikho/.cursor/projects/home-shikho-Brac-Platform-Explore/canvases/lms-product-architecture.canvas.tsx)

---

## 5. Role model for PRD

| Role | Owns | Does not own |
|---|---|---|
| **Student** | Join live, watch recorded, resources, submit work, see standing | Catalogue creation, certify |
| **Teacher** | Live (2 modes), record→topic, resources, assignments/marking, section attendance | University module toggles, whole catalogue alone |
| **Course Coordinator** | Rosters/import hygiene, offerings, syllabus/curriculum context for AI, flag unstaffed→Chair, registrar export ops | Certify grades, teach (unless dual-role) |
| **Administrator / Chair** | Module enablement, semester templates, course enablement, staffing, eligibility policy, certify, audit, institution KB | Day-to-day roster typing |
| **Platform (Shikho) Admin** | Tenant provision, billing, residency, global feature flags | University academic decisions |

**Must support multi-role persons** (TA = student + staff). Demo separate URLs are UX only.

---

## 6. Module packaging (for SaaS sales PRD)

### Core LMS (MVP sellable floor)
1. Tenant + SSO + roles
2. Org / dept / catalogue / course create
3. Configurable term engine + course enablement
4. Sections + staffing + Coord import
5. Live class (laptop + camera modes) + student join
6. Recorded video attached to topic + resume
7. Resources upload (slides/PDF/text/links)
8. Assignments (general types) + teacher review/mark
9. Profiles for four roles
10. Basic notifications / announcements (required for “real product” feel)

### Governance pack
- Attendance ledger + eligibility rules (e.g. 70%) + overrides
- Grade submit → certify → export/passback
- Appeals + audit log
- Flag-to-Chair staffing loop

### Engagement pack (optional, default off for uni)
- Momentum / XP / rings — only if tenant enables

### AI pack (separate SKU)
- Institution KB + Coordinator syllabus context + Teacher KB
- Tutor / Copilot / Analyst grounded only in those layers
- Usage caps / metering
- Academic integrity policy (tutor cannot do graded work)

### Integration pack
- SIS adapters, LTI Advantage, calendar sync, WhatsApp/SMS, Meet/Teams/LiveKit adapter

### Accreditation pack (later high-value)
- CLO/PLO mapping, attainment dashboards, IQAC/BAETE evidence export

---

## 7. Configurability matrix (universities differ — PRD must list)

| Config | Examples | Notes |
|---|---|---|
| Term shape | Trimester (~4 mo), semester (~6 mo), annual | Engine must be flexible; **BD UGC has pushed dual-semester for private unis** — treat as policy validation, not hardcode one shape |
| Windows | Registration, add/drop, teaching, exams, grade lock | Soft/hard close |
| Credit model | Closed programme vs open/flexible electives | Programme-version rules |
| Cross-dept / service courses | CSE takes MAT; other dept teaches | Ownership ≠ enrolment dept |
| Grading schemes | Weighted categories, letter maps, W/I/retake | Policy objects |
| Attendance rule | Join=present, duration threshold, manual | Feeds eligibility |
| Module entitlements | Core / Governance / AI / Accreditation | Admin enable/disable |
| Delivery mode | Per-session in-person / online / hybrid | Teacher home-allow flag |
| Language / branding | English-first; optional Bangla UI later | Tenant theme |
| Data residency | BD region option | Sales/compliance checkbox |

---

## 8. Portal workflows PRD must specify

### Before term
Create term → enable courses → staff sections → set syllabus/context → import/sync roster → (optional) student registration or SIS-only enrolment

### During term
Schedule sessions → live/record → resources → announcements → assignment cycles → attendance → at-risk flags

### Close term
Eligibility lock → submit grades → certify → export/passback → appeals window → rollover (clone structure, new dates, clear cohort submissions)

### Faculty analysis (Chair)
Staffing/load, certification backlog, at-risk, course evals (add), **not** comparative faculty “productivity score”

---

## 9. Bangladesh / regulatory requirements (PRD-critical)

Full report: [PRD-BD-Regulatory-Requirements.md](./PRD-BD-Regulatory-Requirements.md)  
(from [BD regulatory research](1ffe3107-fac8-4048-bf7a-743daccce867))

### Headline

Legal binding surface is **narrower** than expected; **accreditation evidence surface is very wide**. That is the Bangladesh-specific product win vs Moodle/Canvas.

1. **Accreditation is the real requirements engine** — BAC 10 standards + BAETE 9 criteria demand CO→PO attainment, moderation trails, attendance registers, course files, CQI loops.
2. **Data protection is real** — Personal Data Protection Act 2026 applies extraterritorially to foreign-hosted SaaS serving BD data subjects. Localization softened (Feb 2026) to **restricted personal data + CII only** — still need legal verify on biometrics/health.
3. **Almost every academic rule is university-specific** — BRAC vs NSU vs AIUB grade scales, attendance gates, probation differ materially → **tenant-configurable or design defect**.

### Must express without code changes (config test suite)

| Dimension | BRAC | NSU | AIUB |
|---|---|---|---|
| Top grade letter | A | A | A+ |
| Attendance model | 5% of marks + &lt;70% bars final | Instructor-led; 3 consecutive absences → drop | ≥80% or UW→F |
| Probation | Sliding CGPA by seniority | Max 3 terms @ CGPA 2.0 | Separate rules |
| Retake | Cap often B+ | — | — |
| Credit transfer | — | Max 50%; C+; excluded from CGPA | CGPA 3.5; 60% at AIUB |

### Mandatory / high-weight PRD requirements

| ID | Requirement |
|---|---|
| M1–M4 | UGC program approval gate; semester calendar (+ legacy trimester); CLO↔PLO mapping; BNQF credit floors |
| M5–M11 | PDPA consent proof, DSAR, under-18 profiling suppress, deletion cascade, 5-year processing register, automated-decision human review |
| M12 | Digital signatures only via **CCA-licensed BD CA** (no DocuSign for legal transcripts) |
| M16 | Never custody funds — route to licensed PSO/PSP only |
| A1–A7 | Attendance register, next-of-kin, handbook, course file, **question moderation workflow**, feedback SLA, progression engine |
| A9–A12 | Direct-method PO attainment; pluggable BAETE/BAC outcome frameworks coexisting per program |

### Legal verification before locking hosting / public-sector sales

| # | Question | If adverse |
|---|---|---|
| U1 | Is biometric/health/counselling **restricted personal data**? | Need in-BD replica for that domain |
| U2 | Bangla-only PDPA 2026 exact section map | Compliance mapping rework |
| U3 | Does National Cloud Policy bind private HEIs? | Sovereign hosting expectations |
| U4 | Public-uni / gov-funded tenant → source-code escrow? | Proprietary SaaS conflict |
| U7 | Fee-freeze-at-admission amendment enacted? | Per-cohort locked fee schedules |

### Product design constraints from market reality

- **Mobile-first is the access path** (~8.9% household computer vs ~72.8% smartphone).
- Design for **bottom-decile bandwidth** (~2 Mbps regional floors), not median.
- UGC blended policy: **default onsite final exam**; online continuous assessment OK; online summative = emergency mode with recorded academic-committee approval.
- Payments: multi-rail (bKash/Nagad/Rocket/cards/bank slip), per-rail fee disclosure, bulk Excel reconcile — but **finance stays merchant/SIS-side**; LMS holds payment status + gating.
- Accessibility target: **WCAG 2.1 AA** + Bangla Unicode + captions (even if private-sector enforceability is soft).

**Sales PRD rule:** do not claim legal compliance without counsel sign-off. Put Security, PDPA, and accreditation packs as requirements + roadmap with explicit legal-review gates.

---

## 10. What the demo already proves vs what productization needs

**Demo strengths to keep in PRD narrative:**
- Four-role story
- Section-scoped teaching
- Live as first-class UI
- AI draft grading with teacher-in-loop copy
- Certify chain concept (faculty → chair → registrar export)
- Honest partial adoption framing

**Demo lies / risks to strip or fix before selling as product:**
- Scripted AI with “grounded” claims
- Role picker instead of SSO
- Grades/gamification without real academic timeline
- Faculty momentum score (political risk)
- Missing announcements/comms
- Missing term rollover / blueprint sync
- Missing appeals/audit UI
- Attendance % without capture rule
- Hardcoded CSE seed world

---

## 11. PRD document structure (recommended when writing)

1. Vision & positioning  
2. Buyers & jobs-to-be-done (VC/Chair/IQAC/IT/Faculty/Students)  
3. Competitive alternatives  
4. Scope boundaries (in/out)  
5. Personas & permissions  
6. Domain model glossary  
7. Module catalogue & packaging/pricing hypotheses  
8. Functional requirements by module (MoSCoW)  
9. Configurability & multi-tenant admin  
10. Integrations & standards  
11. AI & knowledge-base rules  
12. Non-functionals (scale, security, residency, offline, a11y)  
13. Analytics & success metrics  
14. Implementation / onboarding playbook  
15. Roadmap phases  
16. Open decisions / assumptions  
17. Appendices: workflows, edge cases, competitor matrix, regulatory notes  

---

## 12. Open decisions that block a clean PRD v1

1. **Registration in Campus vs stay in SIS?**  
2. **Live media: own infra vs wrap Meet/Teams/LiveKit?**  
3. **Grade source of truth & passback direction with SIS?**  
4. **First AI SKU after KB: Tutor vs Copilot vs Analyst?**  
5. **Gamification default off for all university tenants?**  
6. **Data residency default region & dedicated-DB SKU?**  
7. **Pilot tenant: BRAC CSE only vs multi-dept day one?**  

---

## 13. Suggested delivery phases (for PRD roadmap section)

| Phase | Ship | Sales claim unlocked |
|---|---|---|
| 0 Foundations | Tenancy, SSO, roles, audit, RLS | “Real SaaS, not a demo” |
| 1 Academic spine | Term, catalogue, sections, teach/grade basics | “Run a term” |
| 2 Ops | SIS sync, waitlist/holds signals, blueprint, appeals | “Works with registrar” |
| 3 Live depth + Governance | Robust live/record, eligibility, certify loop | “Replaces Meet+Drive chaos” |
| 4 AI pack | Grounded KB layers + Tutor/Copilot | “AI-enabled LMS, not chatbot” |
| 5 Accreditation | OBE evidence packs | “IQAC/BAETE-ready” |

---

## 14. Workflow engine requirements (from full HE ops map)

Full inventory: [PRD-Workflow-Edge-Case-Map.md](./PRD-Workflow-Edge-Case-Map.md)  
(~17 lifecycle phases, nine actors, ~120 corner cases — from [workflow research](bdc1cdd8-c8f2-4b37-8faf-ecc4858b6b9b)).

### Expand beyond four demo personas

PRD must support a **permission fabric**, not only Student / Teacher / Coordinator / Admin:

| Tag | Role |
|---|---|
| STU | Student |
| TCH | Teacher |
| CC | Course Coordinator |
| DA | Department Admin / Chair |
| REG | Registrar |
| DEAN | Dean / IQAC |
| TSA | Tenant Super Admin |
| SPA | Shikho Platform Admin |
| FIN | Finance / SIS |

One human can hold many contextual roles (TA who is also a student; Chair who teaches).

### Twelve load-bearing PRD implications

1. **Per-tenant policy registry** — no hard-coded BRAC-only rules (attendance %, grading schemes, term labels).
2. **Effective-dated / append-only records** — grades, enrolments, overrides are historical, not overwrite-in-place.
3. **Rules engines with evaluation traces** — prereq, eligibility, degree audit, attainment must store *why* (inputs + rule version) for appeals.
4. **Role-locked state machines + deadline-breach branches** — enrollment, grade lifecycle, waitlist, incompletes, holds.
5. **Override-with-audit everywhere** — typed, reasoned, approver-scoped; never silent bypass.
6. **Event-driven cascade graph** — grade posted → GPA → standing → holds → registration eligibility → graduation audit.
7. **Integration direction-of-truth per entity** — student master, enrollments, grades, fees/holds declared at setup.
8. **Notification criticality + acknowledgment** — waitlist offers, holds, exam moves are appeal evidence.
9. **Privacy, retention, legal hold** — evaluation anonymity minimum-n, recording consent, retention vs erasure.
10. **BD resilience assumptions** — exam auth break-glass, SMS fallback, low-bandwidth media, offline attendance import, emergency calendar shift.
11. **Permission fabric** — capability grants (grade vs certify vs post), not page-level roles only.
12. **Term-close orchestration UI** — cross-role checklist of blockers (submit → certify → post → export).

### Densest risk zones for PRD writers

- **Registration:** open/closed credit, prereqs/coreqs, waitlists, holds, overrides, cross-listing, repeats, SIS down mid-window.
- **Grading/certification:** draft → provisional → moderated → certified → posted → amended; appeals; bulk amend cascades.
- **Rollover/archival:** clone offerings, reset dates, preserve transcripts, avoid buX-style ghost course runs.

---

## 15. Research track status

| Track | Status | Output |
|---|---|---|
| Boss meeting + team Review | Done | Locked decisions |
| Global LMS competitors | Done | Positioning matrix |
| Product architecture | Done | Domain spine + [architecture canvas](/home/shikho/.cursor/projects/home-shikho-Brac-Platform-Explore/canvases/lms-product-architecture.canvas.tsx) |
| Exhaustive workflow edge cases | Done | [PRD-Workflow-Edge-Case-Map.md](./PRD-Workflow-Edge-Case-Map.md) |
| BD regulatory / ops | Done | [PRD-BD-Regulatory-Requirements.md](./PRD-BD-Regulatory-Requirements.md) |
| Full demo role audit | Done | Steal/kill table in [SHIKHO-CAMPUS-PRD.md](./SHIKHO-CAMPUS-PRD.md) §6 ([audit](dae40bfd-4265-4994-bcd1-dc2c460d59a3)) |

---

*PRD shipped: [SHIKHO-CAMPUS-PRD.md](./SHIKHO-CAMPUS-PRD.md) + [canvas](/home/shikho/.cursor/projects/home-shikho-Brac-Platform-Explore/canvases/shikho-campus-prd.canvas.tsx).*
