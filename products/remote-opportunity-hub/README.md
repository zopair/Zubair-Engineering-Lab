# Remote Opportunity Hub

A zero-budget, open-source remote-work opportunity directory and profile-writing assistant.

## Product constraints
- No paid services, paid APIs, subscriptions, or card-required infrastructure before revenue validation.
- No scraping of marketplaces or automated applications.
- Only public/authorized job-board feeds and sources whose terms permit display.
- Every listing displays its original platform, company, direct application/source link, publication time (when supplied), and last verification time.
- A failed source fetch must never be interpreted as a closed job.
- Only explicitly remote jobs are published; hybrid, on-site, and uncertain records from company ATS feeds are excluded.
- Geographic restrictions are shown, not hidden. Worldwide listings and country-restricted listings are visibly distinguished.
- Profile copy is grounded in user-supplied facts; unanswered optional questions stay unanswered.

## Current implementation
Python standard-library ingestion and profile generation; static Arabic RTL HTML/CSS/JS frontend; JSON storage; GitHub Actions scheduled refresh and optional GitHub Pages deployment. No database, paid model, API key, or paid infrastructure is required.

## Local run
~~~bash
PYTHONPATH=products/remote-opportunity-hub/src python -m unittest discover -s products/remote-opportunity-hub/tests -v
PYTHONPATH=products/remote-opportunity-hub/src python products/remote-opportunity-hub/scripts/refresh.py --config products/remote-opportunity-hub/config/sources.json --output products/remote-opportunity-hub/web/jobs.json
python -m http.server 8000
~~~
Open the local path: http://localhost:8000/products/remote-opportunity-hub/web/.

## Data sources and reuse terms
- **Himalayas Remote Jobs API** is the first enabled feed. Its published API terms allow commercial display on a site we operate without prior approval, provided every Apply action uses the supplied applicationLink, Himalayas receives visible source credit/linking, jobs are shown only on our own site, and expired listings are removed. We do not syndicate this data to another job board. The API cache refreshes every 24 hours; the connector respects that interval.
- **Greenhouse, Lever, and Ashby** adapters are implemented but not enabled as broad aggregators. Add an individual employer board only after checking its public-feed status, eligible geographies, and terms for third-party display. Publicly reachable does not automatically mean freely reusable.
- Job applications remain on the original employer/platform page. We do not collect candidate credentials or submit applications.

See config/sources.json for active source configuration.

## Data freshness
The frontend checks source-level verification timestamps, not merely the JSON file generation time. A warning appears if a source is older than 24 hours or a source refresh fails. A failed source fetch never closes existing records. Records absent from a successful source snapshot are removed from the active feed window; this does not prove that the employer closed the role. Expired listings are also deactivated using the source expiry timestamp.

## Zero-budget hosting
The static frontend can be published through GitHub Pages for a public repository. The workflow is configured to deploy the web/ directory after validation on main. The repository owner may need to enable Pages with GitHub Actions as the publishing source in repository settings.

## Status
Incubation inside Zubair Engineering Lab. This is an MVP implementation branch, not yet a production job marketplace. A dedicated product repository can be split out after the first end-to-end release is validated.
