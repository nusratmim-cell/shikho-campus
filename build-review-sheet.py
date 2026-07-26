#!/usr/bin/env python3
"""One consolidated Review sheet — deduped from Product, UI/UX, Frontend (+ demo visit)."""
import json
import re
import subprocess
import urllib.request
from collections import Counter
from urllib.parse import quote

TOKEN = subprocess.check_output(
    ["gcloud", "auth", "application-default", "print-access-token"], text=True
).strip()
SHEET_ID = "1ZU5acoOddFfejmT6Qynb1PgtLnTwK-FmHMzBOTQ9xGI"

S = "Student — Learn"
F = "Faculty — Teach"
A = "Administrator — Govern"
C = "Coordinator — Operate"
P = "Shared"

MODULE_ORDER = {P: 0, S: 1, F: 2, A: 3, C: 4}
TYPE_ORDER = {"Blocker": 0, "Query": 1, "Feedback": 2}

HEADER = [
    "Module",
    "Section",
    "Point",
    "Type",
    "Ask CEO",
    "Raised by",
    "Connected to",
    "Need from CEO",
]

rows = []


def clean_raised(raised):
    """Keep team/tab names only — strip individual member names."""
    if not raised:
        return raised
    raised = re.sub(r"\s*\([^)]*\)", "", raised)
    parts = []
    for part in raised.split(";"):
        part = part.strip()
        if part and part not in parts:
            parts.append(part)
    return "; ".join(parts)


def clean_point(text):
    """Remove individual name callouts from finding text."""
    if not text:
        return text
    subs = [
        ("Zarif asked", "Frontend review asks"),
        ("Jahid noted", "Data-model review notes"),
        ("Jahid listed", "Data-model review lists"),
        ("Jahid said", "Data-model review notes"),
        ("Rasel asked", "Frontend review asks"),
        ("Rasel and Jahid asked", "Frontend review asks"),
        ("Jahid and Zarif both raised this", "Product and Frontend both raised this"),
        ("Rasel:", "Frontend review:"),
        ("Zarif:", "Frontend review:"),
        ("Jahid:", "Data-model review:"),
    ]
    for old, new in subs:
        text = text.replace(old, new)
    return text


def R(module, section, point, typ, ask_ceo, raised, connected, ceo=""):
    rows.append(
        [
            module,
            section,
            clean_point(point),
            typ,
            ask_ceo,
            clean_raised(raised),
            connected,
            ceo,
        ]
    )


