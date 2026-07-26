# Bangladesh Private-University LMS SaaS — Regulatory & Operational Requirements Research

## Executive summary

The binding legal surface for a university LMS in Bangladesh is narrower than it first appears, but the *accreditation evidence* surface is very wide. Three things drive most of the product scope:

1. **Accreditation is the real requirements engine.** BAC's 10 standards and BAETE's 9 criteria both demand documentary evidence that a generic LMS does not produce — CO→PO attainment mapping, question-paper moderation trails, attendance registers, course files, and CQI loops. This is where a Bangladesh-specific LMS wins against Moodle/Canvas.
2. **Data protection recently became real, then softened.** The Personal Data Protection Act 2026 (enacted 10 April 2026, deemed effective 6 Nov 2025) is in force for substantive obligations, but enforcement machinery is deferred. Crucially, a February 2026 amendment **narrowed data localization** to only restricted personal data and CII data — this materially changes your hosting architecture decision.
3. **Nearly every academic rule is university-specific, not national.** Grading scales, attendance thresholds, and probation rules differ materially across BRAC, NSU, and AIUB. These must be tenant-configurable; hardcoding any of them is a design defect.

Two items require legal verification before the PRD is locked: whether student biometric/health data constitutes "restricted personal data" (triggering mandatory in-country replication), and whether a given university falls under the National Cloud Policy.

---

## 1. Academic model and UGC requirements

### 1.1 What is mandatory

| Requirement | Detail | Status |
|---|---|---|
| UGC approval of programs and curricula | No course may be opened, expanded, or amended — and no student admitted — without UGC approval. Upheld by the Appellate Division. | **Mandatory** |
| Semester system | UGC directed private universities to replace trimesters with semesters from 1 July 2023; ~18 weeks/term, 36 weeks/year. UGC withholds new/revised course approval from non-compliant universities. | **Mandatory** |
| Outcome-Based Education curriculum | UGC OBE Curriculum Template requires PLOs, CLOs, and explicit CLO→PLO mapping per course. | **Mandatory** |
| BNQF alignment | Minimum graduating credits by level: 3-year bachelor's 120, 4-year bachelor's/honours 140. BAC implements BNQF Levels 7–10. | **Mandatory** |
| General education minimum | BAC Criterion 4.7: bachelor's programs ≥25% of total credits as general education; master's ≥10%. | **Mandatory for accreditation** |
| Reserved seats | ≥6% of seats with full tuition waivers (3% children of freedom fighters, 3% meritorious underprivileged); list submitted to UGC. | **Mandatory** |

### 1.2 Product implications

- **Credit definition must be configurable.** The standard is 1 credit = 1 hour/week × 14 weeks for lecture/tutorial, but notional-hours accounting differs for labs, internships, and capstones. Model credits, contact hours, and notional hours as separate fields.
- **Curriculum versioning is non-negotiable.** UGC-approved syllabi are valid for four years. Students admitted under different catalog years must be graduated against their own version. Re-admitted students are counted under the *re-admitted batch's* syllabus, which can produce a total earned credit count different from their original cohort.
- **Trimester→semester migration is a live data problem.** Any university that transitioned carries historical trimester records that must remain renderable on transcripts alongside semester records.
- **Program-level approval state** should be a first-class entity: a program can be pending, approved, approved-with-conditions, or expired, and the LMS should refuse enrollment into unapproved programs.

---

## 2. Accreditation: what the LMS must be able to evidence

### 2.1 BAC (Bangladesh Accreditation Council) — 10 standards

Accreditation requires **≥70% overall in External Quality Assessment with ≥50% in each standard**. 60–69% yields only a one-year, non-renewable "Certificate of Confidence." Eligibility requires a permanent IQAC and at least one graduated cohort two years before application. Institutional accreditation requires ≥20% of programs accredited (minimum three).

The ten standards are: Governance; Leadership, Responsibility and Autonomy; Institutional Integrity and Transparency; Curriculum; Teaching-Learning and Assessment; Student Admission and Support Services; Faculty and Professional Staff; Facilities and Resources; Research and Scholarly Activities; Monitoring, Evaluation and Continual Improvement.

**Directly LMS-relevant criteria with named evidence artifacts:**

| Criterion | Required evidence | LMS feature |
|---|---|---|
| 1.4 Academic calendar | Approved calendar with class start/close, final exam, result publication dates; class routine; **attendance register**; result notifications for last two semesters | Configurable academic calendar; immutable attendance register export |
| 1.5 Class size policy | Enrolled student list per section; **attendance registers per section** | Section-level roster and attendance |
| 1.6 IT-based student database | Student portfolio with contact details, **next of kin**, academic details, credentials | Student master record incl. guardian/next-of-kin fields |
| 3.4 Student handbook | Downloadable handbook for online/blended learning containing curriculum, calendar, disciplinary rules, examination rules | Versioned, publishable handbook artifact |
| 4.8 Course file | Documented course file with course plan | Per-course-offering file bundle, exportable |
| 5.1 Assessment evidence | Course plan with CLOs; **question papers, answer scripts, assignments** for both formative and summative | Artifact retention incl. scanned/uploaded answer scripts |
| 5.3 Class records | Course teachers maintain class schedule and records | Session-level delivery log |
| 5.5 Timely feedback | Students get timely feedback on all assessments | Feedback SLA tracking and reporting |
| 5.6 Question moderation | Semester final question papers **moderated** | Moderation workflow with approver identity and timestamp |
| 5.7 Progression rules | Clearly defined progression rules | Configurable progression rule engine |

### 2.2 BAETE (IEB) — engineering programs

BAETE became a **full Washington Accord signatory on 12 June 2024**. Accreditation Criteria ACC-MAN-02 v3.0 took effect **1 July 2025**.

Eligibility: UGC-approved engineering degree, four years after twelve years of schooling, at least one graduated cohort, OBE pedagogy, and **minimum 130 total credit hours**.

The nine criteria are: Program Educational Objectives; Program Outcomes and Assessment; Curriculum and Teaching-Learning Processes; Interactions with the Industry; Continuous Quality Improvement; Students; Faculty; Governance, Finance and Safety; Academic Facilities and Technical Support.

**The hard LMS requirement here is the outcome attainment engine.** BAETE requires 12 Program Outcomes (PO1–PO12), a 9-attribute Knowledge Profile (WK1–WK9), 7 Complex Engineering Problem attributes (WP1–WP7), and 5 Complex Engineering Activity attributes (EA1–EA5). The program must demonstrate **using direct methods** that students attain all POs by graduation, and must map how each WK attribute is addressed in the curriculum, plus how WP and EA attributes appear in teaching, learning, and assessment. It must additionally map UN SDG coverage.

Note the version drift: v3.0 renumbered the knowledge profile from K1–K8 to **WK1–WK9** and problem attributes from P1–P7 to **WP1–WP7**. Your rubric templates must be versioned against the BAETE document version, because programs accredited under v2.1 and v3.0 coexist.

