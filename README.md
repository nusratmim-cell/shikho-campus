# Shikho Campus

Product requirements for Shikho Campus — a multi-tenant learning management
platform for private universities, Bangladesh first.

The requirements are an HTML document set. Read them in a browser:

```bash
cd prd-local
python3 -m http.server 8000
```

Then open http://localhost:8000/index.html

Start at **Overview**. The menu on every page carries a numbered document map:
Overview, the four modules (Student, Faculty, Administrator, Coordinator),
supporting pages, LMS reference videos, and the live demo.

Live demo: https://shikho-brac-platform.vercel.app/

## What is here

| Path | Contents |
| --- | --- |
| `prd-local/` | The requirements document set — start at `index.html` |
| `SHIKHO-CAMPUS-PRD.md` | Reading guide: the pages, the rules every feature obeys, product decisions |
| `PRD-Research-Foundation.md` | Competitor analysis, architecture patterns, workflow edge cases |
| `PRD-BD-Regulatory-Requirements.md` | PDPA 2026, accreditation, e-signature detail |
| `PRD-Workflow-Edge-Case-Map.md` | Edge cases across the academic term |
| `Shikho-Campus-Adoption-Spec.md` | Adoption and rollout |
