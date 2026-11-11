# Portfolio Sample 01 — Responsive Landing Page Repair

**Category:** Front-end fixes · HTML/CSS · Mobile responsiveness  
**Status:** Completed sample implementation; automated static checks included.

## Client-style brief
A single-page site looks acceptable on desktop but fails on mobile: text becomes too small, duplicated hero copy appears, and a dark notice banner has poor contrast.

## What this sample demonstrates
- Removes duplicated hero content by keeping one authoritative description block.
- Uses a mobile-first responsive breakpoint and readable 17–18px body copy on narrow screens.
- Uses explicit high-contrast notice colors (`#10243a` / `#ffffff`).
- Prevents horizontal page overflow and uses fluid widths.
- Adds semantic landmarks, a skip link, keyboard-visible focus, and reduced-motion support.
- Keeps structure and styling separate; no inline styles or third-party dependencies.

## Files
- `index.html` — semantic page structure and content.
- `styles.css` — responsive layout and design tokens.
- `tests/test_responsive_landing.py` — deterministic checks for the requested acceptance criteria.

## Run checks
```bash
python -m unittest discover -s tests -v
```

## Tools
HTML5, CSS3, Python 3 standard library (`unittest`). No paid tools or external services required.

## Acceptance checklist
- [x] One hero description; no repeated paragraph fragments.
- [x] Responsive viewport and mobile breakpoints.
- [x] Readable mobile body text.
- [x] High-contrast notice banner.
- [x] No horizontal overflow rule.
- [x] Semantic landmarks and skip link.
- [x] Automated acceptance checks.

## Scope boundary
This is a portfolio demonstration, not a claim that a third-party client's website was modified. The contact email is a placeholder and must be replaced with client-provided details for a real deployment. Browser screenshots and real-device validation should be added when a browser runtime is available.