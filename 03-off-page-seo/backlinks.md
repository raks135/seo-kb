---
title: Backlinks, PageRank & Link Quality (and what Google penalizes)
topic_id: 03-off-page-seo/backlinks
tags: [off-page, backlinks, pagerank, link-quality, authority]
last_updated: 2026-07-18
confidence: robust
sources: [S2, S20, S22, S8]
---

## TL;DR
Links remain a core signal of relevance and reputation: Google uses link analysis (descended from PageRank) as one of many ranking factors. Quality beats quantity — links from relevant, trustworthy, editorially-given sources help; manipulative link schemes (buying links, PBNs, excessive exchanges) violate spam policies and can trigger manual actions or algorithmic demotion.

## Core explanation
A link is a vote of confidence. Google's original PageRank modeled the web as a graph where a link from a high-authority page passes more "link equity." Modern link evaluation is far more nuanced — relevance, anchor text, placement, and the linked page's trustworthiness all matter. Google has repeatedly stated links are among the top ranking signals, while also warning that correlations between link counts and rankings don't prove causation.

## Mechanics / how-to
- Earn links via genuinely useful, original content (studies, tools, unique data) and digital PR (see 03-off-page-seo/digital-pr).
- Use descriptive, natural anchor text; avoid exact-match over-optimization.
- Disavow only when you have a manual action or clearly unnatural links you can't remove (see 03-off-page-seo/link-schemes).
- Audit your link profile periodically (Ahrefs/Semrush/Majestic) for toxic patterns.

## Worked example / code
Conceptual PageRank (simplified): a page's score = sum of (neighbor score / out-degree). Not the live formula, but illustrates equity dilution as outbound links increase.
```python
# Toy PageRank (10 iterations) — illustrative only
scores = {p: 1.0 for p in pages}
for _ in range(10):
    new = {p: 0.15 for p in pages}
    for p in pages:
        share = scores[p] / max(1, len(outlinks[p]))
        for q in outlinks[p]:
            new[q] += 0.85 * share
    scores = new
```

## Assumptions & limitations
- "Backlinks are a top-ranking factor" is Google's stance and is corroborated by correlation studies (Ahrefs/Moz, S20/S22), but correlation ≠ causation.
- Link equity is not a public, exact metric; third-party "authority" scores (DA/DR) are proprietary proxies, not Google's internals.
- Paid links that pass PageRank must carry `rel="sponsored"` or `rel="nofollow"` (S8).

## Empirical evidence
- Ahrefs large-scale correlation studies (S20) consistently find a positive correlation between referring domains and organic traffic — strong but correlational.
- Google's "How Search works" lists "relevance" signals including links and reputation (S2).
- Moz's linkage data (S22) shows domain-level link metrics correlate with rankings.

## Conflicting views
- Some claim "links are dead" after various updates; Google and correlation data still show links matter, though content quality and intent-matching have risen in relative importance.
- "Domain Authority predicts rankings" — useful as a relative comparator, not a Google metric (S22 caveat).

## Common mistakes
- Buying links that pass PageRank without `rel="sponsored"`/`nofollow` (violates S8).
- PBNs and link wheels.
- Over-optimized exact-match anchors at scale.
- Chasing volume over relevance.
- Ignoring toxic backlinks until a manual action arrives.

## Further reading
- S2 — Google, "How Search works" — Tier 1
- S8 — Google, "Spam policies" (link schemes) — Tier 1
- S20 — Ahrefs Blog (link studies) — Tier 2
- S22 — Moz (link metrics, Beginner's Guide) — Tier 2
