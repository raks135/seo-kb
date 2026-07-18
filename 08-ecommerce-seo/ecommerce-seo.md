---
title: E-commerce SEO (product/category pages, faceted navigation, schema, marketplaces)
topic_id: 08-ecommerce-seo/ecommerce-seo
tags: [ecommerce, product, category, faceted-navigation, schema, marketplace]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S11, S6, S4]
---

## TL;DR
E-commerce SEO optimizes category and product pages for crawlability and rich results. The hardest problems are **faceted navigation** (filter/combo URLs exploding crawl space) and **duplicate content** (same product under many URLs). Use canonicals, disciplined internal linking, and Product/Review schema for rich results.

## Core explanation
Online stores generate huge URL counts from filters, sorts, and variants. Without control, crawlers waste budget on near-duplicate facet URLs, and link equity dilutes. Product schema enables rich results (price, availability, ratings) in SERPs.

## Mechanics / how-to
1. **Architecture:** logical category → subcategory → product; breadcrumbs with `BreadcrumbList` schema (S11).
2. **Faceted nav:** allow crawling only of high-value facets; `noindex`/`robots` block or canonicalize low-value combos (S4, S5).
3. **Duplicate variants:** canonical color/size variants to a primary product URL; use `robots.txt` to limit crawl of parameter URLs.
4. **Product schema:** `Product` + `Offer` + `AggregateRating`/`Review` (S11).
5. **Sitemaps:** submit canonical product/category URLs (S6).

## Worked example / code
Product JSON-LD:
```html
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"Product",
  "name":"Wool Runner Sneakers",
  "offers":{"@type":"Offer","price":"98.00","priceCurrency":"USD","availability":"https://schema.org/InStock"},
  "aggregateRating":{"@ratingValue":"4.6","reviewCount":"312"} }
</script>
```

## Assumptions & limitations
- Schema enables eligibility for rich results; it does not guarantee them or rank (S11).
- Faceted-navigation control depends on your CMS/platform capabilities.
- Marketplace SEO (Amazon/Etsy) follows the platform's own ranking rules, not Google's (see 08 follow-up).

## Empirical evidence
Google's ecommerce structure guidance (S1) and schema.org Product spec (S11) are first-party. Crawl-waste from faceted nav is a well-known practitioner finding (Tier 2).

## Conflicting views
- **"Block all facet URLs."** Over-blocking hides valuable filter pages that rank; the art is selective allowance.
- **"More products indexed = more sales."** Indexing low-value/duplicate variants wastes crawl and can dilute.

## Common mistakes
- Infinite facet URL combinations crawled.
- Out-of-stock products returning 404 (use 200 + `OutOfStock` or 301 to category).
- Missing/incorrect product schema.
- Thin product descriptions copied from manufacturer.
- Orphaned categories (no internal links).

## Further reading
- S1 — Google, "SEO Starter Guide" (ecommerce structure) — Tier 1
- S11 — Schema.org (Product/Offer vocab) — Tier 1
- S4 — Google, "Canonicals" — Tier 1
- S6 — Google, "Sitemaps" — Tier 1
