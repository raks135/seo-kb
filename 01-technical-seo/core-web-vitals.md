---
title: Core Web Vitals (LCP, INP, CLS) and Field vs Lab Data
topic_id: 01-technical-seo/core-web-vitals
tags: [core-web-vitals, performance, LCP, INP, CLS, page-experience, field-data, lab-data, crux]
last_updated: 2026-07-18
confidence: robust
sources: [S10, S29, S38, S39, S40, S41, S42, S43]
---

## TL;DR
- Google's Core Web Vitals are **three** user-centric field metrics: **LCP** (load), **INP** (interactivity), and **CLS** (visual stability). A page/site passes a metric when **at least 75% of real visits** are "good."
- Good thresholds: **LCP ≤ 2.5 s**, **INP ≤ 200 ms**, **CLS ≤ 0.1**; "poor" begins at **LCP > 4.0 s**, **INP > 500 ms**, **CLS > 0.25** (S38).
- **INP replaced FID as the interactivity Core Web Vital on 12 March 2024**; FID was deprecated (S29, S39).
- Google measures these from **field data** (the Chrome User Experience Report, CrUX), *not* from lab tools like Lighthouse. Use field data for the pass/fail verdict; use lab data to diagnose *why* (S40).
- Core Web Vitals are a **page-experience ranking signal**, but Google explicitly says good scores "don't guarantee good rankings" — treat them as a tie-breaker / holistic quality signal, not a primary ranking lever (S39, S41, S43).

## Core explanation
**Plain language.** Core Web Vitals (CWV) are Google's standardized way of measuring whether a page feels fast and stable to *real people*. They deliberately cover the three moments that most shape a visitor's first impression:

- **LCP — Largest Contentful Paint** = "how long until the main content is visible?" (perceived load speed).
- **INP — Interaction to Next Paint** = "how quickly does the page respond when I tap/click?" (responsiveness across the *whole* visit, not just the first interaction).
- **CLS — Cumulative Layout Shift** = "how much does the page jump around while loading?" (visual stability).

**Precise.** Each metric has a "good" / "needs improvement" / "poor" band defined against the **75th percentile** of visits (S38). In other words, the grade for a URL or origin is the value that 75% of visits are *at or better than*. If ≥75% of visits are "good," the page passes that metric; if ≥25% are "poor," the page is rated "poor." The thresholds were chosen from a combination of human-perception/HCI research and CrUX achievability data, and they are **identical for mobile and desktop** even though most are effectively set by mobile achievability (S38).

A page's overall CWV status in Search Console is the *worst* of its three metrics — a site can "ace two and fail the third" (S40).

## Mechanics / how-to

### 1. Measure — field first, lab to diagnose
- **Field (verdict):** Google Search Console → Core Web Vitals report (CrUX-based, URL-group and origin level), PageSpeed Insights "Field Data" section, CrUX BigQuery/API, or your own RUM. This is what Google actually uses for ranking (S40).
- **Lab (diagnosis):** Lighthouse (in DevTools, PageSpeed Insights "Lab Data", or CI), WebPageTest, GTmetrix. Lab runs a *single simulated* load on a throttled device — it tells you *what could* be wrong, not what your users experience (S40, S42).
- **Collect your own RUM** with Google's open-source `web-vitals` JS library (see example below); CrUX only covers Chrome and only sites above a traffic threshold, and it's a rolling 28-day average so it lags fixes (S40).

### 2. Optimize LCP (≤ 2.5 s)
- Identify the LCP element (Lighthouse/PSI "Diagnostics" or your RUM). It is usually a hero image, a background image, or a large text block.
- `<link rel="preload" as="image" href="hero.webp" fetchpriority="high">` for the LCP image; use `fetchpriority="low"` on below-the-fold images.
- Serve modern formats (AVIF/WebP) at responsive sizes; set explicit `width`/`height` (or `aspect-ratio`) to avoid layout shift.
- Eliminate render-blocking CSS/JS (inline critical CSS, defer the rest), use a CDN, `preconnect` to critical origins, and prefer SSR/streaming over client-side rendering of the main content.
- See also: `01-technical-seo/crawlability-indexation.md` (SSR matters for both indexing and LCP).

