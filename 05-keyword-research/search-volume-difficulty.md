---
title: Search Volume & Keyword Difficulty Metrics — How They're Computed
topic_id: 05-keyword-research/search-volume-difficulty
tags: [keyword-research, search-volume, keyword-difficulty, metrics, tooling]
last_updated: 2026-07-18
confidence: robust
sources: [S141, S142, S143, S144, S145, S146, S147]
---

## TL;DR
Search volume is an *estimate* of average monthly demand, not a count of real searches — only Google has the true number, and every tool (Google Keyword Planner, Ahrefs, Semrush, Moz) derives it differently, so the same keyword can show wildly different volumes. Keyword Difficulty (KD) is a backlink/authority-centric *estimate* of how hard it is to crack the top 10 for a query; each vendor computes it from a different formula (Ahrefs = referring domains of the top 10, Semrush = 6 weighted factors + a personal score, Moz = Page/Domain Authority of the first page). Treat both metrics as directional filters, never as guarantees — volume ≠ traffic, and KD ≠ a ranking prediction.

## Core explanation
**Search volume** quantifies how many times a query is searched, usually reported as *average monthly searches* over a trailing window. The ground-truth source is Google's own query logs, surfaced to advertisers through **Google Keyword Planner (GKP)**. GKP reports volume as an average over the **preceding 12 months** to smooth seasonality, and for accounts without meaningful ad spend it shows **rounded ranges** (e.g. "1K–10K") rather than exact figures; exact numbers are effectively gated behind active ad spend (S143, S147). GKP also **groups close variants** ("pool" absorbs "swimming pool", "pool table") and **rounds into buckets**, so its figure is a broad-match aggregate, not a single-phrase count (S146, S144).

Third-party tools cannot see Google's raw logs, so they **estimate** volume. Ahrefs states plainly it "uses a combination of Google Keyword Planner (GKP), Google trends data and other third party data sources" (S144); Semrush overlays "historical clickstream data acquired from reliable sources" on third-party sets (S146). Because the inputs and models differ, the same keyword yields different numbers across tools (see Empirical evidence).

**Keyword Difficulty** estimates how hard it is to reach the first page (top 10) for a query. Crucially, **none of these scores is a Google metric** — they are vendor models built on the observable correlation that authoritative, heavily-linked pages tend to dominate the first page. The three major formulas:

- **Ahrefs KD** — number of **referring domains (RDs)** pointing at the top 10 ranking pages; 0–100, non-linear scale; explicitly estimates *top-10* (not top-3) difficulty and excludes on-page factors (S141).
- **Semrush KD %** — a percentage from six weighted factors: backlinks to top-ranking sites (median RDs + follow/nofollow ratio), Authority Scores of those sites, the keyword's own search volume, presence of SERP features, branded-ness, and query word count. It also offers a **Personal KD (PKD)** tuned to *your* domain's authority (S142).
- **Moz Difficulty** — Page Authority (PA) and Domain Authority (DA) of the results on the first page, weighted by projected CTR of those positions; 1–100 (S145).

## Mechanics / how-to
**Reading search volume correctly**
1. Pull volume in the *right location* — it is location-specific; a "global" number averages many markets (S143).
2. For non-advertisers, read GKP ranges as orders of magnitude, not precision. If you need a tighter figure, cross-check with a third-party tool or run a small Google Ads campaign.
3. Don't confuse **volume** with **traffic potential**. Many searches end in zero clicks (answer boxes, ads, or the user refines). Ahrefs and Semrush separately expose "Traffic Potential" / estimated clicks precisely because raw volume overstates visit counts (S144, S143).
4. Check trend direction (GKP "3-month change", Google Trends) — a 12-month average hides a keyword that is spiking or dying (S143, S146).

**Using Keyword Difficulty**
1. Treat KD as a *first-pass filter* to sort thousands of keywords, then always do manual SERP analysis — every vendor says the score is insufficient alone (S141, S142, S145).
2. Match KD to your domain's strength. If you're new, target low-KD terms; use Semrush PKD or your own Authority/DR as the realistic ceiling (S142).
3. Remember KD measures *top-10* difficulty, not "will I rank #1." A KD-30 term may still take months and several strong links.
4. Don't let KD override intent. A hard-but-perfectly-aligned term can be worth more than an easy irrelevant one.

