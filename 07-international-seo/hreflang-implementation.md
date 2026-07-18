---
title: Hreflang Implementation & Common Errors
topic_id: 07-international-seo/hreflang-implementation
tags: [international-seo, hreflang, multilingual, x-default, canonicalization]
last_updated: 2026-07-18
confidence: robust
sources: [S179, S180, S181, S182, S183, S184, S185, S186, S12]
---

## TL;DR
- `hreflang` tells Google (and Yandex) which language/region version of a page to serve to a given user. It is a **signal, not a directive** — Google may still show a different version, and may consolidate near-identical regional pages into one canonical (S179, S180).
- The three non-negotiable rules: (1) every page must **list itself**, (2) the set must be **reciprocal** (A↔B), and (3) URLs must be **absolute** with **valid ISO 639-1 / 3166-1 codes** (S179, S184). Break any of these and Google "may ignore or not interpret" the annotations (S184).
- Implement via HTML `<link>` tags, HTTP `Link:` headers, **or** XML sitemap — pick one; don't mix (S179, S183).
- Empirically, hreflang is hard: an Ahrefs scan of 374,756 domains found **67% had at least one hreflang issue** (S180). A reproducible validator is shipped with this article (`hreflang-validator.py`).

## Core explanation
`hreflang` is an HTML attribute (formally `rel="alternate" hreflang="…"`) that declares a relationship between equivalent pages that differ only by language and/or region. It answers one question for the search engine: *"If a user searching in language L / region R lands on this cluster, which specific URL should I surface?"*

Plain-language model: imagine five doors (en, en-gb, en-us, de, x-default) that all lead to the same content in different localizations. `hreflang` is the signage telling Google which door to open for whom. Critically, the signage must be **complete and consistent on every door** — if door A says "for German speakers go to door D," then door D must say "for English speakers go to door A." If the signs contradict, Google tears them all down and guesses (S184).

