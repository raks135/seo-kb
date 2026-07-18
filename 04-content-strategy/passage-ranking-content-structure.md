---
title: Passage Ranking & Content Structure
topic_id: 04-content-strategy/passage-ranking-content-structure
tags: [passage-ranking, content-structure, indexing-vs-ranking, featured-snippets, subtopics, BERT, long-form-content]
last_updated: 2026-07-18
confidence: robust
sources: [S123, S124, S125, S126, S127, S128, S33, S70, S71, S72, S73, S52, S2]
---

## TL;DR
- **Passage ranking is a ranking change, NOT an indexing change.** Google still indexes whole pages; it additionally scores *passages* (sections) within a page as an extra ranking signal (S124). Early "passage indexing" framing was misleading — Google's own liaison corrected it.
- It targets the long, diluted page whose buried sentence answers a very specific query. It launched US-English on 2021-02-10 (fully rolled out 2021-02-15) and Google said it would reach ~7% of queries globally as it rolls out (S123, S125).
- **There is nothing to "optimize."** Google's Martin Splitt says publishers need make no changes; anyone selling "passage-ranking optimization" is capitalizing on a small internal change (S126). Good, well-structured pages are effectively unaffected (S127).
- Practical content-structure advice still holds: clear descriptive headings, self-contained answer-first passages, and logical sectioning help comprehension generally — but treat these as people-first best practice, not a confirmed passage-ranking lever.

## Core explanation
Plain language: Before passage ranking, a page was largely judged as one unit. If your 4,000-word guide to tomato gardening buried a perfect one-sentence answer to "how to prune indeterminate tomatoes" on page 3, that page might never surface for that specific query. Passage ranking lets Google identify *that sentence/section* as relevant and rank the whole page for the query because of it.

Precise: Passage ranking is an additional scoring signal applied *after* a page is crawled and indexed as a whole. Google's official liaison stated it explicitly:

> "This change doesn't mean we're indexing individual passages independently of pages. We're still indexing pages and considering info about entire pages for ranking. But now we can also consider passages from pages as an additional ranking factor." — Google SearchLiaison (S124)

The original "Search On" announcement described it as a "breakthrough in ranking" that lets Google "better understand the relevancy of specific passages... in addition to the relevancy of the overall page" (S123). Martin Splitt (Google) insisted the accurate name is **Passage Ranking**, not "Passage Indexing" (S126).

Two sibling features were announced at the same event and are frequently confused with it:
- **Subtopics** — a *query-understanding* improvement that diversifies results for *broad* queries (e.g., "home exercise equipment" → budget / premium / small-space). It is "a way of understanding things," not a ranking thing (S123, S126).
- **Featured snippets** — a *separate* system that pulls a self-contained answer into an "instant answer" box. Passages, by contrast, rank the whole page as a normal blue link; the relevant section is just *why* it ranks (S126, S127).

## Mechanics / how-to
There is no "passage markup," no tag, and no setting. The mechanism lives entirely inside Google's ranking systems. What you can do is write content that is easy to understand at the section level:

1. **Use clear, descriptive headings (H2/H3).** Splitt: "With any kind of content some semantic and structure... makes it easier for automated systems to understand the structure and the bits and pieces of your content. But even if you would not do that we would still be able to say... this part of the page is relevant to this query" (S126). Headings are a best practice for comprehension — note they are *not* a per-level ranking factor (S70, S71; MDN S72, S73). Don't keyword-stuff headings.
2. **Write answer-first passages.** Put the direct answer or definition near the top of its section, then elaborate. Burying the answer deep in a long paragraph is exactly the failure mode passage ranking was built to rescue — but rescue is not guaranteed, and self-contained answers also help featured-snippet eligibility and readers.
3. **Keep sections focused, not diluted.** Passage ranking specifically helps "long-winded pages that are having a hard time ranking for anything, really because everything is so diluted" (S126). If a page tries to cover 40 unrelated long-tail queries, consider splitting into focused pages/hub-and-cluster (see content-hubs.md).
4. **Don't pad for passage ranking.** Splitt warned against rewriting content to "target" passages; the change "is pretty much not for you" if you already structure content well (S126).
5. **FAQ schema is not a passage lever.** FAQ rich results have been restricted to well-known authoritative gov/health sites since Aug 2023 (S52); answering questions in ordinary prose is what helps comprehension, not the schema.
6. **Ecommerce caveat.** Category/product pages with little prose "don't really benefit" from passage ranking — there isn't enough textual passage content (S126).

