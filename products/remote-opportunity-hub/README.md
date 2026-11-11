# Remote Opportunity Hub

A zero-budget, open-source remote-work opportunity directory and profile-writing assistant.

## Product constraints
- No paid services, paid APIs, subscriptions, or card-required infrastructure before revenue validation.
- No scraping of marketplaces or automated applications.
- Only public/authorized job-board feeds and sources whose terms permit display.
- Every listing displays its original platform, company, direct application link, publication time (when supplied), and last verification time.
- A failed source fetch must never be interpreted as a closed job.
- Only explicitly remote jobs are published in the initial public feed; hybrid, on-site, and uncertain records are excluded.
- Profile copy must be grounded in user-supplied facts; unanswered optional questions stay unanswered.

## Current implementation
Python standard-library ingestion and profile generation; static HTML/JS frontend; JSON storage; GitHub Actions scheduled refresh. No database or paid model required.

## Local run
```bash
python -m unittest discover -s products/remote-opportunity-hub/tests -v
python products/remote-opportunity-hub/scripts/refresh.py --config products/remote-opportunity-hub/config/sources.json --output products/remote-opportunity-hub/web/jobs.json
python -m http.server 8000
```
Open `http://localhost:8000/products/remote-opportunity-hub/web/`.

## Source setup
Add a company only after verifying its public careers board and ATS board identifier. See `config/sources.json`. Sources are disabled by default; no placeholder or unverified employer is presented as a real opportunity.

## Data freshness
The frontend shows the exact `last_verified_at` timestamp. Scheduled refresh runs every six hours. The refresh job does not delete or expire records when a source fails; it marks records absent only after a successful full board response. A stale-feed warning is shown after 24 hours.

## Status
Incubation inside Zubair Engineering Lab. A dedicated product repository can be split out after the initial vertical slice is validated.
