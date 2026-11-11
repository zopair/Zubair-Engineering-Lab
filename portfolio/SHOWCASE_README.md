# Portfolio Showcase

This directory contains the client-facing work-sample gallery and its supporting case studies.

## Entry point

Open [Selected Work](./index.html) to browse the completed samples. The gallery is a static, dependency-free page designed for desktop and mobile screens.

## Presentation rules

- Only completed samples appear as featured work.
- Each card links to a case study, source file, and verified CI evidence.
- Synthetic data and illustrative CSS previews are used; no client assets or private records are included.
- CI status means the linked automated checks passed. It does not imply a live client deployment or browser-based visual QA.
- Do not add screenshots, hosted-demo claims, or client outcomes unless they have been independently verified.

## Structure

- `index.html` — semantic gallery page.
- `assets/portfolio.css` — responsive visual system and component styling.
- `tests/test_portfolio_site.py` — static acceptance checks and internal-link validation.
- `01-responsive-landing-page/`, `02-spreadsheet-cleanup/`, `04-batch-file-automation/` — individual case studies and source.

## Local validation

From the repository root:

```bash
python -m unittest discover -s portfolio/tests -v
```

The GitHub Actions workflow `.github/workflows/portfolio-showcase.yml` runs the same checks. The gallery is not described as publicly hosted until a deployment is configured and verified.
