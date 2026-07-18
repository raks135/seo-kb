---
title: Heading Structure & Semantic HTML
topic_id: 02-on-page-seo/headings
tags: [on-page-seo, headings, h1, semantic-html, accessibility, html, hierarchy]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S70, S71, S72, S73, S74]
---

## TL;DR
- Headings (`<h1>`–`<h6>`) are a **content-organization and accessibility** tool, not a per-level ranking factor. Google uses them to understand what a block of text or image is about, not to weight H1 "more" than H2 (Google Search Advocate John Mueller; Google's own SEO Starter Guide).
- You may use multiple `<h1>` elements or even none — Google says that is "not a critical issue" for ranking (Mueller, via Search Engine Roundtable). A **single logical H1** remains the accessibility best practice.
- Heading order does **not** have to be perfect for Google: per the SEO Starter Guide, "from Google Search perspective, it doesn't matter if you're using them out of order." Skipping levels hurts **screen-reader users**, not rankings.
- Semantic HTML (`<article>`, `<section>`, `<nav>`, `<main>`, `<header>`, `<footer>`, `<aside>`) improves accessibility and machine readability, but Google has **not** confirmed it provides a ranking benefit — treat SEO claims about landmarks as *folklore*.
- Action: write one clear H1 that matches search intent, use H2/H3 to mirror your real outline, never hide headings in CSS-only text, and keep the structure logical for humans and assistive tech.

## Core explanation

HTML headings (`<h1>` through `<h6>`) are six levels of section headings. `<h1>` is the highest level (e.g. the page title); `<h6>` the lowest. By default each renders as a block-level box. They exist for **two audiences at once**: human readers (who scan) and machines (search engines and assistive technology).

The SEO myth that dominates old "best practice" lists is that the *relative importance* of heading tags is itself a ranking signal — i.e. "put your most important keyword in H1, a less important one in H2," and that skipping a level (H2 → H4) hurts rankings. Google has repeatedly stated this is no longer how it works.

Mueller (Google Search Advocate) explains the actual role: Google reads headings "in the way they were meant to be, which is for understanding what the topic is of the paragraphs that follow." In his words, headings are "a bit overrated" as a ranking lever; they help Google "better understand the content on the pages" and "frame that piece of text" so it can be matched to the right queries. The H1-more-important-than-H2 idea "used to be a real ranking factor over 15 years ago," but is not today (S70).

Google's own SEO Starter Guide is even more explicit: *"Having your headings in semantic order is fantastic for screen readers, but from Google Search perspective, it doesn't matter if you're using them out of order. The web in general is not valid HTML, so Google Search can rarely depend on semantic meanings hidden in the HTML specification."* It adds there is *"no magical, ideal amount of headings a given page should have. However, if you think it's too much, then it probably is"* (S1).

**Semantic HTML** is the practice of using elements that describe *meaning* (`<nav>`, `<main>`, `<article>`, `<section>`) rather than generic `<div>`s. It makes the document's structure machine- and assistive-tech-readable. Its value for SEO specifically is **unconfirmed by Google** — see Conflicting views.

## Mechanics / how-to

**1. One clear H1 per page (intent-matching).** Make it the visible title of the page, aligned with the query you want to rank for. It need not be identical to the `<title>` tag, but it should be consistent in meaning.

**2. Mirror your true outline with H2 → H3 → H4.** Each H2 is a major section; each H3 a subsection beneath it. Add keywords only where they fit naturally.

**3. Don't skip levels *for users*.** `<h1>` → `<h3>` (skipping H2) confuses screen-reader navigation. For Google it's tolerable; for accessibility it is not. Use CSS `font-size` for visual sizing — never pick a heading level just to get a certain look.

**4. Multiple H1s are allowed.** With HTML5 sectioning you may legitimately have an `<h1>` inside each `<article>`. Google is fine with this; MDN notes multiple `<h1>` is "allowed by the HTML standard… but not considered a best practice" and recommends a single page-level H1 that "describes the content of the page" (S72, S73).

**5. Use semantic landmarks.**
```html
<body>
  <header>
    <nav aria-label="Primary">…</nav>
  </header>
  <main>
    <article>
      <h1>Complete Guide to Cold Brew Coffee</h1>
      <p>Intro paragraph…</p>
      <h2>What You Need</h2>
      <p>…</p>
      <h3>Choosing the Beans</h3>
      <p>…</p>
      <h2>Step-by-Step Method</h2>
      <h3>Coarse Grind</h3>
      <h3>Steep 16–24 Hours</h3>
    </article>
  </main>
  <footer>…</footer>
</body>
```

**6. Don't hide headings.** A heading that is `display:none`, `visibility:hidden`, `font-size:0`, or off-screen purely to push keywords is cloaking-adjacent and a spam risk — keep headings visible and meaningful.

**7. Check for free.** Use the URL Inspection tool / "View Rendered HTML" in Search Console, or a crawler (Screaming Frog, Sitebulb) to export the H1/H2 outline and spot missing or duplicate H1s.

## Worked example / code

Reproducible heading-audit script (Python ≥ 3.11, `beautifulsoup4>=4.12.0`). It extracts the heading outline of a local HTML file, flags a missing/duplicate H1, and detects skipped levels. Data source: any HTML file you point it at.

```python
# heading_audit.py — audit H1–H6 outline for SEO/accessibility signals
# deps: pip install "beautifulsoup4>=4.12.0"  (Python 3.11+)
from __future__ import annotations
from pathlib import Path
from bs4 import BeautifulSoup

def audit_headings(html_path: str) -> None:
    soup = BeautifulSoup(Path(html_path).read_text(encoding="utf-8"), "html.parser")
    levels = [int(h.name[1]) for h in soup.find_all(["h1","h2","h3","h4","h5","h6"])]
    texts  = [(int(h.name[1]), h.get_text(strip=True)) for h in
              soup.find_all(["h1","h2","h3","h4","h5","h6"])]

    h1s = [t for lvl, t in texts if lvl == 1]
    print(f"Total headings: {len(levels)} | H1 count: {len(h1s)}")
    if len(h1s) == 0:
        print("  [WARN] No H1 found (accessibility best practice: one H1). Google: not a ranking blocker.")
    elif len(h1s) > 1:
        print(f"  [INFO] {len(h1s)} H1s — OK for Google; consider one page-level H1 for screen readers.")

    # detect skipped levels (e.g. h2 -> h4) in sequence
    prev = 0
    for lvl, txt in texts:
        if prev and lvl > prev + 1:
            print(f"  [WARN] Skipped level: …h{prev} then h{lvl} ('{txt[:40]}')")
        prev = lvl

    print("\nOutline:")
    for lvl, txt in texts:
        print(f"  {'  ' * (lvl-1)}h{lvl}: {txt[:60]}")

if __name__ == "__main__":
    audit_headings("page.html")  # replace with your file
```

Expected behavior: a clean article prints a single H1 and a nested H2/H3 tree with no skipped-level warnings. A broken page (H1 → H3 jump, or five H1s) prints the corresponding `[WARN]`/`[INFO]` lines. This is a **diagnostic**, not a ranking guarantee.

## Assumptions & limitations
- Assumes the page is server-rendered or JavaScript-rendered such that Googlebot sees the same headings users do (see `01-technical-seo/javascript-seo.md`). Headings injected only after client-side JS must be in the rendered HTML.
- The "headings aren't a ranking factor" claim applies to *heading level/order/keyword placement*. Headings still help Google **understand** topical relevance, which is indirectly good for matching queries — correlation, not a direct boost.
- Google changes ranking systems; these are statements valid as of 2024–2026 (Mueller hangouts 2019/2023; SEO Starter Guide last updated 2025-12-10). Re-verify if Google publishes new guidance.
- No structured study proves heading *structure* moves rankings; the strongest evidence is Google's explicit statements plus absence of counter-evidence, hence confidence = robust for the "not a per-level ranking factor" claim but *emerging* for any positive ranking effect.

## Empirical evidence
- **Google primary sources (Tier 1):** SEO Starter Guide states heading *order* doesn't matter to Google Search and there is no ideal heading count (S1). Mueller (Google) states headings are used for content understanding, not per-level ranking, and that pages "can do perfectly fine with no h1 tags or with five h1 tags" (S70, S71). Strength: highest (first-party). Limitation: these describe *intent/design*, not a controlled ranking experiment.
- **MDN / web standards (Tier 1):** Heading elements and the don't-skip-levels / single-H1 guidance are standardized for accessibility; screen readers build a heading list and jumping between headings is a primary navigation method (S72, S73). Strength: high for accessibility claims.
- **Ahrefs featured-snippet study (Tier 2, n = ~2M keywords, 2017):** ~12.3% of queries show a featured snippet; **99.58%** of featured-snippet pages already rank in the top 10; the snippet is extracted from a top-ranking page (S74). Relevance here: a *well-structured, top-ranking* page is eligible for passage/snippet features — but this measures **content formatting + existing ranking**, NOT heading order as a ranking input. Sample limitation: dated (2017), pre-passage-ranking and pre-AI-Overviews; treat as directional only.
- **Net:** There is no credible large-scale correlation study showing H1-vs-H2 keyword placement changes rankings. The consensus rests on Google's first-party statements.

## Conflicting views
- **"Headings are a top ranking factor; always keyword-load your H1/H2."** This is the dominant *old* SEO advice (still published by many vendor blogs, e.g. Seobility, SERanking). It **conflicts** with Google/Mueller (S1, S70, S71). Resolution: the per-level ranking-weight claim is *folklore*; headings matter for understanding/UX, not as a keyword-rank lever.
- **"Always use exactly one H1 or you'll be penalized."** Google says multiple H1s are fine for ranking (S71). The single-H1 rule is an **accessibility** best practice (MDN/WCAG), not a Google penalty. Resolution: use one logical H1 for users; don't fear multiple H1s technically.
- **"Semantic HTML (`<article>`/`<section>`/`<nav>`) boosts rankings."** Google has **not** confirmed ranking benefit from landmarks; the SEO Starter Guide even says Google "can rarely depend on semantic meanings hidden in the HTML specification" (S1). Resolution: semantic HTML is real value for accessibility and maintainability; its SEO ranking effect is *unconfirmed* (folklore if asserted as fact).
- **"Fixing your heading hierarchy will change your rankings."** Mueller: "fixing headings won't change rankings" in a meaningful way; it helps understanding, not position (S70). Manage client expectations accordingly.

## Common mistakes
1. **Keyword-stuffing headings** ("Best Cheap Red Shoes Buy Red Shoes Sale") — looks spammy, adds no understanding value, risks spam-policy friction.
2. **Using headings for visual size** (`<h4>` because it's the right font size) — use CSS; keep tag level = outline level.
3. **Skipping levels** (H2 → H4) — breaks screen-reader heading navigation; fix for accessibility even though Google tolerates it.
4. **Hidden/cloaked headings** (off-screen, `font-size:0`, `display:none` with keyword text) — manipulative; can draw a manual action.
5. **Missing H1** on key pages — not a ranking blocker for Google, but a missed opportunity to state the page topic clearly and a poor experience for assistive tech.
6. **Many H1s from template/CMS bugs** (e.g. logo + title + widget each an H1) — tidy up for clarity; Google won't penalize, but it muddies the outline.
7. **Assuming headings = ranking fix** after a drop — headings rarely recover rankings; investigate intent, content quality, and links instead.

## Further reading
- S1 — Google Search Central, *SEO Starter Guide* (developers.google.com/search/docs/fundamentals/seo-starter-guide) — heading-order & count guidance. Tier 1.
- S70 — Search Engine Journal, "Google Explains How to Use Headings for SEO" (Roger Montti) — Mueller transcript on headings/understanding. Tier 2.
- S71 — Search Engine Roundtable, "Google: H1 Tags Are Not Critical For Search Ranking" (B. Schwartz) — multiple-H1 OK. Tier 2.
- S72 — MDN Web Docs, "<h1>–<h6> HTML section heading elements" (developer.mozilla.org) — canonical spec, skip-level & H1 guidance, May-2025 implied-level removal. Tier 1.
- S73 — MDN Web Docs, "Headings and paragraphs" (Learn web development) — single-H1 preference, logical levels. Tier 1.
- S74 — Ahrefs, "Study Of 2 Million Featured Snippets" (T. Soulo) — snippet eligibility correlates with top-10 ranking; dated. Tier 2.
- W3C WAI, "Page Structure — Headings" (w3.org/WAI/tutorials/page-structure/headings) — accessibility standard (success criteria 1.3.1, 2.4.6, 2.4.10).
- Related KB: `02-on-page-seo/onpage-basics.md` (title/meta), `01-technical-seo/javascript-seo.md` (ensure headings are rendered), `04-content-strategy/content-hubs.md` (outline as topic clusters).
