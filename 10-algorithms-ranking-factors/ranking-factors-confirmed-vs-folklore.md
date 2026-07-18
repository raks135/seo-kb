---
title: Ranking Factors — What Google Confirms vs. SEO Folklore
topic_id: 10-algorithms-ranking-factors/ranking-factors-confirmed-vs-folklore
tags: [ranking-factors, algorithm, myths, google-confirmed, seo-folklore]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S2, S13, S14, S29, S33, S41, S43, S58, S67, S84, S85, S91, S114, S129, S161, S243, S244, S245, S246, S247, S248, S249, S250, S251]
---

## TL;DR
- Google uses "many" ranking signals but has **never published a complete list**. The popular "200 ranking factors" infographics are SEO-created compendia — Backlinko's own 2026 list self-classifies its items as "some proven, some controversial, others just SEO nerd speculation" (S251).
- What Google has **named in official docs** (confirmed): relevance / query understanding (BERT, RankBrain, neural matching, MUM), links / PageRank, content quality & helpfulness, page experience (Core Web Vitals), HTTPS, mobile-friendliness, freshness, localized signals, E-E-A-T as a Quality-Rater *framework* (not a score), and spam filtering (S2, S13, S14, S29, S33, S41, S43, S58, S67, S84, S91, S114, S129, S161, S243).
- What is **folklore / not a confirmed factor**: dwell time, bounce rate, social likes/shares/followers, domain age, keyword density, the meta-keywords tag, and third-party "Domain Authority"/"DR" scores (S244, S245, S246, S247, S248, S249, S250, S251).
- Practitioner rule: ranking is multivariate and query-dependent; a factor that *correlates* with top rankings is not causal; no single factor "wins," and Google has repeatedly said there is no fixed weighted list.

## Core explanation
**Plain language.** Google decides what to show by running hundreds of small scoring steps over the pages it has crawled and indexed. Some of those steps are things Google has openly described (e.g., "does this page match the words in the query?", "do other reputable pages link to it?", "is it fast and secure?"). Other "factors" you read about on the internet — dwell time, social shares, domain age — are inferences SEOs made from correlation studies or old patents, not things Google has confirmed it measures.

**Precise.** Google's own statements describe ranking as a set of *systems* applied during the "serving" stage, on top of crawling and indexing (S2). In 2010 Matt Cutts said Google counts "over 200" ranking factors, each "with up to 50 variations" (quoted in S246/S249) — but Google has **never published that list**, and Cutts's phrasing was an approximation given to journalists to convey complexity (S249). The job of a practitioner is therefore to separate **disclosed systems** (Tier-1) from **correlational inference and speculation** (Tier-2/3). We use a three-bucket labeling scheme throughout the KB:

- **Robust** — asserted or demonstrated by a Google primary source (Tier-1).
- **Emerging** — plausible and supported by multiple independent practitioner studies, but Google has not confirmed a mechanism or weight.
- **Folklore** — widely repeated, weakly or not supported, and in several cases explicitly denied by Google.

## Mechanics / how-to
**How to evaluate any claimed "ranking factor" before acting on it:**
1. *Is it in a Google primary doc?* If Google's Search Central docs, a Google blog, or a Google spokesperson names the mechanism, it is **robust** (e.g., links, HTTPS, page experience, freshness).
2. *Is it corroborated by ≥2 independent sources, and is the claim about a stated signal vs. a correlation?* A study showing "pages with X tend to rank higher" is a **correlation**, not proof Google uses X. Label correlation-only claims **emerging** at best (S115).
3. *Does Google deny it?* Several folklore items below are explicitly denied by Google reps on the record.
4. *Is it a prerequisite vs. a score?* Crawlability, indexability, HTTPS, and a mobile-friendly version are **entry tickets**, not ranking boosts — without them a page simply cannot compete (S1, S2, S4, S5, S67, S243).

**Quick triage table (the confirmed bucket):**

| Confirmed factor | What Google actually says | Source |
|---|---|---|
| Relevance / query understanding | BERT, RankBrain, neural matching, MUM are named ranking systems; they match query meaning to content | S13, S14, S33 |
| Links / PageRank | "Links are a signal for relevancy and a way to discover new pages"; PageRank is still a named system | S33, S58 |
| Content quality & helpfulness | People-first, helpful content rewarded by automated systems; not a single toggle | S84, S91 |
| Page experience / Core Web Vitals | Page experience (incl. CWV) "aligns with what core ranking systems seek to reward"; a tie-breaker, **not** a guarantee | S29, S41, S43 |
| HTTPS | "Starting to use HTTPS as a ranking signal" (2014); lightweight, <1% of queries at launch | S243 |
| Mobile-friendliness | Mobile-first indexing: the mobile version is what is indexed and ranked | S67 |
| Freshness / QDF | "Fresher results" update affects ~35% of searches; freshness is a named ranking system | S33, S129 |
| Localized / geographic signals | Location (device GPS, IP, activity) and relevance/distance/prominence drive local results | S35, S161 |
| E-E-A-T | A *Quality Rater* framework used to **evaluate** quality; not a direct score or confirmed ranking factor | S9, S84, S85 |
| Structured data | Not a ranking factor — affects display/rich results only | S45, S53 |
| Spam filtering | SpamBrain and spam policies demote/remove low-quality, manipulative pages | S33, S97, S243(doc) |

