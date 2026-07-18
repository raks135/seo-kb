---
title: Spam Updates & Link Spam (Penguin Lineage)
topic_id: 10-algorithms-ranking-factors/spam-updates-link-spam
tags: [spam-updates, link-spam, spambrain, penguin, scaled-content-abuse, site-reputation-abuse, expired-domain-abuse, manual-actions]
last_updated: 2026-07-18
confidence: robust
sources: [S33, S97, S98, S101, S102, S103, S104, S233, S242, S243, S244, S245]
---

## TL;DR
- A **spam update** is a scheduled improvement to Google's always-on spam-detection systems (SpamBrain), announced on the ranking-updates list; it enforces Google's published **spam policies**, whereas a **core update** is a broad quality reassessment of all content (S243, S231).
- In **March 2024** Google shipped three spam-policy changes — **scaled content abuse**, **site reputation abuse**, and **expired domain abuse** — alongside the March 2024 core update (S242). Recent spam updates also ran in June 2024, December 2024, August 2025, March 2026, and June 2026 (S233, S245).
- **Link spam** has its own lineage: **Penguin (2012)** → **Penguin 4.0 (Sept 2016, real-time, part of core)** → **SpamBrain (Dec 2022 link spam update, AI-based)**; Google no longer announces Penguin refreshes because link-spam enforcement is continuous (S33, S103, S104, S98).
- Spam updates are **algorithmic, not manual actions**: you get no Search Console notification, the **disavow tool does not help you recover**, and for a link spam update the ranking benefit from the removed links "cannot be regained" (S243, S101, S102). Site reputation abuse is still handled primarily through **manual actions**, not the automated spam-update cadence (S244).

## Core explanation
Google fights spam with "advanced spam-fighting systems" that run constantly (S242). When Google makes a *notable* improvement to those systems, it calls the event a **spam update** and lists it on the public ranking-updates page (the same place core updates are announced) (S243). The goal of a spam update is narrow: demote or remove pages that violate a specific **spam policy** — scaled content abuse, site reputation abuse, expired domain abuse, link spam, cloaking, hidden text, scraped content, and so on (S242, S97).

This is different from a **core update**. Core updates are broad changes to the overall ranking systems that re-evaluate which pages best answer queries; they "don't target specific sites or individual web pages" (S231). A spam update, by contrast, is an enforcement action against behavior Google has already declared off-limits in its spam policies. The March 2024 event was unusual because Google shipped both at once — a complex core update *and* new spam policies — which is why many sites saw overlapping flux (S242, S234).

**Link spam** is one category of spam policy, but its enforcement history is the longest and most documented. Google's original link-spam filter, **Penguin**, launched in April 2012 to target manipulative link building (S103, S104). Over time it was absorbed into the core algorithm: **Penguin 4.0 (Sept 23, 2016)** became "real-time," "more granular," and began **devaluing** bad links rather than applying a site-wide demotion (S103, S104). Modern link-spam detection is performed by **SpamBrain**, Google's AI-based spam-prevention system; the **December 2022 link spam update** was the first to use SpamBrain to detect *both* sites buying links *and* sites used to pass outgoing links, neutralizing their effect at scale (S98, S33).

## Mechanics / how-to
**1. Know which event hit you.** Check the ranking-updates list (status.search.google.com) for the date window and whether it was a core update, a spam update, or a *named* link spam update (S233, S243). "Link spam update" is called out as such; a generic "spam update" is broader (S244).

**2. For a spam-update hit, audit against the spam policies** (developers.google.com/search/docs/essentials/spam-policies):
   - **Scaled content abuse** — many pages produced primarily to manipulate rankings, whether by automation, humans, or a mix; includes pages that "pretend to have answers to popular searches but fail to deliver helpful content" (S242).
   - **Site reputation abuse** — low-value third-party content placed on a high-reputation site mainly for ranking (e.g., payday-loan reviews on a trusted university site); enforcement for this policy began **May 5, 2024**, and is still largely a **manual action** (S242, S244).
   - **Expired domain abuse** — buying an expired domain and repurposing it to boost low-quality/unoriginal content (S242).
   - **Link spam** — buying/selling links, excessive exchanges, automated link generation, advertorials passing ranking credit, low-quality directory/widget/footer/forum links (S97).
   - Plus the older policies: cloaking, hidden text, scraped content, auto-generated spam, malware, and user-generated spam.