## Worked example / code
A reproducible, stdlib-only structural audit that flags sections likely to be poorly understood by passage-level systems (non-descriptive headings, over-long diluted sections, empty sections). Data source: **your own Markdown content** — no external calls. Runs on Python 3.8+.

```python
#!/usr/bin/env python3
"""Passage-readiness structural audit (stdlib only, Python 3.8+).

Reads a Markdown file, splits it into heading-delimited sections, and flags
sections that are likely to be poorly understood by passage-level ranking
systems: missing/non-descriptive headings, over-long diluted sections, and
empty sections.

Data source: the Markdown content you supply. No network calls.
"""
import re
import sys
from dataclasses import dataclass

HEADING_RE = re.compile(r'^(#{2,3})\s+(.+)$', re.MULTILINE)
WORD_RE = re.compile(r'[A-Za-z0-9]+')


@dataclass
class Section:
    level: int
    heading: str
    start: int
    end: int


def split_sections(md: str):
    matches = list(HEADING_RE.finditer(md))
    sects = []
    for i, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        sects.append(Section(level, heading, start, end))
    return sects


def descriptive(heading: str) -> bool:
    h = heading.lower()
    words = WORD_RE.findall(h)
    if len(words) < 2:
        return False
    if re.match(r'^(section|part|step)\s*\d', h):
        return False
    return True


def audit(path: str, max_words: int = 350):
    with open(path, encoding='utf-8') as f:
        md = f.read()
    sects = split_sections(md)
    print(f"File: {path}  |  sections: {len(sects)}")
    issues = 0
    for s in sects:
        body = md[s.start:s.end]
        words = len(WORD_RE.findall(body))
        flag = []
        if not descriptive(s.heading):
            flag.append("non-descriptive-heading")
        if words > max_words:
            flag.append(f"over-long({words}w)")
        if words == 0:
            flag.append("empty-section")
        status = "OK" if not flag else "FLAG:" + ",".join(flag)
        if flag:
            issues += 1
        print(f"  H{s.level} '{s.heading[:48]}' -> {words} words [{status}]")
    print(f"Passage-readiness: {len(sects)-issues}/{len(sects)} sections clean")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: passage_audit.py <file.md>")
        sys.exit(2)
    audit(sys.argv[1])
```

Run: `python3 passage_audit.py your-article.md`. It reports per-section word counts and flags diluted/empty/non-descriptive blocks. This measures *structure*, not ranking — use it as an editorial checklist, not a ranking guarantee.

## Assumptions & limitations
- **Whole-page indexing still applies.** Passage ranking adds a passage-level score; it does not create separately-indexed passages (S124). Claims that Google now has a "passage index" are incorrect.
- **Achievable only for text-rich pages.** Pages without substantial prose (e.g., image grids, faceted category pages) cannot benefit (S126).
- **Initial launch scope.** Live US-English from 2021-02-10, fully rolled out 2021-02-15; Google stated further English-speaking countries and then other languages would follow (S125). **The exact completion date of the non-English rollout is not verified in this article** — Google's blog claimed "~7% of queries across all languages" at full global rollout (S123), but the non-English launch timeline is not confirmed here. (Flagged as a Verify task.)
- **No markup, no toggle, no metric.** GSC exposes no "passage ranking" report. You cannot measure its effect directly on a single site.
- **Google changes things.** Ranking-system behavior evolves; treat specifics as current-to-publication, not permanent.

