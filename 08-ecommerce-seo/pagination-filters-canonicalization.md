---
title: Pagination, Filters & Canonicalization for E-commerce
topic_id: 08-ecommerce-seo/pagination-filters-canonicalization
tags: [ecommerce, pagination, canonical, faceted-navigation, crawlability, indexing]
last_updated: 2026-07-18
confidence: robust
sources: [S195, S196, S197, S198, S199, S4, S190, S191, S62]
---

## TL;DR
- Make every paginated page a **unique, crawlable URL** linked sequentially with plain `<a href>` tags, and give **each page a self-referencing `rel="canonical"`** (canonical points to itself — do **not** canonicalize page 2+ back to page 1).
- **Block filter/sort URLs** (`?color=red`, `?order=price`) from indexing with `noindex` or `robots.txt` — don't let them dilute crawl budget or index (S195; ties to faceted-navigation control hierarchy S190/S191).
- **`rel="next"`/`rel="prev"` is ignored for indexing** by Google since 2019 — keep it only for accessibility; Google follows pagination links on its own (S197).
- If you use **infinite scroll or "Load more"**, you MUST also expose a crawlable paginated fallback (full URLs + `pushState`/`replaceState` + a 404 on out-of-range) and a sitemap, or Google won't see the deeper items (S195/S196).