Precision (Google's own wording, S179):
- "Use `hreflang` to tell Google about the variations of your content, so that we can understand that these pages are localized variations of the same content."
- "Google doesn't use `hreflang` or the HTML `lang` attribute to detect the language of a page; instead, we use algorithms to determine the language." So `hreflang` is about *targeting*, not *language detection*.
- "Localized versions of a page are only considered duplicates if the main content of the page remains untranslated." Translations are **not** treated as duplicates; same-language regional variants (fr-FR vs fr-BE) **can** be (S179, S183).

## Mechanics / how-to

### 1. Choose one implementation method
All three are equivalent to Google (S179):
- **HTML `<link>` tags** in `<head>` — most common; works for HTML pages.
- **HTTP `Link:` header** — needed for non-HTML files (PDFs, etc.).
- **XML sitemap `<xhtml:link>` children** — keep all relationships in one file.

Do **not** deploy more than one method site-wide; it multiplies maintenance and error risk (S183). If you use sitemaps, generate them, don't hand-maintain.

### 2. Build a self-referencing, reciprocal, identical set
For a cluster of N pages, **every** page carries the **same** list of N `<link>` elements (N includes the page itself) plus x-default. Example for 5 URLs:

```html
<!-- On EVERY one of the 5 pages (en, en-gb, en-us, de, root): -->
<link rel="alternate" hreflang="x-default" href="https://www.example.com/" />
<link rel="alternate" hreflang="en"      href="https://www.example.com/" />
<link rel="alternate" hreflang="en-gb"   href="https://www.example.com/gb/" />
<link rel="alternate" hreflang="en-us"   href="https://www.example.com/us/" />
<link rel="alternate" hreflang="de"      href="https://www.example.com/de/" />
```
The set is byte-for-byte identical on all five pages. Note the root page lists itself under both `x-default` and `en` — that is allowed and common (S179; the Webmasters StackExchange clarification in research confirms having both `en` and `x-default` pointing at the same URL is fine).

### 3. Code rules
- Language code: **ISO 639-1** (two lowercase letters, e.g. `en`, `de`, `zh`).
- Optional region: **ISO 3166-1 alpha-2** (two UPPERCASE letters, e.g. `gb`, `us`), dash-separated: `en-gb`.
- Script variants: you may add an explicit script via ISO 15924, e.g. `zh-Hant` (Traditional) or `zh-Hans-US` (S179).
- `x-default` = fallback for any unmatched language/region; best paired with a language-selector or neutral entry page (S179).
- **Invalid codes Google explicitly rejects:** `es-419` (regional grouping not supported), `UK`/`EU`/`UN` (not ISO 3166-1 alpha-2 — use `gb`), country-only codes like `gb` without a language (S179, S184).

### 4. XML sitemap variant
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.example.com/</loc>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/"/>
    <xhtml:link rel="alternate" hreflang="en"      href="https://www.example.com/"/>
    <xhtml:link rel="alternate" hreflang="en-gb"   href="https://www.example.com/gb/"/>
    <xhtml:link rel="alternate" hreflang="en-us"   href="https://www.example.com/us/"/>
    <xhtml:link rel="alternate" hreflang="de"      href="https://www.example.com/de/"/>
  </url>
  <!-- repeat <url> block for /gb/, /us/, /de/ with the IDENTICAL child set -->
</urlset>
```

### 5. Canonical vs hreflang — the #1 confusion
- **Canonical** says "index me, not my twin." **Hreflang** says "show the right twin to the right user." They are different jobs (S182).
- **Never** point a canonical tag from one language/region version to another if you want both indexed. A page canonicalized to a different URL should **not** carry hreflang annotations — hreflang belongs on canonical, indexable URLs only (S182, S183).
- If you send conflicting signals (e.g. "don't index me" via canonical-to-other + "please index all my cousins" via hreflang), Google will likely ignore your instructions (S182).

### 6. Operational guardrails
- Only reference **indexable, crawlable** pages. Don't `noindex` or `robots.txt`-block a URL that appears in your hreflang set, or its return link can't be followed and the whole cluster can break (S179, S180).
- Keep tags inside `<head>` (HTML injection into `<body>` is ignored/blocked; DOM "breakout" via unclosed tags or iframes breaks parsing) (S180).
- Don't use `hreflang` to "fix" duplicate content — it signals relationships, it does not resolve which version ranks (S183).
- Per John Mueller: don't over-produce language versions "because you can." Limit to pages that are **critical and valuable**; focus hreflang effort on pages already getting **wrong-language traffic** (often high-volume branded homepages). And never `robots.txt`-block a page that's already indexed to "remove" it — Google can't canonicalize a blocked URL (S185, S186).

## Worked example / code

The repository ships a reproducible validator, `hreflang-validator.py` (Python 3.8+, stdlib only). It checks the six error classes above against a dictionary of extracted clusters and exits non-zero if any error is found. Verified run on this article's demo data: the **correct** cluster returns 0 issues; the **broken** cluster flags relative URLs, invalid region codes (`en-uk`), missing self-reference, missing return tags, orphan targets, and inconsistent sets.

Condensed core (full version in `hreflang-validator.py`):

```python
import re

KNOWN_LANGS = {"en","de","fr","es","it","pt","nl","ru","zh","ja","ko","pl",
               "sv","da","no","fi","tr","ar","cs","hu","ro","th","vi","id"}
KNOWN_REGIONS = {"us","gb","ca","au","ie","de","fr","es","it","nl","be","ch",
                 "at","br","mx","pt","se","dk","no","fi","pl","jp","kr","cn",
                 "ru","tr","ar","cz","hu","ro","th","vn","id"}

def parse_hreflang(value):
    value = value.strip()
    if value.lower() == "x-default":
        return ("x-default", None)
    m = re.match(r"^([a-zA-Z]{2})(-([a-zA-Z]{2}))?$", value)
    if not m: return None
    lang, region = m.group(1).lower(), (m.group(3) or "").lower()
    if lang not in KNOWN_LANGS: return None
    if region and region not in KNOWN_REGIONS: return None
    return (lang, region or None)

def validate(clusters):
    issues = []
    norm = {}
    for url, pairs in clusters.items():
        norm[url] = {}
        for code, href in pairs:
            lab = parse_hreflang(code)
            if lab is None:
                issues.append(f"INVALID CODE: {code} on {url}")
                continue
            label = "x-default" if lab[0]=="x-default" else (f"{lab[0]}-{lab[1]}" if lab[1] else lab[0])
            norm[url][label] = href
            if not href.startswith(("http://","https://")):
                issues.append(f"RELATIVE URL: {url} -> {href}")
    # self-reference + reciprocity
    for url, mapping in norm.items():
        if not any(h.rstrip("/")==url.rstrip("/") for l,h in mapping.items() if l!="x-default"):
            issues.append(f"NO SELF-REFERENCE: {url}")
        for label, href in mapping.items():
            if label=="x-default" or href.rstrip("/")==url.rstrip("/"): continue
            if href not in norm:
                issues.append(f"ORPHAN TARGET: {url} -> {href}")
            elif not any(h.rstrip("/")==url.rstrip("/") for l,h in norm[href].items()):
                issues.append(f"MISSING RETURN TAG: {url} -> {href}")
    return issues
```

**Data source:** hreflang tags extracted from each URL's rendered `<head>` (or sitemap/HTTP header). The script validates relationship logic only; it does not fetch pages. Supply the clusters you collected via crawler or GSC.

## Assumptions & limitations
- **Google does not guarantee** the targeted version will be shown (S180). If two regional pages are too similar (e.g. fr-FR vs fr-BE with near-identical main content), Google may judge them duplicates and pick one canonical, ignoring your hreflang for ranking/distinction (S179, S183). Real localization (pricing, currency, locally-relevant examples, native editorial) is what makes regional variants worth separating.
- `hreflang` is **ignored if malformed** — one missing return link can void the entire cluster's signals (S184). There is no "partial credit."
- Bing treats `hreflang` as a **weak signal** and leans on the `content-language` attribute, links, and visitor geography; Baidu ignores `hreflang` entirely (S180, S12). So hreflang is primarily a Google/Yandex lever.
- Google uses its **own language-detection algorithms**, not your `hreflang`/`lang` attribute, to decide what language a page is (S179). Bad machine translation can still be suppressed locally.
- Subdirectory/subdomain/ccTLD architecture is a **separate decision** from hreflang (covered in the sibling article `07-international-seo` ccTLD vs subdomain vs subfolder). Hreflang works on top of any of them.
- No tool (incl. this script) can confirm Google *honors* your tags — only Search Console's International Targeting / indexed-URL inspection and live SERP spot-checks can. The validator only confirms internal consistency.

## Empirical evidence
- **67% of hreflang implementations are broken.** Ahrefs scanned **374,756 domains** and found 67% had at least one hreflang issue (S180). This is a descriptive prevalence scan (Ahrefs' own crawler), not a causal study, but it is the largest published figure and strongly suggests hreflang is the most error-prone technical-SEO element in practice.
- **Real-world brand failures.** Practitioners have documented hreflang errors at Squarespace, HubSpot, Audible, and Skype — typically missing bidirectional return links (S184). Squarespace's fix demonstrably changed a German searcher's SERP from the English to the German homepage (S184), showing correct hreflang has a measurable serving effect.
- **Strength of evidence:** Google's mechanics (self-reference, reciprocity, ISO codes, x-default, "signal not directive") are Tier-1 documented (S179). The 67% prevalence is Tier-2 first-party scan. The "Google may ignore similar regional pages" behavior is Tier-1 documented for duplicate consolidation (S179) plus Tier-2 corroboration (S180, S183). No controlled experiment isolates ranking lift from hreflang alone — and none should be claimed (see Conflicting views).

## Conflicting views
- **"Hreflang boosts rankings" vs "it's only a serving signal."** Some vendors imply hreflang raises rankings. Google documents it as a signal that helps serve the right version; it is **not** a ranking boost, and pages in a cluster may share some consolidation signals but do not automatically inherit each other's authority (S180). Treat any "% ranking lift from hreflang" claim as folklore.
- **x-default required?** Google calls x-default **recommended** (best for language-selector pages), not mandatory (S179). Some auditors flag its absence as an error; this article treats it as a warning (the validator does too).
- **Should you even use hreflang?** Mueller has repeatedly cautioned against over-engineering: for most sites, focusing hreflang on the homepage and a few high-traffic wrong-language pages captures most of the value, and blanket-applying it across thousands of low-traffic translated pages adds crawl/index/maintenance overhead for little gain (S185, S186). This contradicts "implement hreflang on every page no matter what" guidance from some tools — the nuance is traffic-weighted prioritization.
- **Return-link strictness.** Google's statement is that missing return links *may* cause annotations to be "ignored or not interpreted correctly" (S184 quoting Google) — i.e. it's not a hard 100% penalty but a strong likelihood of failure. Practitioners therefore treat reciprocity as mandatory.

## Common mistakes
1. **Missing self-reference** — forgetting the page's own `<link>` (S179, S184).
2. **Broken return links** — A→B without B→A; the single most common fatal error (S184).
3. **Wrong ISO codes** — `UK`/`EU`/`UN` instead of `gb`; `es-419`; country-only codes (S179, S184).
4. **Region-only targeting** — `hreflang="gb"` with no language; hreflang targets *language*, you cannot target a region alone (S184).
5. **Relative URLs** — must be absolute `https://…` (S181).
6. **Canonical conflicts** — canonicalizing across language/region versions, or putting hreflang on a non-canonical URL (S182).
7. **Blocking referenced pages** — `noindex`/`robots.txt` on a URL in the set breaks the return link (S179, S180).
8. **Multiple alternates → same URL**, or the same alternate pointing to multiple URLs (S181).
9. **hreflang outside `<head>`** (S181).
10. **Mixing implementation methods** (HTML + sitemap) and letting them drift (S183).
11. **Using hreflang to "fix" duplicate content** instead of genuinely localizing (S183).
12. **Over-production** — spinning up 20 languages × 10 countries "because you can," creating thin, low-traffic, maintenance-heavy pages Mueller warns against (S185).

## Further reading
- **[Tier 1]** Google Search Central, "Tell Google about localized versions of your page" — support.google.com/webmasters/answer/189077 (canonical hreflang doc; replaces the older `use-hreflang` URL which now 404s). Last updated 2025-12-22.
- **[Tier 1]** Bing Webmaster Guidelines — bing.com/webmasters/help/webmaster-guidelines (notes Bing recommends hreflang but weights `content-language` more heavily).
- **[Tier 2]** Ahrefs, "Hreflang: The Easy Guide for Beginners" — ahrefs.com/blog/hreflang-tags (Mueller "most complex" quote; 67%/374,756-domain study; Bing/Baidu behavior). Updated 2025-03-08.
- **[Tier 2]** Semrush, "9 Common Hreflang Errors (and How to Fix Them)" — semrush.com/blog/hreflang-errors.
- **[Tier 2]** searchviu, "hreflang & canonical tag: Use them correctly without conflicts" — searchviu.com/en/hreflang-canonical.
- **[Tier 2]** Oncrawl, "Hreflang implementation: Best practices for SEO" — oncrawl.com/local-international-seo/hreflang-and-seo-5-mistakes-to-avoid.
- **[Tier 2]** Collaborada, "Common Hreflang Mistakes to Avoid" — collaborada.com/blog/common-hreflang-mistakes (Google return-link quote; brand failure audit).
- **[Tier 2]** Search Engine Journal, "John Mueller Cautions Against Overuse of Multi-Language Content" — searchenginejournal.com/.../350222 (Mueller Reddit guidance).
- **[Tier 2]** Search Engine Roundtable, "John Mueller Offers Hreflang Google SEO Advice" — seroundtable.com/.../35052.html (Mueller Reddit: x-default for root redirect, per-page basis).
