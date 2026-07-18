#!/usr/bin/env python3
"""
ranking_factor_health_audit.py
---------------------------------
A stdlib-only audit that operationalizes the "confirmed vs folklore" split for a
single URL: it checks the *technical* signals Google has named in official
documentation and flags the classic folklore traps (keyword stuffing).

Design notes / credibility:
  - Every check maps to a Tier-1 Google doc (IDs from the KB sources registry):
      HTTPS         -> S243 (Google: HTTPS as a ranking signal, 2014)
      mobile viewport-> S67  (mobile-first indexing best practices)
      canonical      -> S4    (consolidate duplicate URLs)
      JSON-LD/schema-> S45   (structured data; NOT a ranking factor, display only)
      hreflang      -> S179  (international variants; signal, not directive)
      title/meta    -> S1    (SEO Starter Guide; titles/meta are relevance helpers,
                            meta description is NOT a direct ranking signal - S251 cites Google)
  - This tool does NOT measure ranking. It only surfaces whether the page meets
    the technical prerequisites Google has confirmed matter. Treat output as a
    checklist, not a ranking forecast.
  - Keyword-stuffing detection is a naive frequency heuristic (a single token
    repeating in title/H1). It is a folklore *trap* indicator, not a Google metric.

Requires: Python 3.8+ (stdlib only: urllib.request, html, json, re, sys).
Usage:
  python3 ranking_factor_health_audit.py https://example.com
  python3 ranking_factor_health_audit.py --demo        # offline sample, no network
"""
import sys
import re
import json
import html
import urllib.request
from html.parser import HTMLParser


class _TagScanner(HTMLParser):
    """Collects <title>, <meta> tags, <link rel=canonical>, JSON-LD scripts,
    viewport meta, and hreflang alternates from raw HTML."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self.metas = {}            # name/property -> content
        self.canonical = None
        self.viewport = None
        self.hreflangs = []        # list of hreflang values
        self.jsonld_count = 0
        self._in_title = False
        self._title_parts = []

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "title":
            self._in_title = True
            return
        if tag == "meta":
            name = (attrs_d.get("name") or attrs_d.get("property") or "").lower()
            content = attrs_d.get("content", "")
            if name:
                self.metas[name] = content
            if name == "viewport":
                self.viewport = content
            return
        if tag == "link":
            rel = (attrs_d.get("rel") or "").lower()
            if "canonical" in rel:
                self.canonical = attrs_d.get("href")
            if "alternate" in rel and attrs_d.get("hreflang"):
                self.hreflangs.append((attrs_d.get("hreflang") or "").lower())
            return
        if tag == "script":
            if attrs_d.get("type") == "application/ld+json":
                self.jsonld_count += 1

    def handle_data(self, data):
        if self._in_title:
            self._title_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.title = html.unescape("".join(self._title_parts)).strip()


def _stuffing_score(text):
    """Return (max_repeat_ratio, top_token) for a short string.
    A single word repeating >=40% of tokens is treated as a stuffing smell.
    Returns ratio in [0,1] and the dominant token."""
    if not text:
        return 0.0, ""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    if len(tokens) < 3:
        return 0.0, ""
    counts: dict[str, int] = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    top = ""
    top_n = 0
    for t, n in counts.items():
        if n > top_n:
            top_n = n
            top = t
    return (top_n / len(tokens)), top


def audit(html_text):
    scanner = _TagScanner()
    scanner.feed(html_text)

    checks = []

    # 1. Title present (relevance helper, S1)
    title = scanner.title or ""
    checks.append(("Title tag present", bool(title), "relevance helper (S1)",
                   "Add a descriptive <title>." if not title else ""))

    # 2. Title keyword-stuffing folklore trap
    ratio, tok = _stuffing_score(title)
    if title:
        checks.append(("Title not keyword-stuffed",
                       ratio < 0.40,
                       "folklore trap (stuffing = spam, not a boost)",
                       f"'{tok}' repeats {ratio:.0%} of title tokens"
                       if ratio >= 0.40 else ""))

    # 3. Meta description present (NOT a direct ranking signal, S251)
    desc = scanner.metas.get("description", "")
    checks.append(("Meta description present (display only)",
                   bool(desc),
                   "NOT a direct ranking factor (S251 cites Google)",
                   "" if desc else "Add for CTR; it does not rank you."))

    # 4. Mobile viewport (mobile-first indexing, S67)
    checks.append(("Mobile viewport meta", bool(scanner.viewport),
                   "mobile-first indexing (S67)",
                   "Add <meta name=viewport> for mobile parity." if not scanner.viewport else ""))

    # 5. Canonical (duplicate consolidation, S4)
    checks.append(("Canonical link", bool(scanner.canonical),
                   "duplicate consolidation (S4)",
                   "Add rel=canonical to the preferred URL." if not scanner.canonical else ""))

    # 6. Structured data (display only, NOT a ranking factor, S45)
    checks.append(("JSON-LD structured data", scanner.jsonld_count > 0,
                   "display/rich-result only, NOT a ranking factor (S45)",
                   ""))

    # 7. hreflang (international signal, S179)
    checks.append(("hreflang alternates", len(scanner.hreflangs) > 0,
                   "international signal, not a directive (S179)",
                   ""))

    return checks


def _print_report(checks, source_label):
    print(f"Ranking-factor health audit — {source_label}")
    print("-" * 60)
    ok = 0
    for name, passed, basis, note in checks:
        mark = "PASS" if passed else "----"
        if passed:
            ok += 1
        print(f"[{mark}] {name}")
        print(f"        basis: {basis}")
        if note:
            print(f"        note : {note}")
    print("-" * 60)
    print(f"{ok}/{len(checks)} technical prerequisites met (HTTPS checked separately).")
    print("Reminder: these are prerequisites/display signals, NOT a ranking score.")


_DEMO_HTML = """<!doctype html>
<html lang="en"><head>
<title>Buy cheap cheap cheap shoes cheap online cheap</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Shop shoes.">
<link rel="canonical" href="https://shop.example.com/shoes">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Product"}</script>
</head><body><h1>Cheap shoes</h1></body></html>"""


def main(argv):
    if len(argv) > 1 and argv[1] == "--demo":
        checks = audit(_DEMO_HTML)
        _print_report(checks, "demo (offline sample)")
        # The demo title is deliberately stuffed -> should flag FAIL.
        return 0
    if len(argv) < 2:
        print("Usage: python3 ranking_factor_health_audit.py <url> | --demo", file=sys.stderr)
        return 2
    url = argv[1]
    if not url.startswith("https://"):
        print("FAIL: not HTTPS — Google uses HTTPS as a (lightweight) ranking signal (S243).",
              file=sys.stderr)
        # Still continue to audit the rest if reachable.
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 SEO-audit/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001 - report and exit
        print(f"Could not fetch {url}: {exc}", file=sys.stderr)
        return 1
    checks = audit(raw)
    _print_report(checks, url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
