# Sample 07 — Business KPI Dashboard

A dependency-free Python workflow that turns a sales CSV export into a responsive, self-contained HTML KPI report.

## Business problem

Small businesses often have order exports but no concise view of revenue, order volume, average order value, customer reach, and month-to-month performance. The dashboard converts a simple, documented CSV schema into a readable report with a visible data-quality review.

## What this delivers

- Four KPIs: recognized revenue, qualifying orders, average order value, and unique customers.
- Monthly revenue and order-count breakdown.
- Explicit inclusion policy: `paid` and `completed` count toward revenue; `cancelled`, `refunded`, and `pending` are excluded.
- Data-quality issue reporting for missing IDs, duplicate orders, invalid dates/revenue, negative amounts, and unknown statuses.
- Decimal arithmetic and two-decimal currency presentation.
- Static HTML output with responsive CSS, accessible table headings, and no external JavaScript or CDN.
- Existing output files are never overwritten.
- HTML escaping for untrusted CSV values shown in issue messages.

## Quick start

Python 3.10+; standard library only.

```bash
python kpi_dashboard.py ./examples/sample_orders.csv ./dashboard.html
```

Open `dashboard.html` in a browser. The output is a standalone file and does not require a server or internet connection.

## Input schema

| Column | Required | Rule |
|---|---|---|
| `order_id` | Yes | Unique, non-empty order identifier |
| `order_date` | Yes | ISO date: `YYYY-MM-DD` |
| `customer_id` | Yes | Non-empty customer identifier |
| `revenue` | Yes | Finite, non-negative numeric amount |
| `status` | Yes | paid, completed, cancelled, refunded, or pending |

The currency symbol is intentionally omitted because the CSV schema does not define a currency. All amounts are reported in the source file's currency unit. Mixed-currency inputs must be converted before aggregation.

## Metric definitions

- **Recognized revenue:** sum of revenue for valid paid/completed orders.
- **Qualifying orders:** count of valid paid/completed orders.
- **Average order value:** recognized revenue divided by qualifying orders; zero when there are no qualifying orders.
- **Unique customers:** distinct customer IDs among qualifying orders.
- **Monthly revenue:** recognized revenue grouped by order month.

Duplicate order IDs are reported and only the first occurrence is considered. Invalid qualifying rows are excluded and surfaced in the data-quality table. Excluded statuses are counted separately and are not treated as data errors.

## Data and operating boundaries

- The included dataset is synthetic and contains no customer information.
- This is a sales summary, not an accounting ledger or tax report.
- Refunds are excluded rather than netted against original orders; a real client engagement must confirm its refund and revenue-recognition policy.
- Currency conversion, tax, discounts, chargebacks, cohort analysis, and forecasting are out of scope.
- Output is static HTML; no data is uploaded or transmitted.

## Acceptance evidence

Run:

```bash
python -m unittest discover -s tests -v
```

Eight tests cover KPI arithmetic, monthly aggregation, excluded statuses, duplicate IDs, invalid rows, required headers, overwrite protection, HTML escaping, and empty qualifying datasets.

The dedicated GitHub Actions workflow runs the suite on Python 3.12.

## Deliverables

- `kpi_dashboard.py` — validation, metric engine, HTML renderer, and CLI.
- `examples/sample_orders.csv` — synthetic demonstration input.
- `tests/test_kpi_dashboard.py` — isolated acceptance tests.
- `.github/workflows/portfolio-sample-07.yml` — automated acceptance workflow.

**Work-sample status:** implementation committed; CI verification pending.