## Empirical evidence
- **Google's own reach claim:** "~7 percent of search queries across all languages" at full global rollout (S123). This is a first-party estimate, not an independent measurement, and refers to eventual global coverage rather than the US-English launch day.
- **Observed impact was minimal.** Search Engine Roundtable tracked Mozcast, SERPMetrics, RankRanger, and Semrush Sensor around the 2021-02-10 launch and found them "super calm"; Glenn Gabe reported digging in "heavily" and seeing "no major impact"; industry chatter was "pretty much zero" (S127). This is consistent with Google's framing that passage ranking helps sites *not* doing SEO rather than shifting well-optimized sites.
- **Directional read:** SEO-tracking volatility from passage ranking was far smaller than Panda (~11%) or Penguin (~3% of queries) at their launches (S127) — but those comparisons are about *SEO-visible* volatility, not user-facing query coverage, so don't over-read them.
- **Strength/limitations:** The minimal-impact evidence is observational (tool flux + practitioner reports), n=industry, no controlled experiment. Correlation, not proof, that your site is unaffected.

## Conflicting views
- **"Passage indexing" vs "Passage ranking" (naming).** The original blog said Google could "better understand the relevancy of specific passages"; some outlets ran with "passage indexing" implying separate indexing. Google explicitly corrected this (S124) and Splitt pushed the "ranking" name (S126). **Adopt the ranking framing.**
- **Is there something to optimize?** A minority of vendors/agencies market "passage optimization." Google's position (S124, S125, S126) is a flat no — it's an internal change requiring no action, and Splitt laughed off the idea of optimizing for it. Treat any "passage SEO" product as folklore until Google says otherwise.
- **SMITH algorithm linkage.** Some speculate passage ranking runs on Google's SMITH (a long-document transformer that outperforms BERT on passages). Google has **not** confirmed using SMITH for passage ranking; the link is speculative (S128). Do not assert it.
- **Headings as a passage lever.** Headings help comprehension (S126) but are not a per-level ranking factor (S70–S73). Don't conflate "clearer structure aids understanding" with "more H2s = higher rankings."

## Common mistakes
- **Calling it "passage indexing."** It is ranking, not indexing (S124).
- **Buying "passage-ranking optimization."** No such lever exists; Splitt warns not to fall for it (S126).
- **Rewriting good content to "target passages."** Counterproductive; the feature helps diluted/under-optimized pages, not well-structured ones (S126).
- **Assuming it helps every page.** Only long, text-rich, diluted pages with buried answers benefit; thin/ecommerce pages generally don't (S126).
- **Equating it with featured snippets.** Different systems; a passage-ranked result is a normal blue link, not an answer box (S126, S127).
- **Treating 7% as "your traffic will move 7%."** That figure is Google's global query-coverage estimate, and observed site-level volatility was negligible (S123, S127).

## Further reading
- S123 — Google, "How AI is powering a more helpful Google" (blog.google/products/search/search-on/, Oct 15 2020) — Tier 1 primary: passage ranking + subtopics announcement, 7% claim.
- S124 — Google SearchLiaison (@searchliaison), tweet Oct 20 2020 — Tier 1 primary: "ranking, not indexing" correction.
- S125 — Google SearchLiaison (@searchliaison) Feb 11 2021 + Danny Sullivan Feb 18 2021 — Tier 1 primary: US-English launch + full rollout date.
- S126 — Search Engine Journal, "What Is Google Passage Ranking: 16 Key Points" (Roger Montti, interviewing Martin Splitt) — Tier 2: nothing-to-do, agency warning, BERT/featured-snippet/subtopics distinctions.
- S127 — Search Engine Roundtable, "Google Passage Based Ranking Causing Minimal Impact So Far" (Barry Schwartz) — Tier 2: observational low-impact evidence.
- S128 — Ignite Visibility, "The 2021 Guide to Google Passage Ranking" — Tier 2: recap + SMITH speculation (flagged unconfirmed).
- S33 — Google Search Central, "A guide to Google Search ranking systems" — Tier 1: BERT/neural matching/passage as named systems.
- S52 — Google Search Central Blog, "Changes to HowTo and FAQ rich results" — Tier 1: FAQ schema restriction (not a passage lever).
- S70/S71/S72/S73 — headings are not a per-level ranking factor (Mueller/MDN) — referenced from headings.md.