### 3. Optimize INP (≤ 200 ms) — replaced FID in 2024
- INP looks at the **worst** interaction across the whole page life (FID only looked at the first). Heavy JavaScript is the usual culprit (S39).
- Break up long tasks so the main thread can respond: code-split, defer non-critical JS, and **yield to the main thread** inside long handlers (e.g., `await scheduler.yield()` in supported browsers, or `setTimeout(...,0)` fallback).
- Minimize third-party script impact, use web workers for heavy computation, and debounce/throttle expensive handlers.
- Optimize event handlers themselves (do the minimum synchronous work on the critical path).

### 4. Optimize CLS (≤ 0.1)
- Always set `width`/`height` (or CSS `aspect-ratio`) on images and video so the browser reserves space.
- Reserve fixed space for ads, embeds, and iframes *before* they load.
- Never insert content above existing content (e.g., a late-loading banner pushing text down); animate with `transform`/`opacity`, not `top`/`height`.
- Use `font-display: optional` or a `size-adjust` fallback to avoid invisible-text/FOIT swap shifts.

## Worked example / code

**Measuring CWV in the field (pinned library).** Google's `web-vitals` library (v4) reports all three metrics from real users. Data source: real visitor browser signals (the same family of signals CrUX aggregates).

```html
<!-- Pinned version of the web-vitals library -->
<script type="module">
  import { onLCP, onINP, onCLS } from 'https://unpkg.com/web-vitals@4/dist/web-vitals.attribution.js';

  // Send each metric to your analytics / console.
  function report(metric) {
    // Replace with your beacon endpoint or GA4 event.
    console.log(metric.name, metric.value, metric.rating); // rating: 'good' | 'needs-improvement' | 'poor'
  }
  onLCP(report);
  onINP(report);   // INP is the long-task-aware successor to the retired FID
  onCLS(report);
</script>
```
> Pin the version (here `web-vitals@4`) so attribution output and metric semantics stay reproducible. See `web.dev/articles/vitals-tools` (S40) for GA4/BigQuery export wiring.

**Reserving space to prevent CLS + prioritizing the LCP image (HTML):**
```html
<!-- aspect-ratio reserves layout space -> no shift when the image loads -->
<img src="hero.avif" alt="Hero" width="1200" height="630"
     style="aspect-ratio: 1200 / 630; width: 100%; height: auto;"
     fetchpriority="high">

<!-- preload the LCP image so it paints ASAP -->
<link rel="preload" as="image" href="hero.avif" fetchpriority="high">
```

**Lab gate in CI (Lighthouse-CI excerpt)** — catches regressions before production:
```json
{ "ci": { "assert": { "preset": "lighthouse:recommended",
  "assertions": { "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
                  "cumulative-layout-shift":   ["error", { "maxNumericValue": 0.1 }],
                  "interaction-to-next-paint": ["error", { "maxNumericValue": 200 }] } } } }
```

## Assumptions & limitations
- **Field verdict ≠ lab score.** A page can score 100 in Lighthouse yet fail CWV because real users are on slower devices/networks (S40). Diagnose with lab; judge with field.
- **CrUX is Chrome-only and traffic-gated.** Sites below a popularity threshold have no CrUX data and must rely on their own RUM; CrUX is a 28-day rolling average, so improvements take weeks to appear in GSC (S40).
- **Thresholds are mobile-anchored** and "good" means *achievable for most sites*, not "the best possible" — well-optimized sites should push well beyond the bands (S38).
- **Ranking weight is modest and holistic.** Google has never published a "% ranking boost," and explicitly says good CWV "don't guarantee good rankings" (S39). CWV are one page-experience input into core ranking systems, not a standalone, heavyweight factor (S41).
- Google can and does revise metrics/thresholds (FID→INP in 2024 is the prime example); re-verify annually.