# ── SHARED ──────────────────────────────────────────────────
R(
    P,
    "Product scope",
    "The demo looks like a full university system — registration, attendance, degree rules, semester calendar — but behind the screens much of the data is thin, hardcoded, or seed-only. The team reviewed without a written brief and cannot guess how big version 1 should be. Building everything would take months; building only the AI learning + department control story could ship faster but leaves big gaps visible.",
    "Query",
    "Yes",
    "Product; Frontend (Jahid)",
    "Student registration; attendance; degree audit; semester calendar; Coordinator records; Admin certify",
    "What is Campus in your head?\n\n• Option A — Full university system (registration, attendance, degree audit, exam timetable, batches, real data everywhere)\n• Option B — Focused demo: AI learning for students + department control for CSE (thinner data, faster to show)\n\nPlease also say how deep v1 should go: real semester calendar, batches, and degree rules now — or keep thin demo data for this phase?\n\nUntil you answer, the team will keep building in different directions.",
)
R(
    P,
    "AI honesty",
    "AI Tutor (student), Copilot (faculty), and Analyst (chair) currently give scripted answers — they are not yet connected to a real model with course content. But the UI still says answers are grounded in lectures, shows weekly AI usage caps, and the landing page promises AI-tutored learning and an AI copilot. Frontend review flagged that usage projections on the Admin page may also be static demo numbers.",
    "Blocker",
    "Yes",
    "Product; Frontend (Rasel)",
    "Student AI Tutor; Faculty Copilot; Admin Analyst; landing page; Usage page",
    "What can we honestly show on screen while real AI is being built?\n\nExamples the team needs you to pick:\n• Remove or soften claims like grounded in your lectures until retrieval works\n• Add a clear Preview or Beta label on AI features\n• Keep current marketing language and accept the risk\n• Set real usage caps and show them accurately\n\nWrong claims will break trust fast — especially with a CS audience that will test the Tutor.",
)
R(
    P,
    "Sign-in & roles",
    "Today anyone opens the site, picks Student / Faculty / Administrator / Coordinator, then picks a demo account (e.g. Anika, Dr. Kamrul). There is no real login. Data-model review notes in production one person may hold two roles — for example a teacher who is also a coordinator. Permissions, navigation, and landing flow all depend on how identity works.",
    "Query",
    "Yes",
    "Product; Frontend (Jahid)",
    "All four landing-page roles; permissions; navigation",
    "Please decide two things:\n\n1) For the next phase, keep the demo role-picker, or start building real sign-in (e.g. email / SSO)?\n\n2) If one person has two roles (teacher + coordinator), should they:\n   • switch role inside one account,\n   • pick role at login each time, or\n   • use separate logins?\n\nUntil this is clear, we cannot design permissions or the post-login experience.",
)
R(
    P,
    "Real student data",
    "Many flows assume real rosters, real grades, and real identity: registration, eligibility, certify, profiles, at-risk flags. Right now most of this is demo seed data. The team does not know whether real data must work in this phase, or whether a polished demo with fake data is enough for now.",
    "Query",
    "Yes",
    "Product; Frontend (Jahid)",
    "Registration; grades; eligibility; profiles; Coordinator import",
    "When do real login, student lists, and grades need to work?\n\n• This phase — demo is not enough; we need real or synced data soon\n• Next phase — polished demo is fine for now; real data can wait\n\nIf real data is needed, please say which comes first: rosters, grades, or attendance.\n\nThis sets engineering priority and what we can honestly demo.",
)
R(
    P,
    "Shikho content",
    "Shikho already has content libraries and brand trust in Bangladesh. Campus could reuse Shikho material mapped to BRAC CSE courses, or the team could build BRAC-only content from scratch. This changes how quickly Student Learn and Faculty Teach feel real, and how much content work the team must do.",
    "Query",
    "Yes",
    "Product; Frontend (Jahid)",
    "Student courses & Tutor; Faculty course materials; time to demo",
    "Should we reuse Shikho's content library (mapped to BRAC CSE), build BRAC-only content, or a mix?\n\n• Reuse Shikho — faster, but needs mapping and rights clarity\n• BRAC-only — more control, more content work\n• Mix — e.g. Shikho for some courses, BRAC for labs\n\nYour call sets content strategy and how full courses look in the demo.",
)
R(
    P,
    "Migration story",
    "When Campus launches at a university, people will ask what happens to whatever they use today — old LMS, spreadsheets, past grades, existing rosters. The PRD and demo do not answer this. Product flagged that read-only archive vs live editable history are very different paths with different audit and transcript risk.",
    "Query",
    "Yes",
    "Product",
    "Sales story; transcript integrity; data model",
    "When Campus goes live, what happens to old tools and past grades?\n\n• Old grades become read-only archive (view past transcript, no edits)\n• Old grades stay live and editable in Campus\n• No migration in v1 — Campus starts fresh; history stays in old system\n• Something else — please describe\n\nThe team should not invent this. It shapes the product story and data design.",
)
R(
    P,
    "SSO & student data sync",
    "Product calls real identity and a live roster + grade-posting pipeline the gating item before any pilot — ahead of more UI work. Frontend data-model review lists SSO with role mapping. Today there is no BRACU login, no SIS sync, and no reconciliation when a name/ID is wrong or a late add/drop has not synced. That breaks the find-yourself moment, registration, eligibility, and certify.",
    "Blocker",
    "Yes",
    "Product; Frontend",
    "Sign-in & roles; Real student data; Coordinator import; Admin certify",
    "When must real university login and live student/grade data work?\n\n• Before any external demo beyond internal review\n• Before a pilot with real students\n• Later — demo with seed data is enough for now\n\nIf real data is needed, what connects first?\n• SSO / login only\n• Rosters from SIS\n• Grades posted back to SIS\n• All of the above\n\nAlso: how do we handle mismatches (typo in ID, late add/drop not synced yet)?",
)
R(
    P,
    "AI retrieval pipeline",
    "Beyond scripted answers, a real product needs a model plus retrieval over uploaded course material, with the usage-cap governance already promised. Product warns that thin courses will make Tutor look bad even with a good model — worth a minimum-content bar before Tutor is turned on per course. Flagged wrong Tutor answers should feed the same review queue as teacher-approved content.",
    "Blocker",
    "No",
    "Product",
    "AI honesty; Student AI Tutor; Faculty Copilot; Faculty adoption",
    "",
)
R(
    P,
    "Search",
    "The search bar in the top shell opens a results overlay when clicked — demo visit confirmed this works. Product tab said Cmd+K keyboard shortcut may not work. Worth a quick engineering check; not a CEO decision.",
    "Feedback",
    "No",
    "Product",
    "Shell navigation",
    "",
)
R(
    P,
    "Theme & modals",
    "A working light/dark theme control exists but is buried in Settings, not in the header. Several modal stacking (z-index) bugs were fixed one at a time — a full sweep may still be needed. The demo uses a fixed clock so the world always shows the same moment; that must not break.",
    "Feedback",
    "No",
    "Product",
    "Shell UX; all roles",
    "",
)
R(
    P,
    "Accessibility",
    "No plan yet for keyboard navigation, screen-reader labels, or contrast beyond visual polish. Student Momentum rings and Admin charts use color to convey meaning — that fails for color-blind users and screen readers.",
    "Feedback",
    "No",
    "Product; UI/UX",
    "Student Momentum; Admin charts",
    "",
)
R(
    P,
    "Analytics",
    "There is no product analytics today — no way to show at renewal time that students and faculty actually used Campus. Product noted this should be scoped carefully so teacher private activity is not exposed on aggregate dashboards.",
    "Feedback",
    "No",
    "Product",
    "Usage page; renewal story",
    "",
)
R(
    P,
    "Seed vs real UI",
    "Several numbers and labels on profiles may be demo seed data, not calculated from real events: student attendance 92%, faculty office hours, admin usage projection (93% by week's end). Frontend review asks which stats are real vs placeholder so the team does not build on wrong assumptions.",
    "Feedback",
    "No",
    "Frontend",
    "All role profiles; Admin Usage page",
    "",
)
R(
    P,
    "Multi-department",
    "CSE students also take courses from other departments (math, physics, English). Data-model review notes no institution → school → department hierarchy and no cross-department course ownership. Likely a later-phase item unless you want it in v1.",
    "Feedback",
    "No",
    "Frontend",
    "Course catalogue; registration",
    "",
)

