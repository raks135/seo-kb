#!/usr/bin/env python3
"""scaled_content_audit.py — editorial risk flagger for Google's March 2024
"scaled content abuse" spam policy (see S242).

It flags patterns that *resemble* mass-produced, low-value page generation:
  1. very thin pages (word_count below THIN_WORDS)
  2. templated / near-duplicate titles (shared bigrams across many pages)
  3. a large inventory of thin pages (volume signal for mass generation)

IMPORTANT: This is an EDITORIAL risk signal only. It does NOT mean Google
will take action — and Google's spam policies also weigh intent and value,
not raw counts. Use it to spot pages worth a human quality review.

Run:
    python3 scaled_content_audit.py --demo
    python3 scaled_content_audit.py pages.csv

CSV schema (header row): url,title,word_count
"""
import csv
import re
import argparse
from collections import Counter

THIN_WORDS = 200   # pages below this word count are "thin" by this heuristic
MIN_PAGES = 50     # inventory size at which mass-generation patterns matter more
TEMPLATE_MIN = 3   # a title bigram shared by >= this many thin pages = templated


def title_tokens(title: str):
    return [t for t in re.findall(r"[a-z0-9]+", title.lower())]


def main():
    ap = argparse.ArgumentParser(description="Scaled-content-abuse risk flagger (editorial heuristic).")
    ap.add_argument("csv", nargs="?", help="CSV with header url,title,word_count")
    ap.add_argument("--demo", action="store_true", help="run on built-in sample data")
    args = ap.parse_args()

    if args.demo:
        rows = [
            ("/best-coffee-2024", "Best Coffee 2024 - Our Guide", 80),
            ("/best-coffee-2023", "Best Coffee 2023 - Our Guide", 75),
            ("/best-coffee-texas", "Best Coffee Texas - Our Guide", 90),
            ("/best-coffee-seattle", "Best Coffee Seattle - Our Guide", 85),
            ("/best-coffee-nyc", "Best Coffee NYC - Our Guide", 70),
            ("/about", "About Us", 1200),
            ("/contact", "Contact", 300),
        ]
    elif args.csv:
        rows = []
        with open(args.csv, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows.append((r["url"], r.get("title", ""), int(r.get("word_count", 0))))
    else:
        ap.error("pass a CSV path or --demo")

    thin = [(u, t, w) for (u, t, w) in rows if w < THIN_WORDS]

    # Templated-title detection: bigrams shared across many thin pages.
    bigrams = Counter()
    for _u, title, _w in thin:
        toks = title_tokens(title)
        for i in range(len(toks) - 1):
            bigrams[(toks[i], toks[i + 1])] += 1
    template_hits = {bg for bg, c in bigrams.items() if c >= TEMPLATE_MIN}

    print(f"Pages scanned      : {len(rows)}")
    thin_pct = 100 * len(thin) / max(1, len(rows))
    print(f"Thin pages (<{THIN_WORDS} words): {len(thin)} ({thin_pct:.0f}%)")
    if len(rows) >= MIN_PAGES:
        print("Volume             : large inventory — mass-generation patterns weigh more.")
    if template_hits:
        print("Templated bigrams  : " + ", ".join(" ".join(b) for b in sorted(template_hits)))

    risk = (len(thin) >= 10 and len(rows) >= MIN_PAGES) or bool(template_hits and len(thin) >= 5)
    print("SCALED-CONTENT RISK: " + ("ELEVATED — review these pages for value/intent"
                                      if risk else "low (editorial heuristic only)"))


if __name__ == "__main__":
    main()