**Product implication:** you need a generalized outcomes framework, not a hardcoded one. A single tenant may simultaneously run BAC/BNQF learning-outcome domains (Knowledge, Social, Thinking, Personal) for business programs and BAETE PO1–PO12 with WK/WP/EA tagging for engineering programs. Model outcome sets as pluggable frameworks with per-program binding.

---

## 3. Grading, attendance, and progression — configurable, never hardcoded

The variation between the three reference universities is severe. This table is the strongest argument in the whole research for a configuration-first architecture.

| Dimension | BRAC University | NSU | AIUB |
|---|---|---|---|
| Grade scale | 90–100 = A (4.0), then A- 3.7, B+ 3.3 … D- 0.7, F <50 | Standard 4.0 | 90–100 = A+ (4.0), 85–<90 = A (3.75), 80–<85 = B+ (3.5) … D 2.25, F <50 |
| Highest grade letter | **A** | A | **A+** |
| Attendance | Compulsory; **5% of total marks** allocated to attendance; <70% bars from final exam (per JPGSPH handbook) | Instructor-determined; may be dropped after **3 consecutive** absences | **≥80% required**; below that → **UW grade** |
| Failure-to-meet-attendance outcome | Barred from final | Dropped from course | UW, converts to F if not dropped in time |
| Probation threshold | CGPA 2.0 (general guidelines) / **1.5** (revised policy, Summer-2019 onward) | CGPA 2.00, max 3 terms probation | Separate probation guidelines restricting drops |
| Dismissal | Fails to raise CGPA to 1.5 over two consecutive semesters | After 3 probation terms | Per policy |
| First-semester rule | GPA <1.0 may be asked to withdraw | — | — |
| Retake cap | Retaken course capped at **B+** | — | — |
| Repeat rule | B- or below may repeat once, capped at B+ | — | — |
| Credit transfer | — | Max **50%** of credits; only grade C or above; transferred grades excluded from CGPA | Requires CGPA **3.50**; must complete **60%** at AIUB |
| Min. credits for degree | — | **120** | — |

**Critical corner cases this table exposes:**

