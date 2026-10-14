#!/usr/bin/env python3
"""Invoice chase checker (lite). Read-only: reads a CSV, prints who to chase today.

No network, no files written, nothing deleted. Python 3.8+, standard library only.

CSV columns (header row required):
  number, agency, job, invoice_date, terms_days, amount, currency, paid_date
Dates are YYYY-MM-DD. Leave paid_date empty while unpaid.

Usage:
  python chaser.py invoices.csv
  python chaser.py invoices.csv --today 2026-10-14
"""
import argparse
import csv
import sys
from datetime import date, timedelta

REQUIRED = ["number", "agency", "invoice_date", "terms_days", "amount"]


def parse_date(text, row_no, field):
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        raise ValueError("row %d: %s '%s' is not a YYYY-MM-DD date" % (row_no, field, text))


def step_for(days_overdue):
    """Map days overdue to a chase step. Thresholds are the lite defaults."""
    if days_overdue < -5:
        return "Not due yet"
    if days_overdue <= 0:
        return "P-01 Courtesy nudge"
    if days_overdue <= 7:
        return "P-02 Friendly reminder"
    if days_overdue <= 14:
        return "P-03 Second reminder"
    return "ESCALATE - firm/final steps are in the full kit"


def load(path, today):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("missing column(s): " + ", ".join(missing))
        for i, r in enumerate(reader, start=2):
            if not (r.get("number") or "").strip():
                continue
            inv = parse_date(r["invoice_date"], i, "invoice_date")
            try:
                terms = int(r["terms_days"])
                amount = float(r["amount"].replace(",", "."))
            except ValueError:
                raise ValueError("row %d: terms_days must be a whole number and amount a number" % i)
            paid = (r.get("paid_date") or "").strip()
            paid_d = parse_date(paid, i, "paid_date") if paid else None
            due = inv + timedelta(days=terms)
            rows.append({
                "number": r["number"].strip(), "agency": r["agency"].strip(),
                "job": (r.get("job") or "").strip(), "due": due,
                "amount": amount, "currency": (r.get("currency") or "").strip(),
                "paid": paid_d, "overdue": (today - due).days,
            })
    return rows


def main():
    ap = argparse.ArgumentParser(description="Show which unpaid invoices to chase today (read-only).")
    ap.add_argument("csv_file")
    ap.add_argument("--today", help="override today's date, YYYY-MM-DD (for testing)")
    a = ap.parse_args()
    try:
        today = date.fromisoformat(a.today) if a.today else date.today()
        rows = load(a.csv_file, today)
    except (OSError, ValueError) as e:
        print("Error: %s" % e, file=sys.stderr)
        return 1

    open_rows = sorted((r for r in rows if r["paid"] is None), key=lambda r: -r["overdue"])
    print("Open invoices as of %s\n" % today.isoformat())
    print("%-10s %-18s %-10s %9s  %-8s %s" % ("Invoice", "Agency", "Due", "Amount", "Overdue", "Next step"))
    for r in open_rows:
        od = "%dd" % r["overdue"] if r["overdue"] > 0 else "-"
        print("%-10s %-18s %-10s %9.2f  %-8s %s" % (
            r["number"][:10], r["agency"][:18], r["due"].isoformat(),
            r["amount"], od, step_for(r["overdue"])))
    totals = {}
    for r in open_rows:
        if r["overdue"] > 0:
            totals[r["currency"]] = totals.get(r["currency"], 0.0) + r["amount"]
    print()
    if totals:
        print("Overdue total: " + ", ".join("%.2f %s" % (v, k) for k, v in sorted(totals.items())))
    else:
        print("Nothing overdue.")
    print("Open invoices: %d, paid: %d" % (len(open_rows), len(rows) - len(open_rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
