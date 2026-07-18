---
title: Multi-Location SEO
topic_id: 06-local-seo/multi-location-seo
tags: [local-seo, multi-location, location-pages, google-business-profile, localbusiness-schema, franchises, chains]
last_updated: 2026-07-18
confidence: robust
sources: [S161, S162, S163, S165, S166, S167, S19, S174, S175, S176, S177, S178]
---

## TL;DR
Multi-location SEO means applying single-location best practices to every branch *and* the structural work that only appears at scale: one unique landing page per location, one verified Google Business Profile per location (bulk-verifiable at ≥10), correct `LocalBusiness` schema on each page, and centralized NAP/citation hygiene. The single biggest failure mode is publishing hundreds of near-identical, template-thin "city" pages — Google treats large-scale, low-value template pages as **doorway pages** and can apply a broad ranking adjustment (S174). Each location page must carry genuinely unique, useful content.

## Core explanation
A multi-location business is any brand with more than one physical place of business — retail chains, restaurants, medical/dental practices, service-area businesses (plumbers, HVAC) with several service cities, franchises, and enterprise brands with hundreds or thousands of branches. The goal is for *each* location to have an equal chance of being discovered and chosen by the community it serves (S175).

Two ranking contexts matter, and they differ by query intent:
- **Local pack / Maps results** are governed by Google's local-ranking formula: relevance, distance, prominence. Prominence is informed by "how many websites link to your business" and by review count/ratings — but you cannot pay for or request a better local rank (S161).
- **Organic web results** for location-modified queries ("pizza near me", "personal injury lawyer boston") are governed by the normal web-ranking systems plus the strength of each location's dedicated landing page.

The hard part is **scale economics**: with dozens–thousands of locations, the temptation is to auto-generate location pages from a template, swapping only the city name. That is precisely what trips doorway/duplicate-content filters. Google's position (and the practitioner consensus) is that separate URLs per location are fine *only when each location offers something unique*; if the pages are essentially identical, signals are diluted and the pages may be treated as doorways or folded into one (S174, S178).

"Multi-location SEO" is an **SEO-practitioner framework**, not a named Google system. Google does not publish a "multi-location" tactic; its guidance is expressed through the local-ranking principle (S161), the doorway-page policy (S174), the single-listing-per-location rule (S176, S19), and the `LocalBusiness` structured-data spec (S177).

## Mechanics / how-to

### 1. Site architecture
- Use a **subfolder per location** (e.g. `/locations/boston/` or `/boston-pizza/`), not a subdomain. Subfolders keep PageRank and authority consolidated under the root domain, which already earns trust; subdomains are treated as separate hosts that must earn authority independently. (General architecture rationale covered in `01-technical-seo/site-architecture.md`.)
- Provide a **store locator / location finder** as the hub, linking to every location page with crawlable `<a href>` anchors (not JS-only).
- Each **Google Business Profile should link to its matching location landing page** (S175) — this closes the loop between the listing and the site.

### 2. One unique landing page per location
For every branch, publish a page containing at minimum:
- Accurate, complete contact info (name, address, phone, hours incl. seasonal/holiday, email, map).
- The **most specific `LocalBusiness` sub-type** possible (`Restaurant`, `DaySpa`, `HealthClub`, …) in schema.
- Unique, locally-relevant content. Miriam Ellis' checklist of differentiating elements (S175) is a good minimum bar: location-specific photos/staff, local inventory or menu, location-specific reviews/testimonials, local events/sponsorships/awards, localized FAQs, booking/event calendars, and unique local CTAs.

If a location genuinely shares identical info with another, consolidate into one stronger page rather than publishing near-duplicate URLs (S178). "Unique" does not mean a 400-word essay on every branch — it means *something a searcher at that location couldn't get from any other page*: the actual address, real photos, real reviews, real local inventory/hours.

### 3. One Google Business Profile per real location
- Create and verify **one listing per location that physically exists** (S19, S176). Do not create listings for service areas you don't staff, and do not keyword-stuff the business name (e.g. "Joe's Pizza — Best Pizza Boston" violates name guidelines).
- **Bulk verification** is available when you have **≥10 locations of the same business** via Business Profile Manager; the profiles "must accurately reflect the size of your business" and you may be asked for evidence if your claimed chain size doesn't match (S176). Large chains/franchises should also evaluate the **Business Profile API** for programmatic, at-scale management (S175, S176).
- **All locations must share the same primary category**; only secondary categories may differ per location. Primary-category discrepancies across branches can suppress visibility in local packs (S175).