- **Attendance-as-marks vs. attendance-as-gate.** BRAC awards 5% of course marks for attendance; AIUB uses attendance purely as an eligibility gate producing a UW. These are structurally different features, and a tenant may need both simultaneously for different programs.
- **Grade caps on retake/repeat** mean the transcript must store both the *earned* grade and the *capped awarded* grade, plus which attempt it was.
- **Transferred credits excluded from CGPA** (NSU) means the CGPA engine must distinguish credits-earned-toward-degree from credits-in-GPA-denominator.
- **Non-credit remedial courses** (BRAC's 091/092 category) have their own retake limits and don't affect CGPA.
- **Sliding CGPA thresholds by seniority.** BRAC allows continuation at CGPA 1.50 up to the 6th semester (4th for Pharmacy), then requires 2.00. Progression rules are a function of semester count *and* program.
- **UW→F auto-conversion on a deadline** (AIUB) is a scheduled state transition the LMS must execute and audit.
- **Grade change workflow** requires course teacher initiation, then Chair, then Dean approval, then submission to the Examination Controller, with permitted grounds limited to posting errors, calculation errors, incomplete grades, or procedural shortfalls. This is a multi-role approval chain with a reason code, not a simple edit.
- **Leave of absence** up to three consecutive semesters or one academic year, unavailable to students on probation or excluded on disciplinary/academic grounds — a state machine with eligibility preconditions.

---

## 4. Data protection and privacy

### 4.1 Current legal status (verify before relying on)

The chronology matters and is easy to get wrong:

- **Personal Data Protection Ordinance 2025** (Ordinance No. 61 of 2025) — approved 9 Oct 2025, gazetted 6 Nov 2025.
- **Personal Data Protection (Amendment) Ordinance 2026** (Ordinance No. 23 of 2026) — promulgated 5 Feb 2026.
- **Personal Data Protection Act 2026** — enacted by Parliament **10 April 2026**, repealing both instruments above. Deemed effective **6 Nov 2025**, except Sections 23 and 31–35 (Chief Data Officer appointment; complaints and administrative penalties), which await government notification. Reported enforcement activation is around **13 May 2027**.

> **⚠ Legal verification required.** The Act of 2026 is officially published **only in Bangla**. The detailed section-level analysis below derives from the English translation of the 2025 Ordinance plus reporting on the amendment. Section numbering and wording in the Act may differ. Commission a Bangla-source legal review before finalizing the PRD.

### 4.2 Substantive obligations (in force now)

**Extraterritorial scope.** Applies to processing of data of persons in Bangladesh even where processing occurs outside Bangladesh, if connected to providing products/services to, or monitoring/record management of, data subjects in Bangladesh. **A foreign-hosted SaaS is squarely in scope.**

**Consent.** Must be freely given, specific, unambiguous, and revocable. At collection you must disclose purpose, **retention period**, transfer, and withdrawal procedure. **Burden of proof of valid consent sits with the controller** — so consent capture must be logged with timestamp, version of notice shown, and scope.

Lawful bases without consent include contract performance, legal obligations, vital interests, and employment/labour/social-security rights.

**Sensitive personal data** (includes health, genetic, biometric, financial) requires specific consent or another enumerated basis.

**Children.** A child is **under 18** — which captures a meaningful share of first-year undergraduates in Bangladesh. Requires parental/guardian consent, and **prohibits tracking, monitoring, profiling, or targeted advertising of a specific child**. Guardian consent remains valid until the student turns 18.

> **⚠ Major design constraint.** Learning analytics, engagement scoring, at-risk-student prediction, and behavioural nudges applied to a 17-year-old first-year student may constitute prohibited profiling. The LMS needs an age-derived flag that suppresses profiling features per-user until the 18th birthday, and a scheduled transition at that date.

**Data subject rights:** access, correction, deletion, restriction of automated decisions, **portability** (including direct controller-to-controller transfer via "Federated Interoperable Ecosystems"), and withdrawal of consent.

Access responses must include a summary of data, activities undertaken, purpose, type, recipients, retention, source, **safeguards for cross-border transfers**, and a description of the rationale and significance of automated decisions.

**Automated decisions.** No processing, withdrawal, or transfer by automated means without informing the data subject. Data subjects can restrict automated decisions. **Automated academic decisions — auto-fail on attendance, algorithmic plagiarism flags, auto-computed probation status — need a disclosed rationale and a human-review path.**

**Deletion propagation.** Section 14 requires "system-wide propagation" of approved correction/deletion requests, with a primary-source hierarchy and consistency across all other controllers/processors. **In a SaaS with integrations, deletion must cascade to the SIS, payment gateway records, analytics store, and backups.**

**Record retention.** Controllers must preserve records relating to processed personal data in a register for **at least 5 years**, covering processing, retention, structuring, allocation, storage, adaptation, modification, and portability. This is a floor, not a ceiling — and it conflicts operationally with deletion rights, so deletion must be scoped to the data while preserving the processing register.

**Breach notification.** Where a breach is likely to cause significant damage, notify the Authority in the prescribed form and time limit. The Authority weighs the nature of the breach, categories and approximate number of affected data subjects and records, controller contact details, and mitigation measures taken.

> **⚠ Gap.** The Authority has **not yet been established** and the prescribed form/timeline does not yet exist. Build a breach-notification workflow with configurable recipient and deadline rather than hardcoding.

**Chief Data Officer.** Significant data controllers must appoint qualified CDOs. Not yet in force (Section 23 deferred).

**Penalties.** The February 2026 amendment **removed imprisonment**, leaving monetary fines. Government employees are personally accountable for violations by their agencies.

### 4.3 Data localization — the decisive architectural question

Personal data is classified as **Public, Internal, Confidential, and Restricted**. As amended, the synchronized-real-time-copy-in-Bangladesh requirement applies **only** to:

- **Restricted personal data**, and
- Data processed by **Critical Information Infrastructure** as defined in the Cyber Security Ordinance 2025.

General, internal, and confidential personal data on foreign cloud infrastructure is **no longer** subject to mandatory local mirroring. Cross-border transfers of confidential and internal data are permitted to countries with appropriate data protection standards, subject to consent or contractual necessity.

"Restricted personal data" is described as personal data that may impact national security, public order, defence, critical infrastructure, or an individual's fundamental rights and freedoms — and may include classified datasets, **critical health- or security-related information**, or anything the Authority designates as restricted.

> **⚠ The single highest-value legal question for this PRD:** Does a Bangladeshi private university's LMS hold restricted personal data?
>
> Candidate triggers: **biometric attendance data** (fingerprint/face terminals are widespread in Bangladeshi universities), **student health/disability records** used for accommodations, and **counselling records** from student support services. Biometric and genetic data are expressly defined as sensitive; whether they are *restricted* under the §29 classification is not settled in the sources reviewed.
>
> **If biometric attendance is in scope, foreign-only hosting becomes non-compliant** and you need an in-country synchronized replica. This should be resolved before choosing a hosting topology.
>
> **Mitigation to consider regardless:** architect biometric templates and health/accommodation records as a separately-hosted, in-Bangladesh data domain, so the residency question can be answered "yes" cheaply without relocating the whole platform.

---

## 5. Cybersecurity

### 5.1 Current law

**The Cyber Security Act 2026 (Act No. 81 of 2026) is the operative law**, having repealed the Cyber Security Ordinance 2025 (which itself replaced the Cyber Security Act 2023 and the Digital Security Act 2018). CII designations under Section 15 of the 2026 Act were **gazetted 20 April 2026**.

Note that much secondary commentary — and even the National Cloud Policy — still references the 2025 Ordinance. Cite the 2026 Act.

### 5.2 CII obligations (if designated)

Institutions and regulators referenced: National Cybersecurity Agency (NCSA), National Security Operations Center (NSOC), BGD e-GOV CIRT, and BCC as National CERT.

A designated CII must maintain its **own CERT/CIRT and Security Operations Center**, and every SOC must submit **quarterly activity and success-indicator reports to the national SOC**. Additional obligations: real-time NSOC connectivity, periodic security audits and vulnerability assessments by qualified experts, documented cybersecurity policies, a designated responsible person or team, employee awareness training, immediate incident reporting to NCSA and CIRT, and forensic evidence preservation.

The Act permits cloud-based security tooling — SIEM, SOAR, EDR/XDR, NDR — and log exchange, subject to Council approval.

> **Assessment:** a private university LMS is **unlikely** to be individually designated CII. But if the SaaS also serves public universities or integrates with national registries, designation risk rises. Treat CII-grade controls as an enterprise tier, not a baseline.

**Responsible disclosure note for the security policy:** for vulnerabilities in government systems or CII, BGD e-GOV CIRT is the required channel — direct contact with the department is not the safe legal route.

### 5.3 Bangladesh Bank ICT Security Guideline v4.0 (April 2023)

Applies to banks, NBFIs, MFS providers, PSPs, PSOs, and merchant acquirers — **not** directly to a university or its LMS vendor. However, Chapter 11 (Digital Payment Security) covers ATM/CRM/CDM, POS, QR, internet/application banking, payment cards, interoperability, and MFS, and referenced standards include PCI DSS v4.0, EMVCo, NIST SP 800-63, ISO/IEC 27001, and OWASP.

**This flows down to you contractually via your PSO/PSP integration agreements**, and is a strong buyer expectation in security questionnaires even though it does not bind you directly.

---

## 6. Hosting, data residency, and procurement

### 6.1 National Cloud Policy (ICT Division, 2026)

> **⚠ Scope caveat.** This policy binds **ministries, divisions, departments, and agencies** — government bodies. A private university is not one. **Verify** whether it reaches private HEIs receiving government funds, or public universities that may become tenants. Even where non-binding, treat it as the de facto benchmark for security questionnaires, since it is the most detailed articulation of Bangladeshi state expectations for cloud services.

**Data classification D0–D4 with residency rules:**

| Class | Description | Minimum controls | Residency |
|---|---|---|---|
| D0 Open | Public data, no personal data | Integrity, provenance | Any location |
| D1 Internal | Operational, not public | IAM, TLS, logging | Prefer Bangladesh |
| D2 Confidential | Sensitive govt/personal data, citizen accounts | Strong IAM, encryption, DPIA | **Bangladesh only** |
| D3 Restricted | Health, tax, biometric | HSM/KMS, PAM, SIEM | Sovereign only |
| D4 National Critical | CII, national registries | HYOK, 24/7 SOC, isolation | NDC mandatory |

**Workload placement:** D0 permitted anywhere. D1 permitted on public cloud with controls. **D2 on accredited public cloud only if HYOK is implemented such that the provider has no access to decryption keys.** D3 mandatory in sovereign cloud zones (public cloud prohibited). D4 sovereign only, on-premises air-gapped only.

**Residency applies to all derivative artifacts** — read replicas, object storage replication and versioning copies, backups and snapshots, **log aggregation including SIEM and APM datasets**, support dumps and diagnostic artifacts, and **CDN edge caches**. This is the trap most SaaS vendors fall into: your observability stack and CDN silently violate residency.

**Crypto and access:** TLS 1.2+ mandatory for all workloads; AES-256 at rest for D2+; BYOK/HYOK with Bangladesh-resident KMS/HSM for D3/D4; MFA mandatory for admin access and D2+ data, with **phishing-resistant MFA (FIDO2/WebAuthn) for privileged users**; defined key rotation, revocation, separation of duties between key admins and data users, and audit logging of all key operations.

**Multi-tenancy requirements** (directly relevant to a SaaS): strict tenant isolation; separation of duty preventing any single administrator having unrestricted cross-tenant access; auditable administrative boundaries; separate identity boundaries and admin roles per tenant with **prohibition of shared administrator accounts**; isolated network segments with micro-segmentation for east-west traffic; **tenant-specific encryption keys via separate key hierarchies where feasible**; and comprehensive audit logging with tenant attribution.

**Provider accreditation tiers:** Tier A (baseline) for D0–D2; Tier B (high) for D3, requiring domestic hosting and customer-controlled keys; Tier C (CII) for D4, requiring tested DR exercises, heightened audit rights, and NSOC integration. A National Cloud Provider Registry covers NDC, BDCCL Government Cloud, and accredited Meghna Cloud.

**Sovereign infrastructure options:** National Data Center (under BCC) for highest sensitivity; BDCCL as Government Cloud service integrator; Meghna Cloud and other accredited domestic providers.

The policy also requires **portability and exit readiness** with explicit lock-in avoidance, egress planning, and provider-insolvency continuity — so a documented exit plan and bulk data export are procurement gate items.

### 6.2 National Data Governance Ordinance 2025 and source code

Gazetted 6 Nov 2025, alongside the PDPO. Establishes a National Data Management Authority, the **National Source Code Repository** managed by BCC, a National Responsible Data Exchange (NRDEX) platform, and a Unified Digital Identity concept.

The draft **National Source Code Policy 2025** ("Public Money, Public Code," published December 2025) requires that source code of government-funded software be deposited in the repository, that **no software be deployed to production until source code is stored**, that government-developed code be treated as open source by default unless exempted, and that datasets be classified Open/Restricted/Regulated and registered in a National Data Catalog. It mandates secure coding supervision, an approved CI/CD pipeline, automated and manual security checks, licence verification, RBAC on the repository, and government-approved NDAs for contributors. An **escrow system** may be established where necessary.

> **⚠ Commercial risk to flag.** This applies to government-funded software. A commercial SaaS sold to private universities is outside scope. **But** if a public university procures with government budget or donor funds, source-code deposit or escrow could be demanded — a direct conflict with a proprietary SaaS model. Verify before pursuing public-sector tenants, and price escrow as a contractual option.

---

## 7. Accessibility

**Legal basis.** The Rights and Protection of Persons with Disabilities Act 2013 defines accessibility as the right to equal access and equal treatment in all facilities and services available to the public, including information and ICT. Section 6 requires steps for accessibility of information and services disseminated by **government, private and privately owned entities**, expressly naming web accessibility, video subtitles, audio descriptions, screen readers, and text-to-speech. Section 9 covers education and training with accessibility in existing programs. Section 5(e) addresses accessibility of textbooks via e-learning platforms. Bangladesh has ratified the UNCRPD.

**Standard.** The **Digital Service and Web Designing Guideline for Inclusive Accessibility 2022** (ICT Division) mandates **WCAG 2.1** (or its updated version) for websites, mobile apps, and digital services, requires screen-reader compatibility, and frames requirements in UNCRPD terms. The National Web Accessibility Guideline also targets WCAG 2.1.

> **Status:** The 2022 guideline is framed for government platforms; the 2013 Act's duty on private entities is expressed as "take steps ... and encourage," which is weaker than a hard private-sector mandate. **Verify enforceability against private universities.** Practically, treat **WCAG 2.1 AA as the design target** — it is the stated national standard, and compliance is cheap at design time and expensive to retrofit.

Real-world context: audits found over 90% of Bangladeshi government web pages have accessibility violations, and 51.1% of assessed services fall into the "Beginner" maturity tier. Buyer sophistication on accessibility is therefore low today, but the UGC Blended Learning Policy does require methods to be in place for students with special educational needs — so accessibility is an accreditation-adjacent topic, not just a legal one.

**Practical requirements beyond WCAG:** Bangla (Unicode) content rendering and input throughout; captions/subtitles on lecture video; transcripts for audio; keyboard-only operability for all assessment flows (a timed exam that cannot be completed without a mouse is an access failure with academic consequences).

---

## 8. Payments

### 8.1 Regulatory framing

The LMS/SaaS is a **merchant-side integrator, not a regulated payment entity** — provided it never holds funds. This is the key architectural boundary: route to licensed PSOs/PSPs, never take custody.

Relevant instruments: Bangladesh Payment and Settlement Systems Act 2024; Bangladesh Payment and Settlement Systems Regulations 2014; Bangladesh MFS Regulations 2022; draft **PSO Regulations 2025**.

Under the draft PSO Regulations: five PSO categories (Merchant Acquiring, Payment Switching, ATM/CRM Acquiring, Payment Initiation Service, Card Scheme); PSOs may **not** issue e-money and must settle through licensed commercial banks; **KYC verification for all merchants**; written settlement agreements; **sales proceeds settled within five working days**; cash settlement prohibited; **transaction data preserved for at least 12 years**; major data breach or operational failure reported to Bangladesh Bank **within 24 to 72 hours**. Minimum capital ranges Tk1 crore (digital merchant acquiring) to Tk20 crore (ATM/CRM). Trust and Settlement Account shortfalls attract fines up to Tk30 lakh with personal liability for directors, CEOs, and treasury officers.

MFS providers must be subsidiaries of scheduled banks/FIs/government entities with ≥51% parent equity, licensed as PSPs. P2B payments explicitly include **educational institution fee payments**, merchant payments, and online/e-commerce payments.

Major PSOs: **SSLCOMMERZ, shurjoPay, IT Consultants Ltd, aamarPay, PayStation**. Education-focused aggregators include EPS and Moneybag.

> **⚠ Note the 12-year retention flow-down.** If a settlement agreement passes that obligation to you as a technical service provider, it collides with PDPA deletion rights. Resolve contractually: the PSO should be the record-holder of transaction data; you hold only a reconciliation reference.

### 8.2 Operational realities (from a live university configuration)

Uttara University's published guidelines are a useful concrete model:

- Multiple rails in parallel: MFS (bKash, Rocket, Nagad), cards (VISA, Mastercard, NEXUS), POS at the finance office, and **designated bank branches** with deposit slips.
- **Per-rail merchant fees differ and are passed to the student**: Rocket Bill Pay no charge, bKash 1.50%, Nagad 1%. General market MDR runs ~1–2%.
- **Biller numbers** are a distinct identifier type (Rocket biller 2922, Nagad biller 1388) separate from merchant account numbers.
- **Auto-generated deposit slips printed from the ERP**, plus manually collected printed slips — so offline reconciliation is a first-class flow, not a fallback.
- Only *some* banks are integrated for automatic portal updates; others require manual reconciliation.
- **Cash refused for tuition, but accepted for new-student admission fees** — a per-fee-type payment-method policy.

**Derived requirements:** per-rail fee disclosure before payment confirmation; bulk collection via Excel upload (bKash/Rocket/any bank); idempotent webhook handling with reconciliation by biller reference; partial payment and installment support; auto-generation of semester/per-credit/package bills, over-credit fees, over-semester fees, and retake fees; scholarship and waiver auto-application.

### 8.3 Registration/payment coupling — a corner case with legal edges

NSU's rule that "no registration is complete until all tuition and other fees are paid" means the LMS must support **hard payment gating on enrollment**. But BRAC's rule that "there is no refund of tuition for individual courses dropped after the last day of the change of program period" means drop timing changes financial outcome. **Drop/add windows, refund percentage schedules, and enrollment gating must be a single coordinated configuration**, not three independent settings — inconsistency here produces direct financial disputes with students.

---

## 9. Finance, tax, and statutory reporting

| Item | Detail | Status |
|---|---|---|
| VAT on tuition | Private universities (service code S070.10) and private medical/engineering colleges (S070.20) are **exempted**. Past attempts to impose VAT were withdrawn after protests. | **Exempt** |
| Corporate income tax | Contested. Appellate Division ruled 27 Feb 2024 that private universities pay 15%. Rate cut to 15% then to **10% effective 1 July 2026** (2026-27 budget). Institutions may avoid liability by demonstrating genuine non-profit trust operation. | **Uncertain / evolving** |
| Non-profit constraint | Private University Act 2010 s.44(7): the general fund may not be used for any purpose other than necessary university expenses. Trustees may not take financial benefit. | **Mandatory** |
| Annual financial reporting | s.45(1)–(2): accounts in the UGC-prescribed **PUFR** format, audited by a Ministry-of-Education-designated audit firm, submitted to UGC **and** the Ministry by **31 December** following the financial year. | **Mandatory** |
| Penalty for non-compliance | s.49: investigation, charter cancellation, imprisonment up to 5 years, fine up to Tk10 lakh, or both. | **Mandatory** |

**PUFR forms the LMS/ERP must be able to feed:** PUFR-I Chart of Accounts; PUFR-II Trial Balance after adjustment; PUFR-III Annual Financial Statements (Balance Sheet, Income & Expenditure, Statement of Change in Funds covering Trust Fund/General Fund/Retained Earnings, Cash Flow); PUFR-IV Educational-department-wise Income and Expenditure; **PUFR-V Schedule of Student Fees, headcount of academic and non-academic staff, and remuneration of governing and executive bodies**; PUFR-VI Development (capital) expenditure by year, program, and project; PUFR-VII Performance evaluation / ratio analysis. PUFRs comply with BAS/IAS/IFRS.

**PUFR-V is the direct LMS integration point** — it needs student fee schedules by program and department-wise revenue attribution. Build department/program dimensions into the fee ledger from day one.

**Pending legislative change to watch:** a draft amendment would require **UGC approval for any change to tuition fees**, and freeze fees fixed at admission until the student completes the program. If enacted, the LMS must support **per-cohort fee schedules locked at admission** — a significant data model requirement. Verify current enactment status.

---

## 10. Blended/online learning

The UGC **Policy on Blended Learning for Bangladesh** was approved **27 February 2022**. It sets seven broad policies and requires institutional rules to align with UGC, with sufficient infrastructure, budget, and workforce.

Key assessment provision: **summative assessment (final exam) shall be a regular onsite assessment** unless conditions are unusual (e.g. a pandemic). Continuous assessments — midterms, class tests, quizzes, assignments — **may** be evaluated online with prior academic committee approval, which must create appropriate remote invigilation, online proctoring, or remote online proctoring procedures.

> **Product implication:** do not build an online-final-exam-first product. The default configuration should be **onsite final, online continuous assessment**, with online summative as an emergency mode that requires a recorded academic-committee approval artifact. This also affects proctoring investment priority.

The policy also requires assessment across cognitive, psychomotor, and affective domains, with methods in place for students with special educational needs, and assessment beyond traditional methods (open-ended/scenario-based questions, case studies, assignments, projects).

**Plagiarism.** There is currently **no national anti-plagiarism policy** — universities define plagiarism under their own acts. UGC held a stakeholder workshop on a draft universal anti-plagiarism policy on **9 March 2026**, and plans a central research hub with Turnitin, capable of scrutinising both **Bangla and English**. Build a pluggable similarity-check integration and expect a national policy to land; Bangla-language detection is a differentiator.

---

## 11. Digital signatures and academic records

**Legal basis for e-signed transcripts and certificates:** ICT Act 2006 s.5 (subscriber may authenticate an electronic record by affixing digital signature), s.6 (legal recognition of electronic records, signatures, gazettes), s.7 (where any other law requires a signature, a digital signature suffices), s.8 (e-signature valid for government forms/applications/licences). Evidence (Amendment) Act 2022 inserted **s.85C** into the Evidence Act 1872: the court **shall presume** information in a Digital Signature Certificate is correct unless contrary is proved.

**Critical constraint:** under ICT Act **s.36, no digital signature is recognized in Bangladesh unless the certificate was issued by a CA licensed by the Controller of Certifying Authorities (CCA)**. There are approximately six licensed CAs. **There is no recognised foreign Certifying Authority in Bangladesh.**

> **⚠ This rules out DocuSign/Adobe Sign for legally-recognized transcript signing.** You must integrate with a CCA-licensed Bangladeshi CA. Class-3 certificates are the type used for high-assurance transactions and government dealings, and are typically issued on a **crypto token** with a PIN — meaning signing is a hardware-bound, human-in-the-loop operation, not a server-side batch API. Bulk transcript signing at convocation scale needs explicit design.

Supporting instruments: Information Technology (Certifying Authority) Rules 2010; e-Sign Guideline for Certifying Authorities 2020; Digital Certificate Interoperability Guideline (2018); PKI Enabled Application Guideline 2024; Bangladesh Root CA Certification Practice Statement. Public verification portal: `digisigchecker.cca.gov.bd`.

**Transcript handling norms** (from NSU): a transcript is a certified official copy releasable only to the student, parents of a dependent student, or an authorized person with a specific request signed by the student. Fees paid in advance through the portal or nominated banks. **Access control on transcript release is a privacy requirement, not just a workflow step.**

---

## 12. Connectivity and device reality (design constraints)

| Metric | Value | Source date |
|---|---|---|
| Mobile subscribers | 188.60 million | May 2026 |
| Internet subscribers | 134.07 million (119.12M mobile, 14.95M fixed) | May 2026 |
| Median 4G download | 31.15 Mbps national | Jan 2026 |
| Median 4G upload | 12.22 Mbps | Jan 2026 |
| Operator range (Opensignal) | 15.6–25.4 Mbps | Oct–Dec 2025 |
| Teletalk in weak regions | as low as 2.22 Mbps | Jan 2026 |
| Household mobile phone access | >98% (100% in city corporations) | BBS, recent |
| Household smartphone | 72.8% | BBS |
| Household active internet | 55.1% | BBS |
| **Household computer** | **8.9%** | BBS |
| People offline | 93.4 million | end-2025 |

BTRC's September 2025 QoS framework set minimum 4G at 10 Mbps down / 2 Mbps up, but operators miss it in five to seven of eight regions for bottom-tier users.

**Design implications:**

- **Mobile-first is not a preference, it is the access path.** With 8.9% household computer penetration against 72.8% smartphone penetration, any workflow that assumes a desktop — file uploads, code submission, long-form exams, proctoring with a webcam — excludes a large share of students. Provide mobile-viable equivalents.
- **Design for the bottom decile, not the median.** 31 Mbps median hides 2.22 Mbps regional floors. Video must have low-bitrate and audio-only tiers; assessment must degrade gracefully.
- **Offline tolerance in assessment is essential.** Local answer draft persistence, resumable uploads, and a documented connectivity-failure remediation path. Note the HSTU online exam policy's real-world pattern: students hand-write, photograph, combine into a single PDF, and upload within 20 minutes — with the supervisor empowered to cancel participation on late upload. Your product should make that failure mode rarer, and its adjudication auditable.
- **Data cost sensitivity.** Aggressive asset optimization and a low-data mode are buyer-visible features, not polish.

---

## 13. Consolidated requirements register

### 13.1 Legally or operationally mandatory

| # | Requirement | Basis |
|---|---|---|
| M1 | Program/course entities gated on UGC approval status; block enrollment into unapproved programs | Private University Act 2010; Appellate Division |
| M2 | Semester-based academic calendar (~18 weeks); support legacy trimester records | UGC directive, 1 July 2023 |
| M3 | CLO and PLO entities with CLO→PLO mapping per course | UGC OBE Template |
| M4 | BNQF credit minimums enforced per qualification level (120/140; 130 for BAETE engineering) | BNQF; BAETE ACC-MAN-02 |
| M5 | Consent capture with purpose, retention period, transfer, and withdrawal disclosure; controller-side proof of consent | PDPA 2026 §5 |
| M6 | Data subject rights: access, correction, deletion, restriction of automated decisions, portability, consent withdrawal | PDPA 2026 §§11–13 |
| M7 | Under-18 flag; guardian consent; **suppress profiling, tracking, and targeted content for minors**; auto-transition at 18 | PDPA 2026 §9 |
| M8 | Deletion/correction propagation across integrated systems and backups | PDPA 2026 §14 |
| M9 | Processing register retained ≥5 years | PDPA 2026 §19 |
| M10 | Breach notification workflow with configurable authority, form, and deadline | PDPA 2026 §20 |
| M11 | Automated-decision disclosure and human-review path for algorithmic academic outcomes | PDPA 2026 §13(6), §11(3) |
| M12 | Digital signatures via a **CCA-licensed Bangladeshi CA only** for legally recognized transcripts/certificates | ICT Act 2006 §36 |
| M13 | Transcript release restricted to student, dependent's parents, or student-signed authorization | Privacy norm; PDPA |
| M14 | Financial data model supporting PUFR-V (student fee schedules) and department-wise revenue for PUFR-IV | Private University Act 2010 §45 |
| M15 | 6% reserved-seat tracking with full tuition waiver and UGC list export | Private University Act 2010 |
| M16 | No custody of funds; route to licensed PSO/PSP only | PSS Act 2024; PSO Regs |

### 13.2 Accreditation-driven (mandatory in practice for any credible buyer)

| # | Requirement | Basis |
|---|---|---|
| A1 | Attendance register per section, immutable and exportable | BAC 1.4, 1.5 |
| A2 | Student database with contact details and **next of kin** | BAC 1.6 |
| A3 | Versioned, publishable student handbook artifact | BAC 3.4 |
| A4 | Course file bundle: course plan, CLOs, question papers, answer scripts, assignments, formative and summative | BAC 4.8, 5.1 |
| A5 | **Question paper moderation workflow** with approver identity and timestamp | BAC 5.6 |
| A6 | Timely-feedback SLA tracking and reporting | BAC 5.5 |
| A7 | Configurable progression rule engine | BAC 5.7 |
| A8 | ≥25% general-education credit validation for bachelor's (≥10% master's) | BAC 4.7 |
| A9 | **Direct-method PO attainment computation and reporting** | BAETE 5.2 |
| A10 | Curriculum mapping to WK1–WK9, WP1–WP7, EA1–EA5, and UN SDGs | BAETE 5.3 |
| A11 | CQI loop: PO/PEO review cycles with stakeholder feedback capture | BAETE 5.5; BAC Std 10 |
| A12 | Pluggable, versioned outcome frameworks (BAC/BNQF domains vs. BAETE v2.1 vs. v3.0) coexisting per program | Both |
| A13 | Academic advisor assignment per student with counselling record | BAETE 5.6; BAC 6.5 |
| A14 | Alumni and employer feedback capture for PEO attainment | BAETE 5.1 |
| A15 | Self-Assessment Report data pack export mapped to BAC rubrics | BAC ch. 4 |

