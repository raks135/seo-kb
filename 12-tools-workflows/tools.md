---
title: SEO Tools & Workflows (landscape, audits, automation)
topic_id: 12-tools-workflows/tools
tags: [tools, gsc, ahrefs, semrush, screaming-frog, sitebulb, automation]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S20, S21, S28]
---

## TL;DR
A practical SEO stack: **Google Search Console** (free, first-party truth), a crawler (**Screaming Frog** or **Sitebulb**) for technical audits, and a backlink/keyword suite (**Ahrefs** or **Semrush**) for research. Automate repetitive checks (sitemaps, log parsing, broken-link scans) with scripts so you can focus on strategy.

## Core explanation
Tools fall into tiers: first-party (GSC, GA4, PageSpeed Insights — S1/S28) give ground truth; crawlers reveal on-site issues; suites provide competitive/backlink/keyword data (S20/S21). No tool replaces judgment; each has blind spots.

## Mechanics / how-to
- **GSC:** weekly health check (coverage, CWV, sitemaps).
- **Crawler:** full site crawl → find orphan/duplicate/redirect-chain/title issues.
- **Suite:** gap analysis, backlink audits, rank tracking (secondary KPI).
- **Automation:** cron scripts for sitemap generation, log analysis, schema validation.

## Worked example / code
Generate a sitemap with Python (filesystem walk) — illustrative:
```python
import os, xml.sax.saxutils as u
base="https://example.com/"
urls=[]
for root,_,files in os.walk("public"):
    for f in files:
        if f.endswith(".html"):
            p=os.path.join(root,f).replace("public/","").replace("index.html","")
            urls.append(base+p)
xml="\n".join(f"<url><loc>{u.escape(u)}</loc></url>" for u in urls)
open("public/sitemap.xml","w").write(f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xml}</urlset>')
```

## Assumptions & limitations
- Third-party metrics (DA/DR, volumes) are proprietary estimates, not Google internals.
- Crawlers can miss JS-rendered content unless configured to render.
- Free tiers are limited; paid tools vary in crawl depth and data freshness.

## Empirical evidence
Tool vendors publish methodology (S20/S21); GSC/PageSpeed are authoritative first-party (S1/S28). Crawler accuracy is well established in practitioner use.

## Conflicting views
- **"Tool X is the only one you need."** Each covers different blind spots; a combo is standard.
- **"DA/DR predicts rankings."** Useful as relative comparison, not a Google metric.

## Common mistakes
- Relying solely on a rank tracker as the KPI.
- Ignoring GSC (the free first-party source).
- Crawling without render for JS sites.
- Not automating repetitive checks.

## Further reading
- S1 — Google, "SEO Starter Guide" / Search Central tools — Tier 1
- S28 — PageSpeed Insights / Lighthouse — Tier 1
- S20 — Ahrefs — Tier 2
- S21 — Semrush — Tier 2
