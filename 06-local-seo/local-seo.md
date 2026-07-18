---
title: Local SEO (Google Business Profile, NAP, citations, reviews, local pack)
topic_id: 06-local-seo/local-seo
tags: [local, google-business-profile, nap, citations, reviews, local-pack]
last_updated: 2026-07-18
confidence: robust
sources: [S19, S20, S24]
---

## TL;DR
Local SEO helps businesses appear in the "local pack" and Maps for location-based queries. The three pillars: a complete/optimized **Google Business Profile (GBP)**, consistent **NAP** (Name-Address-Phone) citations, and a steady flow of **reviews**. Relevance, distance, and prominence drive local ranking.

## Core explanation
Google's local results blend organic web signals with GBP/geo signals. The local pack shows a map + 3 listings; ranking factors are generally grouped as **relevance** (match to query), **distance** (proximity to searcher), and **prominence** (off-page reputation: reviews, links, citations).

## Mechanics / how-to
1. **GBP:** claim/verify, complete every section, pick accurate categories, post updates, add products/services (S19).
2. **NAP consistency:** identical name/address/phone across GBP, website, and directories.
3. **Citations:** list in major directories (Yelp, Apple, Bing Places) and niche/geo directories.
4. **Reviews:** ask customers; respond to all; never incentivize positive-only reviews (against policy).
5. **Local content & pages:** location pages with unique, useful content (not duplicate templates).
6. **Local structured data:** `LocalBusiness` schema with NAP + geo + hours (S11).

## Worked example / code
`LocalBusiness` JSON-LD snippet:
```html
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"LocalBusiness",
  "name":"Acme Plumbing", "telephone":"+1-555-0100",
  "address":{"@type":"PostalAddress","streetAddress":"1 Main St","addressLocality":"Springfield","addressRegion":"IL","postalCode":"62701"},
  "geo":{"@type":"GeoCoordinates","latitude":39.78,"longitude":-89.65} }
</script>
```

## Assumptions & limitations
- Distance is uncontrollable; you can only maximize relevance/prominence.
- Review quantity/quality matters but fake or incentivized reviews violate policy (S19).
- Ranking in the local pack is distinct from organic ranking; both benefit from a strong site.

## Empirical evidence
Practitioner/local-SEO studies (S20, S24) and Google's own local guidance (S19) corroborate the relevance/distance/prominence model. Review signals are among the most-cited local ranking correlates (Tier 2).

## Conflicting views
- **"More citations = higher rank."** Consistency matters more than raw count; low-quality directories add little.
- **"Keywords in business name boost rank."** Stuffing your name with keywords violates guidelines and can be flagged (S19).

## Common mistakes
- NAP inconsistency across listings.
- Unverified or incomplete GBP.
- Duplicate GBP listings.
- Buying fake reviews.
- Thin, duplicated city pages ("doorway" risk).

## Further reading
- S19 — Google Business Profile Help & Guidelines — Tier 1
- S20 — Ahrefs Blog (local studies) — Tier 2
- S24 — Search Engine Journal (local SEO) — Tier 2