# ── STUDENT ─────────────────────────────────────────────────
R(
    S,
    "Home",
    "Demo visit confirmed the student home is crowded: identity line, Momentum card (78, Strong, rings), live-class banner, jump-back-in, four course cards, AI Tutor promo, today list, and right-rail items — eight or more sections competing at once. Product and UI/UX both say the home should answer one question: What should I do right now? Live class and deadlines should beat gamification. Product also needs explicit tie-break rules: what shows when a class is live AND an assignment is due within the hour? Design a calm state for a brand-new student with zero courses during add/drop week. Remove AI upgrade promos and any leftover AI edition marketing for students who already have access.",
    "Feedback",
    "Yes",
    "Product; UI/UX; Frontend (Zarif)",
    "Momentum; Live class; navigation; mobile layout",
    "Do you want Student home redesigned around one clear next action?\n\nSuggested order the team proposes:\n1) Join live class (if on now)\n2) Something due soon (quiz / assignment)\n3) Resume a lecture\n4) Calm state when nothing is urgent\n\nAlso: school work above gamification (Momentum / rings lower priority)?\n\nPlease confirm this matches your vision, or say what order you want.",
)
R(
    S,
    "Registration",
    "There is no add/drop or course registration anywhere. Students never choose their courses — the Coordinator bulk-uploads class lists. Data-model review lists this as a core missing flow: browse enabled offerings, pick sections, credit-limit check, prereq check, add/drop until deadline. Product adds waitlists for full sections and cross-enrolled students (PRD flags four cross-enrolled this term) — naive forms break on these cases. If registration is built, the Coordinator role changes completely.",
    "Blocker",
    "Yes",
    "Product; Frontend (Jahid)",
    "Coordinator rosters; prereqs; degree progress; Admin course enablement",
    "Who puts students into courses?\n\n• Option A — Students register themselves inside Campus (browse sections, add/drop, prereq checks)\n• Option B — Coordinator keeps uploading rosters each term (students never self-register)\n• Option C — Mix (e.g. coordinator sets capacity; students pick within rules)\n\nIf students register, also confirm:\n• Hard/soft prerequisite checks?\n• Waitlists for full sections?\n• Cross-enrolled students (courses across sections/programmes)?\n• Advisor or chair override for blocked registrations?\n\nThis is the biggest missing Student feature and directly changes Coordinator Operate.",
)
R(
    S,
    "Attendance",
    "Student profile shows Attendance 92% but nothing in the product actually records class sessions. Data-model review says attendance is the missing input for the whole eligibility system. Administrator Govern uses a 70% rule to bar students from finals. Faculty at-risk flags also assume attendance data. Frontend review asks how attendance is taken and whether profile % matches the Admin eligibility number.",
    "Blocker",
    "Yes",
    "Product; Frontend",
    "Admin 70% eligibility; certify; Faculty at-risk; Student profile",
    "How should attendance work in your vision?\n\nPlease answer:\n1) How is it captured? (live class join, QR/roll call, manual entry, integration, etc.)\n2) Is the % on the student profile the exact same number that drives the 70% eligibility rule?\n3) Who can correct a wrong attendance mark?\n\nNothing can be built honestly for eligibility or at-risk until you decide this.",
)
R(
    S,
    "Live class",
    "The live-class screen is fully designed — join button, classmate count, chat, raise hand, low-bandwidth setting — but there is no real video stream behind it (no Agora, LiveKit, etc.). Product says plan for mid-class disconnect (reconnect path, recording continues), and video-backend outage (graceful degrade vs class fails silently). Faculty Record/Live has the same gap. Landing page promises live learning.",
    "Blocker",
    "Yes",
    "Product",
    "Faculty Record/Live; Integrations video; landing page",
    "Live class UI exists but video does not work yet. How should we present it?\n\n• Preview / Coming soon — show UI but do not claim live classes work\n• Hide live class until video backend is ready\n• Keep current demo as-is and accept the gap for now\n\nYour call sets what we can claim on the landing page and in sales conversations.",
)
R(
    S,
    "Momentum",
    "Momentum shows a score (e.g. 78), label (Strong), weekly change (+6), rings (Absorb / Retrieve / AI practice), and streak. Product and UI/UX say meaning is unclear — UI/UX suggests clearer labels like On track and Today's study goals. Rings should open the real next action, not a dead page; handle the case when nothing is left to do today. Absorb can be gamed by leaving a video open. Product asks whether light attention/recall checks are needed without punishing legitimate 2x review or low-bandwidth viewers.",
    "Query",
    "Yes",
    "Product; UI/UX; Frontend (Zarif)",
    "Student home; gamification vs school work",
    "What is Momentum meant to do for a student?\n\nPlease decide:\n• What should the score represent? (effort, consistency, study time, something else?)\n• When does it reset — daily, weekly, per term?\n• How do we stop passive video-watching from counting as effort?\n• Should rings always link to a real action (open lecture, quiz, tutor)?\n\nThis is a signature feature but the rules are undefined.",
)
R(
    S,
    "Notifications",
    "Today students only get an in-app notification bell (and email digest mentioned in Product). Nothing pushes to phone directly. Product noted WhatsApp or SMS would reach students faster for deadlines and live-class alerts — with frequency limits and fallback to email for students without a phone on file. At scale, messaging volume needs governance similar to AI usage caps.",
    "Query",
    "Yes",
    "Product",
    "Live class alerts; assignment deadlines",
    "How should Campus alert students?\n\n• In-app only (bell + email)\n• WhatsApp for urgent items (deadlines, live class starting)\n• SMS\n• Mix — please say which events go where\n\nThis affects integrations, cost, and whether students actually see alerts in time.",
)
R(
    S,
    "Past papers",
    "Past exam papers are culturally one of the most wanted features for BRAC exam prep — Product flagged it as missing entirely. If added, team needs policy: who uploads, are solutions included, moderation rules. Not built today.",
    "Query",
    "Yes",
    "Product",
    "Exam prep; content strategy",
    "Should Campus include a past-paper bank for students?\n\n• Yes in v1 — with moderation (please say: solutions allowed or questions only?)\n• Yes but later phase\n• No — out of scope\n\nIf yes, who owns uploads — faculty, admin, or central content team?",
)
R(
    S,
    "Group projects",
    "There is no team model: no group formation, shared submission, or peer review. CSE is lab-heavy and group work is routine. Product listed this as a gap. Connects to Faculty grading and plagiarism rules if built.",
    "Query",
    "Yes",
    "Product",
    "Faculty grading; plagiarism; CSE labs",
    "Should team / group projects be in version 1?\n\n• Yes — needed for CSE labs (teams, shared submit, maybe peer review)\n• Later — individual submit is enough for now\n\nIf yes, please say how simple v1 should be (e.g. teacher assigns groups vs students form teams).",
)
R(
    S,
    "Grades",
    "Product says grades should open with plain emotional standing (you are doing fine / CSE110 needs attention) with breakdown on tap. Need calm empty states at term start and clear withheld-grade wording after certify. Missing what-do-I-need-on-the-final calculator — Product calls it the most-requested grades feature; must handle different weighting schemes, pass/fail courses, and students already barred from finals (where a projection would mislead). Frontend review asks how current grade is shown mid-term while the course is still running.",
    "Feedback",
    "No",
    "Product; Frontend (Zarif)",
    "Assessments tab; course progress",
    "",
)
R(
    S,
    "AI Tutor",
    "Tutor should remember last course and topic instead of showing a picker every time — decide if memory is per-device or per-account (phone ↔ laptop matters). No way for students to flag a wrong answer; Product wants a visible flag → review → fix loop. Weekly AI limit display unclear as it runs low. Tied to Shared AI honesty and AI retrieval pipeline.",
    "Feedback",
    "No",
    "Product; Frontend (Zarif)",
    "Shared AI honesty",
    "",
)
R(
    S,
    "Discussions",
    "Course discussions exist as a generic forum. Product says this loses to WhatsApp and Facebook groups students already use. Suggestion: pick one clear job — e.g. official TA Q&A archive — or skip the feature.",
    "Query",
    "No",
    "Product",
    "Course tabs",
    "",
)
R(
    S,
    "Degree progress",
    "Progress-to-graduation is shown but there is no real degree structure: required credits, core vs elective buckets, capstone rules, minimum CGPA. Data-model review lists missing transcript states: retake/repeat with grade-replacement policy, withdrawal (W), incomplete (I + deadline), audit, leave-of-absence — each affects GPA and eligibility workflows.",
    "Blocker",
    "No",
    "Frontend; Product",
    "Registration; Admin certify; Product scope",
    "",
)
R(
    S,
    "Course content browse",
    "UI/UX: course Content tab has too many filter layers (by chapter, by type, chips, topic tags) — unclear what is a filter vs a label. Empty No material here yet blocks take too much space. Simplify to clear types (All, Videos, Slides, Readings, Labs, Links) and collapse empty sections.",
    "Feedback",
    "No",
    "UI/UX",
    "Faculty upload; Student Learn",
    "",
)
R(
    S,
    "Course pages",
    "Frontend review: Explore all 26 courses link — unclear what non-enrolled students see. Live course page has six tabs (Overview, Content, Assessments, Progress, Discussions, AI Tutor) but PRD naming does not fully match. Back from inside an Assessment lands on Overview instead of Assessments list.",
    "Feedback",
    "No",
    "Frontend (Rasel, Zarif)",
    "Navigation; PRD consistency",
    "",
)
R(
    S,
    "Navigation",
    "Product and UI/UX want shorter sidebar: Home, Courses, Grades, Tutor, Profile — with Schedule and Practice folded into Courses. Breadcrumbs and clearer back behavior needed on nested pages. UI/UX marked navigation as important.",
    "Feedback",
    "No",
    "Product; UI/UX; Frontend (Zarif)",
    "Shell navigation",
    "",
)
R(
    S,
    "Calendar sync",
    "Product suggested letting students push schedule and deadlines to Google Calendar or Outlook in one click, and update when a class moves. Small integration, high student value. Not built.",
    "Feedback",
    "No",
    "Product",
    "Notifications; live/reschedule",
    "",
)
R(
    S,
    "Recorded lectures",
    "Recorded lecture player is core to the Learn pillar (live + recorded + AI-tutored). Separate from the live-video gap — team should QA player behavior, resume, and progress tracking.",
    "Feedback",
    "No",
    "Product",
    "Live class; Faculty upload; Momentum Absorb ring",
    "",
)

