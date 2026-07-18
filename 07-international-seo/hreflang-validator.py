#!/usr/bin/env python3
"""
hreflang-validator.py — verify a set of hreflang clusters for the
most common, Google-documented implementation errors.

Checks (all derived from Google Search Central, "Tell Google about localized
versions of your page", support.google.com/webmasters/answer/189077, and
corroborated practitioner guidance):

  1. Self-reference   : every page must list itself in its own hreflang set.
  2. Reciprocity      : if page A references B, B must reference A (return tag).
  3. Absolute URLs    : hreflang href values must be fully-qualified (http/https).
  4. Valid ISO codes  : lang part ISO 639-1 (2 lowercase), optional region
                        ISO 3166-1 alpha-2 (2 UPPERCASE), dash-separated.
  5. x-default        : presence is recommended (warning, not an error).
  6. Consistency      : every page in a cluster must carry the SAME hreflang set.

Usage:
    python3 hreflang-validator.py
Exits 0 if no errors, 1 if at least one error is found. Python 3.8+.

Data source: hreflang tags extracted from the live <head> (or sitemap/HTTP
header) of each URL. This script only validates the *relationship logic* —
it does not fetch pages. Supply the clusters you have collected.
"""

import re
import sys

# Minimal but real ISO 639-1 two-letter language codes (subset used in demos +
# the most common ones). A production tool should load the full list.
KNOWN_LANGS = {
    "en", "de", "fr", "es", "it", "pt", "nl", "ru", "zh", "ja", "ko", "pl",
    "sv", "da", "no", "fi", "tr", "ar", "cs", "hu", "ro", "th", "vi", "id",
}
# ISO 3166-1 alpha-2 region codes (subset).
KNOWN_REGIONS = {
    "us", "gb", "ca", "au", "ie", "de", "fr", "es", "it", "nl", "be", "ch",
    "at", "br", "mx", "pt", "se", "dk", "no", "fi", "pl", "jp", "kr", "cn",
    "ru", "tr", "ar", "cz", "hu", "ro", "th", "vn", "id",
}

# Special tokens allowed as a standalone value.
SPECIAL = {"x-default"}


def parse_hreflang(value: str):
    """Return canonical (lang, region) tuple, ('x-default', None), or None.

    Google treats hreflang case-insensitively, so we accept any case and
    canonicalize to lowercase-language[-UPPERCASE-region].
    """
    value = value.strip()
    if value.lower() in SPECIAL:
        return ("x-default", None)
    m = re.match(r"^([a-zA-Z]{2})(-([a-zA-Z]{2}))?$", value)
    if not m:
        return None
    lang = m.group(1).lower()
    region = m.group(3).lower() if m.group(3) else None
    if lang not in KNOWN_LANGS:
        return None
    if region and region not in KNOWN_REGIONS:
        return None
    return (lang, region)


def canonical_label(value: str):
    """Return the normalized hreflang label string for storage/comparison."""
    parsed = parse_hreflang(value)
    if parsed is None:
        return None
    lang, region = parsed
    if lang == "x-default":
        return "x-default"
    return f"{lang}-{region}" if region else lang


