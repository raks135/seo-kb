---
title: Structured Data, Schema.org & Rich Results
topic_id: 01-technical-seo/structured-data
tags: [structured-data, schema-org, json-ld, rich-results, microdata, rdfa, knowledge-graph, validation]
last_updated: 2026-07-18
confidence: robust
sources: [S44, S45, S46, S47, S48, S49, S50, S51, S52, S53]
---

## TL;DR
- **Structured data** is a standardized, machine-readable label you add to a page so search engines (and other systems) understand *what the content is* — a recipe, product, event, article — not just the raw text. Google and Bing use it mainly to power **rich results** (enhanced SERP features).
- **Schema.org** is the shared vocabulary (founded by Google, Microsoft, Yahoo, Yandex; as of 2024 used by 45M+ domains with 450B+ objects). **JSON-LD** is Google's recommended encoding format, though Microdata and RDFa are also supported (S44, S51).
- **Crucial scope limit:** structured data is **not** a ranking factor. Google's John Mueller has repeatedly stated it "won't make your site rank better" — it is used purely to display the search features in Google's structured-data gallery. A structured-data manual action removes rich-result eligibility but does **not** change how the page ranks (S45, S53).
- Validate with the **Rich Results Test** (Google-feature specific) and the **Schema Markup Validator** (generic schema.org syntax). Google does **not** guarantee a rich result will appear even when markup validates (S44, S45).

## Core explanation
**Plain language.** A normal web page is written for humans: headings, paragraphs, images. Search engines can read that text but must *infer* what it means ("is this a product for sale, or a review of one?"). Structured data adds explicit, standardized labels ("this block is the product name, this number is the price, this is the average rating") so machines don't have to guess. When Google trusts the markup and the page is eligible, it can show a **rich result** — a search listing with extra visual elements (star ratings, prices, images, breadcrumbs, event dates) instead of a plain blue link.

**Precise.** Structured data is typically embedded in the page HTML and describes the page's own content (Google cautions against creating empty pages just to hold markup, or marking up content that isn't visible to users) (S44). The vocabulary is **schema.org**, a community-maintained set of types (e.g., `Product`, `Article`, `Event`, `Organization`, `BreadcrumbList`) and properties. Search engines use markup both to understand page content and to gather information about entities in the world (people, books, companies) (S44). For a given feature, Google documents which schema.org properties are **required** (needed for eligibility) and **recommended** (increase the chance of enhanced display). Providing a few complete, accurate recommended properties beats stuffing many incomplete/inaccurate ones (S44).

## Mechanics / how-to

### 1. Choose the encoding format (JSON-LD recommended)
Google supports three formats and treats them equally **as long as the markup is valid**; it recommends JSON-LD because it sits in a `<script>` tag, is not interleaved with visible text, handles nested items cleanly, and — importantly — **can be read when dynamically injected** by JavaScript (S44).
- **JSON-LD** (recommended): `<script type="application/ld+json">` in `<head>` or `<body>`.
- **Microdata**: HTML tag attributes within `<body>`.
- **RDFa**: HTML5 extension using tag attributes in `<head>`/`<body>`.

> Note: follow the Google Search Central documentation as *definitive* for Google behavior, not schema.org — Google uses a subset of schema.org and adds its own required/recommended properties (S44).

### 2. Pick the feature(s) your page qualifies for
Walk the supported-feature gallery and implement only types that genuinely represent the visible content (S46). Common, broadly useful types:
- **Article / NewsArticle / BlogPosting** — better title/image/date handling (no *required* properties; recommended: `headline`, `image`, `datePublished`, `dateModified`, `author`) (S48).
- **Product** — price, availability, review ratings, shopping knowledge panels (S47).
- **Organization** (or a specific subtype like `OnlineStore`, `LocalBusiness`) — logo, knowledge panel, merchant details (S50).
- **BreadcrumbList** — breadcrumb path in the result (S49).
- Others: Event, Recipe, Review snippet, Video, FAQPage (now restricted — see below), LocalBusiness, JobPosting, Dataset, Course, Q&A, etc. (S46).

### 3. Build → test → deploy → monitor
1. **Build** the JSON-LD for the page's real content (see examples below).
2. **Test during development** with the **Rich Results Test** (google.com/test/rich-results) and the **Schema Markup Validator** (validator.schema.org). The Rich Results Test shows which Google features can be generated and lets you preview them; the Schema Markup Validator checks generic schema.org syntax (S44).
3. **Deploy** and then monitor the **Rich result status reports** in Search Console, which can break after deployment due to templating/serving issues (S44).
4. **Don't block** the markup from Googlebot via `robots.txt`, `noindex`, or other access controls — otherwise it can't be read (S45).

