---
title: Long-Tail & Question Keywords
topic_id: 05-keyword-research/long-tail-question-keywords
tags: [keyword-research, long-tail, question-keywords, people-also-ask, featured-snippets, voice-search, ai-search]
last_updated: 2026-07-18
confidence: robust
sources: [S148, S149, S150, S151, S152, S153, S154, S155, S156, S157, S158, S159, S160]
---

## TL;DR
- Long-tail keywords are defined by **low search volume, not length**. In Ahrefs' US database, ~2.3 billion keywords get fewer than 10 searches/month — almost 93% of the keyword catalog (S148). Google reports ~15% of daily queries are entirely new, so the tail constantly replenishes (S151, S152).
- Question keywords are a high-value slice of the tail. Question-style queries trigger a **People Also Ask (PAA)** box ~86% of the time, and PAA appears on ~49–52% of SERPs (S150).
- They are **easier to rank for on average** but NOT always — some high-volume informational long-tail is as competitive as head terms (S148). Treat "easy + high-converting" as a tendency, not a law.
- Win them with intent-grouped clusters, answer-first structure, judicious FAQ schema, and mining GSC / PAA / autocomplete. There is no long-tail "ranking boost" signal — ranking flows from lower competition + intent match.

## Core explanation
A **long-tail keyword** is a search query with a small number of searches per month (S148, S149). The name comes from the "search demand curve": a tiny number of head terms carry huge volume, while billions of low-volume queries form the long tail. Crucially, *length in words is not the definition* — there are one-word keywords with <100 monthly searches and five-word keywords with hundreds of thousands (S148).

Two metrics are frequently conflated and must be kept distinct:
- **By keyword count:** Ahrefs' US database contains <18,000 keywords with >100k searches/month versus 2.3 billion with <10/month; keywords under 10/month are almost 93% of the catalog (S148).
- **By search-volume share:** the popular claim that "70%+ of searches are long-tail" traces to a Hitwise (2008) study and is restated by agencies today (S157). Its methodology is opaque and dated, so treat it as **directional folklore, not an established fact**. The transparent modern figure is the 93%-by-keyword-count number above.

Google's own data explains why the tail is effectively infinite: **~15% of queries seen each day have never been seen before** (Google's BERT announcement, blog.google; reconfirmed by John Mueller in 2025, S151, S152). AI/conversational search extends the tail further into queries with near-zero measurable volume but real demand (S148).

**Question keywords** are a subset of the tail: queries phrased as questions (what/why/how/where/when/who…) that usually carry informational intent. They are surfaced most visibly through two SERP features:
- **Featured snippets** — Google elevates a page excerpt to "position zero" when it judges the page answers the question well (S153, S154).
- **People Also Ask (PAA)** — an interactive accordion of related questions; question-style queries trigger it ~86% of the time (S150).

## Mechanics / how-to

### 1. Find long-tail & question keywords
- **Google Search Console — your goldmine.** In *Performance → Search results → Queries*, filter with a regex for question words to surface conversational queries you already rank for:
  `^(how|why|what|which|where|when|who|can|is|are|does|do|should|will)\b` (S148). These are the easiest wins — pages already indexed for them need only a content bump.
- **Keyword tools:** Ahrefs Keywords Explorer (use **Parent Topic** to avoid building duplicate pages for "supporting" long-tail variants, S148); Semrush Keyword Magic Tool (27.2B-keyword database; filter Volume 0–1,000 + Personal KD 0–29 + Word count 3+, and use the **Questions** tab, S149); Moz Keyword Explorer questions view (S159).
- **Google autocomplete** — predictions from real searches (personalized, no volumes shown, S149).
- **PAA boxes + bulk question miners** — AnswerThePublic, AlsoAsked, Keywords People Use scrape PAA at scale (S149).
- **Competitor organic rankings** filtered for low-volume / low-difficulty terms (S149).
- **Communities** (Reddit, Quora) for niche questions that never enter keyword databases (S149).
- **AI chatbots** for ideation — but they have no real search data; verify any suggestion against a keyword tool before use (S149).

