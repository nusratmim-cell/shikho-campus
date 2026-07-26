# Higher-Education LMS SaaS — Operations & Edge-Case Map

## Part A — Actor model and conventions

Role tags used throughout (RACI shorthand: **R** = does the work, **A** = accountable/approves, **C** = consulted, **I** = informed):

| Tag | Role | Scope summary |
|---|---|---|
| STU | Student | Own enrollment, learning, submissions, appeals, evaluations |
| TCH | Teacher / Faculty | Section-level delivery, attendance, assessment, provisional grades |
| CC | Course Coordinator | Multi-section course consistency: syllabus, common assessments, records completeness, handoffs |
| DA | Department Admin / Chair | Department-level staffing, offering approval, moderation, certification, at-risk escalation |
| REG | Registrar | Institution-level academic records: calendar, registration rules, official grade posting, transcripts, graduation audit |
| DEAN | Dean / IQAC | Faculty-level oversight, quality assurance, OBE/accreditation, appeals of last resort, policy exceptions |
| TSA | Tenant Super Admin | Institution's platform configuration: org structure, roles/permissions, integrations, branding, policy toggles |
| SPA | Shikho Platform Admin | Cross-tenant SaaS operations: provisioning, upgrades, quotas, support escalation, data residency, platform incidents |
| FIN | Finance / SIS | Fee assessment, financial holds, enrollment/grade sync, scholarship logic, student master data (usually the system of record) |

**Governing PRD principle:** every workflow below must be expressible as a *configurable state machine per tenant* — which states exist, who can transition them, what deadlines gate them, and what happens on deadline breach. The single biggest PRD trap is hard-coding one university's policy.

---

## Part B — Lifecycle workflow inventory

### Phase 1 — Institution onboarding & tenant provisioning

**Workflows**

1.1 Tenant creation, environment/region selection, data residency, domain/SSO setup — R: SPA, A: SPA, C: TSA
1.2 Contract → entitlement mapping (seat counts, modules, storage, AI features) — R: SPA, I: TSA, FIN
1.3 Identity setup: SSO (SAML/OIDC), local accounts fallback, MFA policy — R: TSA, C: SPA
1.4 Org-structure import: faculties/schools → departments → programs — R: TSA, C: REG, DA
1.5 Role/permission model instantiation and delegation rules — R: TSA, A: TSA
1.6 SIS/finance integration wiring (student master, fee status, course/enrollment sync direction-of-truth decisions) — R: TSA + FIN, C: SPA, REG
1.7 Branding, locale (Bangla/English), time zone, grading-scale library, academic terminology mapping ("semester" vs "trimester" vs "term") — R: TSA
1.8 Pilot cohort / sandbox tenant with synthetic data; go-live cutover — R: SPA + TSA
1.9 Historical data migration (past terms, transcripts, legacy LMS content) — R: SPA, A: REG (record accuracy), C: TSA

**Unhappy paths & corner cases**

- SSO IdP outage → students locked out during an exam window. Requires break-glass local auth for designated roles and an exam-mode auth bypass policy.
- SIS and LMS disagree on who is the system of record for enrollments (both writable) → duplicate/conflicting records. PRD must force a per-entity direction-of-truth declaration at integration setup.
- Mid-contract entitlement downgrade while active enrollments exceed the new seat cap.
- Tenant merges/splits (two colleges merge; a department becomes a separate institute) — data ownership and transcript continuity.
- Migration imports grades under a legacy grading scale that no longer exists in the tenant's scale library.
- A user exists in two tenants (adjunct teaching at two universities) — identity must be tenant-scoped or federated deliberately.
- Tenant offboarding: contractual data export format, retention window, verified deletion, and what alumni lose.

**PRD implications:** tenant isolation model (hard multi-tenancy, per-tenant encryption keys optional); entitlement enforcement that degrades gracefully (read-only, not lockout); migration tooling with dry-run/validation reports; SPA "impersonate with consent + audit" support mode; per-tenant feature flags.

---

### Phase 2 — Academic structure

**Workflows**

2.1 Define faculties, departments, programs, majors/minors/concentrations, cohorts/batches — R: TSA, C: REG, DA
2.2 Define credit system (credit hours, ECTS-like, contact hours), grading scales, GPA computation rules, probation/dean's-list thresholds — R: REG, A: DEAN, config by TSA
2.3 Program-level rules: max/min credit load per term, standing progression, degree credit requirements — R: REG + DA
2.4 Cross-department ownership (a course owned by CSE but required by EEE) — R: DA of both, arbitrated by DEAN

**Edge cases**

