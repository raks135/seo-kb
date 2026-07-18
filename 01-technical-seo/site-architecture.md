---
title: Site Architecture & Internal Linking at Scale
topic_id: 01-technical-seo/site-architecture
tags: [internal-linking, site-architecture, crawl-depth, pagerank, siloing, topical-authority, technical-seo]
last_updated: 2026-07-18
confidence: robust
sources: [S2, S3, S20, S22, S25, S58, S59, S60]
---

## TL;DR
Internal links do three jobs at once: they let Google **discover** new pages, they signal **hierarchy and topical context**, and they distribute **link equity (PageRank)** across the site. A crawlable, pyramid/flat structure that keeps important pages within a few clicks of the homepage — plus descriptive contextual anchor text — is the single most controllable on-page lever for large sites. At scale, treat internal linking as an engineered system (hub pages, template-driven contextual links, orphan-page monitoring), not a one-off edit pass. Nofollow-based "PageRank sculpting" no longer works the way it used to (since 2019–2020 Google treats `nofollow`/`sponsored`/`ugc` as hints, not directives).

## Core explanation
**Site architecture** is the blueprint of how URLs relate to each other: the URL hierarchy, the navigation system, and — critically — the internal link graph that connects pages. **Internal links** are hyperlinks from one page on your domain to another page on the same domain.

In plain language: Googlebot finds pages by following links. The links you place tell Google (a) *which pages exist*, (b) *how they relate to each other and what they're about*, and (c) *which pages you consider important* by how often and from where you link to them.

Precisely, Google states links serve two explicit purposes: "Google uses links as a signal when determining the relevancy of pages and to find new pages to crawl" (S58). The PageRank algorithm — confirmed by Google as still in use ("after 18 years we're still using PageRank … in ranking," Gary Illyes, 2017, relayed by Ahrefs S20) — flows authority through the link graph, and internal links are the only part of that graph you fully control. John Mueller (Google) has called internal linking "super critical for SEO … one of the biggest things you can do on a website to guide Google and visitors to the pages that you think are important" (quoted in Ahrefs S20).

At scale (thousands to millions of URLs), architecture ceases to be a design nicety and becomes a **crawl-budget and indexation-control system**: the link graph decides what Google crawls, what it indexes, and what it ranks.

## Mechanics / how-to

### 1. Design a shallow, pyramid/flat hierarchy
- Put the homepage at the top; category pages one level down; subcategory/cluster pages next; detail pages (articles, products) at the leaves (Moz S22).
- Keep important, revenue- or traffic-driving pages **within ~2–3 clicks of the homepage** so crawl depth is low and link equity flows efficiently (Moz S22; Sitebulb guidance notes crawl depth as a core architecture metric, S59).
- Use a **category → subcategory → entity** pattern on large/programmatic sites so every generated page inherits a path from an established, indexed parent (seomatic.ai / practitioner guidance, S25 context).

### 2. Make every link crawlable
- Use real `<a href="…">anchor</a>` markup. Google crawls anchor text inside `<a>` elements it can reach (S58).
- For JavaScript-rendered links, confirm the rendered HTML contains the `<a href>` (use the URL Inspection Tool / compare raw vs rendered HTML). Client-side-only routers that swap content without updating the link graph can leave pages undiscoverable (S3, JS SEO basics).
- If an anchor must be empty, Google may fall back to the `title` attribute; for image links it uses the image `alt` text (S58).

### 3. Write good anchor text
Google's guidance (S58): anchor text should be **descriptive, reasonably concise, and relevant to both the source page and the destination page**.
- Good: "see the list of cheese types" → links to `/cheese-types`.
- Bad (too generic): "click here" or "article".
- Do **not** keyword-stuff anchor text — it violates Google's spam policies (S58). Use natural variation; exact-match anchors on every internal link are an over-optimization risk, not a requirement.
- Don't chain links right next to each other — it hurts readability and wastes surrounding contextual text.

### 4. Build a contextual internal-linking habit
- Link **contextually** within body content (editorial links) to the most relevant supporting/cluster pages — these carry stronger topical signal than nav/footer links (SEL S25 types: navigational, contextual, breadcrumb, related, CTA, HTML sitemap).
- Use **breadcrumbs** (`Home > Blog > SEO > Internal Linking`) with structured `BreadcrumbList` markup — they reinforce hierarchy for users and crawlers (S25).
- Add an **HTML sitemap** page for human browsing (distinct from the XML sitemap for crawlers) on very large sites (S25).

