# Sample 03 — Elementor Responsive Section Repair

A narrowly scoped WordPress plugin and static markup fixture demonstrating a mobile layout repair for one Elementor section.

## Business problem

An Elementor section can look correct on desktop but overflow, stack poorly, or produce oversized headings and unusable buttons on mobile. A safe repair should target the affected section only and avoid changing unrelated theme or page styles.

## What this delivers

- Small WordPress plugin that enqueues one local stylesheet only when Elementor is active.
- CSS scoped to a single Elementor element ID: `elementor-element-7f3a9c2`.
- Mobile column stacking, full-width columns, controlled heading scale, image containment, and touch-friendly CTA width.
- CSS logical properties for spacing.
- Cache-busting stylesheet version based on file modification time.
- No JavaScript, remote fonts, CDN, or third-party runtime dependencies.
- Static preview fixture with representative Elementor markup.

## Preview

Open [the static repair preview](./preview.html). It mirrors common Elementor wrapper classes and loads the exact scoped CSS file used by the plugin.

**Important:** the preview is a local HTML fixture, not a live WordPress or Elementor installation. It verifies the markup/CSS concept but does not prove behavior inside a particular theme, Elementor version, or third-party widget stack.

## Installation on an authorized WordPress site

1. Back up the site and test on staging first.
2. Inspect the target section in Elementor and copy its CSS ID (without the `elementor-element-` prefix).
3. Replace `7f3a9c2` in `assets/elementor-mobile-fix.css` with that ID.
4. Upload this folder to `wp-content/plugins/zubair-elementor-mobile-section-fix/`.
5. Activate **Zubair Elementor Mobile Section Repair**.
6. Confirm Elementor is active, clear page/cache/CDN caches, and inspect the target page at desktop and mobile widths.
7. If the result is not correct, deactivate the plugin to roll back the CSS.

Do not install on a production client site without explicit authorization. Do not copy this target ID to another page; Elementor IDs are page-specific.

## Acceptance and boundaries

Run:

```bash
php -l elementor-mobile-section-fix.php
python -m unittest discover -s tests -v
```

Six static tests cover plugin metadata and direct-access guard, Elementor-only enqueue behavior, scoped selectors, mobile rules, logical properties, local preview references, and absence of remote runtime dependencies. GitHub Actions also runs PHP syntax validation.

Browser/device screenshots and a live WordPress/Elementor integration test remain outstanding. The sample is therefore presented as a code-level repair demonstration, not a verified client-site fix.

## Deliverables

- `elementor-mobile-section-fix.php` — WordPress plugin entry point.
- `assets/elementor-mobile-fix.css` — scoped responsive override.
- `preview.html` — local static markup fixture.
- `tests/test_elementor_repair.py` — static acceptance tests.
- `.github/workflows/portfolio-sample-03.yml` — automated acceptance workflow.