## Worked example / code
The script below operationalizes the confirmed-vs-folklore split for a single URL: it checks the *technical* prerequisites Google has named and flags the classic folklore trap (keyword stuffing). It maps every check to a Tier-1 source ID. It does **not** measure ranking — it is a checklist, not a forecast.

`ranking_factor_health_audit.py` (stdlib only, Python 3.8+, no network needed for `--demo`):

```python
# (full file shipped alongside this article)
# Run:  python3 ranking_factor_health_audit.py --demo
#        python3 ranking_factor_health_audit.py https://example.com
```

Verified `--demo` run (deliberately stuffed title → correctly flagged):

```
[PASS] Title tag present
        basis: relevance helper (S1)
[----] Title not keyword-stuffed
        basis: folklore trap (stuffing = spam, not a boost)
        note : 'cheap' repeats 62% of title tokens
[PASS] Meta description present (display only)
        basis: NOT a direct ranking factor (S251 cites Google)
[PASS] Mobile viewport meta
        basis: mobile-first indexing (S67)
[PASS] Canonical link
        basis: duplicate consolidation (S4)
[PASS] JSON-LD structured data
        basis: display/rich-result only, NOT a ranking factor (S45)
[----] hreflang alternates
        basis: international signal, not a directive (S179)
5/7 technical prerequisites met (HTTPS checked separately).
```

The HTML regex/parse logic runs under the standard library `html.parser`; data source for a live run is the target page's raw HTML fetched over HTTPS (HTTPS itself is the S243 signal).

## Assumptions & limitations
- **Google's algorithm is proprietary and changes.** Every "confirmed" item reflects what Google has *disclosed* — the actual weighting, thresholds, and interaction effects are unknown and revised via core/spam updates (S231, S233, S243(doc)).
- **"Confirmed" ≠ "heavy."** HTTPS is a confirmed signal but Google called it "lightweight" affecting <1% of queries at launch (S243). Page experience is a *tie-breaker between already-relevant pages*, not a primary relevance lever (S41, S43).
- **Correlation ≠ causation.** Studies showing "pages with more X rank higher" (e.g., backlinks↔rankings) are observational; Google's own engineers stress this (S33, S115).
- **Some confirmations are dated.** Cutts's "200 factors / 50 variations" line is from 2010 (S246/S249); patents cited in folklore lists (e.g., historical-data domain scoring, S245) describe research, not necessarily shipped, current behavior.
- **What Google debunks today can be nuanced.** "Links are not a top-3 factor" is Gary Illyes's 2024 position (S114); Andrey Lipattsev said links *were* top-3 in 2016 — so the *relative* weight of links has clearly fallen as ML relevance systems matured, even though links remain a named system (S33, S114). We label "links as a top-3 factor" as **contested**, not folklore.

## Empirical evidence
- **The "200 factors" framing is real but unofficial.** Google has said "over 200 factors," each with "up to 50 variations" (Cutts, via S246/S249), yet no canonical list exists; Moz calls the enumerated "200 list" "useless and dangerous" because items are "myths, correlation factors, or padding to reach 200" (S249). Backlinko's 2026 version admits "some are proven, some controversial, others speculation" (S251).
- **Folklore debunkings are independently corroborated:**
  - *Dwell time / pogo-sticking:* Gary Illyes — "Dwell time, CTR, whatever [theory]… those are generally made-up crap. Search is much more simple than people think"; Martin Splitt confirmed user-interaction metrics are "not used for search" (reported in S244).
  - *Bounce rate / Google-Analytics metrics:* SEJ notes CTR, bounce rate, and similar GA metrics "have no direct impact on your rankings" (S244).
  - *Social signals (likes/shares/followers):* Matt Cutts — "Social signals are not taken into account… we don't currently have any signals like that in our web search ranking algorithms" (reported in S250). Social can *indirectly* help by earning real links (S250), but the raw signal is not a factor.
  - *Domain age:* Cutts — "the difference between a domain six months old versus one year old is really not that big at all"; John Mueller has stated domain age "helps nothing" (S245). A 2005 historical-data patent describes domain-history scoring, but that is a patent, not a confirmation of current use (S245).
  - *Keyword density:* Moz — "Keyword Density never was a Google's ranking factor. Never" (S246); stuffing falls under Google's spam policies instead (S97).
  - *Meta keywords / meta description:* Google does not use the meta-keywords tag and does not use the meta-description tag as a direct ranking signal; description affects CTR only (S251).
  - *Third-party "Domain Authority"/"DR":* These are Moz/Semrush/Ahrefs *proprietary* metrics, not Google signals; they correlate with rankings but are not inputs Google uses (consistent with S111/S115 correlation framing).
