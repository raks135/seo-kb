---
title: Entity SEO & the Knowledge Graph
topic_id: 04-content-strategy/entity-seo
tags: [entity-seo, knowledge-graph, knowledge-panel, schema, sameas, topical-authority, semantic-search]
last_updated: 2026-07-18
confidence: robust
sources: [S33, S51, S93, S116, S117, S118, S119, S120, S121, S122]
---

## TL;DR
- An **entity** is a real-world "thing" — a person, organization, place, product, or concept — that Google can identify as a distinct node in its Knowledge Graph, not just a keyword string. Google's own launch phrase was "things, not strings" (S118).
- Entity SEO is the practice of making your brand, people, and topics **unambiguously identifiable and well-connected** so Google (and AI answer engines) can classify and relate them. The concrete lever is an "entity home" page with Organization/Person schema plus `sameAs` links to Wikidata/Wikipedia and consistent corroborating mentions (S120, S121).
- Entity clarity improves Google's *understanding and relevance* and underpins eligibility for Knowledge Panels and rich features. It is a **mechanism for comprehension, not a confirmed direct ranking factor** — do not promise ranking lifts from it.

## Core explanation
Plain language: For four decades search matched query *strings* to page *strings*. Google's Knowledge Graph (launched May 16, 2012) shifted this toward recognizing the underlying *entities* — the monument vs. the musician both called "Taj Mahal" (S118). Once Google knows the entity you mean, it can disambiguate, summarize, and connect results the way a person would.

Precise: The Knowledge Graph is a knowledge base of entities (nodes) and their relationships (edges). At launch it contained **more than 500 million objects and 3.5 billion facts** (S118) — Google no longer publishes a current count (see Conflicting views). It is built from structured public sources — Freebase, Wikipedia, the CIA World Factorbook — augmented at web scale by extracting facts from text, tables, and page structure (S118). A companion research effort, **Knowledge Vault** (Dong et al., KDD 2014), formalized probabilistic knowledge fusion: combining web extractions with prior knowledge from Wikipedia, Freebase, YAGO, Satori, and the Knowledge Graph, then using supervised ML to compute a calibrated probability that each extracted fact is correct (S117). Note this is a published research system, not a statement of current production internals.

Entities connect to ranking through Google's semantic systems named in the ranking-systems guide: **neural matching, BERT, MUM, and passage ranking** all operate on meaning and concepts rather than literal keyword overlap (S33). Entity recognition is what lets a page built around "Tesla the EV maker" rank for thousands of related phrasings rather than one exact keyword.

## Mechanics / how-to
Practical steps to establish an entity (pattern synthesized from Kalicube and ReputationX, S120, S121):

1. **Find/claim your Knowledge Panel.** Search your brand. If a panel exists, use the "Claim this knowledge panel" flow in Google Search; if not, the steps below build the signals that can earn one.
2. **Build an "entity home."** A single canonical page (homepage for a brand, About page for a person) that clearly states the entity's name, description, and key attributes.
3. **Add schema.org markup.** Use `Organization` or `Person` JSON-LD on the entity home (S51). Include `name`, `description`, `logo`, `url`, and `sameAs`.
4. **Wire `sameAs`.** Link your entity to its external profiles — Wikipedia, Wikidata, LinkedIn, Crunchbase, official social accounts (S93). `sameAs` tells the Knowledge Graph "these are the same entity."
5. **Create or correct a Wikidata item.** Practitioners treat Wikidata as a primary structured input to the Knowledge Graph (S120); a clean Q-ID with correct statements strengthens entity identity.
6. **Keep brand signals consistent.** Name, address, phone, and description should match across your site, social, and directories (the NAP principle from local SEO).
7. **Write topically coherent content** with co-occurring entities (e.g., a Tesla page should naturally mention "electric vehicles," "battery," "Autopilot") so Google's NLP reads a clear central entity (S119 salience principle).
8. **Earn corroborating third-party mentions.** Independent sites, press, and profiles that describe the same entity reinforce its notability (S121).

## Worked example / code
**(a) Entity-home JSON-LD** (Organization with `sameAs` to external profiles). Data source: your own entity facts; validate in Google's Rich Results Test.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Acme Robotics",
  "url": "https://www.acme-robotics.example",
  "logo": "https://www.acme-robotics.example/logo.png",
  "description": "Acme Robotics builds autonomous warehouse robots.",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q123456789",
    "https://en.wikipedia.org/wiki/Acme_Robotics",
    "https://www.linkedin.com/company/acme-robotics",
    "https://twitter.com/acmerobotics"
  ]
}
```

**(b) Knowledge Graph Search API lookup** — find your entity's Google ID and relevance score. Requires a free API key from Google Cloud. Python 3.8+ (stdlib only):

```python
import json, urllib.parse, urllib.request

API_KEY = "YOUR_GOOGLE_CLOUD_API_KEY"          # store in env var in production
query   = "Acme Robotics"
url = ("https://kgsearch.googleapis.com/v1/entities:search?"
       + urllib.parse.urlencode({"query": query, "limit": 5, "indent": True, "key": API_KEY}))

with urllib.request.urlopen(url) as r:          # noqa: S310 (trusted Google endpoint)
    data = json.loads(r.read())

for el in data.get("itemListElement", []):
    res = el["result"]
    print(f"{res.get('name')}  |  id={res.get('@id')}  |  score={el.get('resultScore')}")
