---
title: JavaScript SEO (rendering, hydration, dynamic rendering, SSR)
topic_id: 01-technical-seo/javascript-seo
tags: [javascript, rendering, ssr, csr, hydration, dynamic-rendering, crawl-budget, web-rendering-service]
last_updated: 2026-07-18
confidence: robust
sources: [S3, S54, S55, S56, S57]
---

## TL;DR
Googlebot fetches the raw HTML first, then queues the page for a **separate rendering pass** (an evergreen Chromium "Web Rendering Service") that executes JavaScript before indexing — so content JS-injected at load time is usually discovered, but with an added delay and extra resource cost. Treat JavaScript as a *different* delivery mechanism, not an SEO threat: server-side rendering, static/hybrid rendering, or hydration remains the safest option, while pure client-side rendering (CSR) is "SEO on hard mode." Verify what Google actually sees with the URL Inspection Tool's **View Rendered HTML**, not by trusting the browser.

## Core explanation
JavaScript SEO is the branch of technical SEO that makes JavaScript-heavy sites (SPAs, headless CMS front-ends, React/Vue/Angular/Svelte apps) easy for crawlers to **crawl, render, and index**. The core complication is that, unlike static HTML where the full content is in the initial HTTP response, many JS apps ship an "app shell" and inject content after scripts run.

Plain language: Google visits your page twice in effect — once to grab the skeleton HTML, and again (later, in a queue) to run the scripts and see the finished page. If your important text, links, or metadata only exist *after* the scripts run, Google still needs that second pass to see them.

