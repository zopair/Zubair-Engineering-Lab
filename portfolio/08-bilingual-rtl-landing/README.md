# Sample 08 — Bilingual RTL/LTR Landing Page

A polished, static landing-page demonstration that switches between English LTR and Arabic RTL without duplicating the design system.

## Business problem

Bilingual campaigns often break when an English-first layout is translated literally. Arabic requires correct reading direction, typography, alignment, spacing, and responsive behavior—not merely translated strings.

## What this delivers

- English and Arabic content variants with a visible language switch.
- Correct document `lang` and `dir` updates when switching languages.
- CSS logical properties for spacing and positioning.
- Arabic-specific font and heading adjustments.
- Responsive desktop/mobile layouts.
- Semantic landmarks, labelled inputs, visible focus states, and reduced-motion support.
- Local-only form validation demonstration. No network request, submission endpoint, or data storage.
- No external fonts, scripts, libraries, or remote assets.

## Quick start

Open `index.html` directly in a modern browser. No build step, package installation, server, or internet connection is required.

## Form behavior and privacy

The two forms are demonstrations only. Form controls remain disabled until the local script initializes. Browser validation is then performed locally; on a valid submission the page displays a confirmation message and resets the form. If JavaScript is unavailable, the controls stay disabled and cannot submit. The implementation does not call fetch, XMLHttpRequest, sendBeacon, or any external service. Do not enter real personal information.

## Localization and implementation boundaries

- English is the initial language; Arabic is available through the language control.
- The sample uses illustrative advisory copy and a fictional brand.
- It demonstrates layout and interaction mechanics, not a production CRM or lead-capture integration.
- Before a client launch, replace brand/copy, confirm Arabic terminology with the client, connect an approved form endpoint, and add consent/privacy language appropriate to the target market.

## Acceptance evidence

Run:

```bash
python -m unittest discover -s tests -v
```

Seven static acceptance tests verify both language variants, RTL markup, semantic structure, labels, language-direction switching, local-only form behavior, CSS logical properties, mobile/reduced-motion rules, and local asset references.

The dedicated GitHub Actions workflow runs the suite on Python 3.12.

## Deliverables

- `index.html` — bilingual landing page.
- `styles.css` — responsive LTR/RTL design system.
- `app.js` — accessible language switch and local form validation.
- `tests/test_landing_page.py` — static acceptance suite.
- `.github/workflows/portfolio-sample-08.yml` — automated acceptance workflow.

**Work-sample status:** implementation committed; CI verification pending.
