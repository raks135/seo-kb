#!/usr/bin/env python3
# nap_audit.py — flag NAP inconsistencies across citation sources.
# STDlib only. Python 3.8+. Run: python3 nap_audit.py citations.csv
import csv, re, sys
from collections import defaultdict

# Canonical NAP = your Google Business Profile (single source of truth).
CANON = {
    "name": "Acme Plumbing LLC",
    "address": "1 Main St, Springfield, IL 62701",
    "phone": "+1-555-0100",
}

def norm_phone(p):
    return re.sub(r"\D", "", p or "")

def norm_text(t):
    return re.sub(r"\s+", " ", (t or "").strip().lower())

def audit(row):
    issues = []
    if norm_text(row.get("name", "")) != norm_text(CANON["name"]):
        issues.append("name mismatch")
    if norm_phone(row.get("phone", "")) != norm_phone(CANON["phone"]):
        issues.append("phone mismatch")
    if norm_text(row.get("address", "")) != norm_text(CANON["address"]):
        issues.append("address mismatch")
    return issues

def main(path):
    by_source = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_source[r.get("source", "?")].append(
                (r.get("url", ""), audit(r)))
    total = sum(len(v) for v in by_source.values())
    bad = sum(1 for v in by_source.values() for _, iss in v if iss)
    print(f"Audited {total} citation records across {len(by_source)} sources.")
    print(f"Inconsistent records: {bad} ({100*bad/max(total,1):.0f}%)")
    for src, recs in by_source.items():
        for url, issues in recs:
            if issues:
                print(f"  [{src}] {url or '(no url)'} -> {', '.join(issues)}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "citations.csv")