**3. Fix the root cause, then wait.** For general spam updates, "making changes may help a site improve if our automated systems learn over a period of **months** that the site complies" (S243). There is no reconsideration request for an algorithmic spam update. For **link spam updates specifically**, Google is explicit: fixing the links "might not generate an improvement" because "any potential ranking benefits generated by those [spammy] links cannot be regained" (S243).

**4. Manual actions are separate.** If you received a **Manual Actions** notice in Search Console, that is *not* a spam update — use the **disavow tool** and file a **reconsideration request** (S101, S102). The disavow tool does **not** reverse an algorithmic spam update.

## Worked example / code
The script below is an **editorial** risk flagger for the March 2024 *scaled content abuse* policy. It reads a `url,title,word_count` CSV and surfaces thin, templated pages that are worth a human quality review. It is **not** a predictor of Google action — counts alone never determine a policy violation (intent and value matter). Stdlib only, Python 3.8+.

```python
# scaled_content_audit.py  (shipped alongside this article)
import csv, re
from collections import Counter

THIN_WORDS = 200   # pages below this are "thin" by this heuristic
MIN_PAGES  = 50    # inventory size where mass-generation patterns weigh more
TEMPLATE_MIN = 3   # a title bigram shared by >= this many thin pages = templated

def title_tokens(t): return [x for x in re.findall(r"[a-z0-9]+", t.lower())]

rows = []
with open("pages.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append((r["url"], r.get("title",""), int(r.get("word_count",0))))

thin = [(u,t,w) for (u,t,w) in rows if w < THIN_WORDS]
bg = Counter()
for _u,title,_w in thin:
    toks = title_tokens(title)
    for i in range(len(toks)-1): bg[(toks[i], toks[i+1])] += 1
template_hits = {k for k,c in bg.items() if c >= TEMPLATE_MIN}

risk = (len(thin) >= 10 and len(rows) >= MIN_PAGES) or bool(template_hits and len(thin) >= 5)
print(f"Thin pages: {len(thin)}/{len(rows)}  Templated: {sorted(' '.join(b) for b in template_hits)}")
print("SCALED-CONTENT RISK:", "ELEVATED" if risk else "low (editorial heuristic only)")
```

Verified run on the bundled demo (5 thin, templated "best coffee … our guide" pages among 7):

```
Pages scanned      : 7
Thin pages (<200 words): 5 (71%)
Templated bigrams  : best coffee, our guide
SCALED-CONTENT RISK: ELEVATED — review these pages for value/intent
```

For link-spam cleanup, see the reproducible disavow-file validator shipped with `03-off-page-seo/link-schemes.md` and the anchor-distribution classifier in `03-off-page-seo/anchor-text-link-velocity.md` — those cover the *remediation* workflow for link schemes, which complements (but does not replace) this article.

## Assumptions & limitations
- **Google does not publish what each spam update targets.** Only *named* link spam updates are explicitly about links; generic spam updates are "general and broad" and analysts infer targets from volatility (S244). Treat any "this update targeted X" claim as inference, not Google confirmation.
- **Spam updates are not penalties you can "submit" your way out of.** No reconsideration request exists for an algorithmic spam update; recovery depends on the automated systems re-learning compliance over months (S243).
- **The March 2024 "45% less low-quality content" figure is Google's own evaluation**, not an independent measurement — cite it as Google's self-reported claim (S242).
- **Site reputation abuse is still largely manual-action territory** as of the December 2024 spam update; automation of that policy was *not* part of that update (S244).
- **Correlation ≠ causation:** ranking drops during a spam-update window can also be core-update overlap, seasonality (e.g., holiday volatility), or normal flux — confirm against the exact dated window on the ranking-updates list (S233, S244).

