---
title: Review Acquisition & Management for Local SEO
topic_id: 06-local-seo/review-acquisition-management
tags: [local-seo, reviews, google-business-profile, reputation, local-pack, policy]
last_updated: 2026-07-18
confidence: robust
sources: [S161, S167, S168, S166, S169, S170, S171, S172, S173, S45, S47]
---

## TL;DR
- Google treats reviews as a **local-prominence signal**: its own local-ranking help doc states prominence is informed by review count and ratings (S161). Reviews also feed *relevance* (user-generated text Google can read).
- Reviews almost certainly help local visibility, but **proximity and relevance frequently dominate**, and Google has never published a "review weight." A single-agency case study found the ranking lift **plateaus after ~10 reviews** (S170) — more reviews ≠ linear ranking gains.
- What Google prohibits is explicit and enforceable: paid/incentivized reviews, **review gating** (asking only happy customers), conflict-of-interest reviews, and staff review quotas are all banned under the Maps User-Generated Content Policy (S167). In the US, the FTC's rule (16 CFR 465, effective Oct 21 2024) separately makes buying or suppressing reviews illegal (S168).
- Do: ask **every** customer for a genuine review with no incentive, respond to all reviews, diversify across platforms, and monitor velocity/recency. Don't: buy, gate, incentivize, or script staff quotas.

## Core explanation
**Plain language.** When someone searches "plumber near me," Google decides which businesses to show using three pillars: *proximity* (how close you are), *relevance* (how well you match the query), and *prominence* (how well-known/trusted you are). Reviews feed prominence (and, through their text, relevance). The more genuine, recent, high-quality reviews you have, the stronger the trust signal — but reviews are one input among many, not a magic rank button.

**Precise.** Google's local-ranking help page is explicit that local results are ranked by relevance, distance, and prominence, and that prominence is informed by "how many websites link to your business" and by your **review count and ratings** (S161). BrightLocal's local-algorithm breakdown places reviews under both *prominence* ("online reviews") and *relevance* (reviews are user-generated content that helps match a query) (S171). The Whitespark Local Search Ranking Factors survey — a ~20-year practitioner survey — shows experts increasingly rate review signals as influential for the Local Pack, while link signals have trended down in perceived importance (S166, S169).

Two things the evidence does **not** support:
1. A published numeric weight (e.g., "reviews = 15% of local-pack ranking"). Every such figure is a *practitioner-belief survey* output, not a Google-confirmed coefficient. Treat as directional only.
2. "The more reviews, the higher you rank, forever." Sterling Sky's repeated case tests (Joy Hawkins, 2025 update) observed a ranking bump when a listing crossed the **10-review threshold** (9→10) but no further lift at 10→11 or 16→31; they conclude there is a boost that does **not** continue indefinitely (S170).

## Mechanics / how-to

### 1. Acquire reviews compliantly
- **Ask every customer, every time**, via a post-purchase email/SMS with a direct Google review link (use your GBP "share review form" short link). No incentive, no filtering for satisfied customers (S167 allows soliciting genuine-experience reviews *without* incentives; it bans selective solicitation).
- **Never gate.** Do not send a survey that routes only 5-star responders to Google and buries unhappy ones. Google's policy bans "discourage or prohibit negative reviews, or selectively solicit positive reviews" (S167) — this is exactly what review-gating tools do.
- **No incentives.** Do not offer discounts, free goods, entries into a draw, or anything of value in exchange for a review or for removing a negative one (S167; also unlawful under FTC 16 CFR 465, S168).
- **No conflict of interest.** Do not have employees, owners, family, or competitors post reviews. Google removes conflict-of-interest reviews (S167). Employees *may* review you on some third-party sites (e.g., Facebook, industry directories) but **never on Google or Yelp** (S173).
- **No quotas or scripting.** Merchants may not require staff to solicit "a certain number of reviews" or to solicit reviews that name a specific staff member (S167).
- **Don't pressure on-site.** Do not require/pressure customers to leave a review while physically on your premises, nor dictate specific content (S167).

### 2. Diversify across platforms
Reviews on **other** sites matter too: third-party reviews can appear in your Google Knowledge Panel (boosting credibility of your Google reviews), and Google "digests the data from all your reviews across the web" (S173). Rotating requests (one customer → Google, next → Yelp, next → an industry site) spreads coverage without sacrificing your Google total (S173).

