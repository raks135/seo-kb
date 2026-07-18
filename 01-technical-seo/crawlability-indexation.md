---
title: Crawlability & Indexation (robots.txt, sitemaps, canonicals, log analysis, JS rendering)
topic_id: 01-technical-seo/crawlability-indexation
tags: [technical-seo, robots, sitemap, canonical, crawl-budget, javascript]
last_updated: 2026-07-18
confidence: robust
sources: [S2, S5, S6, S4, S3]
---

## TL;DR
Crawlability = can Googlebot reach your pages; indexation = does Google store them. Control crawling with `robots.txt`, aid discovery with XML sitemaps, and consolidate duplicates with `rel="canonical"`. For JavaScript-heavy sites, ensure Googlebot can render and execute JS. None of these guarantee indexing — they are signals, not commands.

## Core explanation
**Crawlability** is about access: Googlebot must be able to fetch the URL and its critical resources (CSS/JS). **Indexation** is about understanding and storing: Google analyzes the page and may or may not add it to the index. A page can be crawlable but not indexed (low quality, `noindex`, canonicalized away) and — rarely — indexed but not crawlable (if blocked yet linked externally).

## Mechanics / how-to
1. **robots.txt** (S5): manage crawler traffic; not a hiding mechanism.
   - A disallowed page's URL can still appear in results (linked from elsewhere) with no snippet.
   - To truly remove a page: `noindex` or password-protect.
2. **XML sitemap** (S6): a hint listing canonical URLs you want in results.
   - Limits: 50 MB uncompressed or 50,000 URLs per file; split into a sitemap index beyond that.
   - UTF-8, absolute URLs only. Submit via Search Console, API, or `Sitemap:` line in robots.txt.
3. **Canonical** (S4): pick the representative URL among duplicates.
   - Methods, strongest-first: `rel="canonical"` link, canonical HTTP header, sitemap listing, 301 redirect (for deprecated duplicates), hreflang clusters, HTTPS-over-HTTP preference.
   - Methods can stack; Google may still pick a different canonical if signals conflict.
4. **JS rendering** (S3): Googlebot renders with recent Chrome. Use the URL Inspection tool's rendered HTML to confirm content is present post-render.

## Worked example / code
Canonical link in `<head>`:
```html
<link rel="canonical" href="https://www.example.com/dresses/green-dresses" />
```
Sitemap snippet (XML):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.example.com/foo.html</loc><lastmod>2026-07-18</lastmod></url>
</urlset>
```
robots.txt blocking a script folder (use cautiously):
```
User-agent: *
Disallow: /cdn-private/
```

## Assumptions & limitations
- `robots.txt` is advisory; malicious crawlers ignore it (S5).
- Sitemaps are hints; Google may ignore URLs it deems low-value or non-canonical (S6).
- Canonical is a strong hint, not absolute — conflicting signals (e.g., differing internal links) can cause Google to choose another URL.
- Rendering lag: JS content may be indexed later than static HTML.

## Empirical evidence
Google's first-party docs (S2, S4, S5, S6) define the contract. Log-file analyses by SEO tool vendors (Screaming Frog, Botify-style studies) show crawl frequency correlates with site authority and update cadence, but these are observational, not causal.

## Conflicting views
- **"Canonical = redirect."** They differ: canonical keeps both URLs reachable; redirect sends users/SEO to one. Use redirect only when deprecating a duplicate (S4).
- **"More sitemap URLs = better crawling."** Google: only list URLs you want in results; junk in sitemaps wastes crawl attention.

## Common mistakes
- Blocking CSS/JS, breaking render.
- Using `robots.txt` to hide pages (fails if externally linked).
- Relative canonical URLs (`/page` instead of absolute) — supported but error-prone (S4).
- Forgetting `noindex` on staging that gets indexed.
- Pointing sitemaps at non-canonical or redirected URLs.

## Further reading
- S5 — Google, "Manage crawling with robots.txt" — Tier 1
- S6 — Google, "Build and submit a sitemap" — Tier 1
- S4 — Google, "Consolidate duplicate URLs with canonicals" — Tier 1
- S3 — Google, "JavaScript SEO basics" — Tier 1
- S2 — Google, "How Search works" — Tier 1
