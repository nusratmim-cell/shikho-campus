# Shikho Campus — Adoption-Driving Improvements Spec

> Implementation specification for 10 high-impact changes that shift the platform
> from "demo-impressive" to "daily-use indispensable."
>
> **Based on**: PRD (§1–30), Sales Deck (19 slides), Deep browser audit (Jul 15, 2026)
>
> **Audience**: Engineering, Design, QA
>
> **Principle**: Every screen answers ONE question instantly.

---

## Priority Map

| Sprint | Items | Goal |
|--------|-------|------|
| **Immediate** (days) | #7 Fix 3 broken things | Trust — nothing looks interactive and does nothing |
| **Sprint 1** (week 1–2) | #1, #3, #8, #9 | Simplify — every home answers its question in 2 seconds |
| **Sprint 2** (week 3–4) | #2, #4, #5, #10 | Deepen — interactions feel alive, not static |
| **Sprint 3** (week 5–6) | #6, mobile, empty states | Complete — the last-mile polish that earns daily use |

---

## IMMEDIATE — Fix the 3 Broken Things

### 7A. Cmd+K Search

**Current state**: Search icon/bar visible in header across all roles. Neither keyboard shortcut (Cmd+K) nor click triggers any modal or input.

**Required behavior**:
- Cmd+K (or Ctrl+K on Linux/Windows) opens a centered modal overlay (z-50, above content)
- Modal contains a single text input with placeholder: "Search courses, people, pages..."
- Results are scoped to the current persona's world:
  - Student: courses, assignments, lectures, grades
  - Faculty: courses, students, submissions, gradebook entries
  - Admin: courses, faculty, students, sections, policies
  - Coordinator: faculty, students, sections, offerings
- Results appear as-you-type (debounced 200ms) grouped by category
- Enter on a result navigates to that page; Escape closes
- Clicking outside the modal closes it

**Acceptance criteria**:
- [ ] Cmd+K opens modal from any page in any role
- [ ] Typing filters results in real-time
- [ ] Selecting a result navigates correctly
- [ ] Escape and click-outside both close
- [ ] Modal sits at z-50 (above header per PRD §7 stacking law)

---

### 7B. Dark/Light Theme Toggle

**Current state**: Site renders in dark mode. No visible toggle found in the UI. PRD §10 says theme is CSS-variable-backed and persists locally.

**Required behavior**:
- Theme toggle button in the header (right side, near account menu)
- Simple icon: sun for light mode, moon for dark mode
- Click toggles `data-theme` attribute on `<html>` between `"light"` and `"dark"`
- Preference persists in `localStorage` (key: `theme`)
- On first visit, respect `prefers-color-scheme` media query
- Transition: 200ms on `background-color` and `color` properties

**Acceptance criteria**:
- [ ] Toggle visible on every authenticated page
- [ ] Clicking switches between light and dark instantly
- [ ] Refreshing the page preserves the choice
- [ ] Every page renders correctly in light mode (no illegible text, no invisible borders)
- [ ] Momentum green hero is legible in both themes
- [ ] Modal overlays render correctly in both themes

---

### 7C. Dr. Kamrul Hasan in Faculty Picker

**Current state**: Faculty picker modal shows 267 faculty. Searching "Kamrul" returns no results. PRD §8 identifies Dr. Kamrul Hasan as the wired demo teacher whose data is always shown.

**Required behavior**:
- Dr. Kamrul Hasan must appear in the faculty list
- He should be near the top of results when searching "Kamrul" or "Hasan"
- His entry should show: name, rank (Associate Professor), code (KMH), courses (CSE110, CSE321)
- Selecting him should set the displayed identity to his name/title/email
- Data filtering remains unchanged (always shows his teaching data regardless of selection per §8)

**Acceptance criteria**:
- [ ] Searching "Kamrul" in faculty picker returns Dr. Kamrul Hasan
- [ ] Selecting him sets the active identity correctly
- [ ] Teaching data (CSE110, CSE321, 166 students) remains unchanged regardless of selection

---

## SPRINT 1 — Simplify Every Home

### 1. Student Home: Priority Stack

**Current state**: 8+ sections competing for attention: live class banner, jump-back-in, 4 course cards, momentum widget, rings, AI tutor promo, due assignments, upcoming classes.