### 4. Multiple items on a page
A page can carry several topically-relevant items (e.g., a `Recipe` plus `Video` plus `BreadcrumbList`). You may **nest** them (e.g., `aggregateRating` and `video` inside `Recipe`) or list them as **individual** items. Each topically-relevant item gives Google a fuller picture and more potential features (S45).

## Worked example / code

**Product snippet (JSON-LD)** — eligibility for product rich results (price, rating, availability). Data source: your own product database / feed. Syntax follows Google's Product structured-data spec (S47).
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Acme Wireless Headphones",
  "image": [
    "https://example.com/photos/headphones-1x1.jpg",
    "https://example.com/photos/headphones-4x3.jpg",
    "https://example.com/photos/headphones-16x9.jpg"
  ],
  "description": "Over-ear noise-cancelling wireless headphones with 30-hour battery.",
  "brand": { "@type": "Brand", "name": "Acme" },
  "sku": "ACM-WH-001",
  "mpn": "ACMWH001",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "reviewCount": "214"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/headphones",
    "priceCurrency": "USD",
    "price": "129.99",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```

**Article (JSON-LD)** — based on Google's Article spec; `author` uses a `Person` with a `url` to disambiguate the writer (S48).
```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "Concise, non-clickbait headline",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "datePublished": "2026-07-18T08:00:00+00:00",
  "dateModified": "2026-07-18T09:30:00+00:00",
  "author": { "@type": "Person", "name": "Willow Lane", "url": "https://example.com/staff/willow_lane" },
  "publisher": {
    "@type": "Organization",
    "name": "Example News",
    "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" }
  }
}
```

**BreadcrumbList (JSON-LD)** — `position` is 1-indexed; `item` is the trail URL (S49).
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home",        "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Books",       "item": "https://example.com/books" },
    { "@type": "ListItem", "position": 3, "name": "Science Fiction", "item": "https://example.com/books/scifi" }
  ]
}
```

**Organization (JSON-LD)** — place on the home page or an "about us" page; use the most specific subtype (e.g., `OnlineStore` for e-commerce) and nest merchant return/shipping policies (S50).
```json
{
  "@context": "https://schema.org",
  "@type": "OnlineStore",
  "name": "Example Store",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://www.facebook.com/example",
    "https://www.instagram.com/example"
  ],
  "hasMerchantReturnPolicy": {
    "@type": "MerchantReturnPolicy",
    "applicableCountry": "US",
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 30,
    "returnMethod": "https://schema.org/ReturnByMail"
  }
}
```
> Versions: schema.org is at **v30.0** (released 2026-03-19) at time of writing (S51). Google's structured-data feature specs are versioned via the docs "Last updated" dates (e.g., Product/Article last updated 2025-12-10; Organization 2026-04-15). Re-verify against the live docs before shipping, because feature support changes (see FAQ below).

## Assumptions & limitations
- **Valid ≠ guaranteed display.** Google explicitly states it does *not* guarantee a rich result will show, even with passing Rich Results Test markup. Reasons include quality review, query/page relevance, and feature availability (S45).
- **Not a ranking signal.** Structured data does not improve web-search ranking. A structured-data manual action only strips rich-result eligibility; it does not affect ranking (S45, S53).
- **Must reflect visible content.** Quality guidelines require the markup to be a true representation of the page; marking up invisible or irrelevant data can be treated as spam (S45).
- **Access required.** Blocking the page or its markup via `robots.txt`/`noindex` prevents Google from using it (S45).
- **Feature churn.** Google adds, restricts, and retires rich-result types (FAQ/HowTo in 2023; see below). Code that was eligible last year may not be today — monitor the Search Console enhancement reports and the docs "Last updated" stamps.
- **Schema.org vs Google subset.** schema.org has many more types/properties than Google uses; extra properties may help other platforms but won't necessarily trigger a Google feature (S44).

## Empirical evidence
- **Eligibility mechanism:** First-party Google documentation confirms structured data powers the listed rich results and that the Rich Results Test + status reports are the official validation/monitoring path (S44, S45, S46) — this is documented product behavior, not a correlation claim.
- **No ranking effect:** Google's Search Advocate John Mueller has stated multiple times (Bluesky, cited by Search Engine Journal and Search Engine Roundtable) that there is "no generic ranking boost" and "structured data won't make your site rank better"; the sd-policies page confirms a manual action does not change ranking (S45, S53). This is a direct Google statement, not a correlational inference.
- **Adoption scale:** Schema.org reports 45M+ domains and 450B+ objects as of 2024 — evidence of broad ecosystem adoption, not of ranking benefit (S51).
- **CTR / traffic effect:** Google says rich results "might encourage [users] to interact more" with your site — a plausible CTR mechanism, but Google has published **no quantified uplift**, and any before/after traffic change is confounded by seasonality and other edits. Treat "rich results increase CTR" as **emerging/plausible, not proven**; measure with a controlled before/after test on a few pages as Google recommends (S44). *See Verify task — quantify with a dated case study, not anecdote.*