- **Strength of evidence:** The confirmed bucket rests on Tier-1 Google primary sources. The folklore debunkings rest on ≥2 independent practitioner reports (SEJ, Moz, Econsultancy) that quote Google reps on the record — strong enough to label these "not confirmed factors," while noting Google has not published a single primary "X is not a factor" memorandum for each.

## Conflicting views
- **"Links are a top-3 ranking factor."** Contested. Illyes (2024) says links "haven't been a top-3 ranking factor for some time" (S114); Lipattsev (2016) said they *were* top-3 (content, links, RankBrain). Defensible statement: links remain a named Google system (S33) but their *relative* weight has declined versus ML relevance systems. No fixed rank is asserted.
- **Social signals — direct vs. indirect.** Direct social engagement (likes/shares/followers) is denied (S250); the *indirect* path (good content earns links via social exposure) is real (S250). Confusion arises from mixing the two.
- **Entity / brand signals.** Google's Knowledge Graph and entity comprehension (S33, S118) are mechanisms that help Google *understand* pages, not a confirmed "brand ranking factor"; we label brand/entity optimization **emerging**.
- **Exact-match domains (EMD).** Unsettled — the 2012 EMD update demoted spammy EMDs (S251 cites SEL research), but the current standalone effect of a clean EMD is **not asserted here**; an open Verify task tracks the precise post-EMD effect (backlog line 99).
- **Structured data.** Not a ranking factor (S45, S53) — a point of frequent industry confusion, sometimes marketed as a "rich-result ranking boost."

## Common mistakes
- **Chasing folklore metrics.** Optimizing for dwell time, bounce rate, or social likes as if they were dials Google reads (S244, S250). You cannot "set" these; you can only improve content/UX, which may *indirectly* help.
- **Treating third-party scores as Google signals.** "Our DA dropped" or "we need more DR" — DA/DR are vendor metrics, not ranking inputs (S111, S115).
- **Keyword stuffing.** Stacking a term in title/H1 to "raise density" is spam, not a boost (S97, S246); the shipped audit flags a single token repeating ≥40% of title tokens.
- **Trusting any single "ranking factors" infographic.** Most are mixtures of proven + controversial + speculation (S249, S251).
- **Assuming one factor dominates.** Ranking is multivariate; even HTTPS (confirmed) was launched as a <1%-of-queries lightweight signal (S243). No factor is a silver bullet.
- **Confusing correlation with causation.** "Pages with more X rank higher" ≠ "Google ranks higher because of X" (S33, S115).
- **Buying/renting "authority."** PBNs, link buying, and widget/footer schemes are link schemes Google penalizes (S97, S103); see `03-off-page-seo/link-schemes.md`.

## Further reading
Tier 1 (primary, authoritative):
- Google, "How Search works: Crawling, indexing, serving" — S2
- Google, "A guide to Google Search ranking systems" — S33
- Google, "HTTPS as a ranking signal" (2014) — S243
- Google, "Understanding Core Web Vitals and Google search results" — S41
- Google, "Creating helpful, reliable, people-first content" — S84
- Google, "Mobile-first indexing best practices" — S67
- Google, "General structured data guidelines" (not a ranking factor) — S45

Tier 2 (practitioner, data-backed):
- Moz, "The Myth of Google's 200 Ranking Factors" — S249
- Backlinko, "Google's 200 Ranking Factors: The Complete List" (self-labels proven/controversial/speculation) — S251
- Search Engine Journal, "Dwell Time: Is It A Google Ranking Factor?" — S244
- Search Engine Journal, "Domain Age: Is It A Google Ranking Factor?" — S245
- Econsultancy, "Does Google use social signals for ranking?" (Cutts denial) — S250
- Search Engine Land, "Links are not a top-3 ranking factor, says Gary Illyes" — S114

Related KB articles: `10-algorithms-ranking-factors/algorithms.md`, `10-algorithms-ranking-factors/core-updates.md`, `10-algorithms-ranking-factors/helpful-content-system.md`, `10-algorithms-ranking-factors/spam-updates-link-spam.md`, `03-off-page-seo/link-evaluation-models.md`, `01-technical-seo/core-web-vitals.md`, `02-on-page-seo/eeat.md`.