# ── FACULTY ─────────────────────────────────────────────────
R(
    F,
    "Faculty adoption",
    "Product flagged a go-to-market risk: if teachers keep slides and assignments on Google Drive and WhatsApp, Student AI Tutor has nothing to ground on and Momentum stays empty. Campus only works as advertised if faculty actually teach inside it. No adoption plan is written.",
    "Query",
    "Yes",
    "Product",
    "Student Tutor; Student Momentum; content pipeline",
    "If teachers do not upload and teach on Campus, AI Tutor and Momentum will stay empty.\n\nWhat is your plan for faculty adoption?\n\n• Require all materials on Campus (policy / training)\n• Optional — accept that some courses stay thin\n• Pilot with willing teachers first — which courses?\n• Incentives or support (training, TA help, content migration)\n\nPlease describe what you expect in the first real term.",
)
R(
    F,
    "Course & chapter creation",
    "Teachers can add files into existing chapters but cannot create new courses or new chapters. Data-model review notes there is also no admin UI to build the course catalogue. Demo runs on seed data. Admin has a static section list, not a per-semester enablement workflow.",
    "Query",
    "Yes",
    "Frontend (Jahid)",
    "Admin course enablement; demo seed data; Coordinator offerings",
    "Who creates courses and chapters?\n\n• Teachers create their own courses and chapters\n• Coordinator or admin builds structure; teachers only add content\n• Central team / Shikho content team builds catalogue; teachers customize\n• Keep demo seed data for now — no creation UI in this phase\n\nWithout your answer, Faculty Teach cannot scale past the demo.",
)
R(
    F,
    "Grading rules",
    "Product wants a focus mode: one submission at a time, AI draft visible, approve and move to next, with progress and completion state. Frontend review asks: bulk-approve several grades? change grade after approve? Product warned CSV export must not leak unapproved AI draft scores. These rules connect to Admin certify and post-certify fixes.",
    "Query",
    "Yes",
    "Product; Frontend (Zarif)",
    "Admin certify; post-certify correction; gradebook export",
    "Please set grading rules:\n\n1) After a teacher approves a grade, can they change it later? (before certify / after certify?)\n2) Can teachers bulk-approve many submissions at once?\n3) What happens when chair returns a grade to teacher — required reason?\n\nThese rules must match the certify and appeal story.",
)
R(
    F,
    "Gradebook export",
    "Export button exists but Product has not confirmed the CSV contents for withheld finals or unapproved AI draft scores. Accidentally exporting a draft AI-suggested mark would be a real integrity problem.",
    "Blocker",
    "No",
    "Product",
    "Grading rules; Admin certify; transcript integrity",
    "",
)
R(
    F,
    "Grading focus mode",
    "Product proposes full-screen one-at-a-time grading with AI draft visible, approve-and-advance, and a real completion state for the queue. Design for teacher strongly disagreeing with AI draft, and for late/resubmitted work arriving mid-session.",
    "Feedback",
    "No",
    "Product",
    "Grading rules; Faculty home",
    "",
)
R(
    F,
    "Home",
    "UI/UX and Product say faculty home should lead with live class, grading backlog, and at-risk students. Record, upload, and assign should be secondary actions — not equal-weight cards. Sidebar should shorten to Home, Courses, Grading, Copilot, Profile.",
    "Feedback",
    "No",
    "UI/UX; Product",
    "Navigation sidebar",
    "",
)
R(
    F,
    "Copilot",
    "Product wants generate quiz on the chapter page itself, not a separate Copilot trip. Zarif asked: save draft questions and publish later? If teacher has no materials yet, should Copilot push upload-first? Tied to Shared AI honesty.",
    "Feedback",
    "No",
    "Product; Frontend (Zarif)",
    "Shared AI honesty; course content page",
    "",
)
R(
    F,
    "At-risk & advising",
    "At-risk flags exist but need actions attached: pre-drafted check-in, link to student profile, flag to advisor. No advisor model exists — no advisor assignment, advisees view, or registration approval step. Product also says cap repeat outreach so the same student is not flagged every week. Faculty Flag action has nowhere real to go.",
    "Blocker",
    "No",
    "Product; Frontend (Jahid)",
    "Admin at-risk; Student registration",
    "",
)
R(
    F,
    "Demo teacher identity",
    "Dr. Kamrul Hasan is the emotional center of the faculty demo — must be findable searching Kamrul or Hasan. Product says in a room of real faculty everyone will search their own name; empty results for all but Kamrul undercuts the pitch. Switching faculty in the picker must only change displayed identity, never re-filter or wipe underlying class data.",
    "Blocker",
    "No",
    "Product",
    "Faculty demo story",
    "",
)
R(
    F,
    "Record & live",
    "Recording studio UI exists but no topic-tagging on recordings (product expects it, including retag behavior for already-published recordings). Live and Record have no real video backend — same gap as Student live class.",
    "Feedback",
    "No",
    "Product",
    "Student Live class",
    "",
)
R(
    F,
    "Momentum privacy",
    "Product rule: a teacher's private Momentum must never be visible to the Administrator — including if the Chair asks the Analyst about it. Needs verification everywhere Analyst can query.",
    "Feedback",
    "No",
    "Product",
    "Admin Analyst",
    "",
)
R(
    F,
    "Content controls",
    "Should teachers reorder or hide items inside a course chapter? Not specified in PRD.",
    "Query",
    "No",
    "Frontend (Zarif)",
    "Course chapter UI",
    "",
)
R(
    F,
    "Plagiarism",
    "Product expects plagiarism detection on submissions for an academic platform. If group projects are added, need rules for group work and starter code. Integration not built.",
    "Feedback",
    "No",
    "Product",
    "Group projects; grading",
    "",
)
R(
    F,
    "Profile",
    "Faculty profile shows office hours and past term mention — unclear if editable by teacher or fixed seed data only.",
    "Feedback",
    "No",
    "Frontend (Rasel)",
    "Seed vs real UI",
    "",
)

