---
title: Setting Up GA4 + GSC + Looker Studio SEO Dashboards
topic_id: 09-analytics-measurement/ga4-gsc-looker-studio-dashboards
tags: [analytics, ga4, google-search-console, looker-studio, dashboards, measurement]
last_updated: 2026-07-18
confidence: robust
sources: [S210, S211, S212, S213, S214, S6, S215, S216, S217, S218]
---

## TL;DR
- Google Analytics 4 (GA4) measures what users **do on your site** (sessions, engagement, conversions); Google Search Console (GSC) measures how you **perform in Google Search** (impressions, clicks, CTR, queries). They answer different questions and will **never match row-for-row** — that is expected, not a tracking bug.
- Core setup: create a GA4 property + web data stream (gtag.js), verify GSC ownership, submit a sitemap, then link the two and visualize both in **Looker Studio** using Google's official template.
- Two hard limits: GA4 **hides low-volume rows behind data thresholds** (privacy) and does **not expose organic search keywords** (use GSC for queries); and you must **never send PII** to GA4.
- Treat GSC as the **source of truth for search performance** and GA4 as the **source of truth for on-site behavior**; blend them only to explain trends, not to force a match.

## Core explanation
**Plain language.** Think of your SEO reporting as two cameras pointed at the same visitor. Camera A (GSC) sits *outside* your site and watches people pass by your listing in Google Search — how many saw it (impressions), how many clicked (clicks), and the click-through rate. Camera B (GA4) sits *inside* your site and watches what each visitor does after landing — how many pages they viewed, whether they engaged for more than 10 seconds, and whether they converted. Looker Studio is the free tool that puts both camera feeds on one screen so you can see "we got 1,500 clicks from Search and 1,200 of those became sessions, of which 62% engaged."

**Precise.** GA4 is Google's event-based analytics property (it replaced Universal Analytics, which stopped processing data on July 1, 2023) [S210]. It collects interactions via a `gtag.js` tag or Google Tag Manager and models key events (conversions) [S211]. GSC is a verified-owner tool that reports Google's own search telemetry for your property, independent of any on-site tag [S214]. Looker Studio (formerly Data Studio) is Google's free BI layer with **native connectors** for both GA4 and Search Console, letting you blend them on a shared dimension such as landing-page URL [S215] [S217] [S218]. Google's official guide explicitly states the "source of truth for Search performance will always be Search Console, while the source of truth for behavior inside your site will be Google Analytics" [S217].

## Mechanics / how-to

### 1. Set up GA4 (behavior tracking)
1. Create a GA4 **account** and **property** (Editor role required) [S211].
2. Add a **web data stream**; GA4 gives you a `G-` tag ID.
3. Install the tag: paste `gtag.js` immediately after `<head>` on every page, or use your CMS's native GA4 field, or deploy via Google Tag Manager [S211].
4. Turn on **Enhanced Measurement** (page views, site search, outbound clicks, file downloads) and define **key events** (conversions) — an engaged session is one with a key event, >10s duration, or ≥2 pageviews [S210] [S217].
5. If you serve EU/consent-gated traffic, configure **Consent Mode** so modeled data fills gaps where users opt out [S210].

### 2. Set up GSC (search performance)
1. **Add a property.** Prefer a **Domain property** (verifies at the DNS level and covers all protocols/subdomains); otherwise use a URL-prefix property [S214].
2. **Verify ownership** via one of: HTML file upload, HTML `<meta>` tag, Google Analytics tag, Google Tag Manager, or DNS TXT record. Add a backup method so you don't lose access if one token breaks [S214].
3. **Submit your sitemap** (XML/RSS/Atom/text) under *Sitemaps*. Use fully-qualified absolute URLs, UTF-8, ≤50MB and ≤50,000 URLs per file (split + use a sitemap index for larger sites). Sitemaps are a **hint**, not a guarantee Google will crawl or index [S6].
4. Review **Performance** (queries, pages, countries, devices, search types) and **Index Coverage / Page Indexing** weekly.

