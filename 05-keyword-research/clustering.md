---
title: Keyword Clustering & Mapping to Pages
topic_id: 05-keyword-research/clustering
tags: [keyword research, clustering, SERP overlap, search intent, keyword mapping, cannibalization]
last_updated: 2026-07-18
confidence: robust
sources: [S134, S2, S4, S136, S137, S138, S139, S140]
---

## TL;DR
Keyword clustering is the practice of grouping search queries that share the same search intent and targeting each group on a single page (primary + secondary keywords), rather than building one thin page per keyword. The most defensible clustering signal is **SERP overlap** — if Google already ranks the same pages for two queries, they almost certainly share intent and belong on one URL. Map one cluster → one page; when two of your own pages target the same intent, you trigger keyword cannibalization and dilute rankings. Google has never specifically endorsed "clustering" as a tactic — it is an SEO framework that operationalizes Google's long-standing guidance to organize content by clear topic and hierarchy (S134) and avoid serving multiple near-duplicate pages for one query.

## Core explanation
**In plain terms:** A keyword list is just a flat list of strings. Clustering reshapes it into meaningful groups so you can plan pages. If "king size mattress," "king mattress," and "large king bed" all mean the same thing to a searcher, you should write *one* strong page that covers all of them — not three competing pages.

**Precisely:** Keyword clustering = partitioning a keyword set K into clusters C = {c₁, c₂, …} such that, for any two keywords kᵢ, kⱼ in the same cluster, their underlying search intent is equivalent (the user's underlying goal is the same). Each cluster is then assigned to exactly one target URL, where one keyword is the primary (highest volume / strategic) target and the rest are secondary targets woven into the same content (S136, S138). The canonical rule of thumb from practitioners is: **one search intent = one cluster = one page** (S138).

Why this aligns with how Google ranks: Google ranks *pages*, not keywords, and a single well-built page can rank for hundreds or thousands of related queries (Semrush illustrates a page ranking for ~2,200 keywords and drawing an estimated 183,100 US organic visits/month, S136). Clustering is simply the keyword-research step that sets you up to earn that behavior instead of fragmenting it.

## Mechanics / how-to

### Step 1 — Build a keyword list
Start from a seed term and expand with a keyword tool (Google Keyword Planner, Semrush Keyword Magic Tool, Ahrefs Keywords Explorer) and competitor gap analysis. Export each term with: intent class, monthly volume, and a difficulty metric (S136).

### Step 2 — Choose a clustering method
There are four practical methods; the first two are the most reliable.

1. **SERP-overlap clustering (recommended).** For each keyword, capture the set of top-N ranking URLs. If two keywords return largely the same URL set, they share intent → same cluster (S137, S138). This mirrors how Google actually groups queries; it is the method used by dedicated tools such as Keyword Insights and SE Ranking's Keyword Grouper (S138).
2. **Parent-Topic clustering (Ahrefs).** The "parent topic" of a keyword is the query that sends the most traffic to the top-ranking page for that keyword. Keywords sharing a parent topic are clustered together (S137). Ahrefs' own test found its parent-topic method agreed with a SERP-URL-overlap tool on over half of the top 25 clusters (e.g., 38 of 40 keywords in the "best espresso beans" cluster matched, S137).
3. **Morphological / term clustering.** Group by shared words, stems, or n-grams (e.g., "hotels near beach," "hotels downtown," "hotels airport" all stem from "hotels"). Useful for discovering niches and trends, but it keys on *words*, not *intent*, so it can misgroup (S138, S137 "Cluster by terms").
4. **Semantic / embedding similarity.** Vectorize keywords (e.g., word2vec / transformer embeddings) and cluster by cosine distance. Powerful at scale but a black box; verify with a SERP check before committing.

**Manual vs automated:** Manual SERP review gives precise control and is fine for clustering a handful of terms onto one page; automated clustering is necessary for lists of hundreds or thousands of keywords and for new-site planning (S138).

### Step 3 — Map clusters to pages (keyword mapping)
Create a keyword map (spreadsheet) with columns: cluster name, primary keyword, secondary keywords, intent, volume, difficulty, and **target URL**. For each cluster:
- If an existing page already covers the intent → optimize it (add the secondary terms naturally).
- If not → create a new page.
- Ensure **no two pages own the same intent** — that is the cannibalization guardrail (S139).

### Step 4 — Detect and fix cannibalization
Keyword cannibalization = two or more of your pages target the same keyword *and* the same intent, so they compete and typically all rank lower (S139). Detection: GSC Performance report (filter a query → Pages, or a page → Queries), a site:`site.com "keyword"` SERP check, or a cannibalization report in a tool. Fixes, in order of preference (S139):
- **Merge** the weaker pages into one comprehensive page (best for consolidating link equity).
- **Canonicalize** the duplicates to the strongest version (`<link rel="canonical" href="…">`, S4).
- **Differentiate intent** and use descriptive internal anchor text so each page clearly serves a distinct query (S2, internal-linking guidance).
- **Noindex** genuinely low-value variants.

## Worked example / code
Reproducible SERP-overlap clustering using a greedy single-linkage algorithm over Jaccard similarity of top-result URL sets. Stdlib only; runs on Python 3.8+. Input is `{keyword: set(top_N_result_urls)}` — you supply the URLs from a SERP scraper or tool export.

```python
#!/usr/bin/env python3
"""SERP-overlap keyword clustering (greedy single-linkage).
Rationale: if Google ranks the same pages for two queries, they likely
share search intent and can be targeted on one page (S137, S138).

Requires: Python 3.8+. No third-party deps (stdlib only).
Input:    {keyword: set(top_N_result_urls)}.
"""
from __future__ import annotations
from collections import defaultdict

def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def cluster_by_serp_overlap(results: dict[str, set[str]],
                            threshold: float = 0.5) -> list[list[str]]:
    """Two keywords join one cluster if their URL sets overlap >= threshold.
    threshold ~0.5 ≈ 'about half the same top results' (S137: 'similar').
    """
    parent = {k: k for k in results}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    keys = list(results)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if jaccard(results[keys[i]], results[keys[j]]) >= threshold:
                union(keys[i], keys[j])

    clusters: dict[str, list[str]] = defaultdict(list)
    for k in keys:
        clusters[find(k)].append(k)
    return list(clusters.values())

if __name__ == "__main__":
    # Toy example: top-10 result URL sets (illustrative, not real data).
    SERP = {
        "best coffee maker": {"pageA", "pageB", "pageC", "pageX"},
        "best coffee maker for home": {"pageA", "pageB", "pageC", "pageY"},
        "coffee maker reviews": {"pageA", "pageB", "pageC", "pageZ"},
        "buy coffee beans online": {"shop1", "shop2", "shop3"},
        "coffee bean subscription": {"shop1", "shop2", "shop4"},
        "how to brew espresso": {"guide1", "guide2", "guide3"},
    }
    for idx, c in enumerate(cluster_by_serp_overlap(SERP, 0.5), 1):
        print(f"Cluster {idx}: {sorted(c)}")
```

Expected output groups the three "coffee maker" queries together, the two "coffee bean" queries together, and leaves "how to brew espresso" as its own cluster — exactly the one-intent-one-page mapping you want. Tune `threshold` (0.3–0.7) to your SERP depth and how aggressively you merge.

## Assumptions & limitations
- **Google has not published a "clustering" algorithm or endorsed the technique by name.** Clustering is an SEO-created workflow that implements Google's first-party advice to organize content around clear topics/hierarchy and avoid multiple near-duplicate pages for one query (S134, S4). Treat ranking gains as a by-product of clearer structure + comprehensive intent coverage, not a confirmed "clustering" signal.
- **Clustering is interpretive, never "perfect."** Ahrefs explicitly notes results are "almost always open to interpretation" (S137): e.g., "best chocolate cake recipe with coffee" was grouped under "chocolate cake" by tools, yet the coffee variant had far weaker competition (avg DR 33 / 11 linking domains vs 74 / 318) — clustering them would have been a mistake. Always sanity-check with competition metrics (S137).
- **The mechanism is correlation, not proven causation.** A page ranking for many terms does not prove clustering *caused* the rankings; comprehensive, intent-matched content and links likely drive both.
- **SERP overlap depends on SERP stability and location.** Capture top-N for a fixed locale; SERPs personalize and shift (S134 context).
- **Volume is additive only within a cluster, not a guaranteed traffic sum** — you win the cluster's combined potential only if the page actually ranks (S136).

## Empirical evidence
- **Illustrative, not controlled:** Semrush's example page (ranks for ~2,200 keywords, ~183,100 estimated US organic visits/month, S136) and Ahrefs' parent-topic/overlap-tool agreement (over half of top 25 clusters matched; 38/40 keywords in one cluster, S137) demonstrate the *mechanism* works in practice but are single-site anecdotes, not experiments with control groups.
- **Cannibalization is widely observed** across practitioner sources (Surfer, Yoast, Neil Patel, SEmonitor) as a real ranking drag caused by self-competition and split link equity (S139). The fix (merge/canonical/differentiate) is consensus, though quantified lift studies are vendor case studies, not blind trials.
- **Strength of evidence:** moderate. The intent-matching logic is sound and corroborated by how Google serves pages; the *traffic* payoff is plausible and commonly reported but not established by peer-reviewed causal studies. No sample-size claims (e.g., "clustering lifts traffic by X%") are asserted here because no primary controlled study was found.

## Conflicting views
- **Method priority.** Practitioners agree intent is the goal but disagree on the best proxy. Ahrefs argues SERP/parent-topic overlap is the only reliable proxy (S137); SE Ranking presents morphological and SERP methods as co-equal (S138). Use SERP overlap as the arbiter when they disagree.
- **"One page per cluster" vs. "one page per subtopic."** A strict one-intent-one-page rule can over-merge distinct subtopics (the chocolate-cake-with-coffee example, S137). Pragmatic practice: merge when intent *and* competition profile match; split when a subtopic has its own audience and weaker competition.
- **Clustering as an AI-search lever.** Some sources now frame secondary cluster terms as "fan-out queries" that help visibility in ChatGPT/AI Overviews (S136); this is emerging and not confirmed by any Google primary source — treat as a hypothesis, not a ranking guarantee.
- **Topic clusters vs. keyword clusters.** "Topic clusters" (pillar + spokes) are a site-architecture extension of clustering (covered separately in content-hubs.md); both share the same intent-grouping core but differ in whether they mandate a pillar/linking structure.

## Common mistakes
- **One keyword = one thin page.** The anti-pattern clustering exists to prevent; it fragments authority and invites cannibalization (S136, S139).
- **Merging by string similarity alone.** "apple cider vinegar for dog shampoo" (informational) vs. "apple cider vinegar shampoo for dogs" (commercial) look alike but have different intent — Google tells them apart (S136). Always verify intent, not just words.
- **Ignoring cannibalization after publishing.** As sites grow, similar posts compete; audit GSC periodically and consolidate (S139).
- **Trusting the tool blindly.** Automated clusters need a human intent + competition check; the chocolate-cake example shows tools misfire (S137).
- **Keyword stuffing the secondary terms.** Weaving 40 synonyms unnaturally triggers spam policies and hurts readability; cover them in genuinely useful sections (S134, S2).
- **Assuming combined volume = combined traffic.** You only capture the cluster's potential if the page earns rankings (S136).

## Further reading
- Google Search Essentials — organize content by clear topic/hierarchy; avoid duplicate/near-duplicate pages (S134, Tier 1).
- Google "Consolidate duplicate URLs with canonicals" (S4, Tier 1).
- Semrush, "How to Do Keyword Clustering & Why It Helps SEO" (S136, Tier 2) — workflow, intent classes, AI/fan-out angle.
- Ahrefs, "How To Do Keyword Clustering the Easy Way" (S137, Tier 2) — SERP/parent-topic method, real tool comparison, caveats.
- SE Ranking, "Keyword Clustering: The Ultimate Guide" (S138, Tier 2) — morphological vs SERP methods, one-intent-one-page rule.
- SurferSEO, "What Is Keyword Cannibalization?" (S139, Tier 2) — detection + 5 fixes.
- Search Engine Land, "The complete guide to topic clusters and pillar pages" (S140, Tier 2) — pillar/cluster extension.
- Related KB articles: 05-keyword-research/keyword-research.md (intent taxonomy), 04-content-strategy/content-hubs.md (pillar + cluster architecture), 01-technical-seo/site-architecture.md (internal linking).