**New design — Smart Priority Card**:

Replace the top of the page with ONE dynamic card that shows the most important thing right now. The card changes based on context:

```
PRIORITY LOGIC (evaluated in order):

1. CLASS IS LIVE NOW
   → "CSE110 is live — 31 of 35 joined"
   → [Join now] button
   → Shows time elapsed: "Started 12 min ago"

2. CLASS STARTS WITHIN 30 MINUTES
   → "CSE110 starts in 12 minutes"
   → [Join when ready] button
   → Shows room/link

3. ASSIGNMENT DUE WITHIN 24 HOURS
   → "Quiz 4 — Pointers due in 3 hours"
   → [Open quiz] button
   → Shows course name

4. UNFINISHED LECTURE (jump-back-in)
   → "Continue Lecture 8 — Arrays & Strings"
   → [Resume at 45%] button
   → Shows time remaining

5. NOTHING URGENT
   → "You're all caught up, Anika"
   → Shows today's momentum ring progress
   → Suggest: "Practice CSE110 to close your Retrieve ring"
```

**What moves below the fold**:
- Course cards (4 enrolled) — stay but move down
- Momentum summary — compact version in a thin bar
- AI Tutor promo card — REMOVED (see #8)
- Due assignments list — stays below courses
- Upcoming classes — stays at bottom

**Layout**:
```
┌─────────────────────────────────┐
│  SMART PRIORITY CARD            │  ← one thing, full width
│  (dynamic based on context)     │
└─────────────────────────────────┘

  Today's progress: ○ ◐ ● (rings, inline, compact)

┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│CSE110│ │CSE220│ │CSE260│ │CSE321│  ← courses
│ 68%  │ │ 41%  │ │ 55%  │ │ 23%  │
└──────┘ └──────┘ └──────┘ └──────┘

  Due soon (3)          This week (2)
  ─────────            ─────────
  Quiz 4 — 3h          Live class — Tue
  Lab 6 — tomorrow     Lab 7 — Thu
```

**Acceptance criteria**:
- [ ] Only ONE priority card at the top — never two banners competing
- [ ] Priority logic correctly evaluates live > upcoming > due > resume > calm
- [ ] Rings shown inline (not as a separate section)
- [ ] Page loads and answers "what do I do now?" in under 2 seconds visually
- [ ] Mobile: priority card is full-width, courses stack to 2-column grid

---

### 3. Admin Home: Decision-First Layout

**Current state**: Analyst query box, Needs You (3 cards), Timeline, Performance section with tabs — all share equal visual weight.

**New design — Two clear zones**:

```
ZONE 1: "NEEDS YOUR DECISION" (prominent, top)
┌─────────────────────────────────────────────┐
│  3 items need you                           │
│                                             │
│  ┌─────────────────┐  Certify final grades  │
│  │      5          │  5 sections ready       │
│  │   sections      │  [Review & certify →]   │
│  └─────────────────┘                         │
│                                             │
│  ┌─────────────────┐  Finals eligibility    │
│  │      1          │  1 barred student       │
│  │   student       │  [Open eligibility →]   │
│  └─────────────────┘                         │
│                                             │
│  ┌─────────────────┐  Staff a section       │
│  │      1          │  CSE221 Sec 2           │
│  │    open         │  [Assign teacher →]     │
│  └─────────────────┘                         │
└─────────────────────────────────────────────┘

When all items are resolved:
┌─────────────────────────────────────────────┐
│  Nothing needs your decision right now.     │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ Ask your department anything...       │  │  ← Analyst becomes
│  │ "worst attendance?" "lowest marks?"   │  │     the resting state
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘

ZONE 2: "DEPARTMENT HEALTH" (calm, below, collapsed by default)
  ── Closing Summer 2026 ──────────────────
  Timeline: Aug 22 → Aug 28 (you) → Sep 1

  ── Performance ──────────────────────────
  99% pass rate · 3 at-risk · [expand]
```

**Key changes**:
- "Needs You" gets 70% of above-the-fold space
- Performance section defaults to collapsed summary (one line: "99% pass, 3 at-risk")
- Analyst query box moves INTO the "Nothing needs you" calm state
- Timeline stays but is visually quieter (thin horizontal bar, not a full section)

**Acceptance criteria**:
- [ ] Chair knows how many decisions need them within 2 seconds of opening
- [ ] Decision count decrements as items are resolved
- [ ] When no decisions remain, Analyst query box is front and center
- [ ] Performance section is collapsed by default with a one-line summary
- [ ] Expanding performance shows the existing Courses/Teachers/Students tabs

---

### 8. Remove Promo Cards + Reduce Sidebar

**Promo cards to remove**:
- Student home: "Shikho AI Tutor — Stuck on something? Ask, anytime" card
- Faculty home: "Shikho AI Copilot" promotional card
- Any other card that markets a feature the user already has access to

**Sidebar reduction**:

```
STUDENT (current ~10 items → 4 + AI):
  Home
  Courses          ← Schedule lives as a tab inside Courses
  Grades
  Tutor            ← AI mode, always last per PRD §7
  ──
  Profile (bottom) ← Settings, Usage accessible from Profile

FACULTY (current ~10 items → 4 + AI):
  Home
  Courses          ← contains course detail, gradebook
  Grading          ← the review inbox
  Copilot          ← AI mode, always last per PRD §7
  ──
  Profile (bottom) ← Settings, Usage accessible from Profile

  Note: "Record" and "Live" become action buttons on
  the Home page or inside a Course, not sidebar destinations.

ADMIN (current 6 items → keep as-is):
  Home | Program | Directory | Certify | Eligibility | Analyst
  Already clean — each is a distinct governance function.

COORDINATOR (current 3 items → keep as-is):
  Records | Directory | Offering
  Already clean.
```

**Where do removed items live?**
- Schedule → tab inside Courses page (student) or on Home (faculty)
- Catalog → accessible from Courses page as "Browse all 26 courses" link
- Practice → accessible from within each Course's AI Tutor tab, or from Momentum rings
- Momentum → accessible from Home (click the momentum score/rings)
- Live → action button on Home or within the live course
- Record → action button on Faculty Home
- Usage → inside Profile page as a tab
- Settings → inside Profile page as a tab

**Acceptance criteria**:
- [ ] No promotional/marketing cards on any home page
- [ ] Student sidebar has exactly: Home, Courses, Grades, Tutor, Profile
- [ ] Faculty sidebar has exactly: Home, Courses, Grading, Copilot, Profile
- [ ] All removed pages remain accessible via their new locations
- [ ] Mobile bottom nav matches the reduced sidebar (4-5 items max)

---

### 9. Analyst as Resting State of Admin Home

**Current state**: Analyst has its own sidebar page + a query box on the admin home that competes with Needs You and Performance for attention.

**New behavior**:
- When "Needs You" has items: query box is minimal (just an input field below the decision cards)
- When "Needs You" is empty (all resolved or term is calm): the query box BECOMES the hero
  - Full-width, centered
  - "Your department is running smoothly. Anything you want to know?"
  - 6 suggested questions as chips below
  - Previous answers from this session shown below

- The separate Analyst sidebar page remains (for deep exploration sessions) but the home-page integration is the primary discovery path

**Acceptance criteria**:
- [ ] When decisions exist: query box is present but secondary
- [ ] When no decisions: query box is the dominant element on the page
- [ ] Suggested questions are visible and clickable
- [ ] Clicking a suggestion fills the input and submits
- [ ] Answer cards render inline on the home page (don't navigate away)

---

## SPRINT 2 — Make Interactions Feel Alive

### 2. One-at-a-Time Grading Flow

**Current state**: Queue view showing 9 submissions as a list. Each has AI-drafted feedback, Approve/Edit buttons.

**New design — Focus Mode**:

Add a "Review" button that enters a focused, full-screen review flow:

```
┌─────────────────────────────────────────────┐
│  Reviewing 1 of 9                     [×]   │
│─────────────────────────────────────────────│
│                                             │
│  Tanvir Ahmed · CSE110 · Lab 6 Recursion    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Student's code / submission         │    │
│  │ (scrollable)                        │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Score: 27/30 (AI draft)  Tests: 18/20 ✓    │
│                                             │
│  AI Feedback:                               │
│  "Good recursive structure. The base case   │
│   handles empty arrays correctly..."        │
│  [Edit feedback]                            │
│                                             │
│  ┌────────────┐        ┌─────────────────┐  │
│  │  Approve   │        │  Edit & approve  │  │
│  │   (→ next) │        │                  │  │
│  └────────────┘        └─────────────────┘  │
└─────────────────────────────────────────────┘

After Approve:
- Brief success flash ("Approved — 8 remaining")
- Auto-advance to next submission
- Progress bar at top: ████░░░░░ 1/9

After all approved:
- "All caught up — 9 submissions reviewed"
- Satisfying completion state
- [Back to course] button
```

**The queue view stays** as the entry point and overview. The focus mode is an additional flow for rapid review.

**Acceptance criteria**:
- [ ] "Review all" button on grading page enters focus mode
- [ ] One submission fills the screen — no distractions
- [ ] Approve auto-advances to next with brief success feedback
- [ ] Progress indicator shows position (1/9, 2/9...)
- [ ] Completion state feels like an achievement, not a dead end
- [ ] Escape or [x] returns to queue view with updated counts
- [ ] Works on mobile (stacked layout, large touch targets for Approve)

---

### 4. Context-Carrying AI Tutor

**Current state**: Tutor opens to a course-selection screen every time. User must pick a course before starting.

**New behavior**:

```
CONTEXT SOURCES (checked in order):
1. Deep link: /student/tutor?course=CSE110&topic=pointer-arithmetic
   → Opens directly: "Let's work on Pointer Arithmetic in CSE110"

2. Last interaction: stored in localStorage
   → Opens directly into last course's conversation

3. Referral from another page:
   - Grades page "focus area" → Tutor opens with that topic
   - Course progress "weak topic" → Tutor opens with that topic
   - Momentum ring "Practice" → Tutor opens with weakest topic

4. No context: show course picker (current behavior, fallback)
```

**Implementation**:
- Store `lastTutorContext: { courseId, topicSlug, timestamp }` in localStorage
- Pages that link to Tutor pass query params: `?course=CSE110&topic=pointer-arithmetic`
- Tutor page checks: query params → localStorage → fallback to picker
- When opening with context, show a dismissible banner: "Continuing with Pointer Arithmetic · CSE110" with [Change course] link

**Acceptance criteria**:
- [ ] Clicking "Get help" on a weak topic in Grades navigates to Tutor with that topic pre-loaded
- [ ] Reopening Tutor within the same session resumes last course (no picker)
- [ ] "Change course" link always available to switch
- [ ] First-ever visit still shows the course picker (no context available)

---

### 5. Actionable At-Risk Flags

**Current state**: Faculty home shows 3 at-risk students with engagement signals (e.g., "Missed 4 live classes, no submissions in 2 weeks") but no actions beyond viewing.

**New design — Each flag gets an action menu**:

```
┌──────────────────────────────────────────┐
│ ⚠ Rakib Hasan · CSE110 Sec 3            │
│   HIGH RISK · 41% attendance             │
│   Missed 4 live classes, no submissions  │
│                                          │
│   [Send check-in]  [View profile]  [···] │
│                      ↓                   │
│               More: Flag to advisor      │
│                     Schedule meeting     │
│                     Add note             │
└──────────────────────────────────────────┘
```

**Actions**:
- **Send check-in**: Opens a pre-drafted message (email or in-platform notification) — "Hi Rakib, I noticed you've missed a few classes. Is everything okay? Let me know if you need any support. — Dr. Hasan"
- **View profile**: Navigates to student detail page (already exists)
- **Flag to advisor**: Creates a notification for the student's academic advisor
- **Schedule meeting**: Opens a simple time-picker to set office hours
- **Add note**: Attaches a private note to the student's record

For the prototype: "Send check-in" and "View profile" should be functional. Others can show a toast: "In the full version, this would notify the advisor."

**Acceptance criteria**:
- [ ] Every at-risk student card has at least 2 action buttons
- [ ] "Send check-in" opens a pre-drafted message (editable before sending)
- [ ] "View profile" navigates to the student detail page
- [ ] Actions that aren't wired yet show a graceful placeholder (not a dead click)

---

### 10. One-Tap Ring-to-Action

**Current state**: Momentum rings show progress (e.g., "Absorb 22/30 min") but tapping them navigates to the Momentum detail page, not to the action that closes the ring.

**New behavior**:

```
RING → ACTION MAPPING:

Absorb (watch lectures):
  "8 min left" → navigates to the most recent unwatched lecture
  Link: /student/course/CSE110/content?autoplay=true

Retrieve (answer practice questions):
  "1 question left" → navigates to Practice with weakest topic
  Link: /student/practice?course=CSE110&topic=pointer-arithmetic

Apply (submit work):
  Already done (✓) → no action needed
  If incomplete → navigates to the next due assignment
  Link: /student/course/CSE110/assessments?filter=due
```

**On the home page**:
- Each ring is tappable
- Incomplete rings navigate to the action
- Completed rings show a subtle check with no navigation (or navigate to Momentum detail)
- Tooltip/label under each ring shows the action: "Watch 8 more min"

**Acceptance criteria**:
- [ ] Tapping an incomplete ring navigates to the relevant content
- [ ] The destination matches the ring type (lectures for Absorb, practice for Retrieve, assignments for Apply)
- [ ] Completed rings don't navigate to content (show completion state)
- [ ] Each ring shows a micro-label: "8 min left" or "1 question" or "Done"

---

## SPRINT 3 — Last-Mile Polish

### 6. Post-Import Preview with Confirm

**Current state**: Import modal has a drop zone with template/sample data options. Post-drop behavior unknown (not tested during audit).

**New design — Three-step import**:

```
STEP 1: DROP
┌─────────────────────────────────┐
│  Drop your spreadsheet          │
│  CSV from Excel or SIS          │
│  [Browse] [Template] [Sample]   │
└─────────────────────────────────┘

STEP 2: PREVIEW (after file is parsed)
┌─────────────────────────────────┐
│  Ready to import                │
│                                 │
│  42 students will be added      │
│   3 already exist (will skip)   │
│   0 errors                      │
│                                 │
│  Preview:                       │
│  ┌─────────────────────────┐    │
│  │ Name    │ ID     │ Sec  │    │
│  │ Anika R │ 231011 │ Sec1 │    │
│  │ Tanvir  │ 231022 │ Sec2 │    │
│  │ ...     │        │      │    │
│  └─────────────────────────┘    │
│                                 │
│  [Cancel]          [Import 42]  │
└─────────────────────────────────┘

STEP 3: CONFIRM
┌─────────────────────────────────┐
│  ✓ 42 students imported         │
│    3 skipped (already exist)    │
│                                 │
│  Saved to this session only.    │
│  [View in directory]  [Done]    │
└─────────────────────────────────┘
```

**Error handling**:
- If rows have validation errors: show them inline in the preview with red highlights
- "2 rows have errors" with expandable detail
- Import button disabled until errors are fixed or errored rows are excluded

**Acceptance criteria**:
- [ ] After file drop, preview shows count of additions, skips, and errors
- [ ] Preview table shows first ~10 rows with column headers
- [ ] Import button shows the count: "Import 42" not just "Import"
- [ ] Errors are highlighted with actionable messages
- [ ] Success state confirms what happened with a link to view results
- [ ] "Saved to this session only" disclaimer is visible (per PRD §28)

---

### Mobile-First Mindset

**Key mobile changes**:

1. **Bottom navigation** (below `lg` breakpoint per PRD §7):
   - Student: Home | Courses | Grades | Tutor
   - Faculty: Home | Courses | Grading | Copilot
   - Admin: Home | Certify | Directory | Analyst
   - Coordinator: Records | Directory | Offering

2. **Priority card on student home**: full-width, large touch target for the primary action

3. **Grading focus mode**: Approve button should be a large touch target at the bottom of the screen (thumb-zone)

4. **Touch targets**: minimum 44x44px for all interactive elements

5. **Sidebar**: slides in from left on mobile, not always visible

**Acceptance criteria**:
- [ ] Bottom nav appears below `lg` breakpoint with 4 items
- [ ] All primary actions are in the thumb zone on mobile
- [ ] No horizontal scrolling on any page at 375px width
- [ ] Modals are full-screen on mobile (not centered dialogs)

---

### Human Empty States

Replace generic empty states with contextual, warm messages:

```
LIVE CLASS (no class now):
  Before: (blank or generic)
  After:  "No class right now. Your next one is CSE220 tomorrow at 10:00 AM."
          [Add to calendar]

GRADING (all reviewed):
  Before: (empty queue)
  After:  "All caught up — 9 submissions reviewed this session."
          "Your students will see their feedback today."

NOTIFICATIONS (none):
  Before: "No notifications"
  After:  "Nothing new — your term is running smoothly."

SEARCH (no results):
  Before: "No results"
  After:  "Nothing matched '[query]'. Try a course code, student name, or topic."

TUTOR (first visit):
  Before: Course picker
  After:  "Hi Anika — pick a course and ask me anything.
           I'll answer from your lectures and notes — or tell you
           honestly when something isn't covered."
```

**Acceptance criteria**:
- [ ] Every empty state has a contextual message (not generic)
- [ ] Empty states suggest a next action where applicable
- [ ] Tone is warm and reassuring, never clinical

---

## Coordinator Home: Completeness-First Layout

**Current state**: Three cards: Flag to Chair, Export to registrar, Records loaded. All framed around handoffs.

**New design — Lead with the coordinator's own checklist**:

```
YOUR RECORDS STATUS
┌─────────────────────────────────────────┐
│  Faculty   267 loaded    ✓ complete     │
│  Students  162 loaded    ○ 5,951 in SIS │
│  Sections   11 loaded    ⚠ 1 unstaffed  │
│  Offering  published     ✓ ready        │
└─────────────────────────────────────────┘

HANDOFFS
  → 1 section flagged to the Chair (CSE221 Sec 2)
  → Grade sheets due to registrar Sep 1 (awaiting Chair)

IMPORT / EXPORT DESKS
  (existing cards, unchanged)
```

**Acceptance criteria**:
- [ ] Completeness checklist is the first thing the coordinator sees
- [ ] Each line shows: entity, count, status (complete/partial/warning)
- [ ] Handoffs section is below the checklist, not above it
- [ ] Pipeline timeline remains at the bottom

---

## Certify Page: Attention-Sorted

**Current state**: 5 sections listed in section-number order. All look identical.

**New behavior**:
- Sort sections by "needs attention" score:
  - Sections with flags (attendance anomaly, below-norm distribution) → top
  - Sections with negative delta vs course average → next
  - Clean sections (100% pass, no flags) → bottom
- Visual cue for anomaly sections: a subtle left-border accent (coral per design system)
- Clean sections get a "Routine" label to signal they can be certified quickly
- Optional: "Certify all routine" batch button for clean sections

```
SECTIONS AWAITING CERTIFICATION (5)

⚠ CSE110 Sec 3 — 97% pass · -2% vs course
  [Review in detail]  [Certify]  [Return]

  CSE110 Sec 1 — 100% pass · +1%  · Routine
  CSE110 Sec 2 — 100% pass · +1%  · Routine
  CSE321 Sec 1 — 100% pass · +0%  · Routine
  CSE321 Sec 2 — 100% pass · +0%  · Routine

  [Certify all 4 routine sections]
```

**Acceptance criteria**:
- [ ] Sections with anomalies appear first
- [ ] Anomaly sections have a visual accent (not just position)
- [ ] Clean sections are labeled "Routine"
- [ ] "Certify all routine" button certifies all clean sections in one click
- [ ] Certification count updates: "1 of 5 certified" → "5 of 5 certified"

---

## Summary Checklist for QA

- [ ] Search (Cmd+K) works in all 4 roles
- [ ] Theme toggle visible and functional
- [ ] Dr. Kamrul Hasan findable in faculty picker
- [ ] Student home shows ONE priority card (not 8 sections)
- [ ] Admin home separates "Needs you" from "Department health"
- [ ] No promotional cards on any home page
- [ ] Student sidebar: 4 items + profile
- [ ] Faculty sidebar: 4 items + profile
- [ ] Grading has a focus-mode review flow
- [ ] AI Tutor carries context from other pages
- [ ] At-risk flags have action buttons
- [ ] Coordinator home leads with completeness checklist
- [ ] Import shows preview before confirming
- [ ] Momentum rings link to the action that closes them
- [ ] Certify page sorts anomalies first
- [ ] Analyst is the resting state of admin home when nothing needs attention
- [ ] Bottom nav on mobile with 4 items per role
- [ ] Every empty state has a warm, contextual message
- [ ] All above work in both light and dark mode