### 13.3 Likely buyer expectation

- WCAG 2.1 AA conformance; screen-reader compatibility; captions on lecture video; keyboard-operable assessment.
- Full Bangla (Unicode) UI and content support alongside English.
- Mobile-first responsive design with a low-data mode; offline draft persistence and resumable uploads.
- Multi-rail payments (bKash, Nagad, Rocket, cards, POS, bank deposit slip) with per-rail fee disclosure, bulk Excel reconciliation, and auto-generated deposit slips.
- Fee engine: semester/per-credit/package billing, over-credit and over-semester fees, retake fees, scholarship/waiver automation, installments.
- Tenant-configurable grade scales, attendance rules, probation and dismissal thresholds, drop/add and refund windows, credit-transfer rules.
- Turnitin or equivalent similarity checking, with Bangla-language capability as a differentiator.
- ISO/IEC 27001 posture; encryption at rest (AES-256) and in transit (TLS 1.2+); MFA with FIDO2/WebAuthn for privileged users.
- SaaS multi-tenant isolation: per-tenant identity boundaries, no shared admin accounts, tenant-attributed audit logs, per-tenant key hierarchies.
- Documented exit plan, bulk data export, and no-lock-in commitment.
- Integration with an IQAC workspace (a permanent IQAC is a BAC eligibility precondition).

