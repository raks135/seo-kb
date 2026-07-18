---
title: Search Intent Taxonomy
topic_id: 00-foundations/search-intent
tags: [intent, taxonomy, serp, query-classification, keyword-research]
last_updated: 2026-07-18
confidence: robust
sources: [S9, S21, S31, S32]
---

## TL;DR
Search intent is the underlying goal behind a query. Two taxonomies dominate: Google's Quality Rater Guidelines use **Know / Do / Website / Visit-in-Person**, while SEO practitioners use **Informational / Navigational / Commercial / Transactional** (Broder's 2002 three-class model, extended). The most reliable way to infer intent is **SERP analysis** — Google's own ranking systems have already decided which page formats satisfy the query. Match the dominant content format and cover the full intent, not just the literal keyword.

## Core explanation
"Search intent" (also *user intent*, *query intent*, *keyword intent*) is the task or need a person is trying to satisfy when they type a query. Two people searching the same word can want completely different things ("apple" = the fruit vs. the company), so intent is what disambiguates the query for the search engine.

There are two parallel classification systems you will encounter:

**1. Google's framework (from the Search Quality Rater Guidelines, S9), section 12.7:**
- **Know** — the user wants to know about something (information, but also research/reviews).
- **Do** — the user wants to perform an activity (download, use a tool, buy).
- **Website** — the user wants a specific site/page (e.g. "facebook login").
- **Visit-in-person** — the user wants a local business or category of business (e.g. "pizza near me").

**2. The SEO practitioner framework (S21), which descends from Broder 2002 (S31):**
- **Informational** — learn about a topic ("how does a carburetor work").
- **Navigational** — reach a specific site/page ("youtube").
- **Commercial (investigation)** — research options before buying ("best running shoes", "x vs y") (S21).
- **Transactional** — complete an action ("buy nike air max size 10").

**How they map:** Google's *Website* ≈ Navigational; Google's *Visit-in-Person* is a local subset of Do/Transactional; Google's *Know* spans the SEO Informational **and** Commercial buckets (Google folds pre-purchase research into "Know"); Google's *Do* overlaps SEO Transactional. The key difference: SEOs split out **commercial investigation** as its own stage of the funnel, because the optimal page format (comparison/review) differs from pure informational content.

## Mechanics / how-to
**Step 1 — Infer intent from query language (heuristic):**
- Informational cues: what, why, how, when, guide, tutorial, tips, examples, "history of…"
- Commercial cues: best, top, review, vs, comparison, alternative, "worth it", rating
- Transactional cues: buy, purchase, order, coupon, discount, "for sale", price, subscribe
- Navigational cues: brand names, "login", "official site"
- (These signal conventions are documented in S21; word order matters — "dog food ingredients" ≠ "ingredients for dog food".)

**Step 2 — Validate with SERP analysis (the reliable method, S21):**
1. Search the exact keyword in an incognito window in your target locale.
2. Look at the top 10 results: what formats dominate? (blog post, product page, category page, tool, video, local pack)
3. Note SERP features present: featured snippet, knowledge panel, local pack, shopping ads, "People Also Ask", image pack.
4. Open the top pages and catalog the topics/sub-questions they cover.
Google's ranking systems have already solved intent for that query, so the SERP is the clearest signal of what "satisfies" it (S32 states systems "figure out that showing recipes or images may best match your intent").