# ── ADMINISTRATOR ───────────────────────────────────────────
R(
    A,
    "Audit log",
    "Product repeatedly states every chair decision is logged for governance. But there is no screen anywhere that shows that log — certify actions, eligibility overrides, returns to teacher. Team found a claim without UI. Hurts Govern credibility.",
    "Blocker",
    "Yes",
    "Product",
    "Certify; eligibility overrides; governance story",
    "We say every decision is logged, but there is no log screen.\n\nShould we build a visible audit log for the Chair?\n\n• Yes — required for Govern to be credible (who did what, when, why)\n• Later — okay for demo phase\n• No — remove logged claims from copy\n\nIf yes, what actions must appear? (certify, override eligibility, return grade, staffing changes?)",
)
R(
    A,
    "Eligibility 70%",
    "Administrator can mark students not eligible for term exam based on attendance rules (70% mentioned). Frontend review asks whether the chair can override for one student or move a student from not eligible back to eligible. Product asks what happens if the 70% threshold is edited mid-term — recalculate everyone or only going forward?",
    "Query",
    "Yes",
    "Frontend (Zarif); Product",
    "Student attendance; lock eligibility; certify",
    "Please define Chair power on the 70% attendance rule:\n\n• Can the Chair override for a specific student (allow exam despite low attendance)?\n• Can the Chair change a student from not eligible back to eligible?\n• What if the rule changes mid-term — recalculate everyone or grandfather old rule?\n\nDefines how much real power Govern has vs demo UI.",
)
R(
    A,
    "After grades certified",
    "Product says the chair never directly edits a mark — correct. But there is no path to fix a wrong mark after certification, and no student grade appeal flow. Product and Frontend both raised this. Faculty grading rules must align with whatever process you choose.",
    "Query",
    "Yes",
    "Product; Frontend (Jahid, Zarif)",
    "Faculty grading; certify workflow; transcript integrity",
    "If a grade is wrong after the chair certifies, what happens?\n\nPlease describe the path, for example:\n• Teacher requests correction → Chair reviews → re-certify delta → transcript updates\n• Student submits appeal → Chair/admin decides\n• No changes after certify — transcript is final\n\nAlso: can students appeal a grade through Campus?\n\nReal universities need a clear answer; team cannot invent this.",
)
R(
    A,
    "Semester calendar",
    "Term is a hardcoded string with static rows. A real semester needs start/end dates, registration window, add/drop deadline, exam periods, grade and certification deadlines — as data everything else hangs off this. Admin per-semester course enablement (pick subset of 26 catalogue courses with section counts/capacity) is also missing.",
    "Blocker",
    "No",
    "Frontend; Product",
    "Student registration; Coordinator offerings; Product scope",
    "",
)
R(
    A,
    "Exam timetable & rooms",
    "Lock eligibility before finals references finals that have no schedule: no timetable, rooms, seat plans, invigilation, or clash-free slots per student. Data-model review also lists timetable and room management — teacher double-booking, room double-use, batch course collisions. Needed for a real Govern workflow.",
    "Blocker",
    "No",
    "Frontend; Product",
    "Eligibility lock; Coordinator records; Student schedule",
    "",
)
R(
    A,
    "Semester rollover",
    "Launching a new term should be a workflow: create session with calendar → enable courses → advance batch standing → open registration → staff sections → publish. Without this loop, multiple semesters and multiple year-levels of students cannot run operationally.",
    "Feedback",
    "No",
    "Frontend; Product",
    "Semester calendar; Coordinator import; Student registration",
    "",
)
R(
    A,
    "Policy & curriculum tabs",
    "Admin Program has a working This term tab; Curriculum and Policy tabs need review before live demo. Product asks: if 70% attendance threshold is edited mid-term, does eligibility recalculate for everyone or only going forward?",
    "Feedback",
    "No",
    "Product",
    "Eligibility 70%; audit log",
    "",
)
R(
    A,
    "Home",
    "Product and UI/UX: Admin home should lead with decisions needed now — certify, eligibility, staffing — with urgency labels. Department health summary below. When nothing needs a decision, Analyst query box should become the calm hero of the page, not a side widget.",
    "Feedback",
    "No",
    "Product; UI/UX",
    "Analyst; certify; staffing",
    "",
)
R(
    A,
    "Certify workflow",
    "Product: certify screen should sort problem sections first, batch-certify routine clean sections, label routine items clearly. Returning a grade to teacher should require a reason. Connects to audit log and post-certify correction.",
    "Feedback",
    "No",
    "Product",
    "Audit log; post-certify",
    "",
)
R(
    A,
    "Analyst",
    "Admin Analyst promises many question types but only six show as suggested chips; others must be typed. Multi-part ambiguous questions (e.g. at-risk list plus pass-rate trend) need defined behavior. When home is in calm Analyst mode, page should snap back to decision mode when a new urgent flag appears. Still scripted — tied to Shared AI honesty.",
    "Feedback",
    "No",
    "Product",
    "Shared AI honesty",
    "",
)
R(
    A,
    "Usage / AI budget",
    "Chair usage page shows weekly and monthly AI caps plus projected 93% spend by week's end — unclear if calculated live or static demo.",
    "Query",
    "No",
    "Frontend (Rasel); Product",
    "Shared AI honesty; seed vs real UI",
    "",
)
R(
    A,
    "Lock eligibility",
    "Locking eligibility before finals is a consequential action — Product said it needs hands-on QA before the demo relies on it. Depends on attendance decision.",
    "Feedback",
    "No",
    "Product",
    "Student attendance; 70% rule",
    "",
)
R(
    A,
    "Profile labels",
    "Open cockpit link label is unclear without clicking. Valid thru date format is ambiguous (Dec 2027 vs day/month).",
    "Feedback",
    "No",
    "Frontend (Rasel)",
    "Navigation clarity",
    "",
)

