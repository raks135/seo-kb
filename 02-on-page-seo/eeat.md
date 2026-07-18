---
title: E-E-A-T — Experience, Expertise, Authoritativeness & Trustworthiness
topic_id: 02-on-page-seo/eeat
tags: [on-page, quality, ymyl, author-entities, trust-signals, google-guidelines]
last_updated: 2026-07-18
confidence: robust
sources: [S9, S33, S84, S85, S86, S87, S88, S89, S90, S91, S92, S93]
---

## TL;DR
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is Google's quality framework, defined in the Search Quality Rater Guidelines (QRG) and echoed in Search Central's "Creating helpful, reliable, people-first content" guidance.
- It is **not** a single ranking factor and there is **no "E-E-A-T score"** in the algorithm. Google's ranking systems use many separate signals that reward content showing these qualities (links, reputation, accuracy, transparency).
- **Trust is the center of the model** — Google calls it "the most important member of the E-E-A-T family" (Dec 2022 QRG update).
- YMYL ("Your Money or Your Life") topics demand the highest E-E-A-T because errors can harm a person's health, safety, or financial stability.
- Practical levers: real author bylines + bios, `Person`/`Organization` schema with `sameAs`, transparent About/contact/editorial-policy pages, clear sourcing, and a clean review/accuracy process.

## Core explanation
Plain language: E-E-A-T is Google's shorthand for "can we trust this page, and who stands behind it?" It is the lens Google's human Quality Raters use to judge whether a result is the kind of content Google's algorithms should reward. E-E-A-T is not something you "add" to a page like a meta tag — it is an emergent property of the content, the author, the site, and the site's reputation across the web.

Precise: The concept originates in the **Search Quality Rater Guidelines** (S9), the handbook given to Google's third-party Quality Raters. Raters score sample results to give Google feedback on how well its ranking systems perform; their ratings **do not directly affect rankings** (S9, S90). In December 2022 Google added the first "E" (**Experience**) to the prior E-A-T acronym, explicitly to reward first-hand, life experience (S86, S89). In the same update Google stated that **Trust is the most important member of the E-E-A-T family** (S86, S89).

The four pillars:
- **Experience** — the content creator has first-hand, real-world experience with the subject (e.g., used the product, visited the place).
- **Expertise** — the creator has the required knowledge or skill; level scales with topic (a medical article needs clinician expertise, a forum post about a personal fix needs lived experience).
- **Authoritativeness** — the creator/publisher is a recognized, go-to source on the topic; reputation across the web matters.
- **Trustworthiness** — accuracy, transparency, honesty, and security; the central pillar.

## Mechanics / how-to
Use the QRG-aligned self-assessment from Google's people-first content page (S84). Key questions to pass:

**Content & quality**
- Original information, reporting, or analysis? Not just copied/rewritten from other sources?
- Substantial, complete, and accurate? Any easily-verified factual errors? (S84)
- Would you bookmark, share, or cite it? Would you expect it in a reference work? (S84)

**Expertise & trust**
- Clear sourcing and evidence of expertise (author bio, About page, credentials)? (S84)
- Would an outsider researching the site come away trusting it as an authority? (S84)
- Written or reviewed by an expert/enthusiast who demonstrably knows the topic? (S84)

**Who / How / Why (the "people-first" test, S84, S85)**
- **Who** created it (named, accountable author/publisher)?
- **How** it was produced (editorial process, fact-checking, AI involvement disclosed)?
- **Why** it was created (to help people, not just to rank)?

**YMYL check:** If the topic can affect someone's health, financial stability, safety, or happiness, hold the page to the strictest E-E-A-T bar — verifiable expertise, cited sources, named accountable author, and a trustworthy publishing entity (S9, S87).

**Author & entity signals (practical)**
1. Give every substantive article a named author with a real bio page linking to credentials and external profiles (`sameAs`).
2. Mark up the author as `schema:Person` (and the publisher as `schema:Organization`) in JSON-LD; connect both via `sameAs` to authoritative profiles (see worked example).
3. Publish a comprehensive **About** page (who runs the site, mission, editorial standards) and a **Contact**/corrections page; for YMYL, name medical/financial review boards.
4. Cite sources with links; show dates (`datePublished`/`dateModified`); disclose conflicts and AI assistance (Google says listing AI as the author is "probably not the best way" — attribute human accountability, S85).
5. Keep reviews, testimonials, and ratings genuine; never fabricate. (Structured-data review spam is a manual-action risk — see 15-pitfalls/schema-spam.)