### 4. Schema: `LocalBusiness` per location
Define each location as its own `LocalBusiness` (or sub-type) with required `name` + `address`, plus recommended `geo` (latitude/longitude at ≥5 decimal precision), `telephone`, `openingHoursSpecification`, `url`, `priceRange`, and `department` for in-store departments (S177). Put the markup on the location's own page.

### 5. Reviews, citations, links — at the location level
- Run a **review-acquisition + response program per branch**; Google's review policy bans incentives, gating, and conflict-of-interest reviews (S167). (Full playbook in `06-local-seo/review-acquisition-management.md`.)
- Build/maintain **structured citations** (Yelp, Facebook, BBB, industry indexes) and **unstructured citations** (local press, podcasts, events) per location; data aggregators (Data Axle, Neustar Localeze, Foursquare, Factual) seed NAP downstream (S165). NAP consistency feeds prominence (S162, S166).
- Earn **geo-relevant local links** per branch (S163).

## Worked example / code
**A. Per-location `LocalBusiness` JSON-LD** (required `name`/`address`; `geo` at 5-dp precision). Replace literals with each branch's data:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Pasquale's Pizza — Back Bay",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "148 W 51st St",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10019",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.76143,
    "longitude": -73.97812
  },
  "telephone": "+1-212-555-0142",
  "url": "https://example.com/locations/back-bay",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["https://schema.org/Monday","https://schema.org/Tuesday","https://schema.org/Wednesday","https://schema.org/Thursday","https://schema.org/Friday"],
      "opens": "11:00",
      "closes": "23:00"
    }
  ]
}
</script>
```
*Source: Google `LocalBusiness` structured-data spec (S177). `aggregateRating`/`review` are only recommended for sites that capture reviews about **other** businesses (S177) — i.e. not your own first-party ratings; use first-party reviews on-page as content, not as self-asserted schema, to avoid structured-data policy risk.*

**B. Reproducible generator + near-duplicate detector** (Python 3.8+, standard library only). Reads a `locations.csv` and (1) emits per-location JSON-LD, (2) flags location pages whose body text is >85% similar to another — the signature of doorway/duplicate risk.

```python
#!/usr/bin/env python3
# multi_location_seo.py  — stdlib only, Python 3.8+
import csv, json, sys, hashlib
from difflib import SequenceMatcher

