---
title: Log File Analysis for Crawl Budget
topic_id: 01-technical-seo/log-file-analysis
tags: [log-file-analysis, crawl-budget, googlebot, server-logs, technical-seo, crawl-efficiency, internal-linking]
last_updated: 2026-07-18
confidence: robust
sources: [S2, S61, S62, S63, S64, S65, S66]
---

## TL;DR
Server log files are the **only record of what crawlers actually did on your site** — not a simulation. For large or auto-generated sites (thousands+ URLs), log analysis reveals wasted crawl (soft-404s, faceted/parameter URL combinations, redirect chains, 5xx errors) so you can redirect Googlebot's budget toward your valuable pages. For most small sites (a few thousand URLs, content crawled same-day) crawl budget is **not** a priority (Google, S62). Corroborate every Googlebot hit with a reverse-DNS lookup — the user-agent string alone is spoofable (S63). Crawling is **not** a ranking signal (S62): more crawl ≠ higher positions.

## Core explanation
A **server access log** records every HTTP request made to your site: the requesting IP, the request method + path, the HTTP status code returned, the response size, the timestamp, and the user-agent (which crawler/browser made the request). **Log file analysis** in SEO means parsing those logs to see exactly how Googlebot (and Bingbot, and increasingly AI-retrieval bots like OAI-SearchBot/PerplexityBot) crawl your site — which URLs, how often, with what status, and how fast your server answered.

**Crawl budget** is the bridge between logs and SEO. Google defines a site's crawl budget as "the set of URLs that Google can and wants to crawl" (S61/S62). It has two components:
- **Crawl capacity limit** — the maximum number of simultaneous parallel connections Googlebot uses, plus the delay between fetches. This is Google being a "good citizen" so it doesn't overwhelm your server (S62).
- **Crawl demand** — how much Google *wants* to crawl you, driven by a URL's popularity/PageRank, how often its content changes (staleness tolerance), and site-wide events like a move (S61/S62).

The effective budget is the **minimum** of the two: even if capacity is high, low demand means less crawling (S61). Logs let you measure both: response times tell you about capacity, and crawl frequency per URL tells you about demand.

Plain-language upshot: if Googlebot spends 40% of its visits on faceted-navigation URLs that return thin or duplicate content, it has less budget left for your money pages — so new product pages get crawled and indexed slower. Logs make that waste visible and fixable.

## Mechanics / how-to