### 2. Classify the three types of long-tail (S148)
- **Supporting** — a less-popular phrasing of a head topic (e.g. "best healthy treats for dogs" ≈ "healthiest dog treats"). Target with the *one* parent page; don't spin up separate pages.
- **Topical** — a genuinely distinct subtopic ("fly bites on dogs' ears"). Warrants a dedicated page.
- **Conversational** — AI-synthesized sub-queries with ~0 measurable volume but real demand. Cover them by thoroughly addressing the full intent cluster, not by chasing a phrase that won't show up in any tool.

### 3. Target & optimize
- **Group by intent into one page** (keyword clustering); see `clustering.md` (S136, S137). One search intent = one page.
- **Answer first.** Lead the relevant section with a direct 40–60 word answer — paragraph PAA answers average just 41 words (S150). Mirror the question in an `<h2>`/`<h3>` (S156, S159).
- **Use FAQ schema where it helps machines**, but note Google restricted **FAQ rich results to well-known gov/health sites in Aug 2023** (S52) — for most sites the markup is invisible as a rich result yet can still clarify Q&A structure. Don't spam it.
- **Internal links** from related pages to distribute discovery and relevance (S149).
- **E-commerce:** make important filter/facet pages indexable and uniquely described so they capture specific long-tail intents (Wayfair example, S149).
- **Prerequisite:** you generally must **already rank on page 1 (ideally top 5)** to win a snippet or PAA placement — so optimize existing high-rankers first (S156, S159).

## Worked example / code

**A. GSC long-tail / question query filter (stdlib only, Python 3.8+).** Export *Performance → Queries* as CSV (columns: `Query, Clicks, Impressions, CTR, Position`) and run:

```python
#!/usr/bin/env python3
# long_tail_question_filter.py
# Surfaces question-style + long-tail queries from a GSC "Queries" CSV export.
# Pinned to Python 3.8+ (standard library only).
import csv, re, sys

QUESTION_RE = re.compile(
    r"^(how|why|what|which|where|when|who|can|is|are|does|do|should|will|"
    r"has|have)\b",
    re.IGNORECASE,
)

def is_long_tail(query, min_words=4):
    return len(query.split()) >= min_words

def main(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            q = (r.get("Query") or r.get("Top queries") or "").strip()
            if q:
                rows.append(q)
    question = [q for q in rows if QUESTION_RE.match(q)]
    longtail = [q for q in rows if is_long_tail(q)]
    print(f"Total queries:           {len(rows)}")
    print(f"Question-style queries:  {len(question)}")
    print(f"Long-tail (>=4 words):   {len(longtail)}")
    print("\nSample question-style long-tail queries:")
    for q in question:
        if is_long_tail(q):
            print(" -", q)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python long_tail_question_filter.py queries.csv")
        sys.exit(1)
    main(sys.argv[1])
```