## Worked example / code
Runnable JSON-LD (stdlib-only check; no external packages). This marks up an article author as a `Person` and connects them to external profiles via `sameAs`, and declares the publisher:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to winterize your sprinkler system",
  "datePublished": "2026-01-12",
  "dateModified": "2026-06-30",
  "author": {
    "@type": "Person",
    "name": "Jordan Rivera",
    "jobTitle": "Irrigation contractor, 12 years field experience",
    "url": "https://example.com/authors/jordan-rivera",
    "sameAs": [
      "https://www.linkedin.com/in/jordan-rivera",
      "https://www.youtube.com/@jordanirrigation"
    ]
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Landscape Co.",
    "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" }
  }
}
```

A stdlib Python snippet to confirm the author `Person` block is present and well-formed (pin: Python 3.11+, no third-party deps):

```python
import json, re, sys, urllib.request
from html.parser import HTMLParser

class _JSONLD(HTMLParser):
    def __init__(self):
        super().__init__(); self.blocks = []
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            d = dict(attrs)
            if d.get("type") == "application/ld+json":
                self._cap = True; self._buf = []
    def handle_data(self, data):
        if getattr(self, "_cap", False):
            self._buf.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and getattr(self, "_cap", False):
            self._cap = False
            raw = "".join(self._buf)
            for piece in re.split(r"\}\s*,\s*\{", raw):
                piece = piece.strip().strip("[]")
                try:
                    self.blocks.append(json.loads(piece))
                except json.JSONDecodeError:
                    pass

def has_author_person(html: str) -> bool:
    p = _JSONLD(); p.feed(html)
    def walk(obj):
        if isinstance(obj, dict):
            if obj.get("@type") in ("Person", ["Person"]):
                return True
            return any(walk(v) for v in obj.values())
        if isinstance(obj, list):
            return any(walk(v) for v in obj)
        return False
    return any(walk(b) for b in p.blocks)