### 5. Engineer internal links at scale
For sites with thousands of pages, do not hand-link:
- Define **hub/pillar pages** that link out to all cluster pages; ensure cluster pages link back to the hub and to 3–5 sibling "related" pages (hub-to-spoke, spoke-to-variation pattern, practitioner guidance S25/large-site case studies).
- Generate contextual "related/see-also" link blocks **in the page template** (not as an afterthought) so new pages are born with inbound links (seomatic.ai guidance).
- Prioritize linking from your **strongest pages** (high PageRank / top-ranked) to the pages you most want to push — equity flows from where it enters (S20).
- Monitor **orphan pages** (pages with zero internal inbound links) continuously — see the worked example.

## Worked example / code

### A. Breadcrumb with structured data (runnable)
```html
<!-- Breadcrumb links (visible) -->
<nav aria-label="Breadcrumb">
  <a href="https://example.com/">Home</a> &gt;
  <a href="https://example.com/seo/">SEO</a> &gt;
  <span>Internal Linking</span>
</nav>

<!-- Corresponding JSON-LD (valid per Schema.org / Google structured-data intro) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home",     "item": "https://example.com/"},
    {"@type": "ListItem", "position": 2, "name": "SEO",      "item": "https://example.com/seo/"},
    {"@type": "ListItem", "position": 3, "name": "Internal Linking", "item": "https://example.com/seo/internal-linking/"}
  ]
}
</script>
```
*Data source: author-authored example; validate with Google Rich Results Test. Schema vocabulary per S51; breadcrumb feature per S49.*

### B. Find orphan pages (Python, reproducible)
Compare URLs Google *could* know (sitemap + log files) against URLs that actually receive an internal link in a crawl export. Requires: Python 3.11, `pandas>=2.0`. Inputs are your own data.

```python
# orphans.py — find pages with no internal inbound links
import pandas as pd

# 1) URLs Google is told about / has seen
sitemap_urls = pd.read_csv("sitemap_urls.csv")["url"].str.strip().str.lower()
log_urls     = pd.read_csv("access_log_urls.csv")["url"].str.strip().str.lower()
known = set(pd.concat([sitemap_urls, log_urls]).drop_duplicates())

# 2) URLs that received at least one internal link (Screaming Frog
#    "Internal" export, or Ahrefs/Sitebulb internal-link report)
#    Column "Address" = source; "Destination" = linked-to URL.
links = pd.read_csv("internal_links.csv", usecols=["Destination"])
linked = set(links["Destination"].str.strip().str.lower().dropna())

orphans = sorted(known - linked)
print(f"Known URLs: {len(known)} | Linked: {len(linked)} | Orphans: {len(orphans)}")
for u in orphans[:50]:
    print(u)
```
*Run: `python3 orphans.py`. Fix each orphan by adding a relevant contextual link from a related, indexed page (or remove the URL if it should not exist).*

### C. Prioritize by internal-link count (quick triage)
```python
# Which important pages are starved of internal links?
links = pd.read_csv("internal_links.csv")
inbound = links.groupby("Destination").size().rename("inbound_links")
important = pd.read_csv("priority_urls.csv")["url"].str.lower()
starved = important[~important.isin(inbound[inbound >= 3].index)]
print("Priority pages with <3 internal links:", starved.tolist())
```

## Assumptions & limitations
- **PageRank is one of hundreds of signals** (Google, S20/S58). Internal linking improves discoverability and equity flow but will not rank weak, irrelevant, or thin content on its own.
- **Correlation ≠ causation.** Most "internal linking → higher rankings" evidence is correlational (more-linked pages also tend to be better/content-rich). Google has not published a quantified internal-link ranking weight.
- **JS rendering caveat:** if links only exist after client-side JS executes, discovery depends on Google's renderer picking them up (S3). Other bots (some social/AI crawlers) may not run JS at all.
- **Architecture ≠ guarantee of crawl.** Crawl budget on very large sites is also governed by site health, server capacity, and signals like freshness/quality; links help but don't override those.
- Google has **not** published a specific "safe" click-depth threshold; the "2–3 clicks" figure is practitioner consensus (Moz S22, Sitebulb S59), not a confirmed Google rule.