# ── COORDINATOR ─────────────────────────────────────────────
R(
    C,
    "Flag to Chair",
    "UI/UX: Coordinator home sees an unstaffed section but after opening Offerings there is no clear Flag to Chair action or status (e.g. Flagged — awaiting teacher assignment). Product cross-role story requires Coordinator → Chair → staffing update. Four roles on one platform is the pitch — this handoff is incomplete.",
    "Blocker",
    "Yes",
    "UI/UX; Product",
    "Admin staffing; Shared cross-role handoffs",
    "Should Coordinator be able to flag an unstaffed section to the Chair?\n\nIf yes, please confirm:\n• Button on the offering row (e.g. Flag to Chair)\n• Visible status after flagging (e.g. Flagged — awaiting assignment)\n• Chair sees it on Admin home and can assign teacher\n\nWithout this loop, Operate and Govern feel disconnected in the demo.",
)
R(
    C,
    "Rosters vs registration",
    "Today the Coordinator bulk-imports student rosters and maintains directory records. If Student add/drop registration is built, the roster becomes the output of registration — Coordinator role shifts to validation, exceptions, and data cleanup instead of being the only way students get into classes.",
    "Query",
    "Yes",
    "Product; Frontend (Jahid)",
    "Student registration; import workflow",
    "If students register themselves, what does the Coordinator still do?\n\nExamples:\n• Import initial data only; students self-register after\n• Fix exceptions and data errors only\n• Still own all roster changes (no student self-service)\n• Approve registrations before they are final\n\nTied directly to your Student registration decision.",
)
R(
    C,
    "Home",
    "Product and UI/UX: Coordinator home should lead with is the data clean checklist — not chair handoffs first. Group items as Needs action / Waiting on others / Ready. Day-one zeros (0 records loaded) should not look like a broken product.",
    "Feedback",
    "No",
    "Product; UI/UX",
    "Import; directory",
    "",
)
R(
    C,
    "Import & directory",
    "Product: roster import should preview before commit (how many add, skip, error). Do not silently skip same student ID in a new section — surface as a decision. Bulk actions need safety when selection mixes faculty and student rows or spans records being edited elsewhere.",
    "Feedback",
    "No",
    "Product",
    "Student records",
    "",
)
R(
    C,
    "Student records",
    "Student records lack batch, programme, semester standing, and credits earned — only name, ID, section, email today. Data-model review notes a real Summer term serves Year 1–4 batches concurrently, each taking different courses; enrolment must be per batch × offering, not a single-cohort snapshot.",
    "Feedback",
    "No",
    "Frontend (Jahid)",
    "Admin university operations; Student degree",
    "",
)
R(
    C,
    "Profile wording",
    "Section heading What crosses your desk is unclear — daily tasks, pending items, or general scope? Wording could be more direct.",
    "Feedback",
    "No",
    "Frontend (Rasel)",
    "Coordinator home",
    "",
)