### 13.4 Uncertain — requires legal verification

| # | Question | Why it matters | Consequence if adverse |
|---|---|---|---|
| U1 | Does biometric attendance / health / counselling data constitute **"restricted personal data"** under PDPA §29(1)(d)? | Determines mandatory in-Bangladesh synchronized replica | Foreign-only hosting becomes non-compliant |
| U2 | Exact section numbering and wording of the **Bangla-only PDPA 2026** vs. the 2025 Ordinance English text | All §-level citations in this research | Compliance mapping needs rework |
| U3 | Does the **National Cloud Policy** reach private HEIs, or only government bodies? | Determines whether D0–D4 classification and sovereign hosting apply | Sovereign-only hosting for D3 workloads |
| U4 | Would a **public university tenant** trigger National Source Code Policy deposit or escrow? | Conflicts with proprietary SaaS | Source code deposit or escrow obligation |
| U5 | Is the **Rights and Protection of Persons with Disabilities Act 2013** enforceable against private universities' digital services, or hortatory? | Determines whether WCAG is legal duty or best practice | Legal exposure on accessibility |
| U6 | Is the **draft PSO Regulation 2025** finalized, and does its 12-year transaction retention flow down to technical service providers? | Conflicts with PDPA deletion rights | Retention/deletion conflict needs contractual resolution |
| U7 | Has the **Private University Act amendment** requiring UGC approval for fee changes and fee-freeze-at-admission been enacted? | Requires per-cohort locked fee schedules | Significant fee data model change |
| U8 | Current **corporate tax** position for private universities given the 2024 Appellate Division ruling and the 2026-27 rate cut to 10% | Affects finance module and non-profit reporting | Reporting model change |
| U9 | Will the **UGC national anti-plagiarism policy** (draft, March 2026) mandate a specific tool or similarity threshold? | Integration and configurability | Forced tool integration |
| U10 | Likelihood of **CII designation** for a university LMS, especially with public-university tenants | Triggers own SOC/CERT, NSOC connectivity, quarterly reporting | Major operational cost |