- Department renamed or split mid-degree — students' transcripts must show the historical name at time of study.
- A program discontinued with students still in-flight ("teach-out" mode: no new admissions, structure frozen but operable for N terms).
- Dual-degree / double-major students whose two programs impose conflicting credit rules — which rule wins must be configurable (strictest / program-of-primary-major / manual).
- Non-degree students (exchange, audit-only, certificate learners) who exist outside program structures but need enrollment.

**PRD implications:** effective-dated (temporal) structure entities — everything about org structure needs `valid_from/valid_to`, not just current state; student-to-program relationships are many-to-many with a primary flag.

---

### Phase 3 — Catalogue, curriculum & versioning

**Workflows**

3.1 Author course in catalogue: code, title, description, credits, learning outcomes (CLOs), delivery modes allowed — R: CC/TCH proposer, A: DA, C: REG
3.2 Curriculum (degree plan) definition: required/elective buckets, credit distribution, recommended sequence — R: DA, A: DEAN, I: REG
3.3 Curriculum versioning: catalog-year binding — each student is pinned to the curriculum version active at admission (or may opt into a newer one) — R: REG, A: DEAN
3.4 Prerequisite/corequisite/anti-requisite graph authoring, including grade-minimum prereqs ("C or better in CSE110") and credit-standing prereqs ("60+ credits earned") — R: CC/DA, A: REG
3.5 Course equivalency and transfer-credit mapping tables — R: REG, C: DA
3.6 Course retirement / replacement with equivalency chain (CSE201 replaced by CSE211; both satisfy the same requirement) — R: DA, A: REG

**Edge cases**

- Prereq graph cycles introduced by editing (A requires B requires A) — must be validated at authoring time.
- Curriculum changed after students admitted: which students migrate, which are grandfathered; a student who fails a now-retired required course needs a substitution path.
- A course's credit value changes between versions — repeats of that course involve different credit amounts; GPA math must use the credits *at time of attempt*.
- Same course code reused years later for different content.
- Outcome (CLO) edits on a live version would corrupt OBE evidence — outcomes must version with the course.
- Cross-listed catalogue entries (CSE460 = ROBO460) sharing content but reported under different departments.

**PRD implications:** immutable published course versions (edits create new versions); requirement-satisfaction engine that evaluates a student's transcript against *their pinned curriculum version* with substitution/waiver records; prereq expressions as a validated boolean grammar (AND/OR/min-grade/min-credits/co-req/permission-of-instructor).

---

### Phase 4 — Term setup & academic calendar

**Workflows**

4.1 Define terms/sessions (semester, trimester, summer, sub-sessions/modules within a term) with distinct date sets — R: REG, config by TSA
4.2 Key-date engine per term: advising window, registration open/close, add/drop, withdrawal deadline (W grade), census date, exam windows, grade-submission deadline, grade-publication date — R: REG, A: DEAN, I: all
4.3 Per-population overrides (seniors register first; evening program has different drop deadline) — R: REG
4.4 Holiday/closure and make-up-day handling that reflows timetables — R: REG, I: TCH, STU

**Edge cases**

- Overlapping terms (summer overlaps spring grading period) — a student can be "in" two terms simultaneously; dashboards and load rules must handle it.
- Emergency calendar shifts (political unrest, floods — realistic for BD context): bulk deadline extension must cascade to every dependent deadline (assessments, attendance denominators, grade due dates) with an audit trail.
- A sub-session course (7-week module) inside a 14-week term needs proportional add/drop/withdraw deadlines, not term-level ones.
- Deadline falls on a newly declared holiday — auto-shift policy (next business day vs. manual).
- Retroactive date edits after transactions occurred against the old dates (e.g., drops processed under the old refund deadline) — must warn and never silently reprocess.

**PRD implications:** dates are first-class configurable objects with dependency links ("grade deadline = exam end + 7 days"); a calendar-change simulation ("what breaks if I move this date") before commit; all enforcement reads dates at transaction time and records which date version applied.

---

### Phase 5 — Course offering, sections, staffing, timetables, rooms

**Workflows**

5.1 Offering plan: which catalogue courses run this term, projected demand, section counts — R: CC + DA, A: DA, I: REG
5.2 Section creation: capacity, delivery mode (online/hybrid/offline), campus, language of instruction — R: CC/DA
5.3 Staffing: assign instructor(s), co-teachers, TAs, lab instructors, graders; teaching-load accounting against faculty load rules — R: DA, C: CC, I: TCH, DEAN
5.4 Timetable: meeting patterns (lecture + lab + tutorial as linked components), clash detection against instructor, room, and cohort — R: CC/DA (or central timetabling under REG — must be configurable)
5.5 Room/resource allocation: capacity fit, equipment (lab benches, projectors), accessibility needs; online "rooms" (Zoom/Meet license pools) — R: DA/REG, C: TCH
5.6 Cross-listing at offering level: one physical section serving two course codes with a shared or split capacity — R: DA, A: REG
5.7 Section changes after publication: capacity raise, room move, time move, instructor swap — R: DA, I: enrolled STU (mandatory notification), REG
5.8 Section cancellation for low enrollment: threshold policy, student re-placement workflow — R: DA, A: DEAN, I: STU, REG, FIN (refund trigger)