rows.sort(key=lambda r: (MODULE_ORDER[r[0]], TYPE_ORDER[r[3]], r[1].lower()))

sheet_data = [HEADER] + rows
ceo_count = sum(1 for r in rows if r[4] == "Yes")
sheet_data.append(
    [
        "How to read this sheet",
        "",
        "CEO built a vibe-coded demo and a basic PRD. The team reviewed Product, UI/UX, and Frontend tabs (Backend was empty) without a full brief. One row = one topic. Type means: Query = we need an answer | Blocker = work is stuck until decided | Feedback = we found a gap — confirm if it matches your vision. Filter Ask CEO = Yes to see only the items that need your input.",
        "",
        "",
        "",
        "",
        f"{ceo_count} items need your input · {len(rows)} topics total",
    ]
)


def api(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    return json.loads(urllib.request.urlopen(req).read().decode())


def get_meta():
    return api("GET", "?fields=sheets.properties")


meta = get_meta()
review_id = None
for s in meta["sheets"]:
    if s["properties"]["title"] == "Review":
        review_id = s["properties"]["sheetId"]
        break

if review_id is None:
    r = api(
        "POST",
        ":batchUpdate",
        {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": "Review",
                            "index": 4,
                            "gridProperties": {
                                "frozenRowCount": 1,
                                "rowCount": 160,
                                "columnCount": 8,
                            },
                        }
                    }
                }
            ]
        },
    )
    review_id = r["replies"][0]["addSheet"]["properties"]["sheetId"]