## Conflicting views
- **"Structured data boosts rankings" vs "it doesn't."** This is the single most common myth. Vendors sometimes imply markup is a ranking lever. Google's own statements are unambiguous: no ranking boost; rich results only (S45, S53). **Label any "structured data = ranking factor" claim as folklore/contested.**
- **"JSON-LD is required" vs "any format works."** Some guides insist JSON-LD is mandatory. Google says all three formats are acceptable and equal *if valid*; it merely *recommends* JSON-LD for ease of implementation and JS injection (S44). Use JSON-LD as the default, but don't fear Microdata/RDFa.
- **"FAQ schema always shows a dropdown."** Since August 2023, FAQ rich results appear **only for well-known, authoritative government and health websites**; for all other sites they no longer show regularly (S52). Some 2026 reports claim FAQ rich results are being removed entirely — treat that as **unverified/emerge;** the confirmed fact is the 2023 restriction (S52). *See Verify task.*
- **"Schema is required for AI Overviews / generative search."** A popular 2024–2026 claim is that JSON-LD is needed to appear in AI Overviews. Google has **not** confirmed structured data is required for AI-generated answers; it helps machines understand content but is not a documented gate for generative features. **Treat as emerging/contested** until Google publishes specifics.

## Common mistakes
- **Blocking markup from crawlers** — `noindex` or `robots.txt` disallow on the page or the JSON-LD's referenced resources; Google can't read what it can't fetch (S45).
- **Marking up hidden or irrelevant content** — e.g., fake reviews, ratings not on the page, or content that doesn't exist for the user. This violates quality guidelines and can trigger a **structured-data manual action** (rich-result eligibility removed) or be flagged as spam (S45).
- **Fake or self-serving ratings** — `AggregateRating`/`Review` must reflect real, on-page user ratings; invented or incentivized-only ratings are a classic spam pattern (S45).
- **FAQ abuse post-2023** — adding `FAQPage` markup expecting a dropdown on a normal commercial/blog site; since 2023 it won't show for non-gov/health sites, and Google notes unused markup "has no visible effects" — don't expect a SERP change (S52).
- **Over-stuffing recommended properties** — providing many incomplete/inaccurate recommended fields instead of a few complete, accurate ones reduces quality (S44).
- **Wrong entity type** — using `Organization` for a person, or a generic type when a specific subtype (e.g., `OnlineStore`, `LocalBusiness`) applies; specific subtypes aid disambiguation (S50).
- **Assuming validation = appearance** — passing the Rich Results Test is necessary but not sufficient; monitor the live enhancement reports (S44, S45).
- **One-off, unmonitored deployment** — templating or CMS changes can silently break markup after launch; wire the status reports into monitoring (S44).

## Further reading
- **[Tier 1]** Google Search Central, "Introduction to structured data markup in Google Search" — https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data (S44)
- **[Tier 1]** Google Search Central, "General structured data guidelines" (technical + quality; manual actions) — https://developers.google.com/search/docs/appearance/structured-data/sd-policies (S45)
- **[Tier 1]** Google Search Central, "Structured Data Markup that Google Search Supports" (full feature gallery) — https://developers.google.com/search/docs/appearance/structured-data/search-gallery (S46)
- **[Tier 1]** Google Search Central, "Product structured data" — https://developers.google.com/search/docs/appearance/structured-data/product (S47)
- **[Tier 1]** Google Search Central, "Article structured data" — https://developers.google.com/search/docs/appearance/structured-data/article (S48)
- **[Tier 1]** Google Search Central, "Breadcrumb structured data" — https://developers.google.com/search/docs/appearance/structured-data/breadcrumb (S49)
- **[Tier 1]** Google Search Central, "Organization structured data" — https://developers.google.com/search/docs/appearance/structured-data/organization (S50)
- **[Tier 1]** Schema.org (vocabulary, history, validator; ~45M domains / 450B objects as of 2024; v30.0) — https://schema.org (S51)
- **[Tier 1]** Google Search Central Blog, "Changes to HowTo and FAQ rich results" (Aug 2023) — https://developers.google.com/search/blog/2023/08/howto-faq-changes (S52)
- **[Tier 2]** Search Engine Journal, "Google Confirms That Structured Data Won't Make A Site Rank Better" (Mueller quote) — https://www.searchenginejournal.com/google-confirms-that-structured-data-wont-make-a-site-rank-better/544433 (S53)
- **[Tier 1]** Rich Results Test — https://search.google.com/test/rich-results
- **[Tier 1]** Schema Markup Validator — https://validator.schema.org/