### 1. Get the logs
Logs live on your server (Nginx `/var/log/nginx/access.log`, Apache, or your host's control panel). Download a representative window — at least **14–30 days** so you capture crawling rhythm and any weekly seasonality (S65). Note: logs are often rotated/deleted after a limited period, so grab them before they expire (S65).

### 2. Isolate Googlebot (don't trust the user-agent)
Filter log rows where the user-agent contains `Googlebot`. **But** anyone can spoof a user-agent, so for any security/compliance-sensitive decision, verify with reverse DNS (S63):
- Run a reverse DNS lookup on the IP: `host 66.249.66.1` → should resolve to `crawl-66-249-66-1.googlebot.com`.
- Run a forward DNS lookup on that hostname → must return the **same** original IP.
- Genuine Googlebot hostnames end in `googlebot.com`, `google.com`, or `googleusercontent.com` (S63).
- For scale, match IPs against Google's published CIDR ranges (the `common-crawlers.json` / `special-crawlers.json` lists) rather than per-row `host` calls (S63).

### 3. Compute the core metrics
For the Googlebot-filtered rows, aggregate by (S64/S65/S66):
- **Crawl volume by URL** — which URLs get crawled most/least.
- **Status-code distribution** — % `2xx`, `3xx`, `4xx`, `5xx`.
- **Crawl over time** — requests per day; spot drops (crawl demand fell) or spikes (possible move/relaunch).
- **Response time** — slow URLs (high TTFB) cap the crawl capacity limit; a faster server lets Google fetch more per connection (S62).
- **Crawl by directory/section** — e.g., is `/blog/` starving while `/filters/` gorges?

### 4. Find and fix crawl waste
Google explicitly warns that "many low-value-add URLs can negatively affect a site's crawling and indexing," draining budget from valuable pages (S62). In order of significance, the waste categories are (S62):
1. **Faceted navigation / infinite URL-parameter combinations** (e.g., `/shoes?color=red&size=10&sort=price`) — the #1 crawl-budget killer on e-commerce/large sites.
2. **Duplicate content** (near-duplicate URLs).
3. **Soft-404s** — URLs that return `200 OK` but show "not found" content; Googlebot wastes budget re-crawling them.
4. **Hacked / spammy pages.**
5. **Generally low-quality or thin content.**

Fix each by: `noindex` + (where appropriate) `robots.txt` disallow or canonical to a representative URL; return true `404`/`410` for gone pages; collapse facets with canonical/parameter handling; reduce redirect chains (long chains "may have a negative effect on crawling," S62). Note: **URLs disallowed in `robots.txt` do NOT consume crawl budget** because Google won't fetch them (S62) — so `robots.txt` is your cheapest crawl-budget lever for genuinely low-value URLs.

### 5. Close the loop with your sitemap
Cross-reference crawled URLs against your XML sitemap + important template pages (S66). Any high-value URL that Googlebot **hasn't** crawled in the window is a discovery/indexation gap to investigate (internal-link it from strong pages — see `01-technical-seo/site-architecture.md`).

## Worked example / code
Reproducible parser in Python 3.11 with `pandas>=2.0`. Input = your own combined-format access log. Combined log line example:

```
66.249.66.1 - - [01/Jul/2026:12:00:00 +0000] "GET /shoes?color=red HTTP/1.1" 200 1843 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
```

```python
# log_analysis.py — parse + analyze an access log for Googlebot crawl budget
import re
import pandas as pd
from collections import Counter

LOG_RE = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+)[^"]*" '
    r'(?P<status>\d{3}) (?P<size>\S+) '
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"'
)

def load(path: str) -> pd.DataFrame:
    rows = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            m = LOG_RE.search(line)
            if not m:
                continue
            rows.append(m.groupdict())
    df = pd.DataFrame(rows)
    df["status"] = df["status"].astype(int)
    df["time"] = pd.to_datetime(df["time"], format="%d/%b/%Y:%H:%M:%S %z")
    return df

def is_googlebot(ua: str) -> bool:
    return "googlebot" in ua.lower()

# 1) Load + keep only Googlebot
df = load("access.log")
bot = df[df["ua"].map(is_googlebot)].copy()
print(f"Total requests: {len(df):,} | Googlebot requests: {len(bot):,}")

# 2) Core metrics
print("\n-- Status code distribution (Googlebot) --")
print(bot["status"].value_counts(normalize=True).mul(100).round(1))

print("\n-- Top 15 most-crawled URLs --")
print(bot["url"].value_counts().head(15))

bot["day"] = bot["time"].dt.date
print("\n-- Crawl requests per day --")
print(bot.groupby("day").size())

# 3) Crawl-waste detector
waste_404 = bot[bot["status"].isin([404, 410])]
waste_3xx = bot[bot["status"].between(300, 399)]
waste_facet = bot[bot["url"].str.contains(r"[?&](color|size|sort|page|filter)=", case=False, regex=True)]
print(f"\nWasted crawl -> 404/410: {len(waste_404):,} | 3xx redirects: {len(waste_3xx):,} "
      f"| faceted/param URLs: {len(waste_facet):,}")

# 4) Important-but-not-crawled gap (sitemap vs crawled)
sitemap = pd.read_csv("sitemap_urls.csv")["url"].str.lower()
crawled = set(bot["url"].str.lower())
missing = sorted(set(sitemap) - crawled)
print(f"\nSitemap URLs never crawled by Googlebot in window: {len(missing)}")
```

*Data source: your own server `access.log` + `sitemap_urls.csv`. Run with `python3 log_analysis.py`. For production-scale logs (millions of lines), stream or use a columnar engine; the regex + pandas approach is fine up to low millions on a normal laptop. To harden bot identification, replace `is_googlebot()` with a reverse-DNS check (S63) or an IP-range match against Google's published JSON lists before trusting the user-agent.*

## Assumptions & limitations
- **Crawl budget matters mainly for big/auto-generated sites.** Google states plainly that sites with "a few thousand URLs" are "most of the time… crawled efficiently," and if new pages are crawled the same day you publish, "crawl budget is not something webmasters need to focus on" (S62). Don't run log analysis for crawl budget on a 200-page brochure site — you'll find noise, not signal.
- **Logs ≠ rankings.** Crawling is a prerequisite for being in the index, but "an increased crawl rate will not necessarily lead to better positions," and crawling is explicitly **not** a ranking signal (S62). Optimizing crawl budget helps *discovery/indexation of the right pages*; it does not directly lift rankings.
- **User-agent filtering is not proof of identity.** Spoofed bots exist; reverse-DNS/verify for any decision that blocks or allows traffic (S63).
- **GSC Crawl Stats is a partial proxy, not the raw log.** Google Search Console's Crawl Stats report (Settings ▸ Crawl stats) summarizes crawl activity and is useful, but it samples/summarizes and may omit some requests — the raw server log remains the authoritative source of what was fetched (OnCrawl comparison, aligned with practitioner guidance S64; GSC is a Google product UI, not opened as a citation here → see Verify note).
- **Time window bias.** A 7-day log during a quiet period may misrepresent typical crawl demand; prefer ≥14–30 days and avoid drawing conclusions from a single anomalous spike (e.g., a relaunch).
- **Google has not published a "safe" crawl-efficiency percentage** or a guaranteed fix-it threshold; the waste categories and their priority order come from Google's 2017 guidance (S62), which has not been formally superseded.

## Empirical evidence
- **What's robust (Tier 1, Google):** the two-factor crawl-budget definition (capacity limit + demand), the "low-value-add URLs drain budget" finding with its priority order, the fact that disallowed URLs don't cost budget, that `crawl-delay` is ignored by Googlebot, that site speed raises the crawl rate, and that crawling ≠ ranking — all stated directly by Google (S61/S62). Google's reverse-DNS verification procedure is documented step-by-step (S63).
- **What's practitioner-corroborated (Tier 2):** that log analysis is the definitive way to see real crawler behavior (Ahrefs S65, SEL S64), and that tools like Screaming Frog's Log File Analyser operationalize "find the most/least crawled URLs, errors, redirects, and crawl waste" (S66) — consistent with Google's own guidance. Screaming Frog independently restates the crawl-budget = capacity + demand framing (S66), corroborating S61/S62.
- **Strength of evidence:** high for the conceptual model and the waste categories (direct Google statements, corroborated by multiple tool vendors). Lower for any specific "you should aim for X% non-waste" target — Google has not quantified one, so any such figure in the wild is vendor folklore and is **not** asserted here.

## Conflicting views
- **"Everyone needs log analysis."** Google itself pushes back: crawl budget is a non-issue for most sites (S62). The conflicting view (some agency marketing) implies every site must do log analysis constantly. Resolution: do it when you have scale, frequent changes, or suspected crawl problems — not as a default chore.
- **`robots.txt` vs `noindex` for crawl control.** For purely low-value URLs, `robots.txt` disallow is cheaper (zero budget spent, S62). But if you need the URL *indexed* yet not duplicated, use `canonical`/`noindex` instead — and remember `noindex` still lets Googlebot *crawl* the URL (it just drops it from the index), so `noindex` does **not** save crawl budget the way `robots.txt` does. Some guides blur this distinction; Google's position is explicit (S62).
- **Log analysis vs GSC Crawl Stats.** Some argue GSC is "good enough" and logs are overkill; others (OnCrawl, SEL S64) note GSC summarizes and may miss detail. Resolution: GSC for quick health checks, raw logs when you need exact per-URL, per-bot, per-status truth — especially on large sites.

## Common mistakes
1. **Trusting the user-agent alone** — spoofed bots; verify with reverse DNS for security decisions (S63).
2. **Analyzing a too-short window** — one week hides rhythm; use ≥14–30 days.
3. **Doing crawl-budget work on a tiny site** — wasted effort; Google says it doesn't matter below a few thousand URLs (S62).
4. **Confusing crawl with rank** — celebrating "more crawl" as a win; crawling is not a ranking signal (S62).
5. **Using `noindex` to "save crawl budget"** — it doesn't; the URL is still fetched. Use `robots.txt` disallow for truly valueless URLs (S62).
6. **Ignoring soft-404s** — they eat budget and confuse indexing; return real `404`/`410` (S62).
7. **Letting faceted navigation run wild** — infinite `?param` combinations are the top crawl-budget drain (S62); canonicalize or disallow.
8. **Long redirect chains** in internal links — they harm crawling (S62); link directly to final URLs.
9. **Not cross-referencing with the sitemap** — you never notice high-value URLs Googlebot isn't crawling (S66).
10. **Treating GSC Crawl Stats as the complete log** — it's a sample; raw logs are authoritative for per-URL truth (S64).

## Further reading
- **Tier 1:** Google, "Crawl Budget Management" (S61) — official advanced guide (capacity limit + demand, best practices). Google Search Central Blog, "What Crawl Budget Means for Googlebot" by Gary Illyes (S62) — the definitive crawl-budget explainer, waste categories, FAQ. Google, "Verify Requests from Google Crawlers and Fetchers" (S63) — reverse-DNS + IP-range verification.
- **Tier 2:** Search Engine Land, "Log File Analysis for SEO" (S64) — practical end-to-end guide; Ahrefs, "What is Log File Analysis?" (S65) — what logs contain and why it matters; Screaming Frog, "22 Ways To Analyse Logs" (S66) — tool-driven crawl-waste/redirect/status analysis.
- **Related KB articles:** `01-technical-seo/crawlability-indexation.md` (robots.txt, sitemaps, canonicals), `01-technical-seo/site-architecture.md` (internal linking to lift crawl of important pages), `08-ecommerce-seo/ecommerce-seo.md` (faceted navigation), `01-technical-seo/javascript-seo.md` (WRS rendering cost).
