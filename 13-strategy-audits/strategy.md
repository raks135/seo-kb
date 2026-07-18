---
title: Strategy, Audits & Processes (roadmap, technical/site audits, migrations)
topic_id: 13-strategy-audits/strategy
tags: [strategy, audit, migration, roadmap, process]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S4, S5, S6, S10]
---

## TL;DR
SEO strategy turns findings into a prioritized roadmap; audits find the gaps; migrations are where rankings are won or lost. Run a repeatable technical audit (crawl, index, CWV, links), document a quarterly roadmap, and treat site migrations as high-risk projects with full URL mapping and post-launch QA.

## Core explanation
Strategy = aligning SEO work to business goals and sequencing it by impact/effort. Audits are the diagnostic; migrations (redesign, platform change, domain move) are the highest-risk events because they rewrite URLs and signals.

## Mechanics / how-to
1. **Technical audit checklist:** crawlability (robots/S2/S5), index coverage (GSC), canonicalization (S4), redirects, CWV (S10), internal links, schema.
2. **Content audit:** intent match, depth, decay (update stale pages).
3. **Roadmap:** bucket by impact×effort; quarterly cycles; tie to KPIs.
4. **Migration:** inventory all URLs → 1:1 redirect map → staging QA → staged launch → monitor GSC + rankings + traffic for 4–8 weeks (see 13 follow-up).

## Worked example / code
Redirect map (301) CSV concept:
```
old_url,new_url
/old-product-x,/new-product-x
/blog/2020-sale,/promotions/annual-sale
```
Apply via server config (nginx `return 301` / Apache `Redirect 301`).

## Assumptions & limitations
- Audits are point-in-time; sites change continuously.
- Migrations need stakeholder buy-in; SEO is often under-weighted in redesigns.
- CWV thresholds apply at the 75th percentile (S10); a few slow pages won't fail the site.

## Empirical evidence
Google's audit-relevant docs (S4/S5/S6/S10) define the technical baseline. Migration ranking volatility is widely documented by practitioners (Tier 2) and correlates with redirect-map completeness.

## Conflicting views
- **"Audit everything before touching anything."** Pragmatic: prioritize by impact; perfect audits stall execution.
- **"Migrations always lose rankings."** With a complete redirect map and QA, traffic is largely preservable.

## Common mistakes
- Launching a redesign without 1:1 redirects.
- Dropping pages that had links.
- Not monitoring post-launch.
- Audit that produces no roadmap.
- Ignoring CWV until penalized.

## Further reading
- S1 — Google, "SEO Starter Guide" — Tier 1
- S4 — Google, "Canonicals" — Tier 1
- S5 — Google, "robots.txt" — Tier 1
- S6 — Google, "Sitemaps" — Tier 1
- S10 — web.dev, "Web Vitals" — Tier 1