api("POST", "/values:batchClear", {"ranges": ["Review!A:Z"]})
api("PUT", f"/values/{quote('Review!A1')}?valueInputOption=RAW", {"values": sheet_data})

module_colors = {
    S: {"red": 0.72, "green": 0.86, "blue": 0.98},
    F: {"red": 0.94, "green": 0.80, "blue": 0.88},
    A: {"red": 1.0, "green": 0.86, "blue": 0.74},
    C: {"red": 0.78, "green": 0.92, "blue": 0.82},
    P: {"red": 0.88, "green": 0.88, "blue": 0.91},
}
type_colors = {
    "Query": {"red": 1.0, "green": 0.93, "blue": 0.80},
    "Feedback": {"red": 0.85, "green": 0.92, "blue": 1.0},
    "Blocker": {"red": 1.0, "green": 0.86, "blue": 0.86},
}
ceo_yes = {"red": 0.85, "green": 0.95, "blue": 0.85}
ceo_no = {"red": 1.0, "green": 1.0, "blue": 1.0}

nrows = len(sheet_data)
reqs = [
    {
        "updateSheetProperties": {
            "properties": {
                "sheetId": review_id,
                "gridProperties": {
                    "frozenRowCount": 1,
                    "columnCount": 8,
                    "rowCount": max(90, nrows + 10),
                },
            },
            "fields": "gridProperties",
        }
    },
    {
        "repeatCell": {
            "range": {
                "sheetId": review_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": 8,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.10, "green": 0.12, "blue": 0.16},
                    "textFormat": {
                        "bold": True,
                        "foregroundColor": {"red": 1, "green": 1, "blue": 1},
                        "fontSize": 10,
                    },
                    "verticalAlignment": "MIDDLE",
                    "wrapStrategy": "WRAP",
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,verticalAlignment,wrapStrategy)",
        }
    },
    {
        "repeatCell": {
            "range": {
                "sheetId": review_id,
                "startRowIndex": 1,
                "endRowIndex": nrows - 1,
                "startColumnIndex": 0,
                "endColumnIndex": 8,
            },
            "cell": {
                "userEnteredFormat": {
                    "wrapStrategy": "WRAP",
                    "verticalAlignment": "TOP",
                    "textFormat": {"fontSize": 10},
                }
            },
            "fields": "userEnteredFormat(wrapStrategy,verticalAlignment,textFormat)",
        }
    },
    {
        "updateDimensionProperties": {
            "range": {
                "sheetId": review_id,
                "dimension": "ROWS",
                "startIndex": 1,
                "endIndex": nrows - 1,
            },
            "properties": {"pixelSize": 120},
            "fields": "pixelSize",
        }
    },
]
widths = [145, 155, 420, 90, 80, 170, 220, 480]
for i, w in enumerate(widths):
    reqs.append(
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": review_id,
                    "dimension": "COLUMNS",
                    "startIndex": i,
                    "endIndex": i + 1,
                },
                "properties": {"pixelSize": w},
                "fields": "pixelSize",
            }
        }
    )

for i, row in enumerate(rows, start=1):
    reqs.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": review_id,
                    "startRowIndex": i,
                    "endRowIndex": i + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": module_colors[row[0]],
                        "textFormat": {"bold": True, "fontSize": 9},
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat)",
            }
        }
    )
    reqs.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": review_id,
                    "startRowIndex": i,
                    "endRowIndex": i + 1,
                    "startColumnIndex": 3,
                    "endColumnIndex": 4,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": type_colors[row[3]],
                        "textFormat": {"bold": True},
                        "horizontalAlignment": "CENTER",
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
            }
        }
    )
    reqs.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": review_id,
                    "startRowIndex": i,
                    "endRowIndex": i + 1,
                    "startColumnIndex": 4,
                    "endColumnIndex": 5,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": ceo_yes if row[4] == "Yes" else ceo_no,
                        "textFormat": {"bold": row[4] == "Yes"},
                        "horizontalAlignment": "CENTER",
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
            }
        }
    )

reqs.append(
    {
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": review_id,
                    "startRowIndex": 0,
                    "endRowIndex": nrows - 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 8,
                }
            }
        }
    }
)

api("POST", ":batchUpdate", {"requests": reqs})

print(f"Review sheet: {len(rows)} topics ({ceo_count} Ask CEO = Yes)")
print("By module:", Counter(r[0] for r in rows))
print("By type:", Counter(r[3] for r in rows))