---

## 14. Corner cases worth explicit PRD treatment

**Academic**

1. Re-admitted students counted under the re-admitted batch's syllabus, producing a total earned credit count different from their original cohort, plus possible "Complementary Course" requirements decided by the Academic Committee.
2. Retake/repeat grade caps (B+) requiring storage of earned vs. awarded grade and attempt number.
3. Non-credit remedial courses (091/092) with distinct retake limits, excluded from CGPA.
4. Transferred credits counting toward the degree but excluded from the CGPA denominator.
5. Sliding CGPA thresholds by semester count and by program (BRAC: 1.50 to 6th semester, 4th for Pharmacy, then 2.00).
6. UW→F automatic conversion on a deadline, with drop restricted for students on probation.
7. Students who sit a final exam but cannot complete it receive F with no make-up and no appeal — the system must not offer a resit path where policy forbids one.
8. Grade change restricted to enumerated grounds with a teacher→Chair→Dean→Examination Controller chain.
9. Leave of absence up to three consecutive semesters, unavailable to students on probation or excluded on disciplinary grounds, with mandatory registration in the semester immediately following expiry.
10. Dropped-for-consecutive-absence (NSU: three consecutive classes) as an instructor-initiated action distinct from attendance-percentage gating.
11. Exam duration varying by credit value (3 hours for 3-credit, 2 hours for 2-credit).
12. Curriculum validity expiry — UGC-approved syllabi valid four years; expiry must not silently invalidate in-flight students.