def load_locations(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def localbusiness_jsonld(loc):
    return {
        "@context": "https://schema.org",
        "@type": loc.get("type", "LocalBusiness"),
        "name": loc["name"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": loc["streetAddress"],
            "addressLocality": loc["addressLocality"],
            "addressRegion": loc["addressRegion"],
            "postalCode": loc["postalCode"],
            "addressCountry": loc.get("addressCountry", "US"),
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": float(loc["latitude"]),
            "longitude": float(loc["longitude"]),
        },
        "telephone": loc["telephone"],
        "url": loc["url"],
    }

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main(path):
    locs = load_locations(path)
    # 1) emit JSON-LD per location
    for loc in locs:
        print(f"--- {loc['name']} ---")
        print(json.dumps(localbusiness_jsonld(loc), indent=2))
    # 2) flag near-duplicate body content
    bodies = {loc["name"]: loc.get("body", "") for loc in locs}
    names = list(bodies)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            s = similarity(bodies[names[i]], bodies[names[j]])
            if s > 0.85:
                print(f"DUPLICATE RISK: {names[i]} ~ {names[j]} similarity={s:.2f}",
                      file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "locations.csv")
```
*Data source: your own `locations.csv` with columns `name,type,streetAddress,addressLocality,addressRegion,postalCode,latitude,longitude,telephone,url,body`. Run: `python3 multi_location_seo.py locations.csv`. The >85% threshold is a configurable heuristic, not a Google-published cutoff.*

## Assumptions & limitations
- Google **does not publish** a "multi-location" ranking factor or any per-lever weighting; the framework is an interpretation of local-ranking (relevance/distance/prominence, S161), doorway policy (S174), and single-listing rules (S176). Treat any "% of local ranking" figure as practitioner-belief survey data, not Google-confirmed weight (see `06-local-seo/local-link-building-citations.md`).
- A strong brand can sometimes rank thin location pages on authority alone (S175) — that proves brand equity, **not** that thin pages are safe or optimal. They underperform their potential and are vulnerable if authority dips.
- Bulk verification and the Business Profile API require meeting Google's eligibility/accuracy rules; fake or inflated location counts can trigger suspension (S176, S19).
- `LocalBusiness` schema is a **rich-result/eligibility** signal, not a ranking boost; Google doesn't guarantee display (consistent with `01-technical-seo/structured-data.md`).
- `geo` latitude/longitude precision must be ≥5 decimal places or Google may ignore it (S177).

## Empirical evidence
- **Agency observation (S175):** large brands publishing low-quality, near-duplicate landing pages often still rank on brand authority, but leave reputation/ranking/revenue upside unrealized — evidence is correlational/observational, no controlled experiment.
- **Whitespark Local Search Ranking Factors (S166):** practitioner survey rates GBP signals, reviews, links, and citations as the top local-ranking inputs — opinion survey, not a measured weight.
- **BrightLocal consumer surveys (cited in `06-local-seo/review-acquisition-management.md`):** ~72% of consumers use Google for local-business info; reviews strongly influence choice — consumer behavior, supports investing in per-location reviews.
- No peer-reviewed study isolates "multi-location architecture" as an independent ranking variable; evidence is practitioner-driven (Tier 2) or first-party Google statements (Tier 1) about the underlying signals.

## Conflicting views
- **"Just spin up a page per city" vs "only if unique."** Some vendors sell auto-generated city/zip pages; Google's doorway policy (S174) and Mueller's office-hours guidance (S178) explicitly warn that identical-info pages should be consolidated. The KB side: unique-value-or-consolidate.
- **Subdomain vs subfolder for locations.** Marketing platforms sometimes default to subdomains; SEO best practice (and Google's treat-subdomains-as-separate-hosts reality) favors subfolders for authority consolidation. Conflict is tooling-default vs SEO-evidence, not a Google dispute.
- **Primary category uniformity.** Some multi-location managers set different primary categories per branch "to match what each sells"; Google expects the **same primary category across all locations** of the brand (S175). Divergence is a self-inflicted visibility risk.

## Common mistakes
1. **Doorway / near-duplicate city pages** — swapping only the city name across hundreds of template pages; Google can apply a broad ranking adjustment to large doorway campaigns (S174). Fix: unique content per page or consolidate.
2. **Keyword-stuffing the business name** in GBP ("Best Plumber NYC") — violates name guidelines and risks suspension (S19).
3. **Fake or inflated listings** — creating listings for locations that don't exist, or bulk-verifying more profiles than the real chain size, violates GBP accuracy rules (S176).
4. **Mismatched primary categories** across branches (S175).
5. **GBP → wrong/non-matching landing page** — the listing should point to that branch's page (S175).
6. **Self-asserted `aggregateRating`** for your own reviews in schema — only allowed for sites capturing reviews about *other* businesses (S177); use on-page first-party reviews as content instead.
7. **Review violations** — incentives, gating (routing only happy customers to review forms), staff reviews (S167). Covered fully in `06-local-seo/review-acquisition-management.md`.
8. **NAP inconsistency** across citations feeding prominence decay (S162, S166).
9. **Hiding locations behind a form / JS-only store locator** so Google can't crawl each location URL.

## Further reading
- Google, "An update on doorway pages" (S174, Tier 1) — https://developers.google.com/search/blog/2015/03/an-update-on-doorway-pages
- Google, "Verify Business Profiles in bulk" (S176, Tier 1) — https://support.google.com/business/answer/4490296
- Google Search Central, "Local business structured data" (S177, Tier 1) — https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google, "Tips to improve your local ranking" (S161, Tier 1) — https://support.google.com/business/answer/7091
- Google, "Guidelines for representing your business" (S19, Tier 1) — https://support.google.com/business/answer/3038177
- Search Engine Land, "Multi-Location SEO" guide, Miriam Ellis (S175, Tier 2) — https://searchengineland.com/guide/multi-location-seo
- Lumar, "How Google Deals With Duplicate Content" (Office Hours recaps, S178, Tier 2) — https://www.lumar.io/office-hours/duplicate-content
- Companion KB articles: `06-local-seo/local-seo.md`, `06-local-seo/local-link-building-citations.md`, `06-local-seo/review-acquisition-management.md`, `01-technical-seo/site-architecture.md`, `01-technical-seo/structured-data.md`.
