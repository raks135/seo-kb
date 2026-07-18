---
title: Product Schema & Merchant Listings
topic_id: 08-ecommerce-seo/product-schema-merchant-listings
tags: [ecommerce, structured-data, schema.org, product, merchant-listings, rich-results, json-ld]
last_updated: 2026-07-18
confidence: robust
sources: [S47, S200, S201, S45, S53, S202]
---

## TL;DR
- `Product` structured data lets Google surface price, availability, review ratings, shipping and return details in search (product snippets, Popular Products, Shopping knowledge panels, Google Images). Google distinguishes **product snippets** (can use `offers`, `review`, or `aggregateRating`) from **merchant listings** (require a real `Offer` from the selling merchant, price > 0).
- It is a **display** mechanism, not a ranking factor — Google has repeatedly said structured data does not make a page rank better (S45, S53). Treat it as a CTR/qualification lever.
- Required for merchant-listing eligibility: `name`, `image`, and an `Offer` with a valid `price`/`priceCurrency`. Recommended properties (brand, GTIN/MPN/SKU, `aggregateRating`, `description`, `shippingDetails`, `hasMerchantReturnPolicy`) widen the experiences you can earn.
- Most failures are operational: schema drift (markup disagrees with the visible page), missing/invalid offers, fake or incentivized reviews, and JS-injected markup that Shopping crawls less often. Validate with the Rich Results Test and the GSC "Merchant listings" / "Product snippets" reports.

## Core explanation
**Product structured data** is JSON-LD (or Microdata/RDFa) using the schema.org `Product` type placed on a product detail page. It classifies the page for machines the way a title tag classifies it for humans. Google reads it and may render richer search results that show product attributes inline (price, star rating, "In stock", free-shipping badge, return window).

Google documents **two classes** of product markup, and the distinction drives what you must include (S47, S200):

1. **Product snippet** — a normal organic result upgraded with product info (price, ratings, availability). Eligible when the page carries `Product` markup with at least one of: `offers`, `review`, or `aggregateRating` (plus `name` and `image`). A merchant does **not** have to be the seller.
2. **Merchant listing** — a shopping-style experience (Popular Products carousel, Shopping knowledge panel, annotated Google Images). Eligible only when the merchant is the seller, which is why Google **requires an `Offer`** with `price` > 0 and a `priceCurrency` (S200). Product snippets accept an `Offer` *or* `AggregateOffer`; merchant listings require an `Offer`.

The key mental model: **merchant listings = "I sell this, here is the live price/stock"; product snippets = "here is structured info about this product."** Providing the required merchant-listing properties also makes the page eligible for product snippets, so the two overlap (S47).

Structured data is **one input among many**. Google can even generate product results without markup by extracting on-page signals, but that cedes control and is error-prone (e.g., it may pick a membership price or a blog-page price) — so adding explicit markup is the reliable path (S202).

## Mechanics / how-to
### 1. Required vs recommended properties (merchant listings)
Required `Product` properties (S200):
- `name` — product name.
- `image` — crawlable/indexable product photo(s); multiple aspect ratios (1x1, 4x3, 16x9) recommended, min ~50K pixels.
- `offers` — a nested `Offer` (not `AggregateOffer`) because the merchant must be the seller.

Required `Offer` properties (S200):
- `price` (or `priceSpecification.price`) — **must be > 0** for merchant listings.
- `priceCurrency` (or `priceSpecification.priceCurrency`) — ISO 4217 three-letter code.

Recommended `Product` properties that unlock more enhancements (S200): `brand.name`, `description`, `gtin`/`gtin13`/`gtin14`/`mpn`/`sku` (global/merchant identifiers), `aggregateRating`, `review`, `color`, `size`, `material`, `category`, `inProductGroupWithID`/`isVariantOf` (variants), `hasCertification`.

Recommended `Offer` properties: `availability`, `itemCondition`, `priceValidUntil` (listing may drop if this is in the past), `url`, `shippingDetails`, `hasMerchantReturnPolicy`.

### 2. Aggregated ratings — the rules that get people penalized
If you add `aggregateRating`, follow the Review snippet guidelines (S45): supply the average `ratingValue` **and** `ratingCount`/`reviewCount` (and `bestRating`/`worrostRating` where relevant). Incentivized, self-serving, or fabricated ratings violate Google's structured-data policies and can trigger a **manual action** that removes rich-result eligibility (the page can still rank) (S45). Reviews must reflect genuine experiences — see the review-acquisition guidance in `06-local-seo/review-acquisition-management.md`.