## Empirical evidence
- **Thresholds & 75th-percentile method:** derived from HCI/perception research plus CrUX achievability analysis (≥10% of origins can meet "good"; "poor" set where 10–30% fail). This is first-party Google methodology, not a correlation study (S38).
- **Field-vs-lab claims:** corroborated by both Google's own tooling guidance (S40) and independent practitioner analyses of Lighthouse vs RUM divergence (S42).
- **Ranking effect:** Google confirms CWV/page-experience is *a* ranking signal and that it aligns with what core systems reward (S39, S41). Practitioner sources describe it as largely a **tie-breaker between equally-relevant pages** (S43). No peer-reviewed study quantifies a causal ranking lift; industry case studies showing traffic/revenue gains after CWV fixes are **correlational** and often confounded by other site improvements shipped simultaneously.
- **Sample limitations:** CrUX covers only opted-in Chrome users; published CWV-pass-rate studies (e.g., HTTP Archive Web Almanac, Ahrefs) vary by sample and year — do not treat any single pass-rate percentage as current without checking the latest dataset. *See Verify task below.*

## Conflicting views
- **"CWV is a major ranking factor" vs "it's a minor tie-breaker."** Vendors sometimes market CWV as a primary lever. Google's own wording is careful: it "aligns with what our core ranking systems seek to reward" and good scores "don't guarantee good rankings" (S39, S41). Practitioner consensus (S43) is that it mainly breaks ties among otherwise-similar pages. **Treat heavy CWV-focused ranking claims as contested/folklore unless paired with a documented case study.**
- **Lab vs field disagreement.** Some teams act on Lighthouse scores alone. First-party guidance is explicit that only field data counts for the Google verdict (S40) — acting on lab-only can mislead (a green Lighthouse score can still fail in the field).
- **Single score vs three metrics.** CWV is *not* one number; each metric is judged independently at the 75th percentile, and the overall status is the worst metric (S38, S40).

## Common mistakes
- **Optimizing for Lighthouse instead of field data** — shipping a "green" lab score while real users still fail.
- **Ignoring INP because "FID was fine"** — INP covers *all* interactions; sites heavy on JS often pass FID but fail INP (S39).
- **Forgetting image/video dimensions** → large CLS from late-loading media and embeds.
- **Inserting banners/ads above the fold content** → layout shift after load.
- **Treating CWV as a silver bullet for rankings** → over-investing while neglecting content quality, relevance, and links, which Google weights far more heavily.
- **Reading the GSC CWV report as page-level truth** — GSC groups URLs into "URL groups"; drill into the specific failing URLs and their field data, and remember CrUX is a trailing 28-day average.

## Further reading
- **[Tier 1]** web.dev, "How the Core Web Vitals metrics thresholds were defined" — https://web.dev/articles/defining-core-web-vitals-thresholds (S38)
- **[Tier 1]** web.dev, "Core Web Vitals workflows with Google tools" (field vs lab, CrUX, RUM, web-vitals lib) — https://web.dev/articles/vitals-tools (S40)
- **[Tier 1]** Google Search Central Blog, "Introducing INP to Core Web Vitals" — https://developers.google.com/search/blog/2023/05/introducing-inp (S39)
- **[Tier 1]** web.dev, "Interaction to Next Paint becomes a Core Web Vital on March 12" — https://web.dev/blog/inp-cwv-march-12 (S29)
- **[Tier 1]** Google Search Central, "Understanding Core Web Vitals and Google search results" — https://developers.google.com/search/docs/appearance/core-web-vitals (S41)
- **[Tier 1]** web.dev, "Web Vitals" overview — https://web.dev/vitals (S10)
- **[Tier 2]** RUMvision, "Understanding the difference between Lighthouse, Core Web Vitals and RUM data" — https://www.rumvision.com/blog/understanding-the-difference-between-core-web-vitals-tools (S42)
- **[Tier 2]** DebugBear, "Are Core Web Vitals A Ranking Factor for SEO?" — https://www.debugbear.com/docs/core-web-vitals-ranking-factor (S43)
