#!/usr/bin/env python3
"""
marketplace_seo_checklist.py — Offline listing-quality checker for Amazon & Etsy.

Validates the fields each marketplace's own docs say it reads for relevance /
eligibility, and flags the mistakes practitioners most often make. Pure stdlib,
Python 3.8+. No network, no external dependencies.

Sources encoded in the checks (see 08-ecommerce-seo/marketplace-seo.md):
  Amazon  -> S203 (sell.amazon.com/blog/amazon-seo), S204/S207 (A9 factors)
  Etsy    -> S205 (etsy.com/seller-handbook Ultimate Guide), S208 (eRank), S209 (Printify)
"""
import argparse
import re
import sys
from typing import Dict, List

# --- Published platform limits (per S203/S205/S208/S209) -------------------
AMAZON_TITLE_MAX = 200          # char guidance; Amazon truncates long titles in display
AMAZON_BACKEND_BYTES = 250      # Seller Central "Search Terms" budget (approx)
ETSY_TITLE_MAX = 140            # Etsy published title length
ETSY_TAG_MAX = 13               # Etsy allows up to 13 tags
ETSY_TAG_LEN_MAX = 20           # each tag <= 20 characters


def _tokens(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def check_amazon(title: str, bullets: str, backend: str) -> Dict[str, object]:
    """Relevance/eligibility checks for an Amazon product detail page."""
    issues = []
    title_t = _tokens(title)
    if len(title) > AMAZON_TITLE_MAX:
        issues.append(f"title length {len(title)} > {AMAZON_TITLE_MAX} chars (display truncation risk)")
    if not title_t:
        issues.append("title has no readable keywords")
    # backend search terms budget
    if len(backend.encode("utf-8")) > AMAZON_BACKEND_BYTES:
        issues.append(
            f"backend 'Search Terms' = {len(backend.encode('utf-8'))} bytes "
            f"> {AMAZON_BACKEND_BYTES} (Amazon documents ~{AMAZON_BACKEND_BYTES}-byte budget)"
        )
    # repeated keywords across title + bullets + backend = wasted budget (S204/S207)
    all_words = title_t + _tokens(bullets) + _tokens(backend)
    seen, dupes = set(), set()
    for w in all_words:
        if w in seen:
            dupes.add(w)
        seen.add(w)
    if dupes:
        issues.append(f"repeated keywords across title/bullets/backend (wasted): {sorted(dupes)}")
    # backend should not just duplicate the title verbatim
    backend_t = set(_tokens(backend))
    if backend_t and backend_t.issubset(set(title_t)):
        issues.append("backend Search Terms only repeat the title — add non-title synonyms")
    return {"issues": issues, "title_tokens": len(title_t),
            "backend_bytes": len(backend.encode("utf-8")),
            "duplicate_keywords": sorted(dupes)}


def check_etsy(title: str, tags: List[str]) -> Dict[str, object]:
    """Query-matching / relevance checks for an Etsy listing (S205/S208/S209)."""
    issues = []
    if len(title) > ETSY_TITLE_MAX:
        issues.append(f"title length {len(title)} > {ETSY_TITLE_MAX} chars")
    if len(tags) > ETSY_TAG_MAX:
        issues.append(f"{len(tags)} tags > {ETSY_TAG_MAX} allowed")
    long_tags = [t for t in tags if len(t) > ETSY_TAG_LEN_MAX]
    if long_tags:
        issues.append(f"tags exceed {ETSY_TAG_LEN_MAX} chars: {long_tags}")
    # Etsy reads BOTH title and tags for relevance (S205/S208): tags should be
    # represented in the title so the two reinforce each other.
    title_t = set(_tokens(title))
    missing_in_title = [t for t in tags if not set(_tokens(t)).issubset(title_t)]
    if missing_in_title:
        issues.append(f"tags not reflected in title (weaken query match): {missing_in_title}")
    # duplicate tags are pure waste
    lowered = [t.lower().strip() for t in tags]
    dupes = sorted({t for t in lowered if lowered.count(t) > 1})
    if dupes:
        issues.append(f"duplicate tags: {dupes}")
    return {"issues": issues, "title_len": len(title), "tag_count": len(tags),
            "duplicate_tags": dupes}


def _demo() -> int:
    amazon = check_amazon(
        title="Indestructible Dog Toys for Aggressive Chewers Heavy Duty",
        bullets="Built for power chewers. BPA-free rubber. Floats in water.",
        backend="dog toys tough chew toy puppy durable teeth training",
    )
    etsy = check_etsy(
        title="Handmade Gold Ring Dainty Stacking Band Minimalist Jewelry",
        tags=["gold ring", "stacking ring", "minimalist jewelry", "handmade ring",
              "dainty band", "gold band", "bridal jewelry", "gift for her",
              "everyday ring", "thin ring", "stackable ring", "gold jewelry",
              "minimalist ring"],
    )
    print("AMAZON CHECK:", amazon["issues"] or "OK")
    print("ETSY CHECK:", etsy["issues"] or "OK")
    return 0


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(description="Amazon/Etsy listing SEO checklist (offline).")
    p.add_argument("--demo", action="store_true", help="run with built-in sample listings")
    p.add_argument("--amazon-title", default="")
    p.add_argument("--amazon-bullets", default="")
    p.add_argument("--amazon-backend", default="")
    p.add_argument("--etsy-title", default="")
    p.add_argument("--etsy-tags", default="", help="comma-separated Etsy tags")
    args = p.parse_args(argv)

    if args.demo:
        return _demo()
    if args.amazon_title:
        print("AMAZON:", check_amazon(args.amazon_title, args.amazon_bullets,
                                       args.amazon_backend)["issues"] or "OK")
    if args.etsy_title:
        tags = [t.strip() for t in args.etsy_tags.split(",") if t.strip()]
        print("ETSY:", check_etsy(args.etsy_title, tags)["issues"] or "OK")
    if not (args.demo or args.amazon_title or args.etsy_title):
        p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
