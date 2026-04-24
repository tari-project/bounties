#!/usr/bin/env python3
"""Recompute the cumulative_usd column in payouts/ledger.csv.

For each contributor, sorts their rows by date within the same calendar year
and writes a running total of usd_value into the cumulative_usd column.

Usage:
    python3 scripts/update_ledger_cumulative.py
"""
import csv
import os
import sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
LEDGER_PATH = os.path.join(ROOT_DIR, "payouts", "ledger.csv")


def main():
    with open(LEDGER_PATH, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    if "cumulative_usd" not in fieldnames:
        # Insert cumulative_usd before kyc_status
        idx = fieldnames.index("kyc_status")
        fieldnames.insert(idx, "cumulative_usd")

    # Sort rows by date for stable cumulative computation
    rows.sort(key=lambda r: r["date"])

    # Compute per-contributor per-year running totals
    totals = defaultdict(float)  # key: (contributor, year)
    for row in rows:
        contributor = row["contributor"]
        year = row["date"][:4]
        usd = float(row["usd_value"])
        totals[(contributor, year)] += usd
        row["cumulative_usd"] = f"{totals[(contributor, year)]:.2f}"

    with open(LEDGER_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    print(f"Updated {len(rows)} rows in {LEDGER_PATH}")
    contributors = sorted({r["contributor"] for r in rows})
    for c in contributors:
        year_totals = {k[1]: v for k, v in totals.items() if k[0] == c}
        for year, total in sorted(year_totals.items()):
            flag = " ⚠️  APPROACHING $600" if total >= 500 else ""
            flag = " 🚨 OVER $600" if total >= 600 else flag
            print(f"  @{c} ({year}): ${total:.2f}{flag}")


if __name__ == "__main__":
    main()