**Unhappy paths & corner cases**

- Instructor resigns / falls ill mid-term: mid-term staffing swap must transfer gradebook ownership, pending grading queue, attendance history, and communication threads, with the departing instructor's entries preserved under their name.
- Unstaffed section at registration open ("TBA instructor") — allowed or blocked per tenant policy.
- Room double-booked because timetable edited after publication; or room capacity < enrolled count after a capacity override.
- Cross-listed section where the two parent courses have *different* assessment weights or grading scales — PRD must decide: force shared scheme or allow per-code overlays.
- Linked components: student enrolled in lecture but the only compatible lab section is full — atomic enrollment across components or none.
- Time-zone edge for online sections with remote students; DST-free BD context still hits foreign exchange students.
- A TA who is also a student in another section of the same course (conflict-of-interest flag for grading access).
- Section split after registration (60 enrolled, split into 2×30): deterministic student redistribution with preserved records.

**PRD implications:** section as an aggregate of components with atomic co-enrollment; staffing roles with granular capabilities (grader ≠ instructor ≠ observer); every post-publication change generates a student-visible changelog and notification; clash-detection service usable at edit time, not just batch.

---

### Phase 6 — Registration & enrollment

This is the densest edge-case zone; enumerated by sub-area.

**Workflows**

6.1 **Open-credit registration** (student self-selects courses/sections within load rules) — R: STU, C: advisor (DA-delegated), enforcement engine A: REG
6.2 **Closed-credit / cohort registration** (registrar or department block-enrolls a batch into a fixed schedule — common in BD private universities' first years) — R: REG or DA, I: STU
6.3 Hybrid: cohort core + student-chosen electives — both engines simultaneously
6.4 Registration time-tickets / priority windows (by standing, credits earned, program) — R: REG
6.5 Prereq/coreq/anti-req enforcement at cart-checkout time, including "in-progress prereq" policy (allow registering while prereq is being taken this term, revoke if failed) — engine, policy A: REG
6.6 Waitlists: position, auto-promotion on seat open, promotion hold window ("claim within 24h"), waitlist-with-swap ("promote me and drop my backup section") — R: STU, engine, policy A: REG/DA
6.7 Holds: financial (FIN), advising (DA), disciplinary (DEAN), library/clearance, document-missing (REG) — each hold declares *which actions it blocks* (register / view grades / transcript / graduate)
6.8 Overrides: capacity override, prereq waiver, time-conflict permit, credit-overload permit, closed-section permission — requested by STU or TCH, approved per override-type-specific approver (CC/DA/REG/DEAN), all logged
6.9 Add/drop/swap within deadline; withdrawal (W) after add/drop; late add petitions — R: STU, A: REG, I: FIN, TCH
6.10 **Repeats & retakes**: retake policy (grade replacement / averaging / best-of / attempt cap), repeat-for-improvement vs. repeat-after-fail, fee implications — engine, policy A: REG, I: FIN
6.11 Audit enrollment (no credit, no grade) and credit/no-credit (pass/fail) election with election deadline — R: STU, A: REG
6.12 Enrollment verification & census snapshot (official headcount for reporting/finance) — R: REG, I: FIN, DEAN
6.13 Enrollment sync to SIS/FIN → fee assessment, refund calculation on drops by refund-schedule bracket — R: FIN

**Unhappy paths & corner cases**

- **Race conditions**: last seat contested by a direct registrant and a waitlist auto-promotion firing simultaneously; two devices, one student, same cart.
- Waitlist promotion offered while the student now has a time conflict or credit overload created by other adds since joining the waitlist — promotion must re-validate all rules, not just the seat.
- Waitlisted student never claims; hold-window expiry cascades down the list — during a holiday the window shouldn't burn.
- Financial hold applied *mid-registration-session* (cart valid at start, blocked at checkout) — clear error, cart preserved.
- Hold released at 11:59 PM of the last registration day — grace-period policy.
- Prereq satisfied by a transfer credit still "pending evaluation" — provisional registration flag.
- Student fails the in-progress prereq after registering for the next course: auto-drop, notify, and free the seat — but only after grade *posting*, which may be after the next term's registration closes → forced late-add of an alternative.
- Repeat attempt of a course whose credit value or code changed (equivalency chain resolution).
- Attempt cap reached but the course is degree-required → forced substitution/waiver workflow (DA + REG).
- Cross-listed section: student accidentally registers under both codes → must be blocked as a self-anti-requisite.
- Withdrawal after the W deadline for documented emergencies (medical withdrawal, retroactive withdrawal of a whole term) — DEAN-level petition with transcript notation and FIN refund exception.
- Cohort block-enroll collides with a student's approved exception schedule (retaking a failed course from a prior term that clashes with the cohort block).
- Overload permit granted, then the student drops the course that justified surplus scrutiny — no rollback needed, but audit must capture the reasoning.
- Section cancelled after fees paid → refund vs. re-placement credit, per FIN policy.
- International/exchange student registered without a local SIS record yet (SIS lags) — provisional identity reconciliation later.

**PRD implications:** registration is a transactional rules engine — every add/drop is an atomic validated transaction with a recorded rule-evaluation trace ("passed prereq check v3, capacity 39/40, no holds"); waitlist as a first-class queue entity with re-validation on promotion; override objects with type, approver, scope, expiry; every enrollment state change emits events for SIS/FIN sync; a registrar "force" mode that can bypass any rule but never silently (reason required, logged, reportable).

---

### Phase 7 — Teaching delivery (online / hybrid / offline)

**Workflows**

7.1 Course-site provisioning from template on section creation; content copy from prior term or master shell — R: TCH/CC
7.2 Syllabus publication with CLO mapping and assessment plan; syllabus approval flow (optional per tenant) — R: TCH, A: CC or DA
7.3 Content authoring & release: modules, sequential release rules ("watch L3 before L4"), scheduled release, per-section vs. course-wide content (CC pushes common content, TCH adds section-specific) — R: TCH/CC
7.4 Live classes: schedule, join, in-class engagement (polls, hand-raise), auto-attendance capture — R: TCH, STU
7.5 Recording pipeline: auto-record, processing, captioning, publish-to-section, retention policy — R: platform, A: TCH (publish decision), policy TSA
7.6 Resource library: files, links, reading lists, lab manuals; storage quotas — R: TCH, quota A: TSA/SPA
7.7 Offline/physical delivery support: printed-material tracking, physical lab session records — R: TCH
7.8 Guest lecturers and external speaker access (time-boxed accounts) — R: TCH, A: DA, provisioned by TSA

**Edge cases**

- Live class provider outage mid-session → fallback link policy; attendance for that session marked "excused-system" not absent.
- Recording captured but student in-frame requests removal (privacy) — redaction/unpublish workflow.
- Content copied from prior term carries stale dates/links — copy tool must date-shift and dead-link-check.
- Storage quota hit mid-term blocks lecture upload — soft-fail with grace, never block student-facing playback of existing content.
- A student with accessibility accommodation needs captions/transcripts before content counts as "released" for them.
- Instructor uploads content to the wrong section of a multi-section course; CC-pushed common content diverges after a TCH edits their copy — divergence must be visible to CC.
- Bandwidth-poor students (BD context): downloadable low-res renditions, offline viewing with sync-back of watch progress.
- Recorded lecture watched at 2× — completion metrics must define what "watched" means (configurable threshold).

**PRD implications:** content model separates *master course content* (CC-owned) from *section overlays* (TCH-owned) with sync/diff; media pipeline SLA and states (uploaded → processing → ready → published → retired); release-condition engine (date, sequence, group, accommodation-aware).

---

### Phase 8 — Attendance

**Workflows**

8.1 Capture modes: auto (live-class join), QR/code check-in, manual roster marking, biometric/RFID import (offline campuses), bulk edit — R: TCH, config TSA
8.2 Attendance states: present, late, absent, excused, excused-system, on-duty (university event) — configurable set per tenant
8.3 Excuse workflow: student submits documentation → TCH or DA approves → denominator adjustment — R: STU, A: TCH/DA
8.4 Attendance-linked policies: exam-eligibility bar (e.g., <70% barred from finals — visible in the existing spec), grade-component contribution, at-risk signal feed — engine, policy A: DA/DEAN
8.5 Attendance reporting to REG/DEAN; census-related attendance verification (never-attended flag) — R: TCH, A: REG

**Edge cases**

- Joined the live class from two devices; joined for 3 of 90 minutes (minimum-duration threshold); joined but idle.
- Marked absent then excuse approved *after* finals-eligibility was computed and the student was barred → recompute + un-bar workflow with DA approval (matches the "1 barred student" decision card in the existing spec).
- QR code shared to absent friends (proxy attendance) — rotating codes, geofence option, and an integrity-flag rather than silent trust.
- Class cancelled but roster not updated → whole class marked absent; make-up class attendance mapping to the original session's denominator.
- Student added late (late add): are prior sessions counted against them? (configurable: waived / counted / prorated).
- Section transfer mid-term: attendance history must merge across sections.
- Retroactive attendance edits after grade certification — locked, requires REG unlock with reason.

**PRD implications:** attendance is an append-only event log with derived summaries, never a mutable percentage field; eligibility computations are re-runnable and versioned; every derived consequence (bar, grade penalty) links back to the exact records that caused it.

---

### Phase 9 — Assessments (all types)

**Workflows**

9.1 Assessment plan per course/section with weight scheme totaling per grading policy — R: TCH, A: CC (multi-section consistency)
9.2 Types: quizzes (auto-graded MCQ/numeric), assignments (file/code/text), labs, projects (group), presentations, viva/oral, midterm/final exams (online proctored, in-hall with seat plans, take-home), participation, peer assessment, portfolio, thesis/capstone with committee evaluation
9.3 Common assessments across sections (CC authors, all sections take, blind cross-grading option) — R: CC, TCH
9.4 Exam logistics for in-hall: schedule non-clash generation, hall/seat allocation, invigilator assignment, question-paper security — R: REG or DA (configurable), TCH
9.5 Online exam controls: timers, shuffling, lockdown/proctoring integration, network-drop resume policy — R: TCH, policy TSA
9.6 Submission handling: attempts, late policy (penalty %/day, grace minutes, hard cutoff), resubmission, draft autosave — R: STU, policy TCH within tenant guardrails
9.7 Group work: group formation (self/auto/TCH), shared submission, individual-contribution differentiation, peer contribution ratings — R: STU/TCH
9.8 Extensions & accommodations: individual deadline overrides, extra-time multipliers (1.5×) applied automatically to timed assessments for accommodated students — R: TCH, A: DA for accommodations registry
9.9 Academic-integrity pipeline: similarity/AI-detection flags → TCH review → formal case escalation (DA → DEAN committee) with grade-withheld state during investigation — R: TCH, A: DEAN
9.10 Make-up exams for approved absences — R: TCH, A: DA

**Unhappy paths & corner cases**

- Submission at 11:59:59 vs. server clock skew; upload started before deadline, finished after (grace policy on in-flight uploads).
- Corrupt/empty/wrong file submitted; discovered after deadline — resubmission petition flow.
- Timed quiz: power cut mid-attempt (very real in BD) — resume token with elapsed-time policy (pause vs. keep-running, configurable).
- Auto-grader bug discovered after release: bulk regrade of an item with delta notifications to every affected student, and downstream recompute of totals/eligibility.
- Question found ambiguous mid-exam: TCH voids the question live — points redistribution policy (drop item / full credit / rescale).
- Group member never contributes; group splits mid-project; a member drops the course mid-project (group re-formation with grade continuity).
- Peer assessment retaliation/collusion — anonymization and outlier detection.
- Weight scheme edited after some grades entered → all displayed running totals shift; must warn, snapshot, and notify.
- An accommodated student's 1.5× timer collides with the hall booking end time.
- Integrity case pending at grade deadline → an "I/withheld" grade state that doesn't break GPA math or graduation audit until resolved.
- Take-home final released to the wrong section; exam questions leaked → emergency question-swap with per-student version tracking.
- Student in two cross-listed codes of the same section must appear once in grading, not twice.

**PRD implications:** assessment as typed plugins over a common contract (open/submit/grade/return states); grading-scheme calculator that is deterministic, versioned, and re-runnable; deadline engine with per-student overlays; integrity case object with legal-grade audit trail; every regrade is an event, never an overwrite.

---

### Phase 10 — Grading, moderation, certification, posting, appeals

**Workflows** (this mirrors and generalizes the Certify flow already in the workspace spec)

10.1 Gradebook maintenance & running grades visible per policy (always / after each item / hidden until final) — R: TCH, policy DA
10.2 Provisional final-grade computation from scheme; manual adjustment with reason codes (rounding, borderline review) — R: TCH
10.3 **Moderation**: CC reviews cross-section distribution consistency; second-marker/blind double-marking for high-stakes items; scaling/curving proposals — R: CC, A: DA
10.4 **Certification**: DA/Chair reviews section grade sheets, anomaly flags (distribution outliers, attendance mismatches — as in the spec's attention-sorted certify page), certifies or returns to TCH with comments — R: DA, escalate to DEAN
10.5 **Posting**: REG receives certified sheets, validates completeness (every enrolled student has a grade or an approved incomplete), posts to official record on the publication date, triggers GPA/standing recompute, probation/dean's-list flags — R: REG, I: STU, FIN, SIS
10.6 Special grades: Incomplete (I) with completion contract and auto-lapse-to-F date, Withheld (integrity/FIN), In-Progress (thesis spanning terms), Audit, W, transfer-credit notations — engine, policy REG
10.7 **Grade changes post-posting**: TCH initiates → DA approves → REG applies; time-limited window; transcript shows change history per policy — R: TCH, A: DA + REG
10.8 **Appeals**: STU appeals within window → TCH first-level response → DA review → DEAN committee final; recount vs. remark distinction; fee for remark (FIN, refundable if grade improves) — R: STU, A: escalation chain
10.9 Certification of program completion & credentialing: digital certificates, verifiable transcripts, badge/credential issuance — R: REG, A: DEAN

**Unhappy paths & corner cases**

- TCH misses the grade deadline (unreachable, medical) — CC/DA proxy-grading authority with dual-sign-off.
- Certified, then TCH discovers a spreadsheet-style error affecting 40 students → decertify + bulk grade change with per-student cascade (GPA, standing, graduation eligibility already consumed downstream).
- Grade change flips a student from probation to good standing *after* they were blocked from registering — retroactive unblock with a registration-window exception.
- Appeal upheld after graduation and transcript issuance — reissue workflow, notify credential verifiers.
- Curve applied at section level breaks cross-section fairness for a common final — moderation must operate at course level for common items.
- Incomplete lapses to F while the completion contract extension request sits unapproved — lapse must check pending requests.
- Posting date arrives but 1 of 5 sections uncertified — partial-publish policy (publish certified sections vs. hold all; configurable, with the spec's "5 sections ready" framing supporting partial).
- GPA recompute discovers a historical posting error from a migrated term — never auto-rewrite history; open a registrar correction case.
- Student sees grade via API/notification before official publication time (leak) — publication must be atomic across all channels.

**PRD implications:** grade lifecycle is the flagship state machine (draft → provisional → moderated → certified → posted → amended) with role-locked transitions, batch operations, anomaly-flag services, and immutable posted records amended only by superseding entries; every downstream consumer (standing, eligibility, graduation audit, FIN) subscribes to grade events.

---

### Phase 11 — Communications & notifications

**Workflows**

11.1 Announcements: course, section, department, institution scopes, scheduled, multilingual — R: TCH/CC/DA/REG/TSA per scope
11.2 Direct messaging: STU↔TCH office-hours messaging, at-risk check-ins (as in the spec), advisor threads — with quiet-hours and boundaries policy
11.3 System notifications: deadline reminders, grade releases, waitlist promotions, hold placements, schedule changes — event-driven, preference-managed per user with *mandatory* categories a student cannot mute (hold placed, exam moved)
11.4 Emergency broadcast (campus closure) — R: TSA/REG, all channels, override preferences
11.5 Guardian/sponsor communications (configurable — common in BD for scholarship sponsors) — A: REG, consented by STU where required

**Edge cases**

- Notification storm: bulk regrade fires 300 grade-change notifications in a minute — digest/coalescing rules.
- Waitlist promotion notification lands in spam; claim window expires — multi-channel delivery for action-required notices with delivery confirmation.
- Message sent to a section, then a student transfers in — do they see historical announcements? (yes, configurable).
- TCH messages a student who has withdrawn/appealed against them — communication holds during formal proceedings.
- Bangla/English mixed-language rendering and SMS-length costs for Bangla Unicode.

**PRD implications:** notification taxonomy with per-event criticality class; action-required notices tracked to acknowledgment; full audit of who was notified of what and when (this becomes evidence in appeals).

---

### Phase 12 — Advising & at-risk management

**Workflows**

12.1 Advisor assignment (program advisor, thesis supervisor) and caseload management — R: DA
12.2 Risk signal engine: attendance decay, missing submissions, grade trajectory, engagement drop (spec already defines these signals) — platform, thresholds config DA/DEAN
12.3 Intervention workflows: check-in, meeting, note, advisor flag, formal early-alert case with SLA — R: TCH/advisor, A: DA (matching spec item #5)
12.4 Degree-audit advising: what-if analysis (major change simulation), plan-ahead registration — R: STU + advisor
12.5 Probation management: probation terms, credit caps while on probation, mandatory advising hold until meeting occurs — R: DA, A: REG

**Edge cases**

- False-positive at-risk flags on students with accommodations or exam-only enrollment (thesis students look "disengaged").
- Advisor leaves mid-term: caseload reassignment with note continuity and privacy.
- Note privacy tiers: TCH private note vs. advisor-shared vs. student-visible — FERPA-style access rules; students may have the right to read notes about them per tenant policy.
- At-risk flag on a student appearing in multiple sections — signals must roll up per student, not per section, to avoid four teachers independently intervening.

**PRD implications:** student-360 record with tiered visibility; case objects with SLA timers and outcome tracking (so IQAC can measure intervention efficacy); risk model must be explainable ("flagged because attendance 41% + 2 missing submissions") — matching the spec's evidence-based flag cards.

---

### Phase 13 — Evaluations (course & teaching)

**Workflows**

13.1 Evaluation instrument authoring (institution-standard + department extras) — R: DEAN/IQAC, C: DA
13.2 Evaluation window scheduling, anonymity guarantees, response-rate nudges (optionally grade-view gating: must evaluate before seeing grades — configurable, controversial) — R: IQAC, engine
13.3 Results release: aggregate to TCH after grade posting (never before, to prevent bias/retaliation loops), comparative analytics to DA/DEAN — R: IQAC
13.4 Low-score follow-up workflow (development plan) — R: DA, A: DEAN

**Edge cases**

- Section with 3 students — anonymity mathematically broken; minimum-n suppression rule.
- Instructor swap mid-term — split evaluation attribution by teaching period.
- Abusive free-text comments — moderation before release, with policy on redaction vs. suppression.
- Evaluation window overlaps withdrawal: do withdrawn students evaluate? (configurable).

---

### Phase 14 — OBE & accreditation (IQAC-facing)

**Workflows**

14.1 Outcome hierarchy: PEOs → PLOs → CLOs with mapping matrices — R: DA/CC, A: DEAN/IQAC
14.2 Assessment-item-to-CLO tagging so every grade event doubles as outcome evidence — R: TCH/CC
14.3 Attainment computation: per-student, per-CLO/PLO, per-cohort, threshold-based, with direct (assessment) and indirect (survey) measures — engine, A: IQAC
14.4 Continuous-improvement loop: attainment gap → action item → next-cycle re-measure ("closing the loop" records) — R: DA, A: IQAC
14.5 Accreditation evidence packs: BAC/UGC (Bangladesh), Washington Accord-style exports; sample student work archival per assessment item — R: IQAC, platform

**Edge cases**

- CLO mapping changed mid-term invalidates half a term's evidence — mappings version-lock at term start.
- An assessment item tagged to zero CLOs (evidence hole) — completeness linting before term close.
- Transfer students with untagged external credits create attainment denominators gaps.
- Accreditor requests evidence from 4 years ago — archival retrieval must preserve the rubric, submission, and grade context together, not just scores.

**PRD implications:** OBE cannot be an afterthought layer — the assessment data model must carry outcome tags natively; attainment reports must be reproducible (versioned inputs).

---

### Phase 15 — Term close, rollover, archival

**Workflows**

15.1 Term-close checklist engine: all grades posted, incompletes contracted, evaluations closed, integrity cases resolved-or-carried — R: REG, dashboard per role (matches the spec's "Closing Summer 2026" timeline)
15.2 Rollover: copy offerings/sections/content forward with date-shift, staffing reset, enrollment cleared — R: CC/DA, tooling
15.3 Course-site read-only freeze for students (configurable post-term access window) — policy TSA
15.4 Archival: cold storage of submissions/media per retention schedule; legal-hold exemptions (pending appeals/integrity cases block archival) — R: platform, policy TSA/REG
15.5 Statistical snapshots for year-over-year IQAC reporting before archival — R: IQAC

**Edge cases**

- Rollover run twice → duplicate sections; rollover before certification complete pulls provisional artifacts forward.
- A carried-over Incomplete needs the *old* section's assessment tools alive next term for one student.
- Retention conflict: policy says delete after 5 years, but an alumni grade appeal or accreditation cycle needs year 6 — legal hold beats retention, always.
- Storage-cost pressure (SPA) vs. tenant retention promises — quota policy at archival tier.

---

### Phase 16 — Graduation & clearance

**Workflows**

16.1 Graduation application by STU; auto-eligibility pre-check from degree audit — R: STU, engine
16.2 Final degree audit: requirements, substitutions/waivers applied, residency/credit minimums, CGPA threshold — R: REG, A: DEAN
16.3 Clearance matrix: FIN dues, library, lab equipment, hostel, department sign-offs — parallel sign-off workflow, R: each unit, orchestrated by REG
16.4 Credential issuance: provisional certificate, final certificate/diploma, verified digital credentials, transcript legend — R: REG, A: DEAN/VC
16.5 Convocation logistics data (optional module) — R: REG

**Edge cases**

- Passes the audit except one grade under appeal — conditional graduation state.
- Final-term grade posted late, after the convocation list is locked.
- Clearance blocked by a ৳50 library fine (threshold-based auto-clear policy).
- Degree awarded, then a retroactive integrity finding → credential revocation workflow (rare, must exist, DEAN/VC only, fully audited).
- Name/spelling correction on the certificate after issuance; legal name change.
- Student completes requirements of *two* curriculum versions — which appears on record.

---

### Phase 17 — Alumni access

**Workflows**

17.1 Role transition STU → Alumnus on conferral: enrollment functions off, transcript/credential access retained — R: platform, policy TSA
17.2 Transcript/certificate request & verification portal for employers (tokenized verification links) — R: REG, self-service
17.3 Content access policy post-graduation (none / read-only N months / lifetime for own submissions) — policy TSA
17.4 Alumni re-admission (masters after bachelors) — identity continuity, one person one record across student lifecycles — R: REG
17.5 Account lifecycle: institutional email expiry vs. platform access; dormancy and re-verification — R: TSA

**Edge cases**

- Alumnus email (the login) is deactivated by IT — recovery path must not depend on institutional email.
- GDPR/BD-DPA-style erasure request from an alumnus vs. the registrar's statutory duty to retain academic records — erasure applies to behavioral/engagement data, never the official record; PRD must draw this line explicitly.
- Employer verification of a revoked credential must return "revoked," not "not found."

---

## Part C — Consolidated PRD requirement implications

**1. Configurability as the core architecture.** Nearly every phase above forked on "per tenant policy." The PRD needs a *policy registry*: named policy points (≈150+ identified above — retake rule, waitlist claim window, attendance bar, partial-publish, late penalty guardrails…), each with type, default, allowed range, and owning role (TSA vs. REG vs. DA). Shipping these as code constants is the failure mode.

**2. Everything effective-dated, nothing overwritten.** Org structure, curriculum versions, calendars, weight schemes, grades, attendance: all are event-sourced or temporally versioned. Corrections supersede; they never erase. This single principle resolves the majority of "retroactive change" edge cases.

**3. Rules engines with evaluation traces.** Registration eligibility, prereq graphs, degree audit, finals eligibility, attainment: each must record *why* a decision was made (inputs + rule version) so appeals, overrides, and audits are answerable.

**4. State machines with role-locked transitions and deadline behavior.** Grade lifecycle (draft→provisional→moderated→certified→posted→amended), enrollment (carted→registered→dropped/withdrawn/completed), holds, integrity cases, incompletes (with auto-lapse), waitlist entries (queued→offered→claimed/expired). Every state machine needs a defined "deadline passed with work pending" branch — that's where real institutions live.

**5. Override-with-audit everywhere, silent-bypass nowhere.** Registrar force-registration, DA capacity override, DEAN retroactive withdrawal, attendance un-bar: each is a typed, reasoned, approver-scoped object feeding an exceptions report for IQAC.

**6. Event-driven downstream cascade.** Grade posted → GPA → standing → probation hold → registration eligibility → FIN scholarship check → graduation audit. The PRD must specify the cascade graph and what recomputes on amendment, because bulk grade changes are routine, not exceptional.

**7. Integration contracts with declared direction-of-truth per entity.** Student master (SIS→LMS), enrollments (configurable, must pick one), grades (LMS→SIS), fees/holds (FIN→LMS). Include conflict-resolution and reconciliation-report requirements, plus degraded-mode behavior when SIS is down during registration.

**8. Notification criticality classes and acknowledgment tracking** for action-required events (waitlist offers, hold placements, exam moves) — these are appeal evidence.

**9. Privacy, retention, and legal hold.** Tiered note visibility, evaluation anonymity minimum-n, recording consent, official-record retention vs. erasure rights, legal holds beating retention schedules.

**10. Resilience assumptions for the market.** Power/network interruption during timed assessments, SMS-first fallbacks, low-bandwidth media renditions, offline attendance import, and emergency calendar-shift tooling are core requirements in the Bangladesh context, not nice-to-haves.

**11. Role model must be a permission fabric, not four personas.** The current product's Student/Faculty/Chair/Coordinator set must generalize: one human, many contextual roles (a TA who is a student; a Chair who teaches; a Coordinator who grades), with capability-level grants (grade vs. certify vs. post) rather than page-level roles — otherwise Registrar, Dean/IQAC, FIN, and TSA cannot be added without rewrites.

**12. Term-close orchestration as a product surface.** The existing spec's timeline ("Aug 22 → Aug 28 (you) → Sep 1") is the right instinct; the PRD should generalize it into a cross-role checklist engine where every phase above contributes items and blockers.

Time to put together the complete solution and deliver it to the user.