**Step 3 — Optimize to the dominant format (S21):**
- Use the same content type as the top results (don't pitch a 2,000-word guide for a query Google answers with a calculator tool).
- Cover the *full* intent: include the secondary sub-topics competitors and "People Also Ask" reveal.
- Write titles/meta that match the searcher's vocabulary and stage.

## Worked example / code
A runnable heuristic intent classifier (stdlib only). This operationalizes Step 1; **always confirm with SERP analysis** because token signals miss context (e.g. "apple" is ambiguous).

```python
# search_intent_classifier.py  — Python 3.11, stdlib only
# Heuristic classifier based on query-language signal conventions (S21).
# LIMITATION: token signals miss brand/context ambiguity; treat output as a hint,
# then validate against the live SERP.

TRANSACTIONAL = {"buy", "purchase", "order", "shop", "cheap", "discount",
                 "coupon", "price", "subscribe", "for sale"}
COMMERCIAL = {"best", "top", "review", "vs", "comparison", "compare",
              "alternative", "recommend", "worth", "rating"}
INFORMATIONAL = {"what", "why", "how", "when", "where", "who", "which",
                 "guide", "tutorial", "tips", "examples"}

def classify(query: str) -> str:
    q = query.lower()
    tokens = set(q.split())
    if tokens & COMMERCIAL or any(p in q for p in COMMERCIAL if " " in p):
        return "commercial"
    if tokens & TRANSACTIONAL or any(p in q for p in TRANSACTIONAL if " " in p):
        return "transactional"
    if tokens & INFORMATIONAL:
        return "informational"
    return "ambiguous -> validate via SERP"

for t in ["buy nike air max size 10", "best running shoes 2026",
          "how to tie a tie", "facebook login", "apple"]:
    print(f"{t!r:35} -> {classify(t)}")
```
Run: `python3 search_intent_classifier.py`. Expected: transactional / commercial / informational / (ambiguous, actually navigational) / ambiguous. The "facebook login" and "apple" cases show why SERP validation is mandatory — tokens alone misclassify navigational/brand queries.

## Assumptions & limitations
- **Intent is inferred, never directly observed.** Broder himself noted "there is no assumption here that this intent can be inferred with any certitude from the query" (S31). The query text is a noisy signal at best.
- **One query can carry multiple intents** (e.g. "blog platform free" is partly informational, partly commercial) — Google's QRG explicitly covers "queries with multiple user intents" (S9, 12.7.5).
- **Locale, device, time, and personalization shift intent** (S32: "football" → American football in Chicago, soccer in London; mobile/voice queries are longer and more natural-language).
- **Google has NOT published a quantified "intent-match → ranking lift" number.** We know intent is a ranking input (S32) and a quality-rater criterion (S9), but the weight is query-dependent and undisclosed.
- **Prevalence figures below are from 2001 AltaVista data and are dated** — do not treat them as current.

## Empirical evidence
- **Broder 2001 AltaVista study (S31):** user survey (n=3,190) found navigational ≈ 24.5% (26.4% among Q2-answerers), non-navigational 68.4%; transactional at least 23.8% of all queries (shopping 7.65% + downloads 24.65% of non-navigational), rising to ~36% by self-reported open-text intent. Log analysis put navigational ~20%. *Strength:* it is the origin study of the taxonomy. *Limitations:* 2001, AltaVista (not Google), ~10% survey response rate, self-selection bias, English-only after filtering, and "informational" was the residual bucket — so its share is overstated by measurement method. **Not representative of 2026 query mix (more mobile, voice, and local).** → see Verify task below.
- **Google confirms intent determination is a ranking step (S32):** "our systems figure out that showing recipes or images may best match your intent," and ranking weight "varies depending on the nature of your query."
- **No published Google A/B study quantifies the ranking benefit of intent-matched rewrites.** Practitioner case studies report ranking gains after reformatting pages to match SERP intent, but these are anecdotal/correlational — classify as *emerging*, not *robust*.

## Conflicting views
- **Category mismatch:** Google's QRG collapses commercial research into "Know," while most SEO tools/guides treat Commercial as a distinct fourth class (S21). Practitioners care about the distinction because the winning page format differs. Neither is "wrong" — they serve different purposes (rater training vs. content planning).
- **Number of classes:** Some vendors now propose 5–6 (adding *local* and even *generative-AI* intent, e.g. SE Ranking's 2026 framing). The 4-class SEO model remains the consensus baseline; "local" is better understood as a modifier (Google's "Visit-in-person") than a fully separate class. Treat 5–6 class schemes as *emerging*.
- **"Commercial" origin:** often attributed loosely to Broder, but Broder's 2002 paper had only 3 classes (navigational/informational/transactional); the explicit *commercial investigation* split was popularized later (Rose & Levinson, 2004). Assert the 3-class origin from S31; treat the 4-class as the extended practitioner standard.

## Common mistakes
- **Building the wrong format** — writing a long guide for a query Google satisfies with a tool/local pack (classic mismatch).
- **One page for many intents** — a single URL trying to serve informational + transactional usually satisfies neither; follow "one intent = one page = one cluster" (S21).
- **Keyword-stuffing instead of answering** — matching the literal term while ignoring what the searcher needs; this is exactly what helpful-content systems down-rank.
- **Trusting token heuristics alone** — "apple", brand queries, and ambiguous head terms break naive classifiers; always validate via SERP.
- **Ignoring SERP features** — if the result is a featured snippet, you must structure content to win it (concise direct answer), not just rank #1 for the blue link.

## Further reading
- **Tier 1:** Google Search Quality Rater Guidelines (intent: §12.7; Needs Met: §13) — S9.
- **Tier 1:** Google, "How Search works: ranking results" (meaning of query / intent) — S32.
- **Tier 1:** Broder, A. (2002), "A Taxonomy of Web Search," ACM SIGIR Forum — S31.
- **Tier 2:** Semrush, "What Is Search Intent?" (4-class SEO taxonomy + SERP method) — S21.
- **Tier 2:** Semrush, "4 Types of Keywords" (informational/navigational/commercial/transactional examples) — S21.