## Empirical evidence
What the evidence actually supports:
- **Google's own statements (Tier 1):** links are used for relevancy + discovery (S58); PageRank is still a ranking signal (S20 relaying Illyes); `nofollow` family are hints since 2019–2020 (S60).
- **Practitioner correlation (Tier 2):** Ahrefs' internal-linking guide (S20) reports that, generally, the more internal links a page has, the higher its PageRank — but stresses *quality* of the linking page matters as much as quantity. Moz (S22) frames a pyramid structure with low crawl depth as standard for high-performing sites.
- **Large-site case reports (emerging):** programmatic-SEO practitioners report indexation-rate and crawl-priority gaps between well-linked vs poorly-linked template pages (seomatic.ai / marketingagency.sg, S25 context). These are anecdotal/observational, not controlled experiments.
- **Single-source claim (flagged):** a frequently-cited figure — "URLs receiving internal links from top-ranked pages rank ~2 positions higher on average" (attributed to an Ahrefs 1-billion-page study by a third-party blog) — is **not independently verified here**. Treat as directional, not authoritative. → See Verify task below.

**Strength of evidence:** Google's discovery/PageRank/nofollow statements = robust (Tier 1, directly from Google). "Flat/pyramid structure improves outcomes" = practitioner-consensus (robust in practice but not Google-confirmed). Programmatic-scale indexation lift = emerging, sample-limited.

## Conflicting views
- **Flat vs. deep architecture:** Most practitioner guides (Moz S22, many vendor blogs) recommend a flat/pyramid structure with low crawl depth. The contrarian view (some 2025/2026 technical-SEO writing) argues click-depth is overstated and that crawl budget is driven more by site quality and signals than by raw depth — so "flatten everything" can be cargo-culted. Resolution: keep *important* pages shallow; don't sacrifice UX/topic coherence just to reduce depth.
- **PageRank sculpting with `nofollow`:** Pre-2019 playbooks advised funneling equity by `nofollow`-ing less important links. Since Google made `nofollow`/`sponsored`/`ugc` **hints** (S60, effective March 2020 for crawling/indexing), Google *may* still crawl and pass signals through them; the old "conserve PageRank by nofollowing" trick no longer reliably works. Some older articles still recommend it — disregard for post-2020 strategy.
- **Exact-match anchor text:** Black-hat-era advice pushes keyword-exact anchors; Google explicitly warns against anchor keyword-stuffing (S58). Use natural, varied, descriptive anchors.

## Common mistakes
1. **Orphan pages** — pages with zero internal inbound links; hard to discover/index, poor equity flow (Moz S22). Fix via the orphan script above.
2. **Broken internal links / 404s** — waste crawl budget and leak equity; audit and fix redirects (S22).
3. **Redirect chains in internal links** — link directly to the final URL, not through 3xx hops.
4. **JS-only navigation** with no crawlable `<a href>` fallback — pages become undiscoverable to bots that don't render (S3, S58).
5. **Generic anchor text** ("click here", "read more") — loses topical signal (S58).
6. **Keyword-stuffing anchor text** — spam-policy risk (S58).
7. **Over-using `nofollow` on internal links** to "sculpt" — ineffective post-2019 and can harm legitimate flow (S60).
8. **Footer/sidebar link spam** to every page — dilutes signal and looks manipulative; prefer contextual, relevant links (S25).
9. **Ignoring crawl budget at scale** — letting millions of low-value faceted URLs dilute crawl of money pages; use robots/canonicals + internal-link focus on high-value templates.
10. **Linking irrelevant pages just to pass equity** — context matters; off-topic links confuse topical signals.

## Further reading
- **Tier 1:** Google, "Link best practices for Google" (S58) — crawlable links + anchor text. Google, "Evolving 'nofollow'" (S60). Google, "How Search works" (S2). Google, "JavaScript SEO basics" (S3).
- **Tier 2:** Ahrefs, "Internal Links for SEO: An Actionable Guide" (S20, updated Mar 2026). Moz, "Internal Links SEO Best Practices" (S22). Search Engine Land, "Internal Linking for SEO" (S25, updated Nov 2025). Sitebulb, internal-linking audit docs (S59).
- **Related KB articles:** `01-technical-seo/crawlability-indexation.md`, `01-technical-seo/javascript-seo.md`, `04-content-strategy/content-hubs.md` (pillar/cluster), `08-ecommerce-seo/ecommerce-seo.md` (faceted nav).