**Compliance**

13. A 17-year-old first-year student: profiling suppression, guardian consent, and the birthday transition.
14. Deletion request from a graduate whose transcript must be retained for institutional/legal purposes — deletion scope must exclude the academic record of award while honouring the request elsewhere. Reconcile with the ≥5-year processing register.
15. CDN edge caches, SIEM/APM log stores, backups, and support diagnostic dumps silently violating residency.
16. Bulk transcript signing at convocation scale against hardware-token, PIN-bound Class-3 certificates.
17. Breach notification with no established Authority and no prescribed form yet.

**Payments**

18. Per-rail merchant fee differences (bKash 1.50%, Nagad 1%, Rocket 0%) disclosed pre-confirmation.
19. Cash refused for tuition but accepted for new-student admission fees — per-fee-type method policy.
20. Banks not integrated for auto-update requiring manual reconciliation against deposit slips.
21. Drop timing changing refund entitlement, coupled to enrollment payment gating.
22. Duplicate webhook delivery and idempotency keyed on biller reference.

**Operational**

23. A single tenant running BAC/BNQF outcome domains for business programs and BAETE PO1–PO12 for engineering, simultaneously, with programs accredited under different BAETE document versions.
24. Emergency switch to online summative assessment requiring a recorded academic-committee approval artifact.
25. A student on a 2.22 Mbps connection attempting a timed assessment.

---

## 15. Sources

**UGC / curriculum / BNQF**
- UGC OBE Curriculum Template — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-ugc/2024/12/c8f74c31cb91452d9d59e37367b3275f.pdf
- Trimester→semester transition — https://www.tbsnews.net/bangladesh/education/private-unis-replace-trimesters-semesters-1-july-380089
- OBE/BNQF credit levels (IIUC) — https://web.iiuc.ac.bd/home/show-pdf/files4dZfTMdaau8PzjIZ8h9RInformation-on-OBE-curriculum-BAC-AccreditationT4CIV47CEU5qOj2ShAtD
- UGC Policy on Blended Learning for Bangladesh (approved 27 Feb 2022) — https://blendedlearning.ulab.edu.bd/sites/default/files/Policy-on-Blended-Learning-for-Bangladesh.pdf
- UGC anti-plagiarism policy in development (Mar 2026) — https://www.bssnews.net/news/367265
- UGC plagiarism software / central research hub — https://publisher.tbsnews.net/bangladesh/education/ugc-plans-research-hub-software-check-plagiarism-262006

**Accreditation**
- BAC Accreditation Manual 2nd Edition 2025 (full 10 standards) — https://iqac.iubat.edu/wp-content/uploads/2025/08/Reprint_Final_BAC_Manual_2nd_Edition_2025.pdf
- BAC Manual (BAC official mirror) — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-bac/2024/12/358bd524328a4577bd3e38e9cd682dd2.pdf
- BAC Accreditation Process and thresholds — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-bac/2024/12/cb63607106a04544887edd2e88e202c8.pdf
- BAETE Accreditation Criteria ACC-MAN-02 v3.0 (eff. 1 Jul 2025) — http://www.baetebangladesh.org/acc-man-02-v3-f.html
- BAETE Washington Accord full signatory (12 Jun 2024) — https://www.baetebangladesh.org/old-site/recognition.php
- BAETE Accreditation Manual 2nd ed. (130-credit minimum) — https://www.baetebangladesh.org/2nd_edi_05.03.2019_F.pdf
- BAETE definitions and acronyms ACC-MAN-06 — https://www.baetebangladesh.org/acc-man-06-f.html

**Data protection**
- DataGuidance Bangladesh jurisdiction (PDPA 2026 enacted 10 Apr 2026) — https://www.dataguidance.com/jurisdictions/bangladesh
- PDPO 2025 full English text (Ordinance No. 61 of 2025) — https://dpo-india.com/Resources/Privacy_Regulations_in_Asia_Pacific_Countries/Bangladesh-Personal-Data-Protection-Ordinance,2025(Ordinance.No.61-2025).pdf
- PDPO 2025 / PDPA framework analysis — https://www.recordinglaw.com/world-laws/world-data-privacy-laws/bangladesh-data-privacy-laws/
- Cross-border transfer and localization (§§29–30, as amended) — https://juralacuity.com/personal-data-protection-ordinance/
- Localization eased, jail terms dropped (Feb 2026) — https://www.thedailystar.net/news/bangladesh/news/govt-eases-data-localisation-rules-drops-jail-terms-tech-firms-4076391
- Gazette of PDPO and NDGO — https://www.bssnews.net/news-flash/330104
- Securiti PDPA 2026 overview — https://securiti.ai/bangladesh-personal-data-protection-act-overview/