Precise model (per Google's own docs, S3): Google processes a JS page in three phases — **Crawling → Rendering → Indexing**.
- **Crawling:** Googlebot reads `robots.txt`; if a URL or the resources it needs are disallowed, it skips fetching/rendering. It parses the initial HTML for `<a href>` links and queues them.
- **Rendering:** pages returning HTTP `200` (and not blocked by a `noindex` meta/header) are queued for rendering. A headless, evergreen Chromium renders the page and executes JS "once Google's resources allow" — the wait can be seconds but **can take longer**. Rendered HTML is re-parsed for new links, and the rendered DOM is what gets indexed.
- **Indexing:** the rendered content is analyzed and stored.

`robots.txt` is enforced before rendering, so **Google will not render JavaScript from blocked files or on blocked pages** (S3). This is the single most common self-inflicted JS-SEO failure.

## Mechanics / how-to
**1. Pick a rendering strategy (in order of robustness):**
- **SSR (server-side rendering)** or **static/hybrid rendering** — full or near-full HTML in the HTTP response. Fastest for users and most reliable for crawlers (S3 explicitly still recommends SSR/pre-rendering).
- **Hydration / progressive hydration (e.g. Next.js, Astro, Remix)** — server sends HTML, client "hydrates" it into an interactive app. Best of both worlds.
- **CSR (client-side rendering)** — acceptable but riskier: every page pays the render-queue cost and is exposed to WRS limitations.
- **Dynamic rendering** — serve a pre-rendered static HTML snapshot to crawlers, CSR to users. A *temporary* workaround only; not a long-term recommendation (S54).

**2. Make content and links crawlable without depending on execution:**
- Render primary content and internal links in the initial HTML where possible.
- Use the **History API** for client-side routing — never `#`/fragment URLs, which Google cannot reliably resolve (S3).
- Ensure links are real `<a href="…">` elements (S3).

**3. Set critical tags correctly:**
- `<title>`, meta description, and canonical can be set via JS, but **keep the JS value identical to the HTML value**; if no canonical exists in HTML, a JS-injected one is honored (S3; Ahrefs notes Google added this exception after testing, S56). Conflicting tags trigger "most restrictive" behavior.
- Don't rely on JS to inject `noindex`/robots — it works only after rendering, which may be too late for crawl savings.

**4. HTTP status codes & soft-404s:**
- In SPAs, client-side routing often returns `200` even for missing pages, creating **soft-404s** that get indexed (S3, S55). Mitigate by `window.location.href = '/not-found'` (a real `404` URL) or injecting `<meta name="robots" content="noindex">` (S3).

**5. Don't block render-critical resources:**
- Allow crawling of JS and CSS files in `robots.txt`. The Web Rendering Service "continuously analyzes and identifies resources that don't contribute to essential page content and may not fetch such resources" (S55) — so don't hide analytics/non-essential calls but do keep core bundles fetchable.

**6. Monitor:** use the **Crawl Stats report** in Search Console to watch Googlebot/WRS activity, and the **URL Inspection Tool → View Rendered HTML** to confirm what Google sees (S3, S55).

## Worked example / code
**A. robots.txt — allow render-critical assets (do NOT block JS/CSS):**
```txt
User-agent: Googlebot
Allow: /static/js/
Allow: /static/css/
Disallow: /private/
# Note: blocking /static/js/ would prevent Google from rendering the app shell.
```

**B. Detect a crawler and serve a pre-rendered snapshot (dynamic rendering pattern, S54).** Pseudocode — route bot requests to a headless renderer:
```js
// Node/Express-style (conceptual; production uses a real headless renderer)
const isBot = /googlebot|bingbot|slurp|duckduckbot/i.test(req.headers['user-agent'] || '');
if (isBot) {
  const browser = await puppeteer.launch();      // puppeteer@23.x
  const page = await browser.newPage();
  await page.goto(req.url, { waitUntil: 'networkidle0' });
  const html = await page.content();              // fully rendered static HTML
  await browser.close();
  res.send(html);                                 // same content as users see
} else {
  next();                                         // serve the normal CSR app to users
}
```
*Data source / version: Google "Dynamic Rendering" guidance (S54, last updated 2025-12-10); puppeteer@23.x as of 2026. The snapshot MUST contain the same primary content users see — serving different content is cloaking (S54).*

**C. Verify what Google renders — compare raw vs rendered HTML:**
```bash
# 1) Raw HTML Google first receives (may be an app shell)
curl -s https://example.com/product/red-shoes | grep -c "Red Shoes"

# 2) Rendered HTML Google indexes (run a headless browser locally to emulate WRS)
node render-check.js   # uses puppeteer@23 to load the URL and dump rendered DOM
# If "Red Shoes" appears only in step 2, the page depends on JS to show content.
```
Then confirm in Search Console: **URL Inspection → Live Test → View Rendered HTML** and check the text/title/links are present.

## Assumptions & limitations
- **Rendering is not instant or guaranteed.** The queue delay means newly published JS pages may take longer to appear than static pages; Google resources, not your publish time, gate the render (S3).
- **WRS may skip non-essential resources** (S55), so lazy-loaded content that never enters the rendered viewport/DOM may be missed.
- **Not all crawlers run JS.** Bing and most social/AI crawlers (and many LLM bots such as GPTBot/ClaudeBot/PerplexityBot) may not execute JavaScript at all — a CSR page can be invisible to a growing share of AI/search surfaces (S54 notes "other search engines may choose to ignore JavaScript"; corroborated by practitioner reporting, S56). This is an **emerging** claim for the AI-crawler landscape and should be re-verified per bot.
- **Google has not published a quantified ranking penalty** for client-side rendering — the cost is delay + crawl-budget/resource exposure, not a direct demotion. Ranking still depends on relevance/quality once content is indexed.
- **`robots.txt` enforcement precedes rendering**: a blocked page/file is never rendered (S3).
- Everything above applies to Google; other engines vary and are less documented.

## Empirical evidence
- **Strength: strong (Tier-1 primary).** The three-phase crawl→render→index model, the rendering queue, robots.txt precedence, History-API requirement, and soft-404 guidance are all stated directly in Google's official JavaScript SEO documentation (S3, S54, S55) — these are first-party specifications, not correlation studies.
- **Practitioner corroboration (Tier-2):** Ahrefs' Patrick Stox confirms JS "isn't bad for SEO" but that problems arise when JS *builds the whole page or changes existing content*; reports the canonical-via-JS exception Google added after his tests, and notes CSR trades performance for functionality (S56).
- **Sample limitations:** There is no large, dated, peer-reviewed study quantifying how often CSR pages fail to index versus SSR. Most "CSR is worse" evidence is anecdotal/observational (e.g., Search Console "Crawled – currently not indexed" on SPA product pages, S56-adjacent reports). Treat "SSR ranks better" as **folklore-adjacent** until a controlled study appears; the defensible claim is *SSR is more reliable and faster to index*.
- **No guaranteed rankings:** none of these techniques improve rankings by themselves — they remove indexing/visibility blockers only.

## Conflicting views
- **"Two waves of indexing" vs Google's denial.** The popular mental model is that Google crawls HTML in "wave 1" and renders JS in "wave 2." Google's Martin Splitt stated *"there's no such thing as the second wave of crawling-ish"* — Google considers the process more complex than two discrete waves, though he allowed the two-wave framing remains a *useful simplification* (S57). Practitioners (S56) and the official docs (S3) effectively describe the same crawl-then-render delay; the disagreement is terminology, not substance.
- **Dynamic rendering: acceptable vs risky.** Google documents dynamic rendering as a legitimate workaround that is *not* cloaking *if content is equivalent* (S54), while some practitioners (S56) argue it is effectively cloaking and "definitely" risky, and are glad Google now steers against it. Resolution: it's allowed but discouraged; equivalence of content is the bright line.
- **"JS is fine for SEO" vs "CSR is hard mode."** Google says it renders JS fine (S3); many developers observe CSR pages underperform on speed and indexing reliability (Hacker News practitioner consensus, S56-adjacent). Both can be true: Google *can* render JS, but CSR shifts cost/risk onto the crawler and the user.

## Common mistakes
1. **Blocking JS/CSS in robots.txt** → Google never renders the page (S3). Never `Disallow` your framework bundles.
2. **Fragment/`#!` routing** → `#/page` URLs aren't crawlable; use the History API (S3). The old AJAX `#!` scheme is deprecated.
3. **Soft-404s in SPAs** → returning `200` for missing content gets error pages indexed (S3, S55).
4. **Injecting conflicting canonicals/robots via JS** → "most restrictive" wins; duplicate or mismatched tags cause canonicalization chaos (S56).
5. **Lazy-loading above-the-fold or critical content** behind scroll/interaction so it's absent from the rendered DOM.
6. **Assuming instant indexing** of JS pages — the render queue adds latency (S3).
7. **Dynamic rendering that serves different content to bots vs users** → cloaking, a spam-policy violation (S54).
8. **Trusting the browser view** instead of **View Rendered HTML** in Search Console to diagnose what Google sees (S3, S55).
9. **Ignoring non-Google bots** — shipping CSR-only and losing Bing/AI-crawler visibility (S54, S56).

## Further reading
- **[Tier 1]** Google Search Central, "Understand JavaScript SEO Basics" — S3 (developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- **[Tier 1]** Google Search Central, "Dynamic Rendering as a workaround" — S54 (developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering, last updated 2025-12-10)
- **[Tier 1]** Google Search Central, "Fix Search-Related JavaScript Problems" — S55 (developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript, last updated 2025-12-18)
- **[Tier 2]** Ahrefs, "JavaScript SEO Issues & Best Practices" (Patrick Stox) — S56 (ahrefs.com/blog/javascript-seo, updated 2025-05-09)
- **[Tier 2]** Search Engine Roundtable, "Google: No Such Thing As Two Waves Of Indexing Or Crawling" — S57 (seroundtable.com/google-no-two-waves-indexing-29225.html)
- **[Tier 1]** web.dev, "Rendering on the web" (CSR/SSR/CSR-hydration overview) — referenced by S3/S54