### 3. Link GA4 ↔ GSC
In GA4 **Admin → Product links → Search Console**, link a web data stream to a Search Console property. Requires **Editor** on the GA4 property **and verified-owner** status on GSC [S216]. This surfaces two GSC reports inside GA4 (Queries, Landing pages); data appears **48 hours** after collection and is capped at **16 months** of history [S216]. Note: these in-product reports don't support time-series charts and are themselves subject to thresholds — Looker Studio is the better viz layer.

### 4. Build the Looker Studio dashboard
Use Google's official **GA4 + Search Console organic-traffic template** [S217]. It auto-connects both connectors and shows GA4 data in **orange** and Search Console data in **blue**. Five headline metrics: **Sessions** (GA4), **Engagement rate** (GA4), **Returning users** (GA4), **Clicks** (GSC), and **CTR** (GSC) [S217]. The GA4 data is pre-filtered to `Session source = google` AND `Session medium = organic` so you compare like-for-like [S217]. Copy the template, re-point the data sources to your own property, and add charts: traffic-over-time, top pages by clicks/CTR, top queries, top countries.

### 5. Blend for deeper analysis
For page-level diagnosis, blend the two datasets on the **landing-page URL** (manual CSV join, or a Looker Studio blended data source). The companion `ga4_gsc_blend.py` does exactly this with stdlib Python (see below).

## Worked example / code

**GA4 tag (gtag.js)** — place once per page, right after `<head>` [S211]:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX');
</script>
```

**Blend GA4 + GSC exports (stdlib Python 3.8+, no external deps).** Export the GA4 "Pages and screens"/"Landing page" report and the GSC "Landing pages" report to CSV, then:

```bash
python3 ga4_gsc_blend.py ga4.csv gsc.csv   # or: python3 ga4_gsc_blend.py --demo
```

The script normalizes URLs (scheme-insensitive, no trailing slash) and inner/outer-joins on the landing page, printing Sessions, Clicks, CTR, Engagement, and a **Clicks/Sessions ratio** that makes the GA4-vs-GSC gap visible. Sample `--demo` output:

```
URL                                         Sessions   Clicks   CTR%   Eng%    C/S
------------------------------------------------------------------------------------
/                                               1200     1500    6.8   62.0   1.25
/blog/seo-dashboards                             540      610    6.2   71.0   1.13
https://example.com/about                          -       90    6.0      -      -
/pricing                                         310        -      -   44.0      -
```

Note `/about` exists only in GSC (no GA4 session captured — e.g. tracking blocked) and `/pricing` only in GA4 — exactly the kind of asymmetry Google documents [S217].

**Official template link:** `https://lookerstudio.google.com/reporting/408e669d-07d1-4353-a1dc-94f06bde27ef` (referenced by Google's merge guide, S217).

## Assumptions & limitations
- **Thresholds hide data.** GA4 applies privacy **data thresholds** that *remove entire rows* (not just approximate them) when user/event counts are too low — including any row containing **search-query information** [S212]. Workarounds: widen the date range, or export to **BigQuery** (note BigQuery event counts may still differ from the UI) [S212].
- **No keywords in GA4.** GA4 does not expose organic search query strings; GSC is the only first-party source for queries [S217] [S216]. (The in-product GA4↔GSC Queries report is also threshold-limited.)
- **The numbers won't match — by design.** Google lists the causes of clicks-vs-sessions gaps: GA4 tag implementation gaps; consent/cookie opt-outs; **timezone** (GSC is fixed to Pacific Time, GA4 is configurable); **attribution** (GSC counts every Search click, GA4 uses an attribution model); **canonical URLs** (GSC reports only the canonical, GA4 reports any URL with the tag); traffic **breakdowns** (GSC splits web/image/video/news/Discover); **non-HTML pages** (PDFs counted by GSC, often not by GA4); and **bot filtering** (GA4 auto-filters known bots, GSC does not) [S217].
- **Sitemaps are hints.** Submitting one does not guarantee crawling or indexing [S6].
- **16-month SC history.** GSC (and therefore the linked GA4 reports) holds at most 16 months [S216].
- **PII prohibition.** You must not send personally identifiable information (names, emails, phone numbers) to GA4; use data redaction / URL-parameter stripping [S213].
- **Sampling.** Standard GA4 reports and Explorations are not sampled the way old UA reports were, but the GA4 **Data API** (used by Looker Studio) is subject to quotas [S218].

