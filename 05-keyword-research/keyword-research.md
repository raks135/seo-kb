---
title: Keyword Research & Search Intent (taxonomy, long-tail, difficulty, clustering)
topic_id: 05-keyword-research/keyword-research
tags: [keyword-research, intent, long-tail, difficulty, clustering]
last_updated: 2026-07-18
confidence: robust
sources: [S20, S21, S22, S1]
---

## TL;DR
Keyword research is the practice of discovering the words and questions your audience uses, then grouping them by **search intent** and mapping them to the right pages. Prioritize intent fit and realistic difficulty over raw volume; long-tail and question queries often convert better and are easier to rank.

## Core explanation
A "keyword" is a proxy for a need. The job is to infer the *intent* behind the query and whether your content can satisfy it. Volume and difficulty are estimates from third-party tools, not Google's own numbers.

## Intent taxonomy
- **Informational:** "how to…", "what is…" → guides, explainers.
- **Navigational:** brand/product names → home, login.
- **Commercial:** "best…", "vs…", reviews → comparisons, lists.
- **Transactional:** "buy…", "coupon" → product/service pages.

## Mechanics / how-to
1. Seed from your business + autocomplete/related searches/"People also ask".
2. Pull volumes & difficulty from a tool (Ahrefs, Semrush, Moz — S20/S21/S22).
3. Tag each term with intent.
4. Cluster by topic (see 05-keyword-research/clustering) and map to existing or new URLs.
5. Filter by business value, not just volume.

## Worked example / code
Simple intent tagging in Python (heuristic):
```python
def tag_intent(kw):
    kw = kw.lower()
    if any(w in kw for w in ["buy","coupon","price","order"]): return "transactional"
    if any(w in kw for w in ["best","vs","review","top"]): return "commercial"
    if any(w in kw for w in ["how","what","why","guide"]): return "informational"
    return "navigational"  # fallback; manual review needed
```

## Assumptions & limitations
- Search volume is a tool estimate with sampling error; "not provided" hides query data in analytics.
- Difficulty scores are proprietary and tool-specific; they predict competition, not guaranteed rank.
- Keyword stuffing and exact-match obsession ignore Google's synonym understanding (S1).

## Empirical evidence
Ahrefs/Semrush/Moz publish methodology notes (S20/S21/S22) showing volumes derived from click-stream panels — representative but not exact. Long-tail traffic share is well documented in practitioner studies (Tier 2).

## Conflicting views
- **"Exact-match domains/keywords win."** Google: keywords in domain/path have minimal ranking effect beyond breadcrumbs (S1).
- **"Volume is the main priority."** Intent fit and conversion value usually matter more than volume.

## Common mistakes
- Targeting a keyword with the wrong content type (intent mismatch).
- Chasing unwinnable head terms.
- Ignoring long-tail/question queries.
- Mapping multiple intents to one page.

## Further reading
- S20 — Ahrefs Blog (keyword data/methodology) — Tier 2
- S21 — Semrush Blog — Tier 2
- S22 — Moz, Beginner's Guide to SEO — Tier 2
- S1 — Google, "SEO Starter Guide" — Tier 1