html = urllib.request.urlopen("https://example.com/blog/post").read().decode()
print("Author Person schema present:", has_author_person(html))
```

Data source: parse your own rendered article HTML (server-rendered or post-hydration). Validate with Google's Rich Results Test / Schema Markup Validator before shipping.

## Assumptions & limitations
- **Not a direct ranking factor.** Google has repeatedly stated E-E-A-T is a *framework for raters*, not a toggle in the algorithm, and there is no E-E-A-T score (S84, S87, S88). The algorithm expresses these qualities through many separate signals (links, reputation, on-page clarity, factual accuracy, page experience).
- **QRG is a living document.** It is revised regularly; the most recent notable refresh added AI Overviews and refined YMYL definitions on 2025-09-11 (S90). Treat specific page numbers/quotations as version-bound.
- **No guaranteed rankings.** Demonstrating E-E-A-T reduces the risk of underperforming on quality/YMYL queries but does not assure a position; relevance, links, and intent-match still govern.
- **Entity recognition is inferred, not confirmed.** Google "likely" models authors/publishers as entities in its Knowledge Graph (S88), but the exact internal signals are not public — treat author-entity SEO as best practice, not a documented guarantee.
- **Correlation ≠ causation.** Sites that recovered from quality updates after adding author bios may have improved many things at once; author pages are one of several concurrent fixes.

## Empirical evidence
- **Framework origin (strong, Tier 1):** E-E-A-T is documented in the QRG and in Search Central's people-first content help page, both first-party (S9, S84). Trust-as-central is stated by Google in the Dec 2022 QRG update (S86).
- **"Not a score" (strong, multiple sources):** Corroborated by Google's own help page (S84) and by practitioner analyses from Semrush (S87) and Marie Haynes (S88).
- **Author-as-entity (moderate, Tier 2):** Marie Haynes/Olaf Kopp describe Google modeling authors/publishers as entities via Knowledge Graph attribute–value pairs and reputation signals (PageRank, third-party mentions) (S88). This is a well-reasoned industry model, not a Google-confirmed algorithm description.
- **Recovery anecdotes (weak, directional):** Practitioners (incl. Marie Haynes' case work) report YMYL sites hit by 2017–2018 quality updates often lacked author E-A-T versus top-ranking competitors (S88). Sample/selection bias; not a controlled study.
- **Sample limitation:** Public "E-E-A-T impact" case studies are almost always single-site, post-hoc, and confounded by simultaneous changes — do not read them as causal proof.

## Conflicting views
- **"E-E-A-T is a ranking factor" vs "it's only a rater framework."** Many vendor blog posts sell "E-E-A-T optimization" as if it were a lever. Google's own documentation is consistent: it is a *quality concept the algorithms are built to reward*, not a single factor or score (S84, S87). Treat vendor "E-E-A-T boosts rankings by X%" claims as folklore unless they show a controlled study.
- **Author schema necessity.** Some say `Person`/`Author` schema is required for E-E-A-T; others (incl. Google's John Mueller) note Google can understand authorship from on-page context without structured data. Schema helps machines and supports `sameAs` entity connections, but a visible byline + bio is the core signal; markup is reinforcement, not a substitute (S92).
- **How much E-E-A-T a topic needs.** Google calibrates the *required* level to the page's purpose and risk (YMYL = highest). Forums/Reddit can rank for "experience" queries where peer experience is what searchers want (S87) — expertise is topic-relative, not absolute.

## Common mistakes
- **Faking credentials / borrowing authority.** Pretending a named expert wrote content they didn't, or scraping another site's author bio, backfires — Google's QRG explicitly warns raters about sites that *fake* their E-E-A-T (S9, S88).
- **Listing AI as the author.** Google says giving AI an author byline is "probably not the best way" to be transparent about creation; disclose human accountability and how AI was used (S85).
- **Thin "About" / no contact.** A bare About page and missing contact/corrections info weaken Trust, especially for YMYL.
- **Keyword-stuffed author bios / "expert" badges with no proof.** Boilerplate "Jane is an expert" with no credentials, links, or real bio adds nothing and can read as manipulative.
- **Citation-free YMYL claims.** Medical/financial/legal pages without sources, dates, or named reviewers are the classic low-E-E-A-T pattern Google's raters downgrade.
- **Confusing E-E-A-T with a technical tag.** You cannot "implement E-E-A-T" via a plugin; it is built through content quality, accountable authorship, and reputation.
- **Neglecting accuracy after publish.** Stale or factually wrong content (no `dateModified` discipline, no review cadence) erodes Trust over time — see content freshness (04-content-strategy).

## Further reading
- Google, "Creating helpful, reliable, people-first content" (Search Central) — S84 (Tier 1)
- Google, "Search Quality Rater Guidelines" (PDF) — S9 (Tier 1)
- Google Search Central Blog, "E-A-T gets an extra E for Experience" (Dec 2022) — S86 (Tier 1)
- Google Search Central Blog, "Google Search's guidance about AI-generated content" (Feb 2023) — S85 (Tier 1)
- Google, "A guide to Google Search ranking systems" (reliable-information systems) — S33 (Tier 1)
- Semrush, "Google E-E-A-T: What It Is & How It Affects SEO" — S87 (Tier 2)
- Marie Haynes, "Semantic SEO & E-A-T" (author entities, Knowledge Graph) — S88 (Tier 2)
- Search Engine Land, "E-E-A-T and major updates to Google's quality rater guidelines" (Dec 2022) — S89 (Tier 2)
- Search Engine Roundtable, "Quality Rater Guidelines gains AI Overview & YMYL definitions" (Sep 2025 update) — S90 (Tier 2)
- Google Search Central Blog, "What creators should know about the Aug 2022 helpful content update" — S91 (Tier 1)
- Aubrey Yung, "How to use Author schema for E-E-A-T" — S92 (Tier 2)
- jsonld.com, "Social Profiles JSON-LD — sameAs Markup" — S93 (Tier 2)