## Worked example / code
The snippet below re-implements **Ahrefs' published RD→KD mapping** (S141) so you can see *how* KD is derived from top-10 link counts. It is a faithful re-creation of the public table, not the live Ahrefs tool, and needs only the Python standard library (≥3.8).

```python
# ahrefs_kd_from_referring_domains.py  (stdlib only, Python >=3.8)
# Re-creates Ahrefs' published KD<->Referring-Domains mapping via interpolation.
# Source table (S141): KD 0,10,20,30,40,50,60,70,80,90
#                       RD  0,10,22,36,56,84,129,202,353,756
import bisect

KD_POINTS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
RD_POINTS = [0, 10, 22, 36, 56, 84, 129, 202, 353, 756]

def estimate_kd(median_rd_top10: float) -> float:
    """Return an Ahrefs-style KD (0-100) for the median # of referring domains
    across the top 10 ranking pages."""
    if median_rd_top10 <= RD_POINTS[0]:
        return 0.0
    if median_rd_top10 >= RD_POINTS[-1]:
        return 100.0
    i = bisect.bisect_right(RD_POINTS, median_rd_top10)      # upper bracket
    lo, hi = i - 1, i
    rd_lo, rd_hi = RD_POINTS[lo], RD_POINTS[hi]
    kd_lo, kd_hi = KD_POINTS[lo], KD_POINTS[hi]
    frac = (median_rd_top10 - rd_lo) / (rd_hi - rd_lo)        # linear interp
    return round(kd_lo + frac * (kd_hi - kd_lo), 1)

# Example: you analysed the top 10 and found a median of 60 referring domains.
print(estimate_kd(60))    # ~41.4  -> roughly a "KD 41" keyword
print(estimate_kd(0))     # 0.0
print(estimate_kd(756))   # 100.0
```

**Volume-disagreement check** (illustrates why you should never trust a single tool). For the keyword *"reddit marketing"* (US, monthly):
- Google Keyword Planner: **880,000**
- Semrush: **590,000**
- Ahrefs: **100,000**  (S146)

```python
# volume_disagreement.py
volumes = {"Google_KP": 880_000, "Semrush": 590_000, "Ahrefs": 100_000}
lo, hi = min(volumes.values()), max(volumes.values())
print(f"Spread: {hi/lo:.1f}x between highest and lowest estimate")
# -> 8.8x  -- the same query, 8.8x apart depending on tool
```
Takeaway: use volume for *relative* prioritisation (this term >> that term) and always sanity-check against GSC Impressions once a page is live (S144).

