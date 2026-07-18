---
title: International & Multilingual SEO (hreflang, ccTLD vs subdomain vs subfolder, geo-targeting)
topic_id: 07-international-seo/international-seo
tags: [international, hreflang, ccTLD, subdomain, subfolder, geo-targeting]
last_updated: 2026-07-18
confidence: robust
sources: [S17, S12, S1, S4]
---

## TL;DR
International SEO serves the right language/region version to the right user. Use **hreflang** annotations to signal language/region variants; choose a URL structure (subfolder vs subdomain vs ccTLD) based on resources and isolation needs. Geo-targeting in Search Console complements hreflang for country-specific subfolders.

## Core explanation
When you have the same content in multiple languages or country variants, search engines can show the wrong version without signals. **hreflang** (`rel="alternate" hreflang="x"`) tells Google which URL serves which language/region. Canonicalization still applies within each language (S4).

## URL structures (trade-offs)
- **Subfolder** (`example.com/de/`): easiest to set up, shares domain authority, simple geo-targeting in Search Console.
- **Subdomain** (`de.example.com`): separate but still on same root domain; slightly more effort to associate.
- **ccTLD** (`example.de`): strongest geo signal, requires per-country hosting/legal and builds authority separately (S1 notes TLD matters mainly for country targeting).

## Mechanics / how-to
1. Keep content equivalent across variants; translate, don't just machine-spin.
2. Add reciprocal hreflang links on every variant (each URL references all others + itself with `x-default`).
3. Use absolute, self-referential canonicals per language.
4. Set international targeting in Search Console for subfolders if country-specific.

## Worked example / code
```html
<link rel="alternate" hreflang="en-us" href="https://example.com/us/" />
<link rel="alternate" hreflang="de-de" href="https://example.com/de/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/us/" />
```
XML sitemap hreflang variant:
```xml
<url><loc>https://example.com/de/</loc>
  <xhtml:link rel="alternate" hreflang="en-us" href="https://example.com/us/"/>
  <xhtml:link rel="alternate" hreflang="de-de" href="https://example.com/de/"/>
</url>
```

## Assumptions & limitations
- hreflang is a hint; Google may still pick another URL if signals conflict (S17 — note: verify current URL; pre-registered path returned 404).
- Reciprocity is required: if A points to B, B must point back to A.
- Auto-translation without human review can be seen as low-quality (S1).
- ccTLDs don't share link equity across countries (S1/S12).

## Empirical evidence
Google's international targeting docs (S17) and Bing Webmaster Guidelines (S12) both describe hreflang and language/region targeting. Common implementation error rates are high in practitioner audits (see Verify task in backlog).

## Conflicting views
- **"Subdomains are as strong as subfolders."** Google treats subdomains as part of the root but historically passes less unified authority; subfolders are simpler to consolidate.
- **"hreflang guarantees the right version shows."** It's a strong hint, not enforced (S17).

## Common mistakes
- Non-reciprocal hreflang.
- Missing `x-default`.
- Canonicals pointing across languages incorrectly.
- Machine-translated thin content.
- Mixing geo-targeting and hreflang inconsistently.

## Further reading
- S17 — Google, "Use hreflang for language/page variants" — Tier 1 (verify URL)
- S12 — Bing Webmaster Guidelines — Tier 1
- S1 — Google, "SEO Starter Guide" (TLD/country targeting) — Tier 1
- S4 — Google, "Canonicals" — Tier 1