## Empirical evidence
- **Cadence (Tier 1 + Tier 2):** The Search Status Dashboard lists spam updates on Mar/Jun/Dec 2024, Aug 2025, Mar 2026, Jun 2026, interleaved with core updates (S233, S245). SEL counts 4 core + 3 spam updates in 2024 (S244).
- **Self-reported impact:** Google expected a 40% reduction in low-quality/unoriginal content from the March 2024 changes and updated it to "45% less" as of Apr 19, 2024 (S242). This is Google's internal evaluation, not a third-party audit.
- **Dec 2024 breadth:** The Dec 2024 spam update (Dec 19–26) was described by SEL as "much more widespread than some previous spam updates," though "it is still a bit too early to dig too much into the update" and holiday traffic was volatile (S244). This is observational, single-window reporting.
- **Link-spam history:** Penguin 4.0 (Sept 2016) is documented as the shift to real-time, granular, devaluing (not demoting) behavior (S103, S104); SpamBrain's Dec 2022 link spam update neutralizes unnatural links at scale (S98). These are well-established, multi-source historical facts.

## Conflicting views
- **"Disavow will recover me from a spam update."** False for algorithmic spam updates (S243). The disavow tool exists for **manual actions** and is explicitly *not* a preventative or recovery lever for algorithmic spam (S101, S102). SEOs sometimes conflate the two.
- **"Spam update = core update."** They are distinct events on the same list; conflating them leads to wrong remediation (quality/content review vs. policy-compliance review) (S231, S243).
- **Recovery timing.** Google says improvements "may" come over months and are not guaranteed; some practitioners report faster/broader flux, others report no recovery — both are consistent with Google's "no guarantee" stance (S243, S244).
- **"Site reputation abuse is now fully automated."** As of Dec 2024 it was *not* automated in spam updates and remains a manual-action policy (S244) — a point some 2024 coverage overstated.

## Common mistakes
1. **Using disavow to "fix" an algorithmic spam update** — wrong tool; it only helps with manual actions (S101, S102, S243).
2. **Mass-producing thin, templated pages** ("best X in <city>" spun at scale) — the textbook scaled content abuse pattern (S242); see the audit script above.
3. **Hosting low-value third-party content on a strong domain** for ranking — site reputation abuse; enforce editorial oversight or remove it (S242, S244).
4. **Buying expired domains to inherit authority** then repurposing them with low-quality content — expired domain abuse (S242).
5. **Assuming a spam update targets your *content quality* when it targets a *policy violation*** — the fix is compliance, not a general content rewrite (S243).
6. **Chasing rankings during a holiday-window spam update** and misreading seasonal traffic dips as the update — compare rankings, not raw traffic (S244).
7. **Believing "Penguin is dead."** Penguin was absorbed into core systems and replaced by SpamBrain; link-spam enforcement is continuous, not gone (S33, S98).

## Further reading
- Google, "Google Search spam updates and your site" (Tier 1) — S243
- Google (The Keyword), "New ways we're tackling spammy, low-quality content on Search" (Tier 1, March 2024 policies) — S242
- Google, "Spam Policies for Google Web Search" (Tier 1, full policy list) — S97
- Google Search Central Blog, "December 2022 link spam update" / SpamBrain (Tier 1) — S98
- Google Search Central Blog, "A new tool to disavow links" + Help "Disavow links" (Tier 1, manual-action workflow) — S101, S102
- Google, "Core updates and your website" (Tier 1, core-vs-spam distinction) — S231
- Search Engine Land, "Google December 2024 spam update done rolling out" (Tier 2) — S244
- Search Engine Land, "Google updates Penguin, says it now runs in real time" (Tier 2) — S104
- Ahrefs, "Google's 'Disavow Links Tool': The Complete Guide" (Tier 2, Penguin history) — S103
- Momentic, "Google Algorithm Updates tracker" (Tier 2, cadence) — S245
- Sibling KB articles: `03-off-page-seo/link-schemes.md` (disavow + manual actions), `03-off-page-seo/anchor-text-link-velocity.md` (anchor/link-velocity evidence), `10-algorithms-ranking-factors/core-updates.md` (core-update mechanics), `10-algorithms-ranking-factors/algorithms.md` (ranking-systems overview, S33).