**B. FAQ JSON-LD (illustrative — rich result not shown for most sites, S52):**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How do I find long-tail keywords?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Filter Google Search Console queries by question words, use a keyword tool's Questions tab, and mine People Also Ask boxes for related questions."
    }
  }]
}
```

## Assumptions & limitations
- **Tool volumes are estimates** (see `search-volume-difficulty.md`, S144). True long-tail with ~0 volume may not appear in any tool — discovery requires GSC, communities, and PAA (S148, S149).
- **Google publishes no "long-tail ranking boost."** Ranking for long-tail is a function of lower competition plus intent match, not a special signal.
- **"Easy to rank" is a tendency, not a guarantee.** High-volume informational long-tail can be as competitive as head terms (S148).
- **Snippet/PAA selection is algorithmic** with no guaranteed inclusion; you can opt out via `nosnippet` / `max-snippet` robots rules (S153).
- **Question-keyword prevalence has no canonical number** — sources disagree because they measure different things (see Conflicting views). Don't quote a single figure as fact.
- **Voice-search stats are dated.** The often-cited "20% of mobile queries are voice" figure is a 2016 Google statement and is not re-asserted here.

## Empirical evidence
- **Ahrefs US keyword database:** 2.3B keywords <10 searches/month ≈ 93% of the catalog; <18,000 keywords >100k/month (S148). *Strength:* very large proprietary dataset. *Limitation:* this is **keyword-count share**, not search-volume share.
- **Google "15% new queries/day":** stated in Google's BERT blog (blog.google) and reconfirmed by John Mueller in 2025 (S151, S152). *Strength:* Google primary. *Limitation:* directional, not a volume breakdown.
- **Semrush PAA study (1,000,000 US desktop keywords, 2020):** PAA present on 49.37% desktop / 52.27% mobile SERPs; PAA in the top 3 results 75% of the time; question-word queries trigger PAA 86% of the time; 10-word queries trigger PAA 72% of the time (S150). *Strength:* large transparent random sample. *Limitation:* dated 2020; PAA frequency has likely grown since.
- **Featured-snippet CTR:** Moz cites a third-party (EngineScout) study putting average snippet CTR ~35% (S159). *Limitation:* third-party, CTR ≠ guaranteed traffic.
- **"70% of searches are long-tail":** agency restatement of Hitwise 2008 (S157). *Limitation:* opaque methodology, dated — flagged folklore.
- **"Long-tail converts better":** practitioner belief (WordStream, S160; Skillshare). *Limitation:* correlation/intuition, not a controlled causal study.

## Conflicting views
- **"Long-tail = easy to rank" vs "it depends" (S148).** Ahrefs explicitly warns that some long-tail (high-volume informational) is no easier than head terms. Reconcile: low competition is typical but not universal.
- **"70% of searches are long-tail" (S157) vs "93% of keywords by count" (S148).** These are different metrics; the 70% figure is a volume-share claim with weak provenance, the 93% is a transparent count-share claim. State which you mean.
- **Question-keyword share.** Neil Patel's "~8% of Google searches are question-based" comes from a 1,002-person survey and is directional only (S158). This is **not** the same as Semrush's "question words trigger PAA 86% of the time" (S150) — the latter measures PAA *trigger rate for question queries*, not the share of all searches that are questions. Don't conflate.
- **Featured snippets post-AI-Overviews.** Moz notes AI Overviews now precede snippets for logged-in US users and may siphon some clicks, while arguing snippets still outperform the rest of organic (S159). Status: **emerging / contested** as AIO adoption grows.

## Common mistakes
- **Defining long-tail by word count** and building a page for every variant. Use Parent Topic / intent grouping instead (S148).
- **Keyword-stuffing question phrasing** unnaturally — violates Google spam policies (S8, S97).
- **Spinning up thin separate pages** for every long-tail variant → cannibalization. Consolidate via clustering (S139).
- **Assuming FAQ schema = a ranking boost or that FAQ rich results show for everyone** — restricted to gov/health since Aug 2023 (S52).
- **Treating "long-tail = high conversion" as guaranteed** — it is correlation, not causation (S160).
- **Chasing snippets/PAA on pages that don't yet rank page 1** — you usually must already be there (S156, S159).
- **Ignoring GSC** for already-ranking long-tail queries you never targeted (S148).

## Further reading
- **Tier 1 (primary):** Google, "Understanding searches with BERT" (blog.google) — the 15%-new-queries figure (S151); Google Search Central, Featured snippets doc (S153); Google Search Help, "How Google's featured snippets work" (S154).
- **Tier 2 (data-driven):** Ahrefs, "Long-Tail Keywords" (S148); Semrush, "Long-Tail Keywords: The Ultimate Guide for 2025" (S149); Semrush, "People Also Ask SEO Study" (S150); Moz, "Optimize for Featured Snippets" (S159); Search Engine Land, "Targeting featured snippet & PAA" (S156); NN/g, "Three Key SERP Features" (S155).
- **Tier 2/3 (caution):** Embryo, "30 statistics about long-tail keywords" (S157, directional); Neil Patel, "~8% of searches are questions" (S158, small survey).
- **In this KB:** `clustering.md` (intent grouping, S136/S137), `search-volume-difficulty.md` (volume is an estimate, S144), `structured-data.md` (FAQ restriction, S52), `passage-ranking-content-structure.md` (answer-first passages, S123/S124).