```

The API returns entries in JSON-LD using schema.org types and a `resultScore` relevance score; `@id` values look like `kg:/m/0dl567` (S116). A match here is evidence Google already models your entity.

**(c) Entity-salience proxy via Cloud Natural Language API** — estimate which entities are *central* to a page (mirrors the salience concept Google's NLP uses; S119). Pin: `google-cloud-language>=2.0`, Python 3.8+.

```python
from google.cloud import language_v1

text = "Acme Robotics builds autonomous warehouse robots using computer vision and reinforcement learning."

client = language_v1.LanguageServiceClient()
doc = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
resp = client.analyze_entities(document=doc)

for e in sorted(resp.entities, key=lambda x: x.salience, reverse=True):
    print(f"{e.name:30s} type={e.type_.name:12s} salience={e.salience:.3f}")
```

`salience` is a [0, 1.0] score of how central the entity is to the whole document (S119). Use it to check your intended primary entity actually dominates the page.

## Assumptions & limitations
- Google does **not** publish the current size, weight, or update cadence of the Knowledge Graph, nor how entity confidence feeds ranking. Claims of "X billion entities / Y trillion facts" circulating in 2025-2026 vendor posts are inconsistent and unverified — do not cite a specific figure (mark as Verify).
- `sameAs` and schema help **entity disambiguation and Knowledge Graph linkage**; Google has not confirmed they are ranking factors (consistent with structured data generally not boosting rank — see the structured-data article).
- The Cloud Natural Language API is a separate Google Cloud product, not Search; its salience score is a useful *proxy*, not a revealed Search signal.
- Google has not published Hummingbird's (2013) internal architecture; the "entity-based" label is the industry's interpretation of its documented conversational/semantic focus (S122).
- Entity recognition does **not** guarantee a Knowledge Panel; panels depend on notability thresholds Google does not disclose.

## Empirical evidence
- **Verified, primary:** At launch (2012) the Knowledge Graph held >500M objects and >3.5B facts, sourced from Freebase/Wikipedia/CIA World Factbook plus web-scale extraction (S118). The KG Search API demonstrably returns entity matches with `resultScore` (S116). Cloud NL API returns entity `salience` in [0,1] (S119).
- **Strength/limits:** These are first-party facts about Google's systems, but they describe *capability*, not *ranking impact*. Practitioner case studies (Kalicube, ReputationX) showing brands earning panels are **anecdotal, n≈1**, and cannot isolate entity SEO from other signals (S120, S121).
- **Do NOT assert:** Vendor claims such as "entity-recognized content is 50% more likely to win rich results" appear without a cited methodology; treat as folklore until a sourced study appears.

## Conflicting views
- **KG size:** Numbers range from the verified 2012 "500M objects" to unsourced 2026 claims of "54 billion entities / 1.6 trillion facts." Google is the only authority and is silent. Resolution: cite only the 2012 launch figure; flag all current counts as unverified.
- **Does `sameAs` affect ranking?** It clearly supports Knowledge Graph identity/disambiguation (S93, S120). Whether it moves rankings is unconfirmed; do not promise it.
- **Wikidata as "primary input":** Kalicube asserts Wikidata is a primary KG input (S120). Google has not named a single required source; Wikipedia/Wikidata are strong corroborators, not a published prerequisite.
- **Hummingbird = "the entity update":** Google confirmed it was a core-algorithm rewrite improving conversational/long-query matching (Matt Cutts, via SEJ, S122). The explicit "entity" framing is practitioner inference, not a Google statement.

## Common mistakes
- **Keyword-stuffing instead of entity clarity** — repeating a phrase does not build entity identity; coherent topical copy with related entities does (S119).
- **Expecting a Knowledge Panel overnight** — panels need notability; schema alone won't trigger one.
- **Inconsistent brand name/NAP** across site and profiles, which fragments the entity.
- **Fake or mismatched `sameAs`** (pointing to unrelated or wrong entities) — harms disambiguation.
- **Over-claiming a ranking boost** from entity SEO; it aids understanding/relevance, not a measurable rank factor.
- **Blocking or duplicating structured data** so Google can't read your entity declaration (see structured-data article pitfalls).

## Further reading
- S118 — Google Official Blog (A. Singhal, 2012), "Introducing the Knowledge Graph: things, not strings" — launch, rationale, 2012 scale. (Tier 1)
- S116 — Google for Developers, Knowledge Graph Search API — find/verify your entity ID and `resultScore`. (Tier 1)
- S117 — Dong et al., "Knowledge Vault" (KDD 2014, research.google) — probabilistic knowledge fusion. (Tier 1, research)
- S119 — Google Cloud Natural Language API, Entity reference — `salience` scoring. (Tier 1)
- S33 — Google Search Central, ranking-systems guide — BERT/neural matching/MUM/passage ranking. (Tier 1)
- S51 / S93 — Schema.org + jsonld.com `sameAs` — entity linkage markup. (Tier 1 / Tier 2)
- S120 — Kalicube (J. Barnard), Entity SEO / Knowledge Panel process. (Tier 2, practitioner)
- S121 — ReputationX, "Entity SEO: Build Your Brand in Google's Knowledge Graph." (Tier 2, practitioner; ignore its unverified size claim)
- S122 — Search Engine Journal, "Google's Hummingbird Update." (Tier 2, editorial)
