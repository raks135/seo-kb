---
title: Mobile-First Indexing & Separate-URL (Mobile) Redirects
topic_id: 01-technical-seo/mobile-first-indexing
tags: [technical-seo, mobile-first-indexing, responsive-design, separate-urls, hreflang, crawl, index]
last_updated: 2026-07-18
confidence: robust
sources: [S67, S68, S69]
---

## TL;DR
- Mobile-first indexing means Google **predominantly uses the mobile version of your content**, crawled with the **smartphone Googlebot**, for both indexing and ranking. It has been the default for the entire web since September 2020 (S68).
- If your mobile version has less content, weaker structured data, missing titles/alt text, or a `noindex`, those gaps — not your desktop version — are what Google indexes. This is the single biggest source of "we lost rankings after mobile-first" cases (S67).
- Prefer **responsive design** (same HTML/URL for all devices). If you run **separate mobile URLs (m-dot)** or dynamic serving, you must maintain strict content parity, correct `rel=canonical`/`rel=alternate` links, 1:1 redirects, and matching `hreflang` per device (S67).

## Core explanation
Plain language: historically Google indexed the web from a desktop crawler. As mobile searches overtook desktop, Google flipped the default — the "mobile-first" index is now the primary index. The smartphone Googlebot fetches your pages, renders them, and whatever it sees on the mobile experience is what gets stored and ranked. Your desktop experience still matters for desktop users, but it is no longer the source of truth for indexing.

Precise: Google states it "predominates [using] the mobile version of a site's content, crawled with the smartphone agent, for indexing and ranking. This is called mobile-first indexing" (S67). A site does **not** strictly need a mobile version to be included in results, but Google "very strongly recommends" one (S67). Both the desktop Googlebot and smartphone Googlebot still exist; however, "most crawling for Search will be done with our smartphone Googlebot" (S68).

### Timeline (corroborated)
- 2016 — Google announces the mobile-first indexing initiative (S68).
- 2019-07-01 — Mobile-first indexing enabled by default for all **new**, previously-unknown domains (S68; corroborated by industry coverage).
- 2020-03 — Google reports ~70% of sites shown in search results were already served from a mobile-first index, and announces the switch to mobile-first for the **whole web** (S68).
- 2020-09 — Target date for all sites to be crawled/indexed mobile-first (S68; Search Engine Land corroborates the September 2020 cutoff, S69).

## Mechanics / how-to

### 1. Choose a configuration
Google recognizes three mobile-friendly configurations; **responsive design is recommended** because it is the simplest to implement and maintain (S67):
- **Responsive design** — same HTML and URL for all devices; CSS adapts layout to screen size. Content and metadata are automatically identical across devices.
- **Dynamic serving** — same URL, different HTML served via `user-agent` sniffing; requires the `Vary: user-agent` response header.
- **Separate URLs (m-dot)** — different HTML on different URLs (e.g., `m.example.com`); relies on `user-agent` detection + `Vary` headers to redirect users to the device-appropriate version.

The parity rules below apply to dynamic-serving and separate-URL setups; responsive sites satisfy them by construction.

### 2. Enforce content parity (desktop ≡ mobile)
Google indexes from the mobile version, so the mobile version must contain the same substance as desktop (S67):
- **Same primary content** — equivalent text, including content hidden behind accordions/tabs on mobile (moving content into tabs is fine for UX, but the content must still be present and crawlable).
- **Same clear, meaningful headings** on both versions (S67).
- **Same structured data** — present on both versions; prioritize `Breadcrumb`, `Product`, and `VideoObject` if you must triage (S67). URLs inside structured data on the mobile version must point to mobile URLs.
- **Same metadata** — equivalent `<title>` and meta description on both versions (S67).
- **Same images & alt text** — mobile must have the same important images, with equivalent descriptive alt text and sufficient resolution (S67). Don't lazy-load primary content behind user interaction (swipe/click/type) — Google won't trigger it (S67).
- **Same robots `meta` tags** — do **not** place `noindex`/`nofollow` on the mobile version; a mobile `noindex` will prevent indexing under mobile-first (S67).

### 3. Separate-URLs canonical/alternate pattern
For m-dot setups, the **desktop URL is always the canonical**, and the mobile URL is declared as an `alternate` of it (S67). On the desktop page:
```html
<link rel="canonical" href="https://example.com/" />
<link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.example.com/" />
```
On the mobile page, point the canonical back at the desktop URL:
```html
<link rel="canonical" href="https://example.com/" />
```
(S67; see the worked example below for the full block including `hreflang`.)