### 3. Respond to all reviews
Reply to positive and negative reviews professionally and factually. Responding is widely practiced for trust/conversion and is believed by many practitioners to be a minor signal, but **Google has not confirmed a ranking weight for responses** — treat it as a conversion/trust lever, not a ranking hack. For policy-violating reviews (fake, conflict-of-interest), use the "Report review" tool on the Business Profile rather than arguing publicly.

### 4. Surface reviews on your site (optional, with guardrails)
If you display ratings/reviews on a page, `AggregateRating`/`Review` schema can enable star rich results — **but** Google requires the ratings to reflect real, visible on-page reviews; fabricated or mismatched markup is a structured-data violation (S45, S47). See the worked example below.

## Worked example / code

### A. Compliant review-request email (no incentive, asks everyone)
```
Subject: How did we do?

Hi {first_name},

Thanks for choosing {business_name} — we hope everything went well.

If you have 60 seconds, we'd genuinely appreciate your honest feedback on
Google (good or bad, it all helps us improve):
{gbp_review_link}

No incentives, no strings — just your real experience.

— {business_name}
```
This satisfies Google's "solicit genuine experience, without offering incentives" (S167) and stays clear of FTC gating/incentive prohibitions (S168).

### B. Review velocity / recency monitor (stdlib, Python 3.8+)
Sterling Sky's case work suggests rankings can slip if a listing goes ~3 weeks without a new review ("18-day rule," S170) — directional, single-agency, not Google-confirmed. The script below flags stale gaps so you can keep asking customers.

```python
#!/usr/bin/env python3
# review_velocity.py — monitor review recency/velocity from a CSV of review dates.
# Usage: python3 review_velocity.py reviews.csv [stale_days]
# CSV columns: date (YYYY-MM-DD). stdlib only; runs on Python 3.8+.
import csv, sys
from datetime import datetime, date

def main(path, stale_days=18):
    dates = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                dates.append(datetime.strptime(row["date"].strip(), "%Y-%m-%d").date())
            except (ValueError, KeyError):
                continue
    if not dates:
        print("No parseable review dates found."); return
    dates.sort()
    today = date.today()
    last = dates[-1]
    gap_since_last = (today - last).days
    gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
    max_gap = max(gaps) if gaps else 0
    months = max((today - dates[0]).days / 30.44, 1)
    per_month = len(dates) / months
    print(f"Reviews total:        {len(dates)}")
    print(f"First / last:         {dates[0]} / {last}")
    print(f"Days since last review: {gap_since_last}")
    print(f"Avg reviews / month:  {per_month:.2f}")
    print(f"Largest gap (days):   {max_gap}")
    if gap_since_last > stale_days:
        print(f"ALERT: {gap_since_last} days since last review (> {stale_days} day stale threshold) — re-ask customers.")
    if max_gap > stale_days:
        print(f"ALERT: a {max_gap}-day gap occurred historically — keep a steady cadence, not bursts.")

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "reviews.csv"
    sd = int(sys.argv[2]) if len(sys.argv) > 2 else 18
    main(p, sd)
```
Run: `python3 review_velocity.py reviews.csv`. Data source: your exported Google Business Profile reviews (date per review). The 18-day threshold is Sterling Sky's observation (S170), not a Google rule — tune to your cadence.