### 3. Return & shipping policies
Two ways to provide returns (S201):
- **Per-offer** `hasMerchantReturnPolicy` nested in the `Offer` (good for product-specific policies).
- **Site-wide** `MerchantReturnPolicy` nested under `Organization` via `hasMerchantReturnPolicy` (good for one policy covering most products).

A return policy markup needs **either** `applicableCountry` (ISO 3166-1 alpha-2, up to 50 countries) **or** a `merchantReturnLink` to your policy page; if the window is finite you also need `merchantReturnDays` (S201). Shipping uses `shippingDetails` → `OfferShippingDetails` with `shippingRate` + `shippingDestination`.

### 4. Variants (size/color)
Mark each variant on its **own URL** with `Product` markup, linking them via `isVariantOf` (a `ProductGroup`) and/or `inProductGroupWithID` (the feed "item group id") (S200). Google supports pages focused on a single product **or** multiple variants of the same product; a category/listing page is not eligible (S200).

### 5. Delivery & validation loop
1. Add JSON-LD to the server-rendered HTML (preferred; JS-injected Product markup makes Shopping crawls "less frequent and less reliable," risky for fast-changing price/stock) (S200).
2. Validate with the **Rich Results Test**; fix critical errors.
3. Deploy a few pages, test with **URL Inspection**, ensure the page is not blocked by `robots.txt`/`noindex`/login.
4. Submit/keep a sitemap; monitor the **Merchant listings** and **Product snippets** enhancement reports in GSC (S202). GSC reports show *valid*, *valid with warnings* (could be enhanced), and *invalid* (not eligible) items.

## Worked example / code
A complete `Product` + `Offer` with brand, identifiers, aggregate rating, shipping, and an offer-level return policy, paraphrased from Google's documented example (S200, S201):

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "sku": "trinket-12345",
  "gtin14": "00012345600012",
  "image": [
    "https://example.com/photos/16x9/trinket.jpg",
    "https://example.com/photos/4x3/trinket.jpg",
    "https://example.com/photos/1x1/trinket.jpg"
  ],
  "name": "Nice trinket",
  "description": "Trinket with clean lines.",
  "brand": { "@type": "Brand", "name": "MyBrand" },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.4",
    "reviewCount": "89"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/trinket_offer",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "CHF",
    "price": "39.99",
    "priceValidUntil": "2026-12-31",
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": { "@type": "MonetaryAmount", "value": "3.49", "currency": "CHF" },
      "shippingDestination": [{ "@type": "DefinedRegion", "addressCountry": "CH" }]
    },
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "CH",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 60,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/ReturnShippingFees",
      "returnShippingFeesAmount": { "@type": "MonetaryAmount", "value": "3.49", "currency": "CHF" }
    }
  }
}
```

**Reproducible validator** (stdlib only, Python 3.8+). It checks the required merchant-listing properties and flags a common rating mistake. Pin: Python 3.8+, no third-party deps.

```python
import json, sys

def validate_product(data: dict) -> list:
    """Return a list of human-readable issues for a Product JSON-LD dict."""
    issues = []
    if data.get("@type") not in ("Product", ["Product"]):
        issues.append("Root @type is not 'Product'")
    for req in ("name", "image"):
        if req not in data or not data.get(req):
            issues.append(f"Product missing required '{req}'")
    offer = data.get("offers")
    if not isinstance(offer, dict):
        issues.append("Merchant listings require an 'offers' Offer object (not AggregateOffer)")
    elif offer.get("@type") == "AggregateOffer":
        issues.append("Merchant listings require a single 'Offer' object, not 'AggregateOffer'")
    else:
        ps = offer.get("priceSpecification") or {}
        price = offer.get("price")
        if price is None:
            price = ps.get("price")
        curr = offer.get("priceCurrency")
        if curr is None:
            curr = ps.get("priceCurrency")
        if price is None:
            issues.append("Offer missing required 'price' (or priceSpecification.price)")
        elif isinstance(price, (int, float)) and price <= 0:
            issues.append("Merchant listings require price > 0")
        if not curr:
            issues.append("Offer missing required 'priceCurrency'")
    ar = data.get("aggregateRating")
    if isinstance(ar, dict) and "ratingCount" not in ar and "reviewCount" not in ar:
        issues.append("aggregateRating present but missing ratingCount/reviewCount (will be ignored/invalid)")
    return issues

if __name__ == "__main__":
    blob = json.load(sys.stdin)
    # Accept either a raw Product node or {"@graph":[...]} / {"@context":..., "@type":"Product", ...}
    node = blob
    if isinstance(blob, dict) and "@graph" in blob:
        node = next((n for n in blob["@graph"] if n.get("@type") == "Product"), {})
    found = validate_product(node)
    print("OK" if not found else "ISSUES:\n- " + "\n- ".join(found))
