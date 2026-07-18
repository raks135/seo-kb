---
title: On-Page SEO Basics (titles, headings, meta, content optimization, E-E-A-T signals)
topic_id: 02-on-page-seo/onpage-basics
tags: [on-page, title-tag, headings, meta, eeat, content]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S16, S9, S7]
---

## TL;DR
On-page SEO is about making each page clearly understandable to users and crawlers: a descriptive `<title>`, a single clear `<h1>`, useful meta description, and content that demonstrates Experience, Expertise, Authoritativeness, and Trustworthiness (E-E-A-T). Google rewrites titles/snippets automatically when it thinks it can do better, so write for users first.

## Core explanation
On-page elements are the visible and code-level signals Google uses to interpret a page. Google generates title links automatically from several sources — the `<title>` element, the main `<h1>`, and even `og:title` / other prominent text (S16). It does not guarantee your exact title will show.

## Mechanics / how-to
- **Title (`<title>`):** unique per page, descriptive, brand where useful. Avoid boilerplate, stuffed keywords, and obsolete dates (S16).
- **Headings:** one clear `<h1>`; use heading levels for structure. Google: heading order is not a ranking factor and there's no ideal count — but semantic order aids accessibility (S1).
- **Meta description:** not a ranking factor, but influences click-through when shown. Write compelling, accurate summaries.
- **Content:** anticipate the words readers search with; Google's language matching understands synonyms, so don't force every variant (S1).
- **Mobile-first:** Google indexes the mobile version of pages; ensure mobile parity of content/links (S7).
- **E-E-A-T:** especially for Your-Money-Your-Life (YMYL) topics (health, finance, safety), demonstrate first-hand experience and credentials (S9).

## Worked example / code
```html
<head>
  <title>How to tie a tie | ExampleStyle</title>
  <meta name="description" content="Step-by-step guide to four common tie knots, with photos.">
</head>
<body>
  <h1>How to tie a tie</h1>
  <h2>The four-in-hand knot</h2>
  <p>...</p>
</body>
```

## Assumptions & limitations
- Title rewrites are normal; you cannot "force" Google to show your title (S16).
- Meta description is not a confirmed ranking factor.
- E-E-A-T is assessed via many signals, not a single tag; it's most critical for YMYL (S9).
- Heading order is not a ranking signal per Google (S1).

## Empirical evidence
Google's own guidance (S1, S16) and the Quality Rater Guidelines (S9) are first-party. Studies by Moz/Ahrefs on title-tag CTR are correlational, not causal.

## Conflicting views
- **"Exact-match keywords in title are required."** Google: language matching handles variants; over-stuffing can trigger rewrites or look spammy (S1, S16).
- **"Heading order affects ranking."** Google explicitly: it does not depend on semantic heading order (S1).

## Common mistakes
- Duplicate `<title>` across pages (micro-boilerplate triggers rewrites, S16).
- Keyword stuffing in titles.
- Different content on mobile vs desktop (mobile-first indexing penalty risk, S7).
- Treating meta description as a ranking lever.
- Ignoring E-E-A-T on YMYL pages.

## Further reading
- S1 — Google, "SEO Starter Guide" — Tier 1
- S16 — Google, "Create good titles and snippets" — Tier 1
- S9 — Google, "Quality Rater Guidelines" (E-E-A-T/YMYL) — Tier 1
- S7 — Google, "Mobile-first indexing" — Tier 1