## Assumptions & limitations
- **Only Google has true volume.** Every external number is an estimate; Ahrefs explicitly states "search volume in any SEO tool, including Ahrefs, is always an estimation" (S144).
- **Sampling bias.** Clickstream-based estimates come from user panels/partners, not the full population. Low-volume and niche/long-tail keywords are the least reliable (S144; corroborated by practitioner analyses).
- **12-month averaging lags trends.** A breakout keyword looks under-valued until 11 more months accumulate; a declining one looks over-valued (S146).
- **KD ignores on-page, intent, and content quality.** Ahrefs KD omits on-page factors entirely (S141); Semrush/Moz weight link/authority signals only. A weak page can still lose to a stronger one regardless of KD.
- **Location matters.** Volumes and difficulty are location-bound; a US KD is not a UK KD.
- **KD ≠ causation.** The RD↔position relationship is correlational (S141's own study); acquiring links does not mechanically produce rankings.
- **"Not provided."** Google Analytics hides organic keyword data; you can only validate real demand via Google Search Console Impressions, not GA (S144).

## Empirical evidence
- **Tool disagreement is large and real.** The *"reddit marketing"* example shows an 8.8× spread across GKP/Semrush/Ahrefs for one US keyword, attributable to different data sources and aggregation (GKP broad-match grouping vs clickstream panels) (S146).
- **GKP itself can be inaccurate.** Ahrefs' 2021 study found GKP **overestimated** search volumes **54% of the time**, and in a GSC-Impressions benchmark Ahrefs' volume was *directionally* accurate for **~60%** of keywords vs **~45%** for GKP (vendor self-reported, S144). Treat the 54%/60%/45% figures as *Ahrefs' claims*, not independent audits.
- **Strong RD↔rank correlation.** Ahrefs reports a strong correlation between the number of referring domains a page has and its Google position, which is the empirical basis for its KD formula (S141). Correlation, not proof of causation.
- **Semrush volume→difficulty pattern.** Semrush observes keywords >100k volume average ~76% KD while 11–100-volume terms average ~39%, a directional (not causal) relationship (S142).
- Sample/limitation note: the accuracy percentages are vendor-published and self-interested; no disinterested third-party audit was found, so they are reported as vendor claims, not established fact.

## Conflicting views
- **"Which volume is right?"** There is no right number — GKP (broad-match, 12-mo avg, advertiser-oriented) and clickstream tools (panel-sampled, variant-ungrouped) optimise for different use cases. Practitioners generally prefer third-party tools for SEO because GKP's bucketing and variant-grouping make it "often overestimated and inaccurate for a single word or phrase" (S146), while tool vendors note GKP remains the closest thing to a Google-sourced baseline (S144).
- **KD scale semantics.** Ahrefs and Moz publish 0–100 scales; Ahrefs' is explicitly non-linear (RD count explodes at high KD), Semrush uses a percentage, and Moz weights by projected CTR. A "KD 40" in one tool is not comparable to "40" elsewhere.
- **Top-3 vs top-10.** Ahrefs KD targets top-10 only and "doesn't take into account any on-page factors" (S141); some practitioners mistakenly read it as a #1 probability. No tool models the full ranking system.
- **Personal vs general difficulty.** Semrush's PKD (difficulty *for your domain*) directly contradicts the idea of one universal difficulty number (S142).

## Common mistakes
- **Treating volume as traffic.** High volume ≠ visits; zero-click results, ads, and SERP features eat clicks. Use Traffic Potential / estimated clicks instead (S144, S143).
- **Relying on one tool's number.** A single source can be off by 8×; cross-check and use volume for relative ordering (S146).
- **Using GKP ranges as precise.** "1K–10K" is a bucket, not a measurement; don't bid or plan on the midpoint as fact (S143, S147).
- **Letting KD override intent or content quality.** KD is a link/authority proxy; a well-matched, high-quality page can win a "hard" term, and a thin page will lose an "easy" one (S141, S142).
- **Ignoring location/seasonality.** Planning around a 12-month average for a spiking or seasonal term misallocates effort (S146, S143).
- **Confusing GKP "Competition" with KD.** GKP's Competition column describes *paid* auction density, not organic difficulty (S141).
- **Replacing SERP analysis with a score.** Every vendor states the score is only a first filter; skipping manual inspection of the actual top 10 is the most common misuse (S141, S142, S145).

## Further reading
- S147 — Google Ads Help, "About Keyword Planner forecasts / historical metrics" (support.google.com/google-ads/answer/3022575) — Tier 1: 12-month average monthly searches, historical vs forecast metrics.
- S144 — Ahrefs Help Center, "How accurate is keyword search volume in Ahrefs?" (help.ahrefs.com/.../72571) — Tier 2 (first-party): volume sources, GKP grouping/rounding, accuracy study.
- S141 — Ahrefs, "Keyword Difficulty Checker" (ahrefs.com/keyword-difficulty) — Tier 2 (first-party): RD-based KD formula, 0–100 non-linear scale, top-10 scope.
- S142 — Semrush, "What Is Keyword Difficulty?" (semrush.com/blog/keyword-difficulty, Dec 2024) — Tier 2: six-factor KD %, Personal KD.
- S145 — Moz, "Keyword Difficulty Checker" (moz.com/tools/keyword-difficulty) — Tier 2 (first-party): PA/DA + CTR-weighted Difficulty.
- S143 — Semrush, "What Is Keyword Search Volume?" (semrush.com/blog/keyword-search-volume, Feb 2026) — Tier 2: volume definition, GKP ranges, AI-volume distinction.
- S146 — Practical Ecommerce, "Keyword Volume: Google vs. Semrush vs. Ahrefs" (practicalecommerce.com, Nov 2024) — Tier 2: concrete cross-tool discrepancies and methodology differences.
- S2 / prior KB — 05-keyword-research/keyword-research.md and clustering.md for intent grouping and one-intent-one-page mapping that turn these metrics into a plan.
