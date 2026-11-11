"""Build a static, auditable sales KPI dashboard from a CSV export."""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = {"order_id", "order_date", "customer_id", "revenue", "status"}
INCLUDED_STATUSES = {"paid", "completed"}
EXCLUDED_STATUSES = {"cancelled", "refunded", "pending"}
CENT = Decimal("0.01")


class DashboardError(ValueError):
    """Raised when the source file cannot support a reliable KPI report."""


def _money(value: Decimal) -> str:
    return str(value.quantize(CENT, rounding=ROUND_HALF_UP))


def _render_dashboard(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    monthly = result["monthly_revenue"]
    issues = result["issues"]
    peak = max((Decimal(item["revenue"]) for item in monthly), default=Decimal("0"))
    month_rows = []
    for item in monthly:
        amount = Decimal(item["revenue"])
        width = float((amount / peak * 100) if peak else 0)
        month_rows.append(
            "<tr><th scope=\"row\">{}</th><td><div class=\"bar-track\">"
            "<span class=\"bar\" style=\"width:{}%\"></span></div></td>"
            "<td class=\"numeric\">{}</td><td class=\"numeric\">{}</td></tr>".format(
                html.escape(item["month"]), f"{width:.2f}",
                html.escape(item["revenue"]), item["orders"],
            )
        )

    if not month_rows:
        month_content = '<p class="empty">No qualifying transactions for the selected period.</p>'
    else:
        month_content = (
            '<div class="table-wrap"><table><thead><tr><th>Month</th><th>Revenue scale</th>'
            '<th class="numeric">Revenue</th><th class="numeric">Orders</th></tr></thead><tbody>'
            + "".join(month_rows) + "</tbody></table></div>"
        )

    issue_rows = "".join(
        "<tr><td>{}</td><td><code>{}</code></td><td>{}</td></tr>".format(
            item["row_number"], html.escape(item["code"]), html.escape(item["message"])
        )
        for item in issues
    )
    if not issue_rows:
        issue_rows = '<tr><td colspan="3">No data-quality issues detected.</td></tr>'

    template = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Static sales KPI dashboard generated from a CSV export.">
<title>Sales KPI Dashboard</title>
<style>
:root{color-scheme:light;--ink:#17243a;--muted:#64748b;--navy:#12233b;--blue:#37658f;--gold:#c99a54;--paper:#f3f6f9;--line:#e1e7ee;--green:#28745d;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);line-height:1.55}
main{width:min(1080px,calc(100% - 40px));margin:48px auto}
header{padding:30px 34px;background:var(--navy);color:#fff;border-radius:18px}
.eyebrow{margin:0 0 8px;color:#e5bd83;font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
h1{margin:0;font-size:clamp(28px,5vw,42px);letter-spacing:-.04em}header p:last-child{max-width:650px;margin:12px 0 0;color:#c4d0dd;font-size:13px}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:20px 0}
.metric,.panel{background:#fff;border:1px solid var(--line);border-radius:14px}
.metric{padding:20px}.metric span{display:block;color:var(--muted);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.metric strong{display:block;margin-top:8px;color:var(--navy);font-size:clamp(20px,3vw,29px);letter-spacing:-.04em}
.panel{margin-top:18px;padding:24px}.panel h2{margin:0 0 16px;font-size:20px;letter-spacing:-.03em}
.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:12px;text-align:left}th,td{padding:12px 10px;border-bottom:1px solid var(--line)}thead th{color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.07em}
.numeric{text-align:right;font-variant-numeric:tabular-nums}.bar-track{height:9px;min-width:90px;overflow:hidden;background:#edf1f5;border-radius:99px}.bar{display:block;height:100%;background:var(--blue);border-radius:99px}
.quality{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 14px;color:var(--muted);font-size:12px}.quality strong{color:var(--navy)}
.empty{padding:22px;background:#f6f8fa;border-radius:10px;color:var(--muted);font-size:13px}
footer{margin-top:20px;color:var(--muted);font-size:11px}
@media(max-width:720px){main{width:calc(100% - 24px);margin:20px auto}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}header{padding:24px}.panel{padding:16px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
</style>
</head>
<body><main>
<header><p class="eyebrow">Business performance · Monthly snapshot</p>
<h1>Sales KPI Dashboard</h1>
<p>Generated from a supplied order export. Revenue includes paid and completed orders only; cancelled, refunded, and pending orders are excluded.</p></header>
<section class="metrics" aria-label="Key performance indicators">
<div class="metric"><span>Recognized revenue</span><strong>{revenue}</strong></div>
<div class="metric"><span>Qualifying orders</span><strong>{orders}</strong></div>
<div class="metric"><span>Average order value</span><strong>{aov}</strong></div>
<div class="metric"><span>Unique customers</span><strong>{customers}</strong></div>
</section>
<section class="panel" aria-labelledby="monthly-heading"><h2 id="monthly-heading">Monthly revenue</h2>{monthly}</section>
<section class="panel" aria-labelledby="quality-heading"><h2 id="quality-heading">Data quality review</h2>
<div class="quality"><span>Source rows: <strong>{source_rows}</strong></span><span>Excluded statuses: <strong>{excluded}</strong></span><span>Issues: <strong>{issue_count}</strong></span></div>
<div class="table-wrap"><table><thead><tr><th>CSV row</th><th>Issue</th><th>Details</th></tr></thead><tbody>{issues}</tbody></table></div>
</section>
<footer>Static report · Currency units follow the source file · No customer-level personal data is displayed</footer>
</main></body></html>"""
    replacements = {
        "{revenue}": html.escape(metrics["revenue"]),
        "{orders}": str(metrics["orders"]),
        "{aov}": html.escape(metrics["average_order_value"]),
        "{customers}": str(metrics["customers"]),
        "{monthly}": month_content,
        "{source_rows}": str(result["source_rows"]),
        "{excluded}": str(result["excluded_orders"]),
        "{issue_count}": str(len(issues)),
        "{issues}": issue_rows,
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    return template


def build_dashboard(
    csv_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    """Validate a sales CSV, calculate KPIs, and create a static HTML report."""
    source = Path(csv_path).expanduser()
    output = Path(output_path).expanduser()
    if not source.is_file():
        raise FileNotFoundError(source)
    if output.suffix.lower() != ".html":
        raise ValueError("Dashboard output must use the .html extension")
    if not output.parent.exists() or not output.parent.is_dir():
        raise NotADirectoryError(output.parent)

    revenue_total = Decimal("0")
    order_count = 0
    customers: set[str] = set()
    monthly_revenue: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    monthly_orders: dict[str, int] = defaultdict(int)
    issues: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    excluded_orders = 0
    source_rows = 0

    try:
        with source.open("r", newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                raise DashboardError("CSV file is empty or has no header row")
            normalized_headers = [header.strip().lower() for header in reader.fieldnames]
            if len(normalized_headers) != len(set(normalized_headers)):
                raise DashboardError("CSV contains duplicate column names after normalization")
            missing = REQUIRED_COLUMNS - set(normalized_headers)
            if missing:
                raise DashboardError("Missing required columns: " + ", ".join(sorted(missing)))
            header_map = dict(zip(reader.fieldnames, normalized_headers))

            for row_number, raw in enumerate(reader, start=2):
                source_rows += 1
                row = {header_map[key]: (value or "").strip() for key, value in raw.items() if key in header_map}
                order_id = row.get("order_id", "")
                if not order_id:
                    issues.append({"row_number": row_number, "code": "missing_order_id", "message": "Order ID is required"})
                    continue
                if order_id in seen_ids:
                    issues.append({"row_number": row_number, "code": "duplicate_order_id", "message": f"Duplicate order ID: {order_id}"})
                    continue
                seen_ids.add(order_id)

                status = row.get("status", "").lower()
                if status in EXCLUDED_STATUSES:
                    excluded_orders += 1
                    continue
                if status not in INCLUDED_STATUSES:
                    issues.append({"row_number": row_number, "code": "unknown_status", "message": "Status must be paid, completed, cancelled, refunded, or pending"})
                    continue

                customer_id = row.get("customer_id", "")
                if not customer_id:
                    issues.append({"row_number": row_number, "code": "missing_customer_id", "message": "Customer ID is required"})
                    continue
                try:
                    order_date = datetime.strptime(row.get("order_date", ""), "%Y-%m-%d").date()
                except ValueError:
                    issues.append({"row_number": row_number, "code": "invalid_order_date", "message": "Order date must use YYYY-MM-DD"})
                    continue
                try:
                    revenue = Decimal(row.get("revenue", ""))
                    if not revenue.is_finite():
                        raise InvalidOperation
                    if revenue < 0:
                        issues.append({"row_number": row_number, "code": "negative_revenue", "message": "Revenue cannot be negative"})
                        continue
                    revenue = revenue.quantize(CENT, rounding=ROUND_HALF_UP)
                except (InvalidOperation, ValueError):
                    issues.append({"row_number": row_number, "code": "invalid_revenue", "message": "Revenue must be a finite numeric amount"})
                    continue

                month = order_date.strftime("%Y-%m")
                revenue_total += revenue
                order_count += 1
                customers.add(customer_id)
                monthly_revenue[month] += revenue
                monthly_orders[month] += 1
    except csv.Error as exc:
        raise DashboardError(f"Unable to parse CSV: {exc}") from exc

    monthly = [
        {"month": month, "revenue": _money(monthly_revenue[month]), "orders": monthly_orders[month]}
        for month in sorted(monthly_revenue)
    ]
    metrics = {
        "revenue": _money(revenue_total),
        "orders": order_count,
        "average_order_value": _money(revenue_total / order_count) if order_count else "0.00",
        "customers": len(customers),
    }
    result: dict[str, Any] = {
        "metrics": metrics,
        "monthly_revenue": monthly,
        "issues": issues,
        "excluded_orders": excluded_orders,
        "source_rows": source_rows,
    }

    try:
        descriptor = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        raise
    else:
        os.close(descriptor)
    try:
        output.write_text(_render_dashboard(result), encoding="utf-8")
    except Exception:
        output.unlink(missing_ok=True)
        raise

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a static sales KPI dashboard from CSV.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_html", type=Path)
    args = parser.parse_args()
    try:
        result = build_dashboard(args.input_csv, args.output_html)
    except (OSError, ValueError, DashboardError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