**Cybersecurity**
- Cyber Security Ordinance 2025 (repealed by Act 81 of 2026) — http://bdlaws.minlaw.gov.bd/act-1538.html?lang=en
- CERT / SOC / quarterly reporting obligations — http://bdlaws.minlaw.gov.bd/act-1538/section-54707.html
- CII designation gazette under Cyber Security Act 2026 §15 (20 Apr 2026) — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-bdpost/2026/4/c459f199-67ba-4a87-9bb0-19a35afa6e86.pdf
- Business implications of the Ordinance — https://www.mondaq.com/new-technology/1659100/cyber-security-ordinance-2025-implications-for-businesses-in-bangladesh
- Bangladesh Bank Guideline on ICT Security v4.0 (Apr 2023) — https://charteredjournal.com/wp-content/uploads/2023/06/Guideline-on-ICT-Security-Version-4.0.pdf

**Cloud, hosting, source code**
- National Cloud Policy (ICT Division, 2026) — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-ictd/2026/0/ba27f87e-73ba-4b3b-a28d-1c1475e0bf8d.pdf
- Draft National Source Code Policy 2025 — https://www.bssnews.net/news/338627
- National Source Code Policy coverage — https://www.tbsnews.net/tech/govt-unveils-draft-national-source-code-policy-2025-seeks-stakeholder-feedback-1301956

**Accessibility**
- Rights and Protection of Persons with Disabilities Act 2013 — https://legislativediv.portal.gov.bd/sites/default/files/files/legislativediv.portal.gov.bd/page/64379df1_f98c_47ff_b9e6_cbcabadd8ece/26.The%20Rights%20and%20Protection%20of%20Persons%20with%20Disabilities%20Act%2C%202013.pdf
- Digital Service and Web Designing Guideline for Inclusive Accessibility 2022 (WCAG 2.1) — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-titasgas/2024/12/6960d1d5d16b44e99d018de51234e4af.pdf
- National Web Accessibility Guideline — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-msw/2024/12/8676a04bc5c649ac975e03c4d103a715.pdf
- WCAG 2.1 audit of Bangladeshi e-government — https://userhub.com.bd/download/report/WCAG-2.1-Audit-Bangladeshi-E-Government-Accessibility-Maturity-Model.pdf

**Payments**
- Bangladesh MFS Regulations 2022 (BB circular PSD-04) — https://www.bb.org.bd/mediaroom/circulars/psd/feb152022psd04e.pdf
- Draft PSO Regulation 2025 details — https://publisher.tbsnews.net/economy/banking/bb-issues-draft-regulation-payment-system-operators-sets-tk30-lakh-fine-merchant
- Draft PSO rules, categories, retention, breach reporting — https://www.thedailystar.net/business/news/draft-rules-published-digital-payment-operators-4029906
- Uttara University payment guidelines (live fee/rail configuration) — https://www.uttara.ac.bd/payment-guidelines/
- Education payment gateway (EPS) — https://www.eps.com.bd/public/education-payment-solutions

**Tax and statutory reporting**
- UGC PUFR format and §45 obligations — https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-ugc/2024/12/28c830b9f281479d8a110ea1c2b963bf.pdf
- VAT exemption, service codes S070.10/S070.20 — https://legalseba.com/bd-resources/vat-rates-on-services-in-bangladesh/
- Supreme Court tax verdict — https://www.universityworldnews.com/post.php?story=20240402181542501
- Corporate tax cut to 10% (eff. 1 Jul 2026) — https://www.tbsnews.net/economy/corporate-tax-private-universities-medical-and-engineering-colleges-be-cut-10-1459451
- Draft Private University Act amendment (fee approval, published student lists) — https://www.universityworldnews.com/post.php?story=20230906125104438
- §45 compliance failures and §49 penalties — https://en.bd-pratidin.com/index.php/special/2026/02/25/57701
- UGC supervisory powers / program approval — https://en.banglapedia.org/index.php?title=Private_University

**Digital signatures**
- Legal standing of digital signatures (ICT Act §§5–7, 36; CCA; no foreign CA) — https://legalseba.com/bd-articles/legal-standing-of-digital-signature-in-bangladesh/
- Evidence Act 1872 §85C (inserted 2022) — http://bdlaws.minlaw.gov.bd/act-24/section-51396.html
- Rules on electronic signatures — https://www.vdb-loi.com/bd_publications/rules-on-electronic-signatures-in-bangladesh/

**University practices**
- BRAC University Guidelines for Course Teaching (grade scale, 5% attendance) — https://www.bracu.ac.bd/sites/default/files/resources/policies/GUIDELINES_FOR_COURSE_TEACHING_IN_BRACU.pdf
- BRAC retake/repeat/probation clarification — https://www.bracu.ac.bd/clarification-retake-and-repeat-examination-and-probation
- BRAC examinations policy — https://www.bracu.ac.bd/academics/policies-and-procedures/examinations
- BRAC course/semester drop policy — https://www.bracu.ac.bd/academics/policies-and-procedures/coursesemester-drop-policy
- BRAC Academic Handbook — https://bracjpgsph.org/assets/front/pdf/education/mph/BU%20Academic%20Handbook.pdf
- NSU Academic Information and Policies (updated 19 Jul 2026) — https://www.northsouth.edu/newassets/images/Registrs%20Office/updated-19-07-2026-academic-information-and-policies.pdf
- NSU student records and transcripts — https://northsouth.edu/academic/student-records.html
- AIUB academic regulations — http://www.aiub.edu/academic-regulations
- AIUB grading system — http://aiub.edu/academic-regulations/grading-system
- AIUB student handbook (updated 21 Apr 2026) — http://www.aiub.edu/Files/Uploads/updated_(21-4-26)student-handbook.pdf
- HSTU online examination policy (practical online exam workflow) — https://hstu.ac.bd/uploads/online_exam/online_exam_policy_eng_version.pdf

**Connectivity**
- AMTOB / BTRC industry statistics (May 2026) — https://www.amtob.org.bd/home/industrystatics
- Ookla Bangladesh 4G QoS analysis (Jan 2026) — https://www.ookla.com/articles/bangladesh-4g-qos-q42025
- BBS digital divide data — https://www.bssnews.net/special-stories/390214
- Rural connectivity gap — https://dailynewnation.com/news/828740

---

## Recommended next steps

1. **Commission a Bangla-source legal review of the PDPA 2026** covering U1 (restricted-data classification of biometric/health data) and U2 (section mapping). This is the only open question that can force a hosting re-architecture.
2. **Decide the hosting topology conditionally** — design for an in-Bangladesh data domain for biometric/health/counselling records regardless of the answer, so the residency question becomes cheap to satisfy.
3. **Build the outcomes framework as the core differentiator**, not as a reporting add-on. BAC and BAETE evidence generation is what a configured Moodle cannot do.
4. **Treat the grade/attendance/progression table in §3 as the configuration test suite** — if the product can express all three universities' rules without code changes, the configuration model is adequate.