### 4. Redirects & international (hreflang) handling
- **1:1 redirects only.** Each desktop URL must redirect to its exact mobile equivalent. Redirecting many desktop URLs to the mobile home page (or to a single mobile URL) causes all those pages to go "missing from the index" after mobile-first enablement (S67).
- **Matching error status.** If a desktop URL returns 200 but its mobile counterpart returns an error page, that page will be missing from the index (S67).
- **No fragments on mobile URLs.** Mobile URLs with `#` fragments are not indexable and will drop out (S67).
- **hreflang for separate URLs must be device-specific.** When you use `rel=hreflang` for internationalization, link mobile→mobile and desktop→desktop separately: the mobile URL's `hreflang` values must point to mobile URLs, and the desktop URL's `hreflang` values must point to desktop URLs (S67). See worked example.

### 5. Verify & monitor
- Verify **both** the desktop and mobile versions of the site in Search Console (a domain switch can cause a data shift) (S67).
- Use the **URL Inspection tool → View Rendered HTML** to confirm what the smartphone Googlebot actually sees (S67).
- Watch for the mobile-first indexing "troubleshooting" messages in Search Console (missing structured data, `noindex` on mobile, missing/blocked/low-quality images, missing alt, missing title/meta, mobile error pages, fragment URLs, blocked by robots.txt, duplicate mobile targets, desktop→mobile-home redirects, page-quality, video, hostload issues) (S67).

## Worked example / code

### Separate-URLs link block (desktop page) with device-specific hreflang
```html
<!-- On https://example.com/ (desktop) -->
<link rel="canonical" href="https://example.com/" />
<link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.example.com/" />
<!-- hreflang points at DESKTOP locale URLs -->
<link rel="alternate" hreflang="es" href="https://example.com/es/" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
<link rel="alternate" hreflang="de" href="https://example.com/de/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/" />

<!-- On https://m.example.com/ (mobile) -->
<link rel="canonical" href="https://example.com/" />
<!-- hreflang points at MOBILE locale URLs -->
<link rel="alternate" hreflang="es" href="https://m.example.com/es/" />
<link rel="alternate" hreflang="fr" href="https://m.example.com/fr/" />
<link rel="alternate" hreflang="de" href="https://m.example.com/de/" />
<link rel="alternate" hreflang="x-default" href="https://m.example.com/" />
```
The rule: **canonical is always the desktop URL; `hreflang` targets stay within the same device family** (S67).

### robots.txt parity check
Ensure your `robots.txt` rules are the same for both device variants and do not `disallow` mobile resources (images/CSS/JS) that desktop allows (S67). A quick diff:
```bash
# Mobile and desktop should serve functionally identical robots rules
curl -s https://example.com/robots.txt
curl -s https://m.example.com/robots.txt   # if separate host
```

### Python content-parity checker (desktop vs mobile)
Data source: live HTTP fetch of the two device variants. Pinned: `python>=3.10`, `requests>=2.31`, `beautifulsoup4>=4.12`.
```python
import requests
from bs4 import BeautifulSoup

HEADERS_DESKTOP = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
HEADERS_MOBILE  = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960F) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/120 Mobile Safari/537.36"}

def snapshot(url, headers):
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    text = " ".join(soup.stripped_strings)
    return {
        "status": r.status_code,
        "title": (soup.title.string.strip() if soup.title else None),
        "text_len": len(text),
        "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
        "img_count": len(soup.find_all("img")),
        "imgs_missing_alt": len([i for i in soup.find_all("img") if not i.get("alt")]),
        "has_noindex": 'noindex' in r.text.lower() and 'name="robots"' in r.text.lower(),
    }

desktop = snapshot("https://example.com/page", HEADERS_DESKTOP)
mobile  = snapshot("https://m.example.com/page", HEADERS_MOBILE)

print("status match:", desktop["status"] == mobile["status"])
print("title match:", desktop["title"] == mobile["title"])
print("text length ratio (mobile/desktop):", round(mobile["text_len"]/desktop["text_len"], 2))
print("mobile noindex:", mobile["has_noindex"])  # must be False
print("imgs missing alt (mobile):", mobile["imgs_missing_alt"])
```
Interpretation: a text-length ratio well below ~0.9 usually signals the mobile version is missing paragraphs present on desktop — a direct indexing risk under mobile-first (S67). A `mobile noindex: True` is an emergency (S67).

