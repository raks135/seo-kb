---
title: Image SEO — alt text, responsive images, lazy loading, and modern formats
topic_id: 02-on-page-seo/image-seo
tags: [image-seo, alt-text, responsive-images, lazy-loading, webp, avif, core-web-vitals, lcp, image-sitemaps]
last_updated: 2026-07-18
confidence: robust
sources: [S38, S45, S75, S76, S77, S78, S79, S80, S81, S82, S83]
---

## TL;DR

- Images are usually the largest contributor to page weight, so they directly affect Core Web Vitals (especially LCP) and user experience. Optimize them for both discovery (SEO) and speed (UX). [S75, S82]
- Write descriptive, concise `alt` text for meaningful images and leave `alt=""` on purely decorative ones; never keyword-stuff alt text (it's a spam signal). Google reads alt text + computer vision + page content together. [S75, S81, S83]
- Serve responsive images (`srcset`/`sizes` or `<picture>`) in modern formats (WebP/AVIF) with a JPEG/PNG fallback, and set `width`/`height` to avoid layout shift (CLS). [S75, S78, S80]
- Lazy-load only below-the-fold images. **Never** put `loading="lazy"` (or a JS deferred load) on the LCP image — it adds hundreds of ms to LCP. Eager-load and `fetchpriority="high"` the hero. [S77, S78, S79]
- Use an image sitemap to surface images Google might not otherwise crawl (e.g. JS-injected or CDN-hosted), and make sure your landing page's title, text, and structured data support the image. [S75, S76]

## Core explanation

Image SEO is the practice of making images both **discoverable/indexable by search engines** and **fast/pleasant for users**. The two goals overlap: Google's image-quality signals reward images that are relevant, high-resolution, and served on fast pages, while slow or hidden images underperform in both Image Search and web-search Core Web Vitals.

Plain language: search engines "see" an image through (a) the file itself, (b) the `alt` text and surrounding copy, and (c) machine-vision analysis of the pixels. They rank images in Google Images and may show them as thumbnails in regular web results, Discover, and rich results. Meanwhile, a heavy or badly-loaded image makes the page slow, which hurts the page-experience (Core Web Vitals) signals that Google uses as a lightweight ranking tie-breaker.

Precisely: Google recommends standard HTML `<img>` elements (it does **not** index CSS background images), crawlable image URLs that aren't blocked by `robots.txt` or `noindex`, descriptive `alt`/filenames, responsive delivery, and modern compression. [S75] The LCP (Largest Contentful Paint) element is an image on the majority of web pages, so image loading strategy is the single biggest lever for image-related CWV. [S77, S78]

## Mechanics / how-to

### 1. Alt text (accessibility + relevance + Image Search)
- Add `alt` to every **meaningful** image: describes the image for screen readers and gives Google context. [S75, S81]
- Keep it concise, accurate, and in the page's context. Avoid "image of…"/"picture of…", avoid redundancy with the caption, and **never keyword-stuff** (Google flags this as spam). [S83]
- Decorative/spacer/icon images: use empty `alt=""` so screen readers skip them. [S83]
- If an image is a link, its `alt` acts as anchor text describing the destination. [S83]
> Google: "Google uses alt text along with computer vision algorithms and the contents of the page to understand the subject matter of the image. … Avoid filling `alt` attributes with keywords (also known as keyword stuffing) as it results in a negative user experience and may cause your site to be seen as spam." [S75]

### 2. Filenames & placement
- Use short, descriptive filenames (`my-new-black-kitten.jpg` > `IMG00023.JPG`). This is a light signal. [S75, S82]
- Place images near relevant on-page text; Google pulls context from captions and titles too. [S75]
- Reference each image with a **consistent URL** everywhere (don't re-host the same binary under many URLs) — this lets Google cache/reuse it and saves crawl budget. [S75]

### 3. Formats & compression
- Google Search indexes these `src` formats: BMP, GIF, JPEG, PNG, WebP, SVG, AVIF. Match the file extension to the type. [S75]
- Prefer **modern formats**: AVIF/WebP compress far better than legacy JPEG/PNG at similar quality, shrinking the bytes the user downloads (helps LCP "load duration" and bandwidth). Serve them with a JPEG/PNG fallback via `<picture>`. [S75, S78]
- JPEG for photos, PNG for line art/text/transparency, SVG for icons/vector, GIF only for animation. [S82]

### 4. Responsive images
- `srcset` + `sizes` (or `<picture>` for art direction / format negotiation) deliver the right resolution per device, avoiding wasted bytes on small screens. [S75, S78, S80]
- Always include a fallback `src`/`img` (some crawlers/old browsers ignore `srcset`/`picture`). [S75]

### 5. Lazy loading (do it right)
- Native lazy loading: `<img loading="lazy" …>`. Supported in all major browsers since ~2019. [S79]
- **Only** use it for images below the fold. Above-the-fold lazy loading — especially on the LCP image — delays discovery and is the most common image-CWV mistake. [S77, S79]
- For the LCP/hero image: eager-load it (omit `loading="lazy"`) and add `fetchpriority="high"` so the browser prioritizes it; optionally `<link rel="preload" as="image" href="…">`. [S77, S78]

### 6. Prevent layout shift (CLS)
- Set `width`/`height` attributes (or CSS `aspect-ratio`) on images so the browser reserves space before load. Missing dimensions cause CLS; Google's "good" CLS threshold is ≤0.1 at the 75th percentile. [S38]

### 7. Image sitemaps
- If images are injected via JS, hosted on a CDN, or otherwise hard for crawlers to discover, submit an image sitemap (separate or as an extension of your existing sitemap). Up to 1,000 `<image:image>` per `<url>`. Cross-domain image URLs are allowed if both domains are verified in Search Console. [S76]
- Note: `<image:caption>`, `<image:geo_location>`, `<image:title>`, and `<image:license>` were **removed** from Google's image-sitemap spec (2022 cleanup) — don't rely on them. [S76]

### 8. Landing-page & structured-data support
- The page's title, meta description, and on-page text influence which image Google picks as the preview and where it ranks. [S75]
- Mark your preferred image with `og:image` or schema.org `ImageObject` attached to the page's `mainEntity`/`mainEntityOfPage`. Adding supported structured data (e.g. `Product`, `Recipe`, `Article`) can earn a badge in Google Images. [S75] (Structured data affects display, not ranking — see `structured-data.md`. [S45])

## Worked example / code

**Responsive `<picture>` with modern formats + LCP best practice (HTML):**

```html
<!-- Hero / LCP image: eager + high priority, no lazy loading -->
<img
  src="/img/hero-1200.jpg"
  srcset="/img/hero-600.jpg 600w, /img/hero-1200.jpg 1200w, /img/hero-2400.jpg 2400w"
  sizes="100vw"
  width="1200" height="800"
  alt="Barista pouring latte art into a ceramic cup"
  fetchpriority="high"
  decoding="async">

<!-- Below-the-fold gallery image: lazy-load it -->
<picture>
  <source type="image/avif" srcset="/img/croissant.avif">
  <source type="image/webp" srcset="/img/croissant.webp">
  <img src="/img/croissant.jpg" width="800" height="600"
       alt="Fresh butter croissant on a wooden board" loading="lazy">
</picture>
```
Data source: Google Image SEO best practices (supported formats, fallback requirement) [S75]; web.dev LCP/responsive guidance [S77, S78, S80]; MDN picture/srcset examples [S78].

**Image sitemap (XML) — surface a CDN-hosted image:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://example.com/blog/latte-art</loc>
    <image:image>
      <image:loc>https://cdn.example-cdn.net/img/hero-1200.jpg</image:loc>
    </image:image>
  </url>
</urlset>
```
Both `example.com` and `example-cdn.net` must be verified in Search Console. [S76]

**Reproducible alt-text audit (Python ≥3.11, standard library only):**

```python
#!/usr/bin/env python3
"""Find <img> tags missing or empty alt text (stdlib html.parser only)."""
from html.parser import HTMLParser
import sys

class AltAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs = []           # (has_alt_bool, alt_value, line_no)
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            d = dict(attrs)
            alt = d.get("alt")   # None if absent, "" if empty
            self.imgs.append((alt is not None, alt or "", self.getpos()[0]))

if __name__ == "__main__":
    html = open(sys.argv[1], encoding="utf-8").read()
    p = AltAuditor(); p.feed(html)
    missing = [i for i in p.imgs if not i[0]]
    empty   = [i for i in p.imgs if i[0] and i[1] == ""]
    present = [i for i in p.imgs if i[0] and i[1] != ""]
    print(f"total <img>: {len(p.imgs)} | has alt: {len(present)} | empty alt: {len(empty)} | missing alt: {len(missing)}")
    for m in missing:
        print(f"  missing alt at line {m[2]}")
```
Run: `python3 alt_audit.py page.html`. Pin `python>=3.11` (uses stdlib only; no third-party deps).

## Assumptions & limitations

- **Google's ML can recognize image content** (Cloud Vision accuracy is high), so alt text is one of several signals, not the only one. Alt text still matters for accessibility and for telling Google *which* specific subject an ambiguous image shows. [S82, S83]
- CWV is a **tie-breaker**, not a guarantee of rankings; a fast image won't rank a low-relevance page. [S45] (See `core-web-vitals.md`.)
- The exact LCP benefit of compression is **bounded**: field data shows image *download* time is rarely the bottleneck — TTFB and "resource load delay" (time before the browser even requests the image) usually dominate. So fix request chains and prioritization before obsessing over byte size. [S77]
- Specific **compression ratios** (e.g. "WebP is 30% smaller, AVIF 50% smaller than JPEG") vary by encoder/quality and are vendor-reported; treat them as directional, not guaranteed. (See Verify note below.)
- Google can change supported formats, sitemap tags, and CWV thresholds at any time. This article reflects docs current as of 2026-07-18.

## Empirical evidence

- **LCP subpart field study (web.dev/CrUX, n = origins in Chrome UX Report, 75th-percentile medians):** for poor-LCP origins, the median p75 image *load duration* is only ~350 ms while TTFB (~2,270 ms) and resource load delay (~1,290 ms) dominate. "The majority of origins with poor LCP spend less than 10% of their p75 LCP time downloading the LCP image." This reframes image optimization toward discovery/prioritization, not just compression. Strength: strong (first-party Chrome field data), limitation: CrUX is Chrome-only and traffic-gated. [S77]
- **Lazy-loading adoption/performance (HTTP Archive + WordPress A/B test, web.dev):** native `loading="lazy"` is used by ~29% of websites (HTTP Archive); 84% of those are WordPress. Correlational CrUX data shows lazy-loaded pages have slightly *worse* median LCP (3,546 ms vs 2,922 ms) — but the authors stress this is **correlational, not causal** (WordPress cohort skews slower). A controlled WebPageTest A/B on the twentytwentyone theme showed disabling lazy load improved archive-page LCP 13–15% (desktop/mobile), while single pages were neutral (within one standard deviation). Conclusion: above-the-fold/hero lazy loading is the harm; below-the-fold lazy loading helps. Strength: solid (public crawl data + controlled A/B), limitation: single theme/CMS, 2021-era. [S79]
- **Format support:** Google indexes AVIF and WebP; MDN lists AVIF/WebP as the recommended modern formats for smaller files at equal quality. Strength: robust (first-party + canonical reference), but exact savings are encoder-dependent. [S75, S78]

## Conflicting views

- **"Just shrink your images to fix LCP."** The dominant historical advice (and three Lighthouse image audits) says compress images. Field data shows download time is usually *not* the bottleneck; TTFB and load delay are. Both are true — compress *and* fix discovery/prioritization — but the emphasis shifts. [S77] vs common Lighthouse-audit framing.
- **"Alt text is dead because Google sees images."** Ahrefs demonstrates Google's Cloud Vision can mislabel (calls butter "cheese" at 91% confidence), arguing alt text still adds value; Google itself says it uses alt text + vision + page content together. Consensus: alt text still matters, especially for specific/ambiguous subjects. [S75, S82, S83]
- **"Lazy load everything for speed."** Native lazy loading helps below the fold but hurts LCP when applied to the hero — a nuance many CMS defaults get wrong (WordPress lazy-loads above the fold by default, which web.dev flagged as an antipattern). [S79]

## Common mistakes

1. **Keyword-stuffing alt text** (`alt="buy red shoes cheap red shoe store"`) — spam signal, bad UX. Use natural, descriptive text. [S75, S83]
2. **Lazy-loading the LCP image** — adds 500 ms+ to LCP in many cases; remove `loading="lazy"` and add `fetchpriority="high"` to the hero. [S77, S79]
3. **Blocking images from crawl** — `robots.txt` disallow or `noindex` on image URLs you want indexed; also, never rely on CSS background images for content you want indexed (Google doesn't index them). [S75]
4. **Missing `width`/`height`** — causes CLS layout shift; reserve space. [S38]
5. **No `<img>` fallback** in `<picture>`/JS image swaps — some crawlers ignore `srcset`/`picture`; always keep a real `src`. [S75]
6. **Inconsistent image URLs / CDN not verified** — re-hosting the same image under many URLs wastes crawl budget; cross-domain CDN images need both domains verified in Search Console for image-sitemap credit. [S75, S76]
7. **Cloaking images** — serving a different image to Googlebot than to users is cloaking (a spam violation). The documented "opt out of inline linking" (return 200/204) is explicitly *not* cloaking. [S75]
8. **Treating image SEO as ranking magic** — image optimization improves discoverability and UX, not direct web rankings; don't expect image tweaks to rescue an irrelevant or thin page. [S45]

## Further reading

- S75 — Google Search Central, "Image SEO best practices" (developers.google.com/search/docs/appearance/google-images) — Tier 1.
- S76 — Google Search Central, "Image sitemaps" (developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps) — Tier 1.
- S77 — web.dev, "Common misconceptions about how to optimize LCP" (web.dev/blog/common-misconceptions-lcp) — Tier 1.
- S78 — MDN, "Fix your website's LCP by optimizing image loading" (developer.mozilla.org/en-US/blog/fix-image-lcp) — Tier 1.
- S79 — web.dev, "The performance effects of too much lazy loading" (web.dev/articles/lcp-lazy-loading) — Tier 1.
- S80 — web.dev, "Responsive images" (web.dev/articles/responsive-images) — Tier 1.
- S81 — W3C, "Images Tutorial" (w3.org/WAI/tutorials/images) — Tier 1 (accessibility).
- S82 — Ahrefs, "Image SEO: 12 Actionable Tips" (ahrefs.com/blog/image-seo) — Tier 2.
- S83 — Ahrefs, "Alt Text for SEO" (ahrefs.com/blog/alt-text) — Tier 2.
- Related in this KB: `01-technical-seo/core-web-vitals.md` (LCP/CLS thresholds), `01-technical-seo/structured-data.md` (ImageObject/rich results), `02-on-page-seo/onpage-basics.md`.