### C. AggregateRating schema (only if ratings are real and visible on-page)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Example Plumbing Co.",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "128"
  }
}
</script>
```
Caveat: Google requires the page to **visibly show** the same ratings/reviews; marking up numbers you don't display, or faking them, violates structured-data policies and can trigger a manual action (S45, S47). Only deploy after the reviews genuinely exist on the page.

## Assumptions & limitations
- **Google does not publish review weights.** Any "reviews = X% of ranking" number is a survey estimate (S166, S169), not a Google coefficient. Do not present as fact.
- **Proximity often dominates.** For "near me" queries, distance to the searcher can override review volume; a business with fewer reviews but closer proximity may outrank a review-heavy farther one (S161, S171).
- **Case-study evidence is small-n.** Sterling Sky's threshold findings come from one agency's repeated client tests (S170) — directionally useful, not a controlled experiment.
- **Policy enforcement is algorithmic + manual.** Google removes violating reviews and can suspend profiles (S167); the FTC rule (S168) is US law and carries civil penalties — but enforcement varies by jurisdiction.
- **No guaranteed rankings.** Reviews are a trust/prominence input; they do not guarantee position.

## Empirical evidence
- **Google's own doc (Tier 1):** local ranking = relevance + distance + prominence; prominence informed by review count/ratings (S161). This is the strongest available evidence that reviews are a ranking input.
- **Sterling Sky 2025 case study (Tier 2):** observed ranking lift crossing the 9→10 review mark, with no further lift at 10→11 or 16→31; "18-day rule" — rankings can slip after ~3 weeks without a new review (S170). Single agency, small n; directional.
- **Whitespark/GatherUp consumer survey (Tier 2, large consumer sample):** 98% of consumers consult reviews before choosing a local business, 94% place some trust in local-business reviews, 55% trust customer reviews over what brands say about themselves, 93% require ≥3 stars to choose (reported via S169). Measures *consumer behavior*, not ranking.
- **Whitespark Local Search Ranking Factors (Tier 2, practitioner survey):** experts rate review signals as increasingly influential for the Local Pack; link signals trending down (S166, S169). This is *belief*, not measured weight.
- **BrightLocal local-algorithm guide (Tier 2):** frames reviews under prominence and relevance (S171). Corroborates Google's three-pillar model.

## Conflicting views
- **"Reviews are the #1 local factor" vs Google's 3-pillar model.** Vendors and some practitioners elevate reviews above all else; Google's documentation and practitioner surveys put *proximity* and *primary category/relevance* at or near the top for the Local Pack (S161, S166, S171). Reviews matter, but rarely outrank physical distance for "near me" intent.
- **"More reviews = always higher" vs plateau evidence.** Marketing folklore says pile up reviews; Sterling Sky's data shows diminishing/zero marginal ranking return past ~10 (S170). Volume still helps *conversion* and trust even when ranking lift plateaus.
- **"Review-gating tools are compliant."** Some vendors sell "ask only promoters to review" flows. Google's policy explicitly bans selectively soliciting positive reviews and discouraging negative ones (S167) — directly contradicting those claims. Where a vendor says gating is allowed, the primary Google policy wins.
- **"Responding to reviews boosts rankings."** Commonly asserted; Google has not confirmed a ranking weight for owner responses. Treat as a trust/conversion practice.

## Common mistakes
- **Buying reviews** (Fiverr, review farms) — removed by Google (S167) and illegal under FTC 16 CFR 465 (S168).
- **Review gating** — routing detractors away from public review sites; prohibited "selective solicitation" (S167).
- **Offering incentives** ("10% off for a review") — banned by Google and the FTC (S167, S168).
- **Employee/competitor/family reviews** — conflict of interest; Google removes them (S167).
- **Staff quotas / scripting named employees** — "request that staff solicit a certain number of reviews" or "reviews that include specific content, including a staff member" are explicitly disallowed (S167).
- **Fake negative reviews on competitors** — prohibited manipulation (S167).
- **Faking AggregateRating markup** — rich-result manual action if numbers aren't genuinely displayed on-page (S45, S47).
- **Chasing volume, ignoring recency** — a stale profile (no new reviews for weeks) can lose the cadence signal Sterling Sky observes (S170).

## Further reading
- S161 — Google, "Tips to improve your local ranking on Google" (support.google.com/business/answer/7091) — Tier 1: reviews → prominence.
- S167 — Google, "Maps User Generated Content Policy — Prohibited & restricted content" (support.google.com/contributionpolicy/answer/7400114) — Tier 1: incentives, gating, conflict of interest, quotas all banned.
- S168 — FTC, "Rule on the Use of Consumer Reviews and Testimonials" (16 CFR Part 465, effective Oct 21 2024) — Tier 1 (US regulation): buying/selling/suppressing reviews unlawful.
- S170 — Sterling Sky, "Does the Number of Google Reviews Impact Ranking?" (Joy Hawkins, 2025 update) — Tier 2: 10-review threshold, plateau, recency.
- S169 — Whitespark, "7 Local Search Ranking Factors… (2026 report)" + GatherUp consumer review survey — Tier 2.
- S166 — Whitespark, "Local Search Ranking Factors" survey — Tier 2 (practitioner belief).
- S171 — BrightLocal, "Google's Local Algorithm and Local Ranking Factors" (Jan 2026) — Tier 2.
- S173 — Whitespark, "3 Ways to Diversify Your Local Business Reviews" (Darren Shaw, 2025) — Tier 2.
- S45 / S47 — Google Search Central, structured-data general guidelines + Product structured data — Tier 1 (AggregateRating guardrails).
