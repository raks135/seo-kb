#!/usr/bin/env python3
"""Pagination & filter canonicalization auditor for e-commerce category pages.

What it checks, per paginated URL:
  - self-referencing rel=canonical  (RECOMMENDED: each page canonical -> itself)
  - # fragment in the URL           (Google ignores fragments -> pagination breaks)
  - presence of rel=next/prev       (kept for a11y; Google IGNORES them for indexing)

It also emits a robots.txt Disallow block for filter/sort parameters you pass,
matching Google's "avoid indexing URLs with filters or alternative sort orders"
guidance (see pagination docs / faceted-navigation control hierarchy).

Pure stdlib. Python 3.8+. No external dependencies.
Run `--demo` to see it work without network access.

Sources behind the rules checked here:
  S195 Google pagination & incremental page loading (2025-12-10)
  S196 Google infinite-scroll search-friendly recommendations (2014-02-13)
  S197 Google dropped rel=next/prev for indexing (2019-03-21)
  S198 Semrush pagination SEO guide (2025-02-21)
  S199 Shopify pagination SEO guide
"""
import argparse
import re
import sys
import urllib.request
from urllib.parse import urlparse

# canonical may appear as rel-before-href or href-before-rel
CANON_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', re.I)
CANON_RE2 = re.compile(
    r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', re.I)
NEXT_RE = re.compile(r'rel=["\'][^"\']*\bnext\b[^"\']*["\']', re.I)
PREV_RE = re.compile(r'rel=["\'][^"\']*\bprev\b[^"\']*["\']', re.I)


def get_canonical(html: str):
    m = CANON_RE.search(html) or CANON_RE2.search(html)
    return m.group(1).rstrip('/') if m else None


def norm(url: str) -> str:
    return url.split('#')[0].rstrip('/')


def audit_url(url: str, html: str) -> dict:
    parsed = urlparse(url)
    canon = get_canonical(html)
    return {
        'url': url,
        'uses_hash_fragment': bool(parsed.fragment),
        'canonical': canon,
        'self_canonical': (canon is not None and norm(canon) == norm(url)),
        'has_rel_next': bool(NEXT_RE.search(html)),
        'has_rel_prev': bool(PREV_RE.search(html)),
    }


def robots_block(base: str, filters) -> str:
    if not filters:
        return ''
    path = urlparse(base).path or '/'
    lines = ['# Block filtered/sorted variants from indexing (Google pagination guidance)']
    for f in filters:
        lines.append('Disallow: %s*?*%s=' % (path, f))
    return '\n'.join(lines)


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0 pagination-audit/1.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode('utf-8', 'replace')


DEMO_GOOD = """<html><head>
<link rel="canonical" href="https://shop.example.com/products?page=2">
<link rel="prev" href="https://shop.example.com/products?page=1">
<link rel="next" href="https://shop.example.com/products?page=3">
</head><body>products...</body></html>"""

# Mistake A: page 2 canonicalizes to page 1 (drops deeper products from index)
DEMO_CANON_TO_P1 = """<html><head>
<link rel="canonical" href="https://shop.example.com/products">
</head><body><a href="https://shop.example.com/products?page=3">next</a></body></html>"""

# Mistake B: pagination via # fragment (Google ignores fragments -> not crawled)
DEMO_FRAGMENT = """<html><head>
<link rel="canonical" href="https://shop.example.com/products#page=3">
</head><body>products page 3...</body></html>"""


def demo():
    base = 'https://shop.example.com/products'
    print('== DEMO A: good page 2 (self-canonical + sequential links) ==')
    print(audit_url(base + '?page=2', DEMO_GOOD))
    print('\n== DEMO B: MISTAKE - page 2 canonical -> page 1 ==')
    print(audit_url(base + '?page=2', DEMO_CANON_TO_P1))
    print('\n== DEMO C: MISTAKE - # fragment pagination (Google ignores #) ==')
    print(audit_url(base + '#page=3', DEMO_FRAGMENT))
    print('\n== robots.txt block for filters color,size,order ==')
    print(robots_block(base, ['color', 'size', 'order']))


def main():
    p = argparse.ArgumentParser(description='Audit e-commerce pagination & filters.')
    p.add_argument('--base', help='Base category URL, e.g. https://site.com/shop')
    p.add_argument('--pages', type=int, default=1, help='Number of paginated pages')
    p.add_argument('--filters', default='', help='Comma list of filter/sort params to block')
    p.add_argument('--demo', action='store_true', help='Run offline demo')
    args = p.parse_args()

    if args.demo:
        demo()
        return
    if not args.base:
        print('Provide --base or --demo', file=sys.stderr)
        sys.exit(1)

    filters = [f.strip() for f in args.filters.split(',') if f.strip()]
    for n in range(1, args.pages + 1):
        url = '%s?page=%d' % (args.base.rstrip('/'), n)
        try:
            html = fetch(url)
        except Exception as e:  # noqa: BLE001 - report and continue
            print({'url': url, 'error': str(e)})
            continue
        print(audit_url(url, html))

    block = robots_block(args.base, filters)
    if block:
        print('\n' + block)


if __name__ == '__main__':
    main()
