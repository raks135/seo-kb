---
title: Emerging & Alternative Search (AI Overviews, voice, visual, non-Google engines)
topic_id: 11-emerging-search/emerging-search
tags: [ai-overviews, generative-search, voice, visual-search, bing, tiktok, chatgpt]
last_updated: 2026-07-18
confidence: emerging
sources: [S14, S24, S25, S12]
---

## TL;DR
Search is fragmenting beyond the blue links: Google's **AI Overviews (AIO)** generate summarized answers, voice/conversational search rewards concise, spoken-friendly answers, and visual search (Lens) matches images. Non-Google surfaces (Bing/Copilot, TikTok, Amazon, ChatGPT) have their own ranking logics. Optimize for being cited as a trustworthy source and for structured, extractable content.

## Core explanation
**AI Overviews** use generative AI to synthesize answers from multiple pages, often with links to sources. Early data shows AIO can reduce some organic clicks for informational queries (zero-click trend), but cited sources still gain visibility. **Voice search** favors natural-language, question-based, concise answers (often pulled from featured snippets). **Visual search** matches images to products/info.

## Mechanics / how-to
- Write clear, factual, extractable answers to questions; use headings/FAQ + structured data.
- Earn citations via authority + original data (sources AIO links to tend to be reputable).
- For voice: target featured-snippet-style conciseness; optimize local ("near me").
- For visual: high-quality images, descriptive alt/filenames, `ImageObject` schema.
- For Bing/Copilot: follow Bing Webmaster Guidelines (S12); for TikTok/Amazon, learn each platform's ranking.

## Worked example / code
FAQ JSON-LD (helps answer extraction):
```html
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"FAQPage",
  "mainEntity":[{"@type":"Question","name":"What is crawl budget?",
    "acceptedAnswer":{"@type":"Answer","text":"The number of pages Googlebot crawls on your site in a given timeframe."}}] }
</script>
```

## Assumptions & limitations
- AIO traffic impact is still being measured; early studies have small/biased samples (see Verify task).
- Google has not published how AIO selects sources; citation behavior is observed, not specified.
- Voice/visual ranking is less documented than web search.

## Empirical evidence
- MUM (S14) is the multimodal foundation behind generative search features.
- Practitioner reporting (S24/S25) documents AIO rollout and early zero-click trends; samples are limited and evolving.
- SparkToro/Similarweb zero-click data (S26) shows rising no-click searches pre-AIO, accelerating the trend.

## Conflicting views
- **"AIO kills SEO."** More accurate: it changes the click distribution; being a cited source still matters.
- **"Optimize separately for each engine."** Core web/structured-data quality transfers; platform-specific tactics vary.

## Common mistakes
- Blocking crawlers that power AIO (e.g., Googlebot, and AI crawlers).
- Thin content hoping to be cited.
- Ignoring non-Google surfaces where your audience searches.
- Over-claiming AIO "traffic drops" without sample context.

## Further reading
- S14 — Google, "MUM" — Tier 1
- S12 — Bing Webmaster Guidelines — Tier 1
- S24 — Search Engine Journal (AI Overviews coverage) — Tier 2
- S25 — Search Engine Land (generative search) — Tier 2
- S26 — SparkToro (zero-click data) — Tier 2