## Empirical evidence
- The architecture (two complementary tools + Looker Studio blend) is Google's own published recommendation, not a third-party interpretation [S217]. Google shipped an official Looker Studio template and a dedicated Search Central guide for combining the two data sets (updated 2026-01-07) [S217].
- The documented discrepancy between clicks and sessions is described directly by Google with a checklist of nine causes [S217] — so "the numbers don't match" is a confirmed property of the system, not a misconfiguration to be fixed.
- Strength of evidence: **high** — claims rest on first-party Google documentation (Tier 1). There is no independent controlled study needed because the behavior is defined by the vendor's own processing.

## Conflicting views
- **"Make GA4 and GSC match exactly."** Some vendor walkthroughs imply the tools can be reconciled to identical totals. Google explicitly says they measure different things and only the *trend pattern* should align [S217]. Reconcile for diagnosis; do not expect equality.
- **Native vs third-party connectors.** Third-party Looker Studio connectors exist, but Google's guide and the in-product link use the **native GA4 and Search Console connectors**, which are built and supported by Looker Studio [S215] [S217] [S218]. Prefer native to avoid quota/accuracy surprises.
- **UA is dead.** Universal Analytics stopped processing data July 1, 2023; any dashboard still on UA is collecting nothing new [S210]. Migrate to GA4.

## Common mistakes
1. **Using GA4 for keyword research.** GA4 has no organic query data — go to GSC Performance [S217].
2. **Expecting Sessions == Clicks.** They differ for the nine reasons above; compare trends, not absolutes [S217].
3. **Forgetting to filter GA4 to `google / organic`** when comparing to GSC, so paid/social/direct sessions pollute the comparison [S217].
4. **Never verifying GSC ownership or forgetting the sitemap** — you then have no search-performance visibility and no crawl hint [S214] [S6].
5. **Sending PII** (e.g. email in a page path after a form submit) to GA4 — violates policy; strip it [S213].
6. **Panicking at thresholded (hidden) rows** — expand the date range or use BigQuery rather than assuming data loss [S212].
7. **Relying on the in-product GA4↔GSC reports for time series** — they don't support time-series charts; use Looker Studio [S216].
8. **Leaving the GA4 Search Console reports unpublished** — the collection is unpublished by default and must be published from the Library [S216].

## Further reading
**Tier 1 (first-party):**
- Google, "Introducing the next generation of Analytics (GA4)" — support.google.com/analytics/answer/10089681 [S210]
- Google, "Set up Analytics for a website and/or app" (data streams, tag) — support.google.com/analytics/answer/9304153 [S211]
- Google, "About data thresholds (GA4)" — support.google.com/analytics/answer/9383630 [S212]
- Google, "Best practices to avoid sending PII" — support.google.com/analytics/answer/6366371 [S213]
- Google, "Verify your site ownership" (GSC) — support.google.com/webmasters/answer/9008080 [S214]
- Google, "Build and submit a sitemap" — developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap [S6]
- Google, "Connect Search Console to Google Analytics" — support.google.com/analytics/answer/10737381 [S216]
- Google Search Central, "Using Search Console and Google Analytics data for SEO" (official Looker Studio template + discrepancy guide) — developers.google.com/search/docs/monitor-debug/google-analytics-search-console [S217]
- Google, "Connect to Search Console" (Looker Studio connector) — support.google.com/looker-studio/answer/7314895 [S215]

**Tier 2 (practitioner / implementation notes):**
- GOV.UK GA4, "Looker Studio best practice" (native GA4 connector, quotas) — docs.data-community.publishing.service.gov.uk/analysis/govuk-ga4/use-ga4/looker-studio [S218]
- Search Engine Journal, "Google Adds New Guidance For Merging GA4 & Search Console Data" — searchenginejournal.com/google-adds-new-guidance-for-merging-ga4-search-console-data/539285 (news of the S217 guide)
