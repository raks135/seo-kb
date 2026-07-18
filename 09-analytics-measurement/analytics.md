---
title: Analytics, Measurement & Reporting (GSC, GA4, rankings, attribution)
topic_id: 09-analytics-measurement/analytics
tags: [analytics, gsc, ga4, rankings, attribution, dashboards]
last_updated: 2026-07-18
confidence: robust
sources: [S28, S1, S10]
---

## TL;DR
Measure what matters: organic visibility (Search Console), on-site behavior (GA4), and business outcomes (conversions/revenue) — not vanity rankings. Connect SEO effort to revenue via event/goal tracking and avoid over-indexing on daily rank positions, which are personalized and sampled.

## Core explanation
Measurement has three layers: (1) **technical health & visibility** via Google Search Console (impressions, clicks, CTR, position, index coverage, Core Web Vitals); (2) **user behavior** via GA4 (engagement, conversions); (3) **business value** via attribution. Rank-tracking tools show approximate positions and should be a secondary diagnostic, not the headline KPI.

## Mechanics / how-to
1. **GSC:** verify property; monitor Performance (query/URL), Index Coverage, Core Web Vitals, Sitemaps (S10/S28).
2. **GA4:** configure events, conversions, and ecommerce; link to GSC for query-level landing data.
3. **Dashboards:** blend GSC + GA4 in Looker Studio (see 09 follow-up).
4. **Attribution:** use last-non-direct or data-driven; segment organic.
5. **Alerts:** set anomaly alerts on clicks/impressions for sudden drops.

## Worked example / code
GA4 purchase event (gtag):
```js
gtag('event', 'purchase', {
  transaction_id: 'T-12345',
  value: 59.00,
  currency: 'USD',
  items: [{item_id:'SKU1', item_name:'Wool Runner'}]
});
```

## Assumptions & limitations
- "(Not provided)" hides most query data in GA4; use GSC for query-level data.
- Rankings vary by location/device/personalization; a single "position" is approximate (S1).
- Correlation between metrics ≠ causation; set expectations accordingly.

## Empirical evidence
Google's GSC and GA4 documentation are first-party (S1, S28). Industry data shows organic "not provided" dominates, reinforcing GSC as the query source of truth.

## Conflicting views
- **"Track rankings as the primary KPI."** Rankings are volatile and personalized; clicks/conversions are better business signals (S1).
- **"More traffic = success."** Traffic quality (engagement, conversion) matters more than volume.

## Common mistakes
- No conversion tracking (can't prove ROI).
- Treating daily rank dips as emergencies.
- Ignoring GSC index-coverage errors.
- Mixing filtered and unfiltered data.
- Vanity-metric reporting (impressions without CTR context).

## Further reading
- S1 — Google, "SEO Starter Guide" — Tier 1
- S28 — PageSpeed Insights / Lighthouse docs — Tier 1
- S10 — web.dev, "Web Vitals" — Tier 1
