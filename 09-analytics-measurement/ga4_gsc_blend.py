#!/usr/bin/env python3
"""Blend an exported GA4 landing-page report with an exported GSC
Landing Pages report on a shared URL key.

Why: Google Analytics 4 (behavior) and Google Search Console (search
performance) never match row-for-row. The fastest way to see *both*
views on one line -- and to quantify the sessions-vs-clicks gap -- is to
join the two CSV exports on the landing-page URL. This is the manual
equivalent of the Looker Studio blend described in the KB article.

Usage:
    python3 ga4_gsc_blend.py --demo            # runs on built-in sample data
    python3 ga4_gsc_blend.py ga4.csv gsc.csv   # joins your own exports

GA4 export:  "Pages and screens" (or "Landing page") report -> Export CSV.
              Expected column "Landing page" (or "Page path and screen class").
GSC export:  Performance -> Landing pages -> Export CSV.
              Expected column "Landing page".

Requires: Python 3.8+ standard library only (csv, argparse, sys).
The script normalizes URLs (strip trailing slash, lower-case host) before
joining so http/https and trailing-slash variants collapse to one key.
"""
import argparse
import csv
import sys
from urllib.parse import urlsplit

PYTHON_MIN = (3, 8)
if sys.version_info < PYTHON_MIN:
    sys.exit("Requires Python >= 3.8")


def norm_url(u: str) -> str:
    """Normalize a URL for joining.

    For a single-site landing-page blend, the path is the stable key. We strip
    scheme and host so GA4's "/" and GSC's "https://example.com/" both collapse
    to "/" (and "/blog/x" matches "https://example.com/blog/x"). Hosts are
    assumed identical (a single property); cross-domain rows are rare here.
    """
    u = (u or "").strip()
    if not u:
        return ""
    try:
        parts = urlsplit(u)
    except Exception:
        return u.lower().rstrip("/") or "/"
    path = parts.path or "/"
    return path.rstrip("/") or "/"


def load(path: str, key_col_hint):
    """Load a CSV into {normalized_url: {col: val}} using a flexible key column."""
    rows = {}
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = [h.strip() for h in (reader.fieldnames or [])]
        key_col = next((h for h in header if h in key_col_hint), None)
        if key_col is None:
            sys.exit(f"Could not find a URL column ({key_col_hint}) in {path}. "
                     f"Found: {header}")
        for r in reader:
            url = norm_url(r.get(key_col, ""))
            if url:
                rows[url] = {k.strip(): (v.strip() if isinstance(v, str) else v)
                             for k, v in r.items()}
    return rows, key_col


def to_num(v):
    try:
        return float(str(v).replace("%", "").replace(",", "").strip())
    except (ValueError, AttributeError):
        return None


def main():
    ap = argparse.ArgumentParser(description="Blend GA4 + GSC landing-page CSVs.")
    ap.add_argument("ga4", nargs="?", help="GA4 landing-page CSV export")
    ap.add_argument("gsc", nargs="?", help="GSC landing-page CSV export")
    ap.add_argument("--demo", action="store_true", help="run on built-in sample data")
    args = ap.parse_args()

    ga4_hint = ("Landing page", "Page path and screen class", "Page")
    gsc_hint = ("Landing page", "Page", "URL")

    if args.demo or not (args.ga4 and args.gsc):
        # Built-in demo data: note how the same URL shows different numbers in
        # each tool -- exactly the discrepancy Google documents.
        ga4_rows = {
            "/": {"Landing page": "/", "Sessions": "1200",
                  "Engagement rate": "62.0%", "Conversions": "84"},
            "/blog/seo-dashboards": {"Landing page": "/blog/seo-dashboards",
                  "Sessions": "540", "Engagement rate": "71.0%", "Conversions": "12"},
            "/pricing": {"Landing page": "/pricing", "Sessions": "310",
                  "Engagement rate": "44.0%", "Conversions": "39"},
        }
        gsc_rows = {
            "/": {"Landing page": "https://example.com/", "Clicks": "1500",
                  "Impressions": "22000", "CTR": "6.8%", "Average position": "4.2"},
            "/blog/seo-dashboards": {"Landing page": "https://example.com/blog/seo-dashboards",
                  "Clicks": "610", "Impressions": "9800", "CTR": "6.2%",
                  "Average position": "5.1"},
            "/about": {"Landing page": "https://example.com/about", "Clicks": "90",
                  "Impressions": "1500", "CTR": "6.0%", "Average position": "8.0"},
        }
        gkey, skey = "Landing page", "Landing page"
        print("# DEMO MODE -- sample GA4 + GSC exports\n")
    else:
        ga4_rows, gkey = load(args.ga4, ga4_hint)
        gsc_rows, skey = load(args.gsc, gsc_hint)
        print(f"# Loaded {len(ga4_rows)} GA4 rows, {len(gsc_rows)} GSC rows "
              f"(key cols: '{gkey}' / '{skey}')\n")

    # Join on normalized URL.
    keys = sorted(set(ga4_rows) | set(gsc_rows))
    print(f"{'URL':42} {'Sessions':>9} {'Clicks':>8} {'CTR%':>6} {'Eng%':>6} {'C/S':>6}")
    print("-" * 84)
    for k in keys:
        g = ga4_rows.get(k, {})
        s = gsc_rows.get(k, {})
        sessions = to_num(g.get("Sessions"))
        clicks = to_num(s.get("Clicks"))
        ctr = to_num(s.get("CTR"))
        eng = to_num(g.get("Engagement rate"))
        cs = (round(clicks / sessions, 2) if (sessions and clicks is not None) else None)
        label = (g.get(gkey) or s.get(skey) or k)[:42]
        print(f"{label:42} {str(int(sessions) if sessions else '-'):>9} "
              f"{str(int(clicks) if clicks else '-'):>8} "
              f"{str(ctr if ctr is not None else '-'):>6} "
              f"{str(eng if eng is not None else '-'):>6} "
              f"{str(cs if cs is not None else '-'):>6}")
    print("\nC/S = GSC Clicks / GA4 Sessions for the same URL (the organic gap;")


if __name__ == "__main__":
    main()
