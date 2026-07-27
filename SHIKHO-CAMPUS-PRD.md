# Shikho Campus — Product Requirements (v5)

The PRD is an HTML document set. Read it in a browser.

## Open it

```bash
cd "/home/shikho/Brac Platform Explore/prd-local"
python3 -m http.server 8000
```

Then open http://localhost:8000/

## How to read

| Page | Job |
| --- | --- |
| `index.html` | Product overview, rules, devices, permissions |
| `student.html` / `faculty.html` / `admin.html` / `coordinator.html` | Feature specs for that role |
| `wireframes.html` | Reference wireframes — not fixed UI |
| `build.html` | Cross-cutting UI & engineering contracts |
| `ai.html` | Campus AI |
| `platform.html` | Signals between modules |
| `university-activities.html` | University activity coverage map |
| Live demo | https://shikho-brac-platform.vercel.app/ |

**Modules = behaviour.** **Wireframes = reference layout (not fixed).** **Build = shared contracts** (breakpoints, toasts, print/PDF, RBAC, session, PDPA).

Every module has the same three parts:

1. **Introduction** — who uses it, what it owns
2. **Feature list** — every feature, priority, connections
3. **Feature details** — screens and exact copy, steps, rules, edge cases

## Rules every feature obeys

1. Chairperson certifies; teacher marks — no admin mark edit
2. AI drafts; a person decides
3. Platform never holds university money
4. Fee amounts come from finance
5. Marks, attendance, payments, holds, approvals keep full history
6. Every automated decision can show its source records
7. University differences are settings, not new software
8. Teachers never invite students — rosters from university records
9. No public ranking of students
10. One responsive web app across phone, tablet, laptop, desktop, classroom TV

## Research appendix

`PRD-Research-Foundation.md` · `PRD-BD-Regulatory-Requirements.md` · `PRD-Workflow-Edge-Case-Map.md`