## Core explanation
**Pagination** is splitting a long list (a product category, a search-results page, a blog archive) into numbered chunks so each page loads fast and is easy to browse. It exists for two reasons: **performance** (a page with 1,000 products loads slower and hammers the server) and **UX** (users don't want to scroll a wall of items).

For SEO the question is purely about **discovery and indexing**: can Google reach every product, and does it understand how the chunks relate? The mechanics differ sharply depending on whether pagination is rendered as crawlable HTML links or triggered by JavaScript/user action.

Google's current guidance (S195, last updated 2025-12-10) is explicit that **Googlebot generally crawls URLs found in the `href` attribute of `<a>` elements** and **does not "click" buttons or trigger JavaScript functions that require user actions** to load more content. That single fact drives every recommendation below: whatever paging mechanism you choose, the content behind it has to be reachable through a normal link. Google also notes you can supplement discovery with an **XML sitemap** or a **Google Merchant Center feed** to help it find all products (S195).

On canonicalization: older SEO advice (circa 2011–2013) often told you to point all paginated pages at a single "View All" page or at page 1. That advice has been superseded. Google's own pagination doc and multiple practitioner guides now state each paginated page should carry a **self-referencing canonical** (S198/S199, both citing Google). Canonicalizing page 2 to page 1 is actively discouraged because the pages are not duplicates — page 2 contains products page 1 does not — and pointing the canonical at page 1 risks Google dropping those deeper products from the index (Mueller, via S198/S197 discussion; Shopify S199: "Google advises against using the first page of the paginated sequence as the canonical page").

## Mechanics / how-to

### 1. Make pagination crawlable (sequential `<a href>` links)
- Link each page to the **next** (and previous) page with real `<a href>` tags.
- Also link **every page back to page 1** of the collection. Google treats this as a hint that page 1 is the preferred landing page and helps concentrate signals there (S195, S199).
- If pagination is built in JavaScript, either render the links server-side or provide a pre-rendered/HTML snapshot so the crawler sees them (see `javascript-seo.md` and S195).

### 2. Canonicalize each page to itself
Add in `<head>` of every paginated URL:
```html
<!-- page 1 -->
<link rel="canonical" href="https://shop.example.com/products?page=1">
<!-- page 2 -->
<link rel="canonical" href="https://shop.example.com/products?page=2">
```
Do **not** point page 2's canonical at page 1. Self-referencing canonicals prevent Google from mistakenly folding deeper pages into page 1 and keep each chunk independently indexable (S198/S199). Note a canonical is a **hint, not a directive** — Google may pick a different canonical if the content diverges (S4/S60); this is normal and not a sign of error unless it consistently ignores a correct self-canonical.

### 3. URL structure: query params or clean paths, never fragments
- Preferred: `?page=n` (Google recommends this because it's easy to segment in Search Console) or `/page/n` (S195/S198/S199). Pick one and stay consistent.
- **Never** use `#page=n` — Google ignores URL fragments, so a fragment-based paginated URL collapses to the base page and the deeper items become undiscoverable (S195/S199).

### 4. Filter & sort URLs: keep them out of the index
Filters (`?color=red`) and alternate sort orders (`?order=price`) generate near-duplicate variants of the same list. Google's pagination doc says to **avoid indexing these** by blocking them with a `noindex` robots meta tag or discouraging crawling with `robots.txt` (S195). This is the same control hierarchy described in `faceted-navigation-crawl-budget.md`: `robots.txt` Disallow is the most effective for crawl budget (disallowed URLs aren't fetched), while `noindex` still gets crawled (S190/S191). Use `rel="canonical"` on filtered pages **only** if you intentionally want a specific filtered view indexed — generally you do not.

### 5. Infinite scroll & "Load more": add a crawlable fallback
Google's 2014 infinite-scroll guidance (still the reference) requires that, alongside the scroll UX, your CMS produces a **paginated series of component pages** with:
- **full, unique URLs** (e.g. `?page=n`) — not `#` fragments (S196);
- `pushState`/`replaceState` so the address bar and history reflect each component page (S196);
- a **404** (or redirect) when the index runs out (e.g. `?page=999`) so crawlers don't loop (S196).
"Load more" buttons have the same requirement: the button must ultimately resolve to crawlable, linked URLs, or the items behind it won't be indexed (S195/S199). Supplement with a sitemap or Merchant Center feed (S195).

### 6. View All — only for small collections
A single "View All" page is the most SEO-friendly option for **small** categories (a sale with ~20 items) but becomes slow and UX-hostile for large catalogs, which can hurt rankings via page experience (S199). For large catalogs, the self-canonical paginated approach above is preferred over the outdated "canonicalize everything to View All" pattern.

## Worked example / code

### Correct paginated page (page 2)
```html
<head>
  <link rel="canonical" href="https://shop.example.com/products?page=2">
  <!-- optional, for accessibility only; Google ignores these for indexing -->
  <link rel="prev" href="https://shop.example.com/products?page=1">
  <link rel="next" href="https://shop.example.com/products?page=3">
  <title>Running Shoes, page 2</title>
</head>
<body>
  <!-- products... -->
  <nav>
    <a href="https://shop.example.com/products?page=1">1</a>
    <a href="https://shop.example.com/products?page=2">2</a>
    <a href="https://shop.example.com/products?page=3">3</a>
    <a href="https://shop.example.com/products?page=1">First page</a>
  </nav>
</body>
```

### robots.txt for filter/sort params (generated by the auditor)
```
# Block filtered/sorted variants from indexing (Google pagination guidance)
Disallow: /products*?*color=
Disallow: /products*?*size=
Disallow: /products*?*order=
```

### Reproducible auditor (`pagination_audit.py`, stdlib, Python 3.8+)
The companion script in this folder audits each paginated URL for: a self-referencing canonical, use of a `#` fragment, and presence of `rel=next/prev`. Run it offline to see the three checks in action:

```bash
python3 pagination_audit.py --demo
```

It prints, for a good page 2, `{..., 'self_canonical': True, 'uses_hash_fragment': False}`; for the classic mistake (page 2 canonical → page 1) it shows `'self_canonical': False`; and for `#` fragment pagination it flags `'uses_hash_fragment': True`. The live mode fetches real URLs (`--base https://site.com/shop --pages 5 --filters color,size,order`). All logic is pure stdlib (`re`, `urllib.request`, `urllib.parse`) — no external dependencies, versions pinned to Python 3.8+.

## Assumptions & limitations
- **Crawlable links assumed.** Everything above assumes pagination is reachable via `<a href>`. If your pager only fires on click/scroll with no linked fallback, Google won't see deeper items regardless of canonicals (S195/S196).
- **Crawl budget only matters at scale.** Illyes (S62) notes sites with "a few thousand URLs" are "most of the time… crawled efficiently." Pagination/index-bloat problems are real for large catalogs (hundreds–thousands of paginated + filtered URLs), not for a 3-page blog (S62).
- **Self-canonical ≠ guaranteed indexing.** A self-referencing canonical tells Google "this URL is the preferred version of itself"; it does not force indexing of a thin or low-value page.
- **Canonical is a hint.** Google may choose a different canonical than the one you declare if it judges the pages divergent (S4/S60).
- **Filters blocked by robots.txt are never crawled**, so they pass no signals — that is the intended trade-off (use `noindex` instead if you need the URL fetched but not indexed; S190/S191).
- **Google changes behavior.** The rel=next/prev deprecation (2019) and the shift away from "View All" canonicalization are recent enough that legacy advice still circulates; always re-verify against current Google docs (S195).

## Empirical evidence
- **Google follows pagination links without explicit signals.** Ilya Grigorik (Google Web Performance Engineer, 2019): "Googlebot is smart enough to find your next page by looking at the links on the page, we don't need an explicit 'prev, next' signal" (quoted in S197). This is the basis for dropping rel=next/prev as an indexing factor.
- **Log evidence of link-following.** A 2019 OnCrawl/SEJ crawl-log study (S197) found pagination received *higher* crawl frequency than non-paginated pages and that Google followed the link series page-by-page — consistent with Google using the link graph to traverse pagination. Caveat: single dataset, small sample, directional only; not a controlled experiment.
- No reputable study quantifies a ranking "lift" from correct pagination; the benefit is **discoverability and avoiding index dilution**, not a direct ranking boost. Any "pagination increased traffic by X%" claim should be treated as correlation (confounded by the site improvements that usually accompany a pagination rebuild).

## Conflicting views
- **Self-canonical vs "canonical to View All / page 1."** The current consensus (S195/S198/S199) is self-referencing canonicals; the older "consolidate to one page" pattern is deprecated. A minority of practitioners still recommend `noindex` or canonical-to-page-1 for pages 2+ to "consolidate signals," but that risks hiding products and conflicts with Google's stated goal of finding *all* content (S195). Treat consolidation tactics as higher-risk and test in batches.
- **Keep or drop rel=next/prev?** Drop it for SEO (Google ignores it for indexing, S197), but Grigorik explicitly says keep it for **accessibility** reasons (screen readers, assistive tech). Keep it; it's harmless and helps users.
- **De-optimize pages 2+?** Semrush (S198) suggests giving pages 2+ generic titles/meta/H1 so they don't compete with page 1 for keywords. This is a practitioner tactic to reduce cannibalization, not a Google requirement; it's reasonable but optional.
- **Index filtered pages for long-tail?** Some retailers intentionally index a few high-value filtered pages (e.g. Zalando-style "grey t-shirts") for long-tail traffic. This is legitimate but higher-risk (near-duplicate/thin content) and should be tested, not blanket-applied (see `faceted-navigation-crawl-budget.md`).

## Common mistakes
1. **Canonicalizing page 2+ to page 1** — tells Google the deeper pages are duplicates of page 1 and can drop their unique products from the index. Use self-referencing canonicals instead.
2. **`#` fragment pagination** — Google ignores fragments, so `?page=` content behind `#page=3` is never discovered. Use query params or clean paths.
3. **Infinite scroll / "Load more" with no crawlable fallback** — Google doesn't scroll or click; deeper items stay invisible. Add paginated component pages + sitemap (S195/S196).
4. **Noindexing paginated pages** — kills internal link flow and product discovery. (Contrast: it's fine to noindex *filter/sort* URLs, but not the paginated sequence itself.)
5. **Not linking sequentially / excluding paginated URLs from the sitemap** — severs Google's path to deep products.
6. **Letting filter facets eat crawl budget** — thousands of `?color=x&size=y&order=z` combinations waste crawl on low-value URLs (S190/S191/S62). Block them (step 4 above).
7. **Treating rel=next/prev as a ranking signal** — it isn't used for indexing at all since 2019 (S197).

## Further reading
- S195 — Google Search Central, "Pagination, incremental page loading, and their impact on Google Search" (developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading) — Tier 1.
- S196 — Google Search Central Blog, "Infinite scroll search-friendly recommendations" (developers.google.com/search/blog/2014/02/infinite-scroll-search-friendly) — Tier 1.
- S197 — Search Engine Journal, "Rel=Next/Prev & SEO: Insights from Google Crawling Behavior" (searchenginejournal.com/rel-next-prev-seo-google-crawling-behavior/301389) — Tier 2 (Google dropped rel=next/prev for indexing, 2019-03-21).
- S198 — Semrush, "Pagination and SEO: A Complete Guide to Best Practices" (semrush.com/blog/pagination-seo, 2025-02-21) — Tier 2.
- S199 — Shopify, "Pagination SEO: Best Practices for Website Pagination" (shopify.com/blog/pagination-seo) — Tier 2.
- S4 — Google Search Central, "Consolidate duplicate URLs with canonicals" (canonical = hint not directive) — Tier 1.
- S190 / S191 — Google faceted-navigation docs (control hierarchy: robots.txt vs noindex vs canonical) — Tier 1.
- S62 — Google, "What Crawl Budget Means for Googlebot" (Illyes; crawl budget matters at scale) — Tier 1.
- Related KB: `08-ecommerce-seo/faceted-navigation-crawl-budget.md`, `01-technical-seo/javascript-seo.md`, `01-technical-seo/site-architecture.md`.