## Assumptions & limitations
- **Responsive design assumed best.** Google recommends responsive design as the easiest to maintain; the parity burden falls almost entirely on dynamic-serving and separate-URL setups (S67).
- **Crawl-rate spike.** When a domain is switched to mobile-first indexing, Googlebot's crawl rate on the mobile version increases while the index updates to the mobile version — ensure the mobile host has enough capacity ("hostload") (S67, S68).
- **Mobile-first indexing is the indexing methodology, not a ranking "bonus."** It determines *which* content Google stores. If your mobile version is equivalent, nothing changes; if it is weaker, rankings can fall because the weaker version is what is indexed. Treat "mobile-first indexing hurt my rankings" as a parity problem, not a penalty.
- **What Google has NOT confirmed:** an exact quantified ranking weight for mobile-friendliness, or any guarantee that a perfectly parity-matched mobile site outranks a stronger desktop-only competitor. Mobile-friendliness has been a ranking signal since 2015, but Google has not published a numeric contribution.
- **Google changes.** The separate-URLs/hreflang and troubleshooting guidance was last updated 2025-12-10 (S67); re-verify before large-scale migrations.

## Empirical evidence
- **Primary source (Google):** As of March 2020, ~70% of sites shown in Google search results were already served from a mobile-first index, and the remaining sites were migrated by September 2020 (S68). This is first-party and high-confidence for the *fact* of broad rollout, though it does not quantify ranking impact.
- **Corroboration (Tier 2):** Search Engine Land reported the same September 2020 whole-web cutoff (S69), aligning with Google's announcement — the timeline is well-corroborated.
- **Strength/limitations:** These are Google's own statements and reputable reporting; there is no independent large-sample study of *ranking delta* attributable purely to mobile-first indexing, because parity gaps are confounded with overall site quality. Confidence in "parity matters" is robust (directly stated by Google, S67); confidence in any specific "X% traffic loss" figure is low — do not cite such numbers without a dated, methodologically transparent study.

## Conflicting views
- **"Mobile-first indexing is a ranking factor."** Strictly, it is an indexing methodology, not a standalone ranking signal. Practitioners sometimes conflate it with the separate mobile-friendly ranking signal (2015). The accurate framing: mobile-first indexing changes *what* is indexed; mobile-friendliness is a ranking consideration; a weak mobile version *manifests* as ranking loss because that weak version is what gets indexed (S67).
- **"Responsive vs separate URLs — which is safer?"** Google recommends responsive, but acknowledges separate URLs are supported if configured correctly (S67). Vendors often overstate the danger of m-dot; the risk is real but concentrated in parity/redirect/hreflang errors, not the pattern itself.
- **"Desktop site no longer matters."** False. Desktop content still serves desktop users and can still rank for desktop queries; it is simply not the *indexing source*. Both must remain high quality (S67).

## Common mistakes
1. **Thin mobile content** — stripping paragraphs, images, or structured data from the mobile version "to be clean." Under mobile-first, that thinning is what Google indexes (S67).
2. **`noindex`/`nofollow` on mobile only** — a mobile `noindex` prevents indexing entirely once mobile-first is on (S67).
3. **Blocking mobile resources in robots.txt** — disallowing mobile-specific image/CSS/JS URLs hides them from the smartphone crawler (S67).
4. **Lazy-loading primary content behind taps/swipes** — Google won't fire the interaction, so the content is invisible to indexing (S67).
5. **Broken m-dot redirects** — redirecting many desktop URLs to the mobile home page, or to a single mobile URL, drops all of them from the index (S67).
6. **Fragment (`#`) in mobile URLs** — unfetchable/indexable under mobile-first (S67).
7. **Mismatched `hreflang` across devices** — pointing mobile `hreflang` at desktop URLs (or vice-versa) breaks international targeting for separate-URL setups (S67).
8. **Missing alt text / low-res images on mobile** — flagged as page-quality issues (S67).

## Further reading
- S67 — Google Search Central, "Mobile site and mobile-first indexing best practices" (developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing) — Tier 1, last updated 2025-12-10. Authoritative: definition, 3 configs, parity rules, separate-URLs canonical/alternate, full troubleshooting table.
- S68 — Google Search Central Blog, "Announcing mobile first indexing for the whole web" (developers.google.com/search/blog/2020/03/announcing-mobile-first-indexing-for) — Tier 1. Rollout timeline (2016 → 2019-07 new sites → 2020-09 whole web; ~70% already mobile-first by Mar 2020).
- S69 — Search Engine Land, "Google to switch completely over to mobile-first indexing by September 2020" (searchengineland.com/google-to-switch-completely-over-to-mobile-first-indexing-by-september-2020-330174) — Tier 2. Corroborates the Sept 2020 cutoff.
- S1 — Google Search Central, "SEO Starter Guide" (developers.google.com/search/docs/fundamentals/seo-starter-guide) — Tier 1. Foundational mobile-friendly guidance.
- S3 — Google Search Central, "JavaScript SEO basics" (developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) — Tier 1. Relevant because lazy-loaded/JS content must be renderable by the smartphone Googlebot.
