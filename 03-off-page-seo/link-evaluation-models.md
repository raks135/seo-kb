---
title: Link Evaluation Models — PageRank, Link Equity & Topical Relevance
topic_id: 03-off-page-seo/link-evaluation-models
tags: [off-page-seo, pagerank, link-equity, link-juice, topical-relevance, authority, nofollow]
last_updated: 2026-07-18
confidence: robust
sources: [S33, S58, S60, S110, S111, S112, S113, S114, S115]
---

## TL;DR

- Google still uses **PageRank** as one of many ranking signals — it is explicitly named in Google's "guide to Google Search ranking systems" (S33). But PageRank is *one* signal among hundreds, not "the algorithm."
- **Link equity** ("link juice") is the value a followed link passes from a referring page to a target page. Its strength depends on the referring page's own authority, topical relevance to the target, whether the link is crawlable/indexable/followed, the number of competing outbound links, and anchor-text relevance (S111, S113).
- **Topical relevance matters**: links from pages/sites about the same subject, and from prominent (more-clicked) placements, are worth more than off-topic or buried links (S112).
- **Contested**: whether "backlinks are a top-3 ranking factor" depends on whom you ask. Google's Gary Illyes said (2024) links "haven't been a top 3 ranking factor for some time" (S114), walking back a 2016 "top 3" statement. Treat link equity as real but *necessary, not sufficient* — never assert a fixed ranking-weight number.

## Core explanation

A hyperlink is, at its root, a citation. The early web had no good way to separate authoritative pages from spammy ones until Larry Page and Sergey Brin modeled the link graph as a **reputation network**: a page is important if important pages link to it (S110). That model is **PageRank**.

In plain terms: every followed, indexable link casts a vote. The weight of the vote depends on the voter (the referring page) and the context (is the vote topically relevant, prominently placed, and editorial rather than bought?). The cumulative weight a page accumulates is what SEOs call **link equity** or **link juice** (S111).

