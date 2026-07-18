---
title: Playbooks by Scenario (new site, recovery, enterprise, programmatic, news)
topic_id: 14-playbooks/playbooks
tags: [playbooks, new-site, recovery, enterprise, programmatic, news]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S8, S25, S15, S4]
---

## TL;DR
Reusable steps per scenario: **new site** → foundation + GSC + sitemap + content; **recovery** → diagnose manual action vs algorithmic, fix root cause, wait; **enterprise** → governance + templates + automation; **programmatic** → unique value per page or don't scale; **news** → structured data + speed + E-E-A-T.

## Core explanation
Playbooks compress the KB into situation-specific checklists. They reference deeper articles (00–13) rather than re-teaching fundamentals.

## Mechanics / how-to
**New site launch**
- Technical foundation: robots allowed, XML sitemap, logical architecture, mobile parity (S1, S7).
- Verify GSC; submit sitemap (S6); set canonicals (S4).
- Publish intent-matched, E-E-A-T content (S9).

**Recovery from penalty/update**
- Check GSC for manual actions (S8); if algorithmic, identify lost query clusters and audit intent/depth/E-E-A-T (S25/S15).
- Remove/manipulative links or disavow; improve content; wait for next evaluation cycle.

**Enterprise / programmatic**
- Scale via templates + automation (see 12-tools-workflows); ensure each programmatic page has unique, useful data or content — mass thin pages invite helpful-content demotion (S18/S25).
- Governance: centralized standards, logged audits.

**News/publishing**
- `NewsArticle` schema, fast CWV (S10), clear bylines/E-E-A-T (S9), submit to Google News where eligible.

## Worked example / code
Recovery triage checklist (Markdown):
```
- [ ] GSC: manual action present? (S8)
- [ ] Identify dropped queries (GSC Performance)
- [ ] Audit top dropped pages: intent? depth? E-E-A-T? (S9)
- [ ] Link audit: unnatural patterns? disavow (S8)
- [ ] Improve + document; monitor 4-8 weeks
```

## Assumptions & limitations
- Recovery timing is indeterminate; Google re-evaluates on its cycles (S15).
- Programmatic scale amplifies both good and bad; unique value is the differentiator.

## Empirical evidence
Google's manual-action and webspam docs (S8) and update communications (S15) are first-party. Case analyses (S25/S27) show recovery correlates with genuine quality fixes, not cosmetic changes.

## Conflicting views
- **"Disavow proactively."** Only when you have a problem; blanket disavows can hurt good links (S8).
- **"Programmatic SEO is a shortcut."** It works only with differentiated data/value.

## Common mistakes
- Launching before technical foundation is sound.
- Cosmetic "fixes" after an update without addressing quality.
- Programmatic pages with duplicate/thin content.
- No monitoring post-launch/recovery.

## Further reading
- S1 — Google, "SEO Starter Guide" — Tier 1
- S8 — Google, "Spam policies" — Tier 1
- S15 — Google Search Central Blog — Tier 1
- S25 — Search Engine Land (updates/recovery) — Tier 2
- S9 — Google, "Quality Rater Guidelines" — Tier 1