def validate_hreflang(clusters: dict) -> list:
    """clusters: {url: [(hreflang_value, href_url), ...], ...}"""
    issues = []

    # Build a normalized map of {url: {canonical_label: href_url}}
    norm = {}
    for url, pairs in clusters.items():
        norm[url] = {}
        for code, href in pairs:
            label = canonical_label(code)
            if label is None:
                issues.append(f"INVALID CODE: '{code}' on {url} is not a "
                              f"valid ISO 639-1/3166-1 hreflang value.")
                continue
            norm[url][label] = href
            if not href.startswith(("http://", "https://")):
                issues.append(f"RELATIVE URL: {url} uses relative href "
                              f"'{href}' for {label} (must be absolute).")

    # 1: self-reference (a page must list itself for its own language code)
    for url, mapping in norm.items():
        has_self = any(href.rstrip("/") == url.rstrip("/")
                       for lbl, href in mapping.items() if lbl != "x-default")
        if not has_self:
            issues.append(f"NO SELF-REFERENCE: {url} does not list itself in "
                          f"its hreflang set.")

    # 2: reciprocity / orphan (if A links to B, B must link back to A,
    #    possibly under A's own language code — hreflang sets are identical
    #    across the cluster, so the return edge uses A's self-label).
    for url, mapping in norm.items():
        for label, href in mapping.items():
            if label == "x-default":
                continue
            if href.rstrip("/") == url.rstrip("/"):
                continue  # self-reference, handled above
            if href not in norm:
                issues.append(f"ORPHAN TARGET: {url} -> {label} points to "
                              f"{href} which is not part of any cluster.")
                continue
            back = [l for l, h in norm[href].items()
                    if h.rstrip("/") == url.rstrip("/")]
            if not back:
                issues.append(f"MISSING RETURN TAG: {url} references "
                              f"{label} at {href}, but {href} does not link "
                              f"back to {url}. Hreflang may be ignored.")

    # 6: consistency — every page in a cluster should carry the same
    # non-x-default label set (Google expects identical sets on all pages).
    parent = {u: u for u in norm}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for url, mapping in norm.items():
        for _label, href in mapping.items():
            if href in norm:
                union(url, href)
    groups = {}
    for u in norm:
        groups.setdefault(find(u), set()).add(u)
    for members in groups.values():
        ref_set = None
        inconsistent = False
        for m in members:
            labels = frozenset(k for k in norm[m] if k != "x-default")
            if ref_set is None:
                ref_set = labels
            elif labels != ref_set:
                inconsistent = True
        if inconsistent:
            issues.append(f"INCONSISTENT SET: pages {sorted(members)} "
                          f"carry mismatched hreflang label sets; Google "
                          f"expects the identical set on every page.")

    # 5: x-default presence (warning only)
    for url in norm:
        if "x-default" not in norm[url]:
            issues.append(f"NO X-DEFAULT (warning): {url} has no x-default "
                          f"fallback for unmatched languages/regions.")
    return issues


# ---------------------------------------------------------------- demo data
if __name__ == "__main__":
    # CORRECT cluster
    correct = {
        "https://www.example.com/": [
            ("x-default", "https://www.example.com/"),
            ("en", "https://www.example.com/"),
            ("en-gb", "https://www.example.com/gb/"),
            ("en-us", "https://www.example.com/us/"),
            ("de", "https://www.example.com/de/"),
        ],
        "https://www.example.com/gb/": [
            ("x-default", "https://www.example.com/"),
            ("en", "https://www.example.com/"),
            ("en-gb", "https://www.example.com/gb/"),
            ("en-us", "https://www.example.com/us/"),
            ("de", "https://www.example.com/de/"),
        ],
        "https://www.example.com/us/": [
            ("x-default", "https://www.example.com/"),
            ("en", "https://www.example.com/"),
            ("en-gb", "https://www.example.com/gb/"),
            ("en-us", "https://www.example.com/us/"),
            ("de", "https://www.example.com/de/"),
        ],
        "https://www.example.com/de/": [
            ("x-default", "https://www.example.com/"),
            ("en", "https://www.example.com/"),
            ("en-gb", "https://www.example.com/gb/"),
            ("en-us", "https://www.example.com/us/"),
            ("de", "https://www.example.com/de/"),
        ],
    }

    # BROKEN cluster (illustrates real-world errors)
    broken = {
        "https://www.example.com/": [
            ("en", "https://www.example.com/"),
            ("en-gb", "https://www.example.com/gb/"),
            # missing self-reference for en-us, missing de, missing x-default
        ],
        "https://www.example.com/gb/": [
            ("en", "https://www.example.com/"),
            ("en-gb", "https://www.example.com/gb/"),
            ("en-us", "https://www.example.com/us/"),
        ],
        "https://www.example.com/us/": [
            ("en", "https://www.example.com/"),
            ("en-gb", "https://www.example.com/gb/"),
            # broken: points en-us at /gb/ instead of /us/ (return mismatch)
            ("en-us", "https://www.example.com/gb/"),
        ],
        "https://www.example.com/de/": [
            # relative URL (error), invalid region "UK" (error)
            ("de", "/de/"),
            ("en-uk", "https://www.example.com/"),
        ],
    }

    print("=== CORRECT cluster ===")
    ok = validate_hreflang(correct)
    print("Issues found:", len(ok))
    for i in ok:
        print("  -", i)

    print("\n=== BROKEN cluster ===")
    bad = validate_hreflang(broken)
    for i in bad:
        print("  -", i)

    # Sanity: the correct cluster must produce zero issues.
    sys.exit(1 if (bad or ok) else 0)