Precisely:
- **PageRank (original, 1998)** models a "random surfer" who clicks links at random. The probability of landing on a page = its PageRank. A damping factor `d` (traditionally 0.85) models the chance the surfer gets bored and jumps to a random page. The score is computed iteratively across the whole link graph until it stabilizes (S110). See the worked example below.
- **Link equity** is the *operational* concept SEOs use for "how much ranking value does this specific link pass." It is not a single published number; it is an umbrella for the many signals Google derives from a link (authority of source, relevance, placement, crawlability, follow state) (S111, S113).
- **Topical relevance** is the degree to which the linking page's subject matches the target's subject. Google has described several mechanisms that weight links by relevance: *topic-sensitive PageRank* (seed pages grouped by topic propagate topic-specific score), the *reasonable surfer* model (links more likely to be clicked — prominent, relevant — carry more weight), and *phrase-based indexing* (related phrases on source and target raise the link's relevance score) (S112).

Important: Google's production ranking system is **not** the 1998 algorithm. PageRank is one input to a much larger machine-learned system (S33). The teaching code below reproduces the original math for intuition only.

## Mechanics / how-to

### What makes a link pass more equity (consensus factors)
Synthesized from Ahrefs (S111) and ReputationX (S113):

1. **Referring-page authority** — a link from a high-authority page passes more than one from a low-authority page. We can't see Google's PageRank, so tools estimate it (Ahrefs URL Rating, Moz DA/PA, Semrush Authority Score). These are *proxies*, not Google's number (S111).
2. **Topical relevance** — a dog-food page links to a dog-diet page with more effect than a gardening page would (S111, S112).
3. **Site-wide authoritativeness / trust** — reputation of the linking domain and its creators (S111).
4. **Crawlable + indexable + canonical + followed** — a `noindex`, `robots`-blocked, non-canonical, or `nofollow`/`sponsored`/`ugc` link does **not** pass ranking credit (S111; see nofollow-as-hint nuance below).
5. **Number of competing outbound links** — classic model: a page's passable equity is split across its outbound links, so each additional link dilutes the share. *Caveat:* Google's Gary Illyes has said the real model is **not a simple equal division** by link count; the simplification is a useful approximation only (S114 context; see Conflicting views).
6. **Anchor-text relevance** — descriptive, topically-matching anchor text gives Google context about the target (S58, S112).
7. **Placement / click-likelihood** — links in prominent, likely-clicked positions (vs. footers, widgets, hidden blocks) carry more weight under the reasonable-surfer model (S112).

### Internal vs external links
Both internal and external followed links pass equity (S111). External links from other sites signal third-party trust and generally carry more weight than your own internal links; internal links are mainly a navigation/architecture tool but are essential for distributing equity to deep pages (S113).

### Nofollow / sponsored / ugc — the hint model
Since 2019, `rel="nofollow"`, `rel="sponsored"`, and `rel="ugc"` are treated as **hints**, not directives (S60). Google *may* still consider or crawl such links. Practical consequence: the old "PageRank sculpting" trick — spraying `nofollow` across internal links to concentrate equity on a few pages — **no longer works as designed**, because Google treats the hints as optional (S60). Use `nofollow`/`sponsored` for links you don't vouch for (ads, sponsored, comments), not as an equity funnel.

### Checklist: is this link actually helping?
- [ ] Is the referring page indexed and not `noindex`/canonical to elsewhere?
- [ ] Is the link `follow` (not `nofollow`/`sponsored`/`ugc` unless it's a paid/UGC link)?
- [ ] Is the referring page itself topically relevant to my target?
- [ ] Is the anchor text descriptive and natural (not stuffed)?
- [ ] Is the link in a place a real user would click (not a hidden footer/widget)?
- [ ] Is the referring domain trustworthy (not a PBN/link farm)?

## Worked example / code

The original PageRank iterative algorithm (power iteration) with damping factor `d = 0.85`, reproduced in stdlib Python. **Teaching model only** — it shows the intuition (votes weighted by voter importance, divided among outlinks, with a random-jump floor), not Google's secret production system.

```python
# PageRank teaching model — Python 3.8+ (stdlib only).
# Reproduces the 1998 Page/Brin random-surfer model for intuition.
# Google's live system is far more complex and NOT public.
from collections import defaultdict

def pagerank(graph, damping=0.85, iterations=50, tol=1e-9):
    # graph: dict page -> list of outlinked pages
    nodes = set(graph)
    for outs in graph.values():
        nodes.update(outs)
    nodes = list(nodes)
    n = len(nodes)
    rank = {p: 1.0 / n for p in nodes}

    for _ in range(iterations):
        new_rank = {p: (1 - damping) / n for p in nodes}
        for p in nodes:
            outs = graph.get(p, [])
            if not outs:                       # dangling node: spread to all
                share = damping * rank[p] / n
                for q in nodes:
                    new_rank[q] += share
            else:                              # distribute to outlinks
                share = damping * rank[p] / len(outs)
                for q in outs:
                    new_rank[q] += share
        delta = sum(abs(new_rank[p] - rank[p]) for p in nodes)
        rank = new_rank
        if delta < tol:
            break
    return rank

if __name__ == "__main__":
    graph = {
        "A": ["B", "C"],
        "B": ["C"],
        "C": ["A"],
        "D": ["A", "C"],   # D is a strong "hub" pointing at A and C
    }
    for p, r in sorted(pagerank(graph).items(), key=lambda x: -x[1]):
        print(f"{p}: {r:.4f}")
    # Typical output (order may vary slightly): C and A highest, D moderate, B lowest.
```

Run with `python3 link-evaluation.py`. The takeaway: a page that many *important* pages link to (here C, linked by A, B, and D) accumulates the most score; adding more outlinks from a page reduces each individual share.

## Assumptions & limitations

- **You cannot measure link equity directly.** There is no public Google PageRank score (the Toolbar PR was discontinued in 2016, S113). Third-party metrics (UR, DR, DA, PA) are *estimates* built on their own link indexes — useful for comparison, not ground truth (S111).
- **The "divided by number of outlinks" rule is a simplification.** Google has stated the real model is more nuanced than equal division (S114). Don't over-engineer internal-link sculpting on the assumption of exact division.
- **Correlation is not causation.** Pages with more referring domains tend to rank higher (large Ahrefs correlation studies), but that does not prove links *cause* the ranking — better content attracts both links and rankings (S111, S115).
- **Google changes how links are weighted.** Machine-learning relevance signals (BERT, MUM, neural matching) now carry more weight than in the early 2000s (S114). Link equity is a *table-stakes* signal, not a guaranteed ranking lever.
- **A single link rarely moves the needle.** Authority accumulates across a profile of many relevant, trustworthy links (S113).

## Empirical evidence

- **Google still lists PageRank.** PageRank appears by name in Google's official "guide to Google Search ranking systems" (S33) — direct confirmation it remains part of the stack. Strength of evidence: strongest (first-party).
- **Large-scale correlation.** Ahrefs' studies of hundreds of millions of pages consistently show a positive correlation between the number of *referring domains* and ranking position; the same studies stress correlation ≠ causation (S111, S115). Sample: very large, but English/web-index biased and proprietary methodology.
- **Topical relevance is supported by concept papers and patents.** Topic-sensitive PageRank (Haveliwala) and the reasonable-surfer / phrase-based-indexing ideas are documented in Moz's synthesis of Google patents and research (S112). These are *patents and research papers*, not statements that the exact mechanisms ship today — treat as directional.
- **"Links no longer top-3."** Search Engine Land reports Gary Illyes (2024) stating links "haven't been a top 3 ranking factor for some time," contrasting a 2016 statement by Andrey Lipattsev that links, content, and RankBrain were the top 3 (S114). This is a direct Googler statement but is informal (podcast/interview), and "top 3" is a fuzzy, shifting category.
- **A 2024 leak** of internal Google API documentation (not an official release) reportedly contained PageRank-like signals, but this is an unverified leak, not a Google confirmation — cited here only as a weak corroborating data point (S113 mentions it).

## Conflicting views

- **"Links are a top-3 ranking factor" — CONTESTED.** 2016: Lipattsev (Google) named links as a top-3 factor. 2024: Illyes (Google) said they have *not* been top-3 "for some time" (S114). Resolution: both are Googlers speaking informally over different eras; the safe, defensible statement is "links/PageRank remain a real ranking signal but are one of many, and Google says their relative weight has declined vs. ML relevance signals." Do **not** assert a specific rank.
- **"Equity is split equally by outlink count" — SIMPLIFIED/FOLKLORE-ish.** The textbook formula divides by outlink count, but Google reps say the live model isn't a clean division (S114). Use the division as a rough mental model, not a precise lever.
- **"PageRank is dead."** False — it is explicitly in Google's ranking-systems guide (S33) and Googlers confirm it's still used (S115). What died is the *public, manipulable* Toolbar score and the idea that link-count alone wins.
- **"Use nofollow to sculpt PageRank."** Obsolete since the 2019 hint-model change (S60). Mark as folklore.
- **Anchor-text optimization.** A weak-but-real relevance signal; over-optimized exact-match anchors trigger spam demotion. No published "safe ratio" exists (see anchor-text-link-velocity.md). Moz frames natural variation as the safe approach (S112).

## Common mistakes

1. **Chasing PageRank/Toolbar numbers.** The public Toolbar PR is gone (2016); any "PageRank checker" is a proxy or fiction. Don't optimize for a number you can't see (S113).
2. **Buying links to manufacture equity.** Paid links that pass ranking credit violate Google's link-spam policy; qualify them with `rel="sponsored"`/`nofollow` or risk manual action (see link-schemes.md). Google's SpamBrain detects buyers and sellers at scale (S33, S115).
3. **Nofollow-sculpting internal links.** Wasting effort since nofollow became a hint (S60).
4. **Ignoring topical fit.** A high-DA but off-topic link passes less value than a relevant, trustworthy one (S111, S112).
5. **Linking out "to lose equity."** You do **not** lose your own equity by linking out; linking to good sources is normal, helpful practice (S111). Only spammy outbound linking patterns risk manual penalties.
6. **Treating a single big link as a ranking fix.** Authority is cumulative and contextual; one link rarely changes rankings (S113).
7. **Over-optimizing anchor text.** Natural, varied anchors beat keyword-stuffed exact match (S112; see anchor-text-link-velocity.md).

## Further reading

- **S33** — Google, "A guide to Google Search ranking systems" (developers.google.com/search/docs/appearance/ranking-systems-guide) — Tier 1. Confirms PageRank is still a named system.
- **S110** — Page, L. & Brin, S. (1998), "The PageRank Citation Ranking: Bringing Order to the Web" (Stanford technical report) — Tier 1 primary. Original algorithm, damping factor 0.85.
- **S111** — Ahrefs, "Link Equity" glossary (ahrefs.com/seo/glossary/link-equity) — Tier 2. 7 factors; "can't measure, only estimate"; internal vs external.
- **S112** — Moz / Cyrus Shepard, "Topical SEO: 7 Concepts of Link Relevance" (moz.com/blog/link-relevance-seo) — Tier 2. Anchor text, hub/authority, reasonable surfer, topic-sensitive PageRank, phrase-based indexing.
- **S113** — ReputationX, "Link Equity: What It Is & How Google Calculates It" (reputationx.com/blog/link-equity) — Tier 2. 11 factors; Toolbar PR discontinued 2016; PageRank still active.
- **S114** — Search Engine Land, "Links are not a top 3 Google Search ranking factor, says Gary Illyes" (searchengineland.com/links-google-search-ranking-factor-gary-illyes-432422) — Tier 2. Contested "top-3" claim.
- **S115** — Ahrefs, "The Evolution Of Google PageRank" (ahrefs.com/blog/google-pagerank) — Tier 2. History; Googlers confirm PageRank still used; links feed E-E-A-T.
- **S58** — Google Search Central, "Link best practices" (developers.google.com/search/docs/crawling-indexing/links-crawlable) — Tier 1. Anchor-text guidance.
- **S60** — Google Search Central Blog, "Evolving 'nofollow'" (developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) — Tier 1. Hint model; sculpting obsolete.
- Companion articles in this KB: `03-off-page-seo/backlinks.md`, `03-off-page-seo/anchor-text-link-velocity.md`, `03-off-page-seo/link-schemes.md`, `02-on-page-seo/eeat.md`.