```

Save as `validate_product.py`, run `python3 validate_product.py < product.json`. Data source: your own rendered JSON-LD (paste from the page's view-source or a rendered-HTML fetch).

## Assumptions & limitations
- **Not a ranking factor.** Structured data changes *how* a result looks, not *whether* it ranks (S45, S53). Any "product schema boosts rankings" claim is folklore.
- **Display is not guaranteed.** Google shows rich results "at its discretion" and may change experiences over time; providing more properties only increases *eligibility* (S47, S200).
- **Markup must match the visible page.** Google may verify merchant-listing data against the page; drift (stale price, wrong stock) hurts eligibility and can draw a manual action (S45, S202).
- **Server-rendered preferred.** JS-injected `Product` markup is explicitly noted to make Shopping crawls less frequent/unreliable — a real risk for price/availability that changes often (S200).
- **Merchant Center feed synergy.** You can provide product data via on-page structured data, a Merchant Center feed, or both; providing both maximizes eligibility and lets Google cross-check (e.g., it may use feed pricing when markup lacks it) (S47). Search Console return-policy settings override on-page markup (S201).
- **Single-product focus.** Only pages about one product (or its variants) are eligible; category/listing pages are not (S200).

## Empirical evidence
- Google's own documentation is the primary, authoritative source for property requirements and the snippet-vs-merchant-listing split (S47, S200, S201). This is first-party spec, not a correlation study.
- Schema App's practitioner write-up (S202) documents real-world failure modes observed across client sites: Google awarding product results to the wrong page/price when markup is absent ("schema drift"), and GSC enhancement reports splitting items into valid / valid-with-warnings / invalid. This is practitioner evidence (n not stated), directional rather than controlled.
- No published study quantifies a CTR lift from product rich results that is attributable to markup alone (confounded by price, ratings, brand). Treat any "% CTR uplift from product schema" vendor figure as unverified.

## Conflicting views
- **"Merchant listings require structured data" vs "Google shows them from the feed."** Both are true: merchant-listing experiences can be powered by on-page `Product` markup *or* a Google Merchant Center feed (or both) (S47). If you run free/product listings in Merchant Center, keep that feed accurate even if you also use markup.
- **"Add markup to every page" vs "only where it helps."** Google recommends focusing markup on product detail pages, not category/listing pages (S200). Adding `Product` to a category page is ineligible and wasteful.
- **Markup as a ranking lever.** Practitioner marketing sometimes implies schema "helps rankings"; Google is explicit it does not (S45, S53). This article treats display/CTR as the real benefit.

## Common mistakes
1. **Schema drift** — markup shows a price/stock/rating that no longer matches the page (often from manual edits that skip the JSON-LD). Cause of inaccurate rich results and manual-action risk (S202, S45).
2. **Missing or zero-price Offer** — merchant listings require `offers` with `price` > 0; without it you fall back to (at best) a product snippet (S200).
3. **Fake or incentivized reviews / ratings** — violates spam policies; can trigger a structured-data manual action. Never self-assert ratings you don't genuinely have (S45).
4. **`aggregateRating` without `ratingCount`/`reviewCount`** — incomplete rating markup is ignored or invalid.
5. **JS-injected Product markup** — Shopping crawls it less often, so price/availability go stale in results (S200).
6. **Putting `Product` on category/listing pages** — ineligible; only single-product (or variant-group) pages qualify (S200).
7. **Blocking the markup or images** — `robots.txt`/`noindex` on the page or non-crawlable image URLs prevents ingestion (S200).
8. **Ignoring GSC enhancement reports** — "valid with warnings" pages are missing recommended properties (brand/GTIN/returns) that would widen eligibility; "invalid" pages need fixing before they show (S202).
9. **Variant spam** — marking unrelated products as variants, or one URL for many variants without distinct variant URLs, confuses clustering and can be seen as manipulative (S200).

## Further reading
- Google, "Intro to Product structured data" (Tier 1) — S47.
- Google, "Merchant listing (`Product`, `Offer`) structured data" (Tier 1) — S200.
- Google, "Merchant return policy (`MerchantReturnPolicy`) structured data" (Tier 1) — S201.
- Google, "General structured data guidelines" (Tier 1, manual-action + no-ranking-factor) — S45.
- Search Engine Journal, "Structured data won't make a site rank better" (Tier 2, relays John Mueller) — S53.
- Schema App, "6 Common Product Rich Result Mistakes" (Tier 2) — S202.
- Related KB articles: `01-technical-seo/structured-data.md`, `08-ecommerce-seo/faceted-navigation-crawl-budget.md`, `06-local-seo/review-acquisition-management.md`